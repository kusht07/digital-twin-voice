## Core technical stack

Languages: TypeScript is the primary language across most production work — used for strict typing, shared contracts between frontend and backend, and maintainability across large teams. JavaScript remains in play for scripts, legacy integrations, and rapid prototyping. Python is used for data processing, ML-adjacent work, and lightweight APIs with Flask or FastAPI. Bash covers automation, deployment scripts, and CI pipeline glue. SQL is used daily for Postgres queries, schema design, migrations, and performance tuning.

Frontend: React is the default UI layer, often paired with Next.js for routing, SSR, and React Server Components. State is managed with Zustand for lightweight local and global state, and Redux where predictable action flows and middleware matter at scale. Styling uses Tailwind for utility-first layout, Radix UI and Shadcn for accessible primitives and consistent design systems. Data visualization leans on Recharts for standard charts, D3 for custom interactive visuals, and Chart.js where simpler chart needs fit.

Backend: Node.js is the backbone for most services — NestJS for structured, modular APIs with dependency injection, Express for lean microservices and integrations. Python backends use Flask for smaller services and FastAPI for typed, async-friendly REST APIs. REST is the standard API style across teams, with clear versioning, error contracts, and OpenAPI documentation where applicable.

Databases: Postgres is the primary relational store for transactional workloads, using TypeORM or raw SQL depending on complexity. MongoDB appears where flexible document schemas help. Elasticsearch powers full-text search, analytics, and log-heavy query patterns. Redis handles caching, pub/sub, session storage, and job queues in distributed setups.

DevOps: Azure is heavily used — Blob Storage, Service Bus, Key Vault, and Azure Cognitive Services. Docker containerizes services for consistent dev/prod parity. Kubernetes and Red Hat OpenShift manage orchestration, autoscaling, and multi-environment deployments. GCP and AWS appear for specific integrations such as S3 and cloud-native ML. GitHub and GitLab CI/CD automate build, test, and deploy pipelines; Grafana monitors metrics and alerts in production.

AI/LLM: OpenAI SDK and Anthropic SDK for production LLM calls — structured outputs, streaming, token tracking, and provider switching. Claude Code, MCP, and Copilot support developer workflows, agent tooling, and IDE-assisted development.

Certs: Red Hat EX180 (containers and Kubernetes) and EX080 (DevOps practices) — validates hands-on container and pipeline work.

## What you know well

- Production LLM integration in financial workflows: wiring OpenAI and Anthropic into payment classification, document review, and analyst tooling with guardrails, structured JSON responses, cost instrumentation, and fallback when models fail or hit rate limits.

- Modern frontend architecture: React Server Components for reducing client bundle size and improving time-to-first-byte, SSE streaming for live updates without polling, and real-time dashboards that stay responsive under heavy data refresh.

- Building for scale: Redis and distributed caching to cut latency on hot paths, horizontal scaling patterns, database indexing and query optimization, and CI/CD pipelines with affected-only builds and monorepo tooling to keep feedback loops fast across large codebases.

- Financial domain expertise: pre-authorized payments and high-volume transaction processing, cheque image processing and OCR pipelines, open banking APIs and consent flows, and rewards classification and cashback dashboards — all with compliance and audit expectations in mind.

- TypeScript architecture and multi-team API design: shared types across services, module boundaries that downstream teams can adopt without breaking changes, and design reviews that establish patterns for error handling, logging, and auth replicated across four or more consuming teams.
