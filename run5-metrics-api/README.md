\# Run 5: Time-Series Aggregation \& Metrics API (`run5-metrics-api`)



\## Overview

A lightweight microservice designed to ingest real-time metric telemetry data and serve summary analytics.



\## Key Features

\- \*\*Metric Ingestion:\*\* Accepts real-time numerical readings with auto-generated or custom timestamps.

\- \*\*On-the-Fly Aggregations:\*\* Computes live `count`, `min`, `max`, and `average` summary stats.

\- \*\*Fast Cleanups:\*\* Endpoint for purging metric history between test runs.

