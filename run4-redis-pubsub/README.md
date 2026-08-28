\# Run 4: Real-Time Event Worker with DLQ (`run4-redis-pubsub`)



\## Overview

An event-driven message worker built for Redis Pub/Sub channels featuring an automated Dead Letter Queue (DLQ) error recovery pattern.



\## Key Features

\- \*\*Payload Validation:\*\* Enforces strict JSON schema validation for all incoming message payloads.

\- \*\*Dead Letter Queue (DLQ):\*\* Prevents infinite processing loops by routing malformed or unparseable messages to a dedicated error queue.

\- \*\*Resilient Parsing:\*\* Protects worker threads from crashing when handling broken message strings.

