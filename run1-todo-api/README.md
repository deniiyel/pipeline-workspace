\# Run 1: Task Management CRUD API (`todo-crud-api`)



\## Overview

Persistent task management REST API built with FastAPI and SQLite.



\## Architecture

\- \*\*Framework:\*\* FastAPI (Python)

\- \*\*Database:\*\* SQLite (`tasks.db`)

\- \*\*Testing:\*\* Pytest automated test suite



\## Endpoints

\- `GET /tasks` - Retrieve all tasks

\- `POST /tasks` - Create a new task (validates non-empty title)

\- `GET /tasks/{id}` - Fetch task by ID

\- `DELETE /tasks/{id}` - Remove task by ID

