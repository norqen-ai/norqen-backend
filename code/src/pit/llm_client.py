"""Thread-safe, cached, multi-provider structured-output client for the PIT study.

Same output schemas as the live system (src/agents/llm.py: Judgement, DecisionProposal),
called through the OpenAI SDK directly so thousands of calls can run concurrently.
Providers: OpenAI (gpt-4o-mini, gpt-4.1-mini, gpt-5-mini) and Groq's OpenAI-compatible
endpoint (open-weight models) when GROQ_API_KEY is set. Every response is cached in
SQLite keyed by (model, prompts, temperature, tag), so re-runs are free and resumable.
Keys are read from the environment and never logged.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import sqlite3
import threading
import time
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

CACHE = Path(os.environ.get("PIT_CACHE_PATH", str(Path(__file__).resolve().parents[2] / "data" / "pit" / "llm_cache.sqlite")))
CACHE.parent.mkdir(parents=True, exist_ok=True)
_lock = threading.Lock()
_db = sqlite3.connect(CACHE, check_same_thread=False, timeout=120)
try:
    _db.execute("PRAGMA journal_mode=WAL")      # persistent; a concurrent switch may be locked -> fine
except sqlite3.OperationalError:
    pass
_db.execute("CREATE TABLE IF NOT EXISTS c (k TEXT PRIMARY KEY, model TEXT, v TEXT, ts REAL)")
_db.commit()

# Training-data cutoffs as published by the providers (reported in the paper's model table).
MODELS = {
    "gemma-3-4b-local": {"provider": "ollama", "id": "gemma3:4b", "cutoff": "2024-08"},
    "phi-4-local": {"provider": "ollama", "id": "phi4:latest", "cutoff": "2024-06"},
    "llama-3.1-8b-local": {"provider": "ollama", "id": "llama3.1:8b", "cutoff": "2023-12"},
    "gpt-oss-20b-local": {"provider": "ollama", "id": "gpt-oss:20b", "cutoff": "2024-06", "reasoning": True},
    "gemma-3-27b": {"provider": "openrouter", "id": "google/gemma-3-27b-it", "cutoff": "2024-08"},
    "phi-4": {"provider": "openrouter", "id": "microsoft/phi-4", "cutoff": "2024-06"},
    "gpt-4o-mini":   {"provider": "openai", "id": "gpt-4o-mini-2024-07-18", "cutoff": "2023-10"},
    "gpt-4.1-mini":  {"provider": "openai", "id": "gpt-4.1-mini-2025-04-14", "cutoff": "2024-06"},
    "gpt-5-mini":    {"provider": "openai", "id": "gpt-5-mini-2025-08-07", "cutoff": "2024-05", "reasoning": True},
    "llama-3.3-70b": {"provider": "groq", "id": "llama-3.3-70b-versatile", "cutoff": "2023-12"},
    "gpt-oss-120b":  {"provider": "groq", "id": "openai/gpt-oss-120b", "cutoff": "2024-06", "reasoning": True},
    "gpt-oss-20b":   {"provider": "groq", "id": "openai/gpt-oss-20b", "cutoff": "2024-06", "reasoning": True},
    "llama-4-scout": {"provider": "groq", "id": "meta-llama/llama-4-scout-17b-16e-instruct", "cutoff": "2024-08"},
}

# OpenAI-compatible providers for open-weight models: name -> (base URL, env var holding the key).
# To add a model from one of these, add a MODELS entry with that provider (and its published cutoff).
PROVIDERS = {
    "groq":       ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "together":   ("https://api.together.xyz/v1", "TOGETHER_API_KEY"),
}

_clients: dict = {}


def _client(provider: str):
    if provider == "openai" and os.environ.get("PIT_DISABLE_OPENAI") == "1":
        raise RuntimeError("OpenAI API disabled for this run")
    if provider not in _clients:
        from openai import OpenAI
        if provider in PROVIDERS:
            url, env = PROVIDERS[provider]
            _clients[provider] = OpenAI(api_key=os.environ[env], base_url=url, max_retries=0, timeout=90)
        else:
            _clients[provider] = OpenAI(max_retries=0, timeout=120)
    return _clients[provider]


def available(model: str) -> bool:
    m = MODELS[model]
    if m["provider"] == "ollama":
        return True
    return bool(os.environ.get(PROVIDERS[m["provider"]][1] if m["provider"] in PROVIDERS else "OPENAI_API_KEY"))


def _key(model, system, human, temperature, tag):
    return hashlib.sha256(json.dumps([model, system, human, temperature, tag]).encode()).hexdigest()


def cache_get(k):
    with _lock:
        r = _db.execute("SELECT v FROM c WHERE k=?", (k,)).fetchone()
    return json.loads(r[0]) if r else None


def cache_put(k, model, v):
    with _lock:
        _db.execute("INSERT OR REPLACE INTO c VALUES (?,?,?,?)", (k, model, json.dumps(v), time.time()))
        _db.commit()


def _schema_hint(schema: type[BaseModel]) -> str:
    props = schema.model_json_schema()["properties"]
    fields = ", ".join(f'"{n}": <{p.get("type", "value")}: {p.get("description", "")}>' for n, p in props.items())
    return f"\nRespond with ONLY a JSON object of the form {{{fields}}}."


def structured(model: str, system: str, human: str, schema: type[BaseModel],
               temperature: float = 0.0, tag: str = "") -> dict | None:
    """Return schema-validated dict (plus '_usage'), or None after retries. Cached."""
    k = _key(model, system, human, temperature, tag)
    hit = cache_get(k)
    if hit is not None:
        return hit
    m = MODELS[model]
    if m["provider"] == "ollama":
        return _local_structured(model, system, human, schema, temperature, k)
    if m["provider"] == "openrouter" and os.environ.get("PIT_FREE_ONLY") == "1" and not m["id"].endswith(":free"):
        raise RuntimeError("Paid OpenRouter calls disabled")
    cl = _client(m["provider"])
    for attempt in range(7):
        reservation = None
        try:
            if m["provider"] == "openai":
                kw = {"model": m["id"], "messages": [{"role": "system", "content": system},
                                                       {"role": "user", "content": human}],
                      "response_format": schema}
                if m.get("reasoning"):
                    kw["reasoning_effort"] = "low"
                else:
                    kw["temperature"] = temperature
                r = cl.chat.completions.parse(**kw)
                parsed = r.choices[0].message.parsed
                if parsed is None:
                    raise ValueError("refusal/empty parse")
                out = parsed.model_dump()
            else:
                kw = {"model": m["id"], "messages": [{"role": "system", "content": system + _schema_hint(schema)},
                                                       {"role": "user", "content": human}],
                      "response_format": {"type": "json_object"}, "temperature": temperature}
                if m.get("reasoning"):
                    kw["reasoning_effort"] = "low"
                if m["provider"] == "openrouter":
                    from src.pit.spend_guard import reserve, settle
                    kw["max_tokens"] = 2048
                    free = m["id"].endswith(":free")
                    kw["extra_body"] = {"provider": {"max_price": {"prompt": 0 if free else 0.08, "completion": 0 if free else 0.16}}}
                    if not free:
                        reservation = reserve(kw)
                r = cl.chat.completions.create(**kw)
                if reservation is not None:
                    settle(reservation, getattr(r.usage, "cost", None))
                out = schema.model_validate_json(r.choices[0].message.content).model_dump()
            u = r.usage
            out["_usage"] = {"in": getattr(u, "prompt_tokens", None), "out": getattr(u, "completion_tokens", None)}
        except Exception as e:  # rate limits, transient 5xx, malformed JSON
            msg = repr(e)
            if isinstance(e, RuntimeError) or getattr(e, "status_code", None) in (401, 402, 403) or "insufficient_quota" in msg or "invalid_api_key" in msg:
                raise
            time.sleep(min(60, (2 ** attempt) + random.random() * 2))
            continue
        try:
            cache_put(k, model, out)
        except Exception:
            pass                       # a cache write failure must not trigger a paid re-call
        return out
    return None


def _local_structured(model, system, human, schema, temperature, key):
    """Local Ollama inference; no cloud fallback, schema constrained and cached by model digest."""
    m = MODELS[model]
    base = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
    def post(path, body):
        req = urllib.request.Request(base + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as response:
            return json.load(response)
    # Ollama's digest changes if weights/template change; never reuse another quantization's cache.
    with urllib.request.urlopen(base + "/api/tags", timeout=10) as response:
        installed = json.load(response)["models"]
    digest = next(x["digest"] for x in installed if x["name"] == m["id"])
    local_key = hashlib.sha256((key + digest + ":ctx8192:predict2048:low").encode()).hexdigest()
    hit = cache_get(local_key)
    if hit is not None:
        return hit
    body = {"model": m["id"], "stream": False, "format": schema.model_json_schema(),
            "messages": [{"role": "system", "content": system + _schema_hint(schema)},
                         {"role": "user", "content": human}],
            "options": {"temperature": temperature, "num_ctx": 8192, "num_predict": 2048}}
    if m.get("reasoning"):
        body["think"] = "low"
    r = post("/api/chat", body)
    out = schema.model_validate_json(r["message"]["content"]).model_dump()
    out["_usage"] = {"in": r.get("prompt_eval_count"), "out": r.get("eval_count"),
                     "duration_ns": r.get("total_duration")}
    out["_model"] = {"id": m["id"], "digest": digest, "provider": "ollama",
                     "num_ctx": 8192, "num_predict": 2048, "think": body.get("think")}
    cache_put(local_key, model, out)
    return out
