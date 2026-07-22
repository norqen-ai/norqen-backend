# Reflection Agent

Runs **after execution** and turns outcomes into lessons. Reflection is mandatory — every executed decision is reflected on (see [../00-overview/philosophy.md](../00-overview/philosophy.md)).

## What it compares

- **Expected outcome** — what the planner predicted.
- **Actual outcome** — what really happened.
- **Planner assumptions** — which held and which did not.
- **Missing evidence** — what, in hindsight, should have been gathered.

## Output

Structured lessons, for example:

- assumptions that proved incorrect,
- evidence that was missing or underweighted,
- reasoning paths that worked well,
- strategies that failed.

These are written to **reflection memory** so they improve future planning (see [../05-memory/reflection-memory.md](../05-memory/reflection-memory.md)).

## Why it matters

Reflection is what makes Norqen improve over time rather than repeat mistakes. Its lessons feed back into confidence estimation and tool/agent selection on future runs (see [../02-runtime/confidence-model.md](../02-runtime/confidence-model.md)).

## Boundary

Reflection creates knowledge; it never changes past decisions or executes anything (see [../01-architecture/module-boundaries.md](../01-architecture/module-boundaries.md)).
