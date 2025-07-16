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

## Connection Modes (Session vs. Transaction)

Your database connection can operate in one of two Supabase pooler modes, configured via the `DB_PORT` environment variable in `.env` (or `config.py`).
The `session.py` file automatically adjusts pooling based on this setting.

- **Session Mode (DB_PORT="5432")**:  
  Default mode, ideal for applications with long-lived connections (e.g., scripts, CLIs, or low-traffic apps). 
  It uses client-side pooling in SQLAlchemy for efficiency but has lower concurrency limits (typically 15–20 simultaneous connections on Supabase Pro plans). 
  Use this if your app doesn't expect high traffic or many parallel requests.

- **Transaction Mode (DB_PORT="6543")**:  
  Recommended for high-concurrency, serverless apps (e.g., FastAPI web services with many users or background tasks). It disables client-side pooling 
  (using `NullPool`) and relies on Supabase's server-side pooler for short-lived transactions, supporting hundreds of concurrent connections (e.g., 200–500+ on Pro plans). 
  Switch to this if you hit "max clients reached" errors or need scalability. 
  Note: It may not support session-level features like prepared statements, so test migrations and queries.

To switch modes:  
- Set `DB_PORT="6543"` in `.env` for transaction mode (or `"5432"` for session).  
- Restart your app and monitor Supabase Reports (Database > Reports > Connections) for usage. 
If using Alembic, transaction mode works for most migrations but may require temporary switches for complex ones.


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
