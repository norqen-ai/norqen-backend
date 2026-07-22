# News Agent

Turns the flow of news into ranked, reliable evidence.

## Collects and summarizes

- Company news
- Global events
- Regulatory announcements
- Earnings releases
- Market-moving headlines

## How it works

The agent **ranks evidence by relevance, freshness, and source reliability**, and deduplicates overlapping coverage so the planner sees signal rather than noise.

## Tools it uses

- News tools — retrieval, deduplication, entity extraction, reliability scoring (see [../04-tools/news-tools.md](../04-tools/news-tools.md)).
- ML tools — sentiment analysis (as evidence only) (see [../04-tools/ml-tools.md](../04-tools/ml-tools.md)).

## Output

A concise set of ranked news items with source, timestamp, relevance, and reliability — plus extracted entities linking each item to instruments or themes.

## Boundary

Returns to the planner; never executes, enforces risk, or contacts other agents (see [agent-framework.md](agent-framework.md)).
