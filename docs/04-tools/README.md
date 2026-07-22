# 04 - Tools

This folder defines the **Tool Framework** — the capability layer that sits under the planner and every agent. In Norqen, *everything external is a tool*.

## Reading order

1. [tool-framework.md](tool-framework.md) — the "everything is a tool" model
2. [tool-interface.md](tool-interface.md) — the common contract every tool exposes
3. [market-data-tools.md](market-data-tools.md) — prices, quotes, fundamentals
4. [news-tools.md](news-tools.md) — news retrieval and scoring
5. [technical-analysis-tools.md](technical-analysis-tools.md) — indicators, computed locally
6. [ml-tools.md](ml-tools.md) — models as evidence providers
7. [broker-adapters.md](broker-adapters.md) — order execution adapters
8. [memory-tools.md](memory-tools.md) — semantic search and recall
9. [tool-registry.md](tool-registry.md) — the catalog the planner queries
10. [tool-selection.md](tool-selection.md) — how the planner picks a tool
11. [observability.md](observability.md) — telemetry for every invocation

## Why a tool layer

Uniform capabilities behind a common interface let the planner treat providers as **interchangeable**. It requests "get market history" or "compute RSI" without knowing — or caring — which provider answers. This is what makes adaptive evidence acquisition and automatic provider fallback possible (see [tool-selection.md](tool-selection.md), [../02-runtime/failure-recovery.md](../02-runtime/failure-recovery.md)).
