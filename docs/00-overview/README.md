# 00 - Overview

This folder defines the vision, philosophy, and engineering principles of Norqen. Read it first — every later section (architecture, runtime, agents, tools, memory, risk, API, data) assumes the concepts and vocabulary established here.

## Reading order

1. [vision.md](vision.md) — what Norqen is and the reasoning loop that defines it
2. [philosophy.md](philosophy.md) — the core beliefs that shape every design decision
3. [why-norqen.md](why-norqen.md) — why a reasoning system instead of a workflow engine
4. [core-principles.md](core-principles.md) — the non-negotiable rules of the system
5. [terminology.md](terminology.md) — the shared vocabulary used throughout the docs
6. [backend-master-prompt.md](backend-master-prompt.md) — the guiding brief for anyone (human or AI) building the backend

## How the docs are organized

| Section | Purpose |
| --- | --- |
| `00-overview` | Vision, philosophy, principles, vocabulary |
| `01-architecture` | System shape, layering, module boundaries, deployment |
| `02-runtime` | The autonomous reasoning runtime (planner + LangGraph) |
| `03-agents` | The specialist agents the planner orchestrates |
| `04-tools` | The capability layer every agent and the planner use |
| `05-memory` | How Norqen accumulates and reuses experience |
| `06-risk` | The deterministic authority that validates every decision |
| `07-api` | The public interface of the backend |
| `08-data` | Persistence, ingestion, and data architecture |

## Scope of the current phase

Phase 1 is a **single modular monolith** (see [deployment.md](../01-architecture/deployment.md)). The immediate build target is the **core backend foundation**: the FastAPI application, configuration, database/session layer, authentication, error handling, and observability that everything else plugs into. The reasoning system (planner, agents, tools) is designed alongside it but layered in on top of that foundation.

## Out of scope: ML

**Machine learning is not in the scope of this repository.** Norqen does not train, host, or serve ML models here. ML capabilities (forecasting, regime detection, sentiment, anomaly detection, etc.) live in a **separate repository/service** and are **fetched over an interface when needed**.

Within this repo, ML appears only as a **port with adapter stubs** — a uniform tool interface the planner and agents call. The actual model implementations sit behind that interface, external to this codebase. See [../04-tools/ml-tools.md](../04-tools/ml-tools.md) and the ML port in [../01-architecture/hexagonal-architecture.md](../01-architecture/hexagonal-architecture.md).
