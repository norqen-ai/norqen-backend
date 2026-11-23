"""Real specialist tools/agents. Each is a callable(ticker) -> EvidenceItem,
backed by live market data, with an LLM judgement when a key is present and a
deterministic fallback when it is not."""
