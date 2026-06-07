<!-- Loaded on demand. -->

# Architecture Overview

## System Diagram

```text
                  ┌───────────────────────┐
HTTP request  →   │   presentation/       │
                  │   Express routes      │
                  │   + zod validation    │
                  └──────────┬────────────┘
                             ▼
                  ┌───────────────────────┐
                  │   domain/             │
                  │   use case +          │
                  │   repository iface    │
                  └──────────┬────────────┘
                             ▼
                  ┌───────────────────────┐
                  │   data/               │
                  │   Postgres impl       │
                  └───────────────────────┘
```

## Layer Structure

- **Presentation** — Express 5 routes + zod input validation
  (`src/notifications/presentation/`).
- **Domain** — pure business logic. Owns the `Notification` entity, the
  `NotificationRepository` interface, and the `SendNotification` use
  case (`src/notifications/domain/`).
- **Data** — `PostgresNotificationRepository` against `pg`
  (`src/notifications/data/`).

Dependency direction: `presentation → domain ← data`. Domain owns the
repository INTERFACE; data implements it. Domain has no imports from
`presentation/` or `data/`.

## Module Map

| Module          | Purpose                       | Key Files                                                |
| --------------- | ----------------------------- | -------------------------------------------------------- |
| `notifications` | Create + list notifications   | `src/notifications/{domain,data,presentation}/`          |

## Data Flow

```
client
  └─ POST /notifications  →  notification-routes.ts
                              ├─ zod validates body
                              └─ SendNotification.execute()
                                  └─ NotificationRepository.save()
                                      └─ PostgresNotificationRepository
                                          └─ INSERT into notifications
                              ← 201 Created + Notification JSON
```

## Composition Root

`src/app.ts` builds the dependency graph: instantiates the
`Pool`-backed `PostgresNotificationRepository`, wraps it in the
`SendNotification` use case, registers routes. No DI container.

## External Dependencies

| Service       | Purpose                | Docs                              |
| ------------- | ---------------------- | --------------------------------- |
| PostgreSQL 16 | Notifications storage  | <https://www.postgresql.org/>     |
