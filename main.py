#!/usr/bin/env python3
"""
Monorepo Setup Script
Automatically creates a new monorepo with backend (Python/UV) and frontend (Next.js) setup
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


class MonorepoSetup:
    def __init__(self, project_name, base_path=None):
        self.project_name = project_name

        # Determine base path with fallback hierarchy
        if base_path:
            # Use explicitly provided path
            self.base_path = Path(base_path)
        elif os.environ.get("MONOREPO_BASE_PATH"):
            # Use environment variable if set
            self.base_path = Path(os.environ["MONOREPO_BASE_PATH"])
        else:
            # Use sensible default: ~/Projects
            self.base_path = Path.home() / "Projects"

        self.project_path = self.base_path / project_name

    def run_command(self, command, cwd=None, shell=True, check=True):
        """Run a shell command and handle errors"""
        print(f"➤ Running: {command}")
        try:
            result = subprocess.run(
                command,
                shell=shell,
                cwd=cwd or self.project_path,
                capture_output=True,
                text=True,
                check=check,
            )
            if result.stdout:
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running command: {command}")
            print(f"Error output: {e.stderr}")
            sys.exit(1)

    def create_file(self, relative_path, content):
        """Create a file with the given content"""
        file_path = self.project_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"📝 Creating: {relative_path}")
        with open(file_path, "w") as f:
            f.write(content)

    def remove_file(self, relative_path):
        """Remove a file if it exists"""
        file_path = self.project_path / relative_path
        if file_path.exists():
            print(f"🗑️  Removing: {relative_path}")
            file_path.unlink()

    def setup(self):
        """Run the complete monorepo setup"""
        print(f"\n🚀 Setting up monorepo: {self.project_name}")
        print(f"📍 Location: {self.project_path}\n")

        # Ensure base path exists
        if not self.base_path.exists():
            print(f"📁 Creating base directory: {self.base_path}")
            self.base_path.mkdir(parents=True, exist_ok=True)

        # Check if directory already exists
        if self.project_path.exists():
            response = input(
                f"⚠️  Directory {self.project_path} already exists. Remove it? (y/N): "
            )
            if response.lower() == "y":
                shutil.rmtree(self.project_path)
            else:
                print("Setup cancelled.")
                sys.exit(0)

        # Create project structure
        self.create_project_structure()
        self.create_gitignore()

        # Initialize git immediately to prevent subdirectory repos
        print("📦 Initializing git repository...")
        self.run_command("git init", check=False)

        self.create_vscode_settings()
        self.setup_backend()
        self.setup_frontend()
        self.create_readme()

        print("\n✅ Monorepo setup complete!")
        print(f"\n📂 Project location: {self.project_path}")
        print("\n🔧 Next steps:")
        print("  1. cd " + str(self.project_path))
        print("  2. git add . && git commit -m 'Initial commit'")
        print(
            "  3. Backend: cd backend && source .venv/bin/activate && python -m uvicorn app.main:app --reload"
        )
        print("  4. Frontend: cd frontend && npm run dev")

    def create_project_structure(self):
        """Create initial directory structure"""
        print("📁 Creating project structure...")
        self.project_path.mkdir(parents=True, exist_ok=True)
        (self.project_path / "frontend").mkdir(exist_ok=True)
        (self.project_path / "backend").mkdir(exist_ok=True)

    def create_gitignore(self):
        """Create root .gitignore file"""
        gitignore_content = """# Common file types to be ignored

# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info
*.egg
*$py.class
.Python
downloads/
develop-eggs/
eggs/
.eggs/
lib64/
parts/
sdist/
var/
.installed.cfg

# C extensions
*.so

# Virtual environments
.venv

# Environment variables
.env
.env.local
env/
venv/
ENV/
.env.deployment

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# PyInstaller
# Usually these files are written by a python script from a template
# before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# IDE files
.idea/
*.swp
*.swo

# Jupyter
.ipynb_checkpoints/

# Django / Flask locals
local_settings.py
db.sqlite3
instance/
.webassets-cache

# Cython debug
cython_debug/

# pip installer logs
pip-log.txt
pip-delete-this-directory.txt

# Scratch files
scratch.py
scratch
notes

# Windows extensions
*.pyd

# OS files
.DS_Store
Thumbs.db

# Other files
*.csv
*.png
*.xlsx

# dependencies
**/node_modules/
node_modules
node_modules/
/node_modules
.pnp
.pnp.*
.yarn/*
!.yarn/patches
!.yarn/plugins
!.yarn/releases
!.yarn/versions

# testing
coverage

# next.js
**/.next/
.next
.next/
/.next
out/

# misc
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts

# logs
logs/
"""
        self.create_file(".gitignore", gitignore_content)

    def create_vscode_settings(self):
        """Create .vscode/settings.json"""
        vscode_settings = """{
  "python.defaultInterpreterPath": "./backend/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.linting.flake8Enabled": false,
  "python.linting.pylintEnabled": false,
  "ruff.nativeServer": "on",

  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    },
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}"""
        self.create_file(".vscode/settings.json", vscode_settings)

    def setup_backend(self):
        """Setup backend with UV and Python"""
        print("\n🐍 Setting up backend...")
        backend_path = self.project_path / "backend"

        # Initialize UV project
        self.run_command("uv init .", cwd=backend_path)

        # Remove UV's auto-generated files
        self.remove_file("backend/.gitignore")
        self.remove_file(
            "backend/hello.py"
        )  # UV sometimes creates this instead of main.py
        self.remove_file("backend/main.py")  # Remove if UV created it in root

        # Create virtual environment
        self.run_command("uv venv", cwd=backend_path)

        # Create source structure
        (backend_path / "src" / "app").mkdir(parents=True, exist_ok=True)
        self.create_file("backend/src/app/__init__.py", "")

        # Create main.py with basic FastAPI app
        main_py_content = '''"""Main application file"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Backend API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello from backend!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
'''
        self.create_file("backend/src/app/main.py", main_py_content)

        # Create pyproject.toml - using 'backend' as the name to match MONOREPO.md
        pyproject_content = f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "backend"
version = "0.1.0"
description = "Backend service for {self.project_name}"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []

[tool.setuptools.packages.find]
where = ["src"]

[tool.uv.sources]
backend = {{ workspace = true }}

[dependency-groups]
dev = [
    "backend",
]"""
        self.create_file("backend/pyproject.toml", pyproject_content)

        # Create backend README
        backend_readme = f"""# {self.project_name} Backend

## Overview
FastAPI backend service for {self.project_name}.

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
Copy `.env.example` to `.env` and fill in your Supabase credentials.

```bash
cp .env.example .env
```

## Development
```bash
# Run the development server
python -m uvicorn app.main:app --reload --port 8000

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
        self.create_file("backend/README.md", backend_readme)

        # Install dependencies (UV doesn't need venv activation)
        print("📦 Installing backend dependencies...")

        # Install editable and dev dependencies
        self.run_command("uv add --editable . --dev", cwd=backend_path)

        # Add ruff
        self.run_command("uv add --dev ruff", cwd=backend_path)

        # Sync dependencies
        self.run_command("uv sync --dev", cwd=backend_path)

        # --------------------------------------------------
        # Add backend dependencies (FastAPI and uvicorn, DB, migrations, env management)
        self.run_command(
            "uv add fastapi uvicorn alembic sqlalchemy psycopg psycopg2 pydantic-settings python-dotenv supabase",
            cwd=backend_path,
        )

        # Install newly added dependencies into the virtual-env
        self.run_command("uv sync --dev", cwd=backend_path)

        # --------------------------------------------------
        # Create core configuration package
        core_dir = backend_path / "src" / "app" / "core"
        core_dir.mkdir(parents=True, exist_ok=True)
        self.create_file("backend/src/app/core/__init__.py", "")

        core_config = """from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from supabase import create_client


class Settings(BaseSettings):
    # supabase
    DB_USER: str = "postgres"
    DB_NAME: str = "postgres"
    DB_PORT: str = "5432"
    DEV_LOGS: bool = False
    SUPABASE_DB_PASSWORD: str
    SUPABASE_PROJECT_ID: str

    # supabase storage
    SUPABASE_BUCKET: str = "your-bucket-name"
    SUPABASE_URL: str
    SUPABASE_KEY: str

    @property
    def supabase_connection_string(self):
        # normal url encoding (runtime usage)
        encoded_password = quote_plus(self.SUPABASE_DB_PASSWORD)
        return (
            f"postgresql://{self.DB_USER}.{self.SUPABASE_PROJECT_ID}:{encoded_password}"
            f"@aws-0-us-east-2.pooler.supabase.com:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def async_supabase_connection_string(self):
        return self.supabase_connection_string.replace(
            "postgresql://", "postgresql+psycopg://"
        )

    @property
    def supabase_connection_string_alembic(self):
        # alembic-compatible connection string with '%%'
        encoded_password = quote_plus(self.SUPABASE_DB_PASSWORD).replace('%', '%%')
        return (
            f"postgresql://{self.DB_USER}.{self.SUPABASE_PROJECT_ID}:{encoded_password}"
            f"@aws-0-us-east-2.pooler.supabase.com:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=True,
    )


load_dotenv()

settings = Settings()

sb_client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY,
)
"""
        self.create_file("backend/src/app/core/config.py", core_config)

        # --------------------------------------------------
        # Environment example file
        env_example = """# supabase
SUPABASE_DB_PASSWORD=your-password
SUPABASE_PROJECT_ID=your-project-id
SUPABASE_URL=your-url
SUPABASE_KEY=your-key
"""
        self.create_file("backend/.env.example", env_example)

        # --------------------------------------------------
        # Database package setup
        db_dir = backend_path / "src" / "app" / "database"
        models_dir = db_dir / "models"
        models_dir.mkdir(parents=True, exist_ok=True)

        self.create_file("backend/src/app/database/__init__.py", "")

        self.create_file(
            "backend/src/app/database/models/__init__.py",
            'from .base import Base\n\n__all__ = ["Base"]\n',
        )

        base_model = """from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class Mixins:
    def to_dict(self):
        mapper = inspect(self).mapper
        return {attr.key: getattr(self, attr.key) for attr in mapper.column_attrs}


class Base(Mixins, DeclarativeBase):
    pass
"""
        self.create_file("backend/src/app/database/models/base.py", base_model)

        session_py = """from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# synchronous session
engine = create_engine(settings.supabase_connection_string, echo=settings.DEV_LOGS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# asynchronous session
async_engine = create_async_engine(
    settings.async_supabase_connection_string, echo=settings.DEV_LOGS
)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@contextmanager
def get_session() -> Generator[Any, Any, Any]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as adb:
        try:
            yield adb
        finally:
            await adb.close()


class BaseSession:
    def __init__(self):
        self.session = None
        self._session_cm = None

    def __enter__(self):
        self._session_cm = get_session()
        self.session = self._session_cm.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            # log or handle the exception here
            pass
        else:
            self.session.commit()
        return self._session_cm.__exit__(exc_type, exc_val, exc_tb)
"""
        self.create_file("backend/src/app/database/session.py", session_py)

        db_readme = """# Database & Migrations Guide

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
        self.create_file("backend/src/app/database/README.md", db_readme)

        # --------------------------------------------------
        # Alembic initialization and configuration
        alembic_exe = backend_path / ".venv" / "bin" / "alembic"
        self.run_command(f"{alembic_exe} init alembic", cwd=db_dir)

        alembic_env = """from logging.config import fileConfig

from alembic import context
from app.core.config import settings
from app.database.models.base import Base
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override the sqlalchemy.url setting with an environment variable value
DATABASE_URL = settings.supabase_connection_string_alembic

if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
else:
    raise Exception("DATABASE_URL environment variable is not set.")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    '''Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    '''
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    '''Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    '''
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""
        self.create_file("backend/src/app/database/alembic/env.py", alembic_env)

    def setup_frontend(self):
        """Setup frontend with Next.js"""
        print("\n⚛️  Setting up frontend...")
        frontend_path = self.project_path / "frontend"

        # Create Next.js app - exactly matching MONOREPO.md
        # Using stdin to handle any prompts
        create_next_cmd = """npx create-next-app@latest . \\
  --typescript \\
  --tailwind \\
  --app \\
  --src-dir \\
  --import-alias "@/*" \\
  --no-eslint \\
  --turbo"""

        # Run with 'y' piped to stdin to accept package installation
        process = subprocess.Popen(
            create_next_cmd,
            shell=True,
            cwd=frontend_path,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Send 'y' to accept npx package installation
        stdout, stderr = process.communicate(input="y\n")

        if process.returncode != 0:
            print("❌ Error creating Next.js app")
            print(f"Error output: {stderr}")
            sys.exit(1)
        else:
            print(stdout)

        # Remove the auto-generated .gitignore
        self.remove_file("frontend/.gitignore")

        # Install additional dependencies
        print("📦 Installing frontend dependencies...")
        self.run_command("npm install axios", cwd=frontend_path)

        self.run_command(
            "npm install -D @types/node prettier eslint "
            "@typescript-eslint/parser @typescript-eslint/eslint-plugin",
            cwd=frontend_path,
        )

        # Create configuration files
        prettier_config = """{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "tabWidth": 2,
  "printWidth": 80
}"""
        self.create_file("frontend/.prettierrc", prettier_config)

        eslint_config = """{
  "extends": ["next/core-web-vitals", "plugin:@typescript-eslint/recommended"],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "warn"
  }
}"""
        self.create_file("frontend/.eslintrc.json", eslint_config)

        # Update tsconfig.json to add forceConsistentCasingInFileNames
        tsconfig_path = frontend_path / "tsconfig.json"
        if tsconfig_path.exists():
            import json

            with open(tsconfig_path, "r") as f:
                tsconfig = json.load(f)

            # Update target to match MONOREPO.md
            tsconfig["compilerOptions"]["target"] = "ES2017"
            tsconfig["compilerOptions"]["forceConsistentCasingInFileNames"] = True

            with open(tsconfig_path, "w") as f:
                json.dump(tsconfig, f, indent=2)

    def create_readme(self):
        """Create root README.md"""
        readme_content = f"""# {self.project_name}

## Structure
- [Backend](backend/README.md) - Python backend service (FastAPI)
- [Frontend](frontend/README.md) - Frontend application (Next.js/React)

## Getting Started

### Prerequisites
- Python 3.13+
- Node.js 18+
- UV (https://github.com/astral-sh/uv)

### Backend
```bash
cd backend
source .venv/bin/activate  # Unix/macOS
# or
.venv\\Scripts\\activate  # Windows
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

## Development

### Add Backend Dependencies
```bash
cd backend && source .venv/bin/activate
uv add package-name              # Production
uv add --dev package-name        # Development
```

### Add Frontend Dependencies
```bash
cd frontend
npm install package-name         # Production
npm install -D package-name      # Development
```

### Create git repository
```base
`gh auth switch`  # switch the right account
git config user.name "your-user-name"
git config user.email "your-email"
git add .
git commit -m "initial commit"
gh repo create repo-name --public/private  # public or private
git remote add origin git@host:user-name/repo-name.git
git push -u origin master
```
"""
        self.create_file("README.md", readme_content)


def main():
    parser = argparse.ArgumentParser(
        description="Create a new monorepo with Python backend and Next.js frontend"
    )
    parser.add_argument("project_name", help="Name of the project directory to create")
    parser.add_argument(
        "--base-path",
        default=None,
        help="Base path where the project will be created (default: $MONOREPO_BASE_PATH or ~/Projects)",
    )

    args = parser.parse_args()

    # Validate project name
    if not args.project_name.replace("-", "").replace("_", "").isalnum():
        print(
            "❌ Error: Project name should only contain letters, numbers, hyphens, and underscores"
        )
        sys.exit(1)

    # Run setup
    setup = MonorepoSetup(args.project_name, args.base_path)
    setup.setup()


if __name__ == "__main__":
    main()
