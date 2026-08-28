\# Run 3: JWT Authentication \& User Authorization Service (`run3-jwt-auth`)



\## Overview

Stateless JWT authentication and authorization module using FastAPI, SQLite, and SHA-256 password hashing.



\## Key Features

\- \*\*User Registration \& Login:\*\* Enforces unique username constraints and validates hashed password comparison.

\- \*\*JWT Token Generator:\*\* Issues signed HS256 access tokens with 1-hour expiration.

\- \*\*Protected Endpoint:\*\* `/me` route secured via FastAPI `HTTPBearer` dependency injection.

