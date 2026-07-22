# Versioning

The API uses **explicit versions** so capabilities can evolve without breaking existing clients.

## Scheme

```
/api/v1/...
```

Every endpoint lives under a version prefix. The current major version is `v1`.

## Rules

> Avoid breaking changes. Introduce new capabilities through new versions or additive endpoints.

- **Additive by default** — new optional fields and new endpoints can ship within a version.
- **Breaking changes go to a new version** — anything that would break an existing client (removing/renaming fields, changing semantics) requires `v2`, not a mutation of `v1`.
- **Deprecate, don't delete** — old versions are supported through a deprecation window before removal.

## Why

Clients (the Next.js frontend and any service integrations) depend on a stable contract. Because the API exposes capabilities rather than internal schemas (see [api-philosophy.md](api-philosophy.md)), internal refactors rarely require a version bump — only changes to the public contract do.
