def readme_backend(project_name):
    return f"""# {project_name} Backend

## Overview
FastAPI backend service for {project_name}.

## Setup
```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Unix/macOS
# or
.venv\\Scripts\\activate  # Windows

# Install dependencies
uv sync --dev
```

## Environment variables
Copy `.env.example` to `.env` and fill in your credentials.

```bash
cp .env.example .env
```

## Development
```bash
# Run the development server
uv run uvicorn src.app.api.main:app --reload --host 0.0.0.0 --port 8000

# Run the server in production
uv run uvicorn src.app.api.main:app --host 0.0.0.0 --port 8000

# API will be available at:
# - http://localhost:8000
# - http://localhost:8000/docs (Swagger UI)
# - http://localhost:8000/redoc (ReDoc)
```

## Project Structure
```
backend/
├── src/
│   └── app/
│       ├── core/
│       │   └── config.py
│       ├── database/
│       │   ├── alembic/
│       │   ├── models/
│       │   │   └── base.py
│       │   └── session.py
│       ├── __init__.py
│       └── main.py
├── .env.example
├── .venv/
├── pyproject.toml
└── README.md
```

## Adding Dependencies
```bash
# Production dependencies
uv add package-name

# Development dependencies
uv add --dev package-name
```
"""
