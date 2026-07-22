# Authentication

Every request is authenticated and authorized. Authentication is part of the core backend foundation (see [../00-overview/backend-master-prompt.md](../00-overview/backend-master-prompt.md)).

## Mechanisms

| Mechanism | Use |
| --- | --- |
| **JWT access tokens** | Short-lived credentials carried on each request. |
| **Refresh tokens** | Long-lived, rotated, and revocable; used to mint new access tokens. |
| **API keys** | Service-to-service authentication (hashed at rest). |
| **Role-based authorization (RBAC)** | Determines what an authenticated principal may do. |

## The rule

> Every request is authenticated and authorized.

- **Authentication** establishes *who* is calling (a user via JWT, or a service via API key).
- **Authorization** establishes *what* they may do (via roles/permissions).

Both apply to REST and WebSocket connections (see [rest-api.md](rest-api.md), [websocket-api.md](websocket-api.md)).

## Token model

- **Access tokens** are short-lived JWTs; they minimize the blast radius of a leaked token.
- **Refresh tokens** are long-lived, **rotated on use**, and **revocable** (tracked server-side, e.g. in Redis) so sessions can be invalidated.
- **Passwords** are hashed with a strong algorithm (e.g. bcrypt/argon2) — never stored in plaintext.
- **API keys** follow a prefix + secret pattern and are stored only as hashes.

## RBAC

Roles such as `user`, `admin`, and `service` gate access to capabilities. Authorization is enforced as a dependency at the endpoint boundary, before business logic runs.

## Failure behavior

Auth failures return the standard error envelope with an appropriate code, never leaking whether a user exists or why exactly a token failed (see [error-handling.md](error-handling.md)).
