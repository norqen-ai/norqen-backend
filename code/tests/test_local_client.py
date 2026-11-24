import importlib
import io
import json

import pytest
from pydantic import BaseModel


def test_local_cache_changes_with_model_digest(tmp_path, monkeypatch):
    monkeypatch.setenv("PIT_CACHE_PATH", str(tmp_path / "cache.sqlite"))
    from src.pit import llm_client
    client = importlib.reload(llm_client)
    class Reply(BaseModel):
        value: int
    digest, chats = ["first"], []
    def request(req, timeout):
        if isinstance(req, str):
            body = {"models": [{"name": "llama3.1:8b", "digest": digest[0]}]}
        else:
            chats.append(json.loads(req.data))
            body = {"message": {"content": '{"value": 3}'}, "eval_count": 4}
        return io.BytesIO(json.dumps(body).encode())
    monkeypatch.setattr(client.urllib.request, "urlopen", request)
    for _ in range(2):
        assert client.structured("llama-3.1-8b-local", "system", "human", Reply)["value"] == 3
    assert len(chats) == 1
    digest[0] = "second"
    client.structured("llama-3.1-8b-local", "system", "human", Reply)
    assert len(chats) == 2
    assert chats[0]["format"] == Reply.model_json_schema()


def test_paid_routes_blocked_before_client_creation(tmp_path, monkeypatch):
    monkeypatch.setenv("PIT_CACHE_PATH", str(tmp_path / "cache.sqlite"))
    monkeypatch.setenv("PIT_FREE_ONLY", "1")
    from src.pit import llm_client
    client = importlib.reload(llm_client)
    class Reply(BaseModel):
        value: int
    with pytest.raises(RuntimeError, match="Paid OpenRouter"):
        client.structured("phi-4", "system", "human", Reply)
    monkeypatch.setenv("PIT_DISABLE_OPENAI", "1")
    with pytest.raises(RuntimeError, match="OpenAI API disabled"):
        client._client("openai")
