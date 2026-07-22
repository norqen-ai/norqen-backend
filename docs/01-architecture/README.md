# 01 - Architecture

This folder defines the overall architecture of Norqen: the system shape, the layering rules, the module boundaries, and how it deploys.

## Reading order

1. [system-architecture.md](system-architecture.md) — the end-to-end request/decision flow
2. [backend-architecture.md](backend-architecture.md) — stack and backend engineering principles
3. [project-structure.md](project-structure.md) — the suggested package layout
4. [clean-architecture.md](clean-architecture.md) — the four layers and the dependency direction
5. [hexagonal-architecture.md](hexagonal-architecture.md) — ports and adapters for external systems
6. [event-driven-design.md](event-driven-design.md) — how components communicate through events
7. [module-boundaries.md](module-boundaries.md) — who owns what
8. [dependency-rules.md](dependency-rules.md) — the allowed and forbidden dependencies
9. [deployment.md](deployment.md) — how Norqen is deployed and scaled

## The one-paragraph summary

Norqen is a **modular monolith** built with Clean + Hexagonal architecture. FastAPI is the presentation layer; the application layer coordinates use cases; the domain holds framework-free business rules; infrastructure implements ports (databases, brokers, market data, ML) as swappable adapters. The **planner** (LangGraph) is the brain, the **Risk Engine** is the final authority, and components communicate through **events** for auditability and loose coupling.
