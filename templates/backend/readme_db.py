README_DB = """# Database & Migrations Guide

This directory ships **ready-to-use** tooling for working with a Postgres (Supabase) database via SQLAlchemy & Alembic.

## What you already have

```
database/
├── alembic/            # Alembic already initialised for versioned migrations
│   ├── env.py          # pre-configured to use our Settings + Base metadata
│   └── versions/       # (empty) place where revision files will be generated
├── models/
│   └── base.py         # Declarative SQLAlchemy Base (+ to_dict mixin)
├── session.py          # Sync & Async session helpers bound to Supabase
└── README.md           # (this file)
```

## First-time setup

1. `cd backend && source .venv/bin/activate`
2. Ensure `.env` contains valid Supabase credentials (see `.env.example`).
3. Upgrade dependencies if you add new DB libraries: `uv sync --dev`.

## Creating migrations

```bash
# Navigate into the database directory so Alembic picks up the right ini file
cd src/app/database

# Generate a new migration with autogenerate
alembic revision --autogenerate -m "create users table"

# OR start a blank migration
alembic revision -m "custom changes"
```

Alembic will compare the models imported via `Base.metadata` (all models that subclass `Base`) against the current DB schema and emit the SQL needed.

## Applying / rolling migrations

```bash
# Upgrade to the latest version
alembic upgrade head

# Downgrade one revision
alembic downgrade -1
```

## Tips

* The engine & session are configured in `session.py`; adjust logging or isolation as needed.
* Use the **async** helpers for async frameworks (e.g. FastAPI) and the sync helpers for scripts.
* If autogenerate misses changes, check that your new model modules are imported somewhere before Alembic runs (e.g. inside `database/models/__init__.py`).
"""
