# News Tools

Tools that retrieve and process news, sitting behind the News port. Consumed primarily by the News Agent (see [../03-agents/news-agent.md](../03-agents/news-agent.md)).

## Providers (adapters)

- NewsAPI
- GDELT
- RSS feeds
- Financial news vendors

## Responsibilities

- Retrieve news
- Deduplicate articles
- Rank relevance
- Score reliability
- Extract entities

## Notes

- **Reliability scoring** attaches a source-trust signal to every item, which feeds the confidence model (see [../02-runtime/confidence-model.md](../02-runtime/confidence-model.md)).
- **Entity extraction** links articles to instruments and themes so evidence can be tied to a goal.
- **Deduplication** collapses overlapping coverage so the planner sees signal, not repetition.
- Outputs are evidence, always carrying source, timestamp, relevance, and reliability.
