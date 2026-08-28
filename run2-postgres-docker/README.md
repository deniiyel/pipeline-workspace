\# Run 2: Multi-Container Microservice (`a2-postgres-docker`)



\## Overview

Infrastructure orchestration using Docker Compose combining an Express API, persistent PostgreSQL storage, and a Redis caching layer.



\## Key Features

\- \*\*Cache-Aside Pattern:\*\* Fast key lookups via Redis with 60-second TTL before hitting PostgreSQL.

\- \*\*Container Healthchecks:\*\* Dependency ordering configured via `service\_healthy` conditions.

\- \*\*Stateless API:\*\* Node.js Express server containerized for consistent deployments.

