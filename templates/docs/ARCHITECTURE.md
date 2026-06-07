<!-- Loaded on demand when the agent needs architectural context. -->

# Architecture Overview

## System Diagram

<ASCII diagram or reference to an image in assets/>

## Layer Structure

- **Presentation**: <framework, patterns>
- **Domain**: <business logic organization>
- **Data**: <persistence strategy, repositories>

## Module Map

| Module    | Purpose                          | Key Files       |
| --------- | -------------------------------- | --------------- |
| `<auth>`  | <Authentication & authorization> | `src/<auth>/`   |
| `<users>` | <User management CRUD>           | `src/<users>/`  |

## Data Flow

<Description of how data flows through the system. 5–10 lines max.>

## External Dependencies

| Service    | Purpose      | Docs    |
| ---------- | ------------ | ------- |
| `<Stripe>` | <Payments>   | <link>  |

<!--
Why this file exists: when the agent asks "what's the architecture?",
it should read this file, not scan 50 source files.
-->
