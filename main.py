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

from templates.backend.alembic_env import ALEMBIC_ENV
from templates.backend.base import BASE
from templates.backend.config import CONFIG
from templates.backend.env_example import ENV_EXAMPLE
from templates.backend.main import MAIN
from templates.backend.pyproject import pyproject_toml
from templates.backend.readme_backend import readme_backend
from templates.backend.readme_db import README_DB
from templates.backend.session import SESSION
from templates.frontend.api_index import API_INDEX
from templates.frontend.env_local_example import ENV_LOCAL_EXAMPLE
from templates.frontend.eslint_config import ESLINT_CONFIG
from templates.frontend.layout_content import LAYOUT_CONTENT
from templates.frontend.login_form import LOGIN_FORM
from templates.frontend.login_page import LOGIN_PAGE
from templates.frontend.prettier_config import PRETTIER_CONFIG
from templates.frontend.react_query_provider import REACT_QUERY_PROVIDER
from templates.frontend.supabase_client import SUPABASE_CLIENT
from templates.frontend.use_auth import USE_AUTH
from templates.root.gitignore import GITIGNORE
from templates.root.readme_root import readme_root
from templates.root.vscode_settings import VSCODE_SETTINGS


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
        self.create_file(".gitignore", GITIGNORE)

    def create_vscode_settings(self):
        """Create .vscode/settings.json"""
        self.create_file(".vscode/settings.json", VSCODE_SETTINGS)

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
        self.create_file("backend/src/app/main.py", MAIN)

        # Create pyproject.toml - using 'backend' as the name to match MONOREPO.md
        self.create_file("backend/pyproject.toml", pyproject_toml(self.project_name))

        # Create backend README
        self.create_file("backend/README.md", readme_backend(self.project_name))

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

        self.create_file("backend/src/app/core/config.py", CONFIG)

        # --------------------------------------------------
        # Environment example file
        self.create_file("backend/.env.example", ENV_EXAMPLE)

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

        self.create_file("backend/src/app/database/models/base.py", BASE)

        self.create_file("backend/src/app/database/session.py", SESSION)

        self.create_file("backend/src/app/database/README.md", README_DB)

        # --------------------------------------------------
        # Alembic initialization and configuration
        alembic_exe = backend_path / ".venv" / "bin" / "alembic"
        self.run_command(f"{alembic_exe} init alembic", cwd=db_dir)

        self.create_file("backend/src/app/database/alembic/env.py", ALEMBIC_ENV)

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

        # dev-time tooling
        self.run_command(
            "npm install -D @types/node prettier eslint "
            "@typescript-eslint/parser @typescript-eslint/eslint-plugin "
            "@supabase/supabase-js @tanstack/react-query @tanstack/react-query-devtools",
            cwd=frontend_path,
        )

        # Create configuration files
        self.create_file("frontend/.prettierrc", PRETTIER_CONFIG)
        self.create_file("frontend/.eslintrc.json", ESLINT_CONFIG)

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

        # ------------------------------------------------------------------
        # Environment template
        self.create_file("frontend/.env.local.example", ENV_LOCAL_EXAMPLE)

        # Supabase client
        self.create_file("frontend/src/lib/supabase.ts", SUPABASE_CLIENT)

        # Axios API wrapper
        self.create_file("frontend/src/api/index.ts", API_INDEX)

        # Auth React hook
        self.create_file("frontend/src/hooks/useAuth.ts", USE_AUTH)

        # React Query Provider component
        self.create_file(
            "frontend/src/components/ReactQueryProvider.tsx", REACT_QUERY_PROVIDER
        )

        # Update root layout to include provider
        layout_path = frontend_path / "src" / "app" / "layout.tsx"
        if layout_path.exists():
            with open(layout_path, "w") as f:
                f.write(LAYOUT_CONTENT)

        # Simple login form component
        self.create_file("frontend/src/components/LoginForm.tsx", LOGIN_FORM)

        # Route page that renders the LoginForm component (Next.js App Router)
        self.create_file("frontend/src/app/login/page.tsx", LOGIN_PAGE)
        # ------------------------------------------------------------------

    def create_readme(self):
        """Create root README.md"""
        self.create_file("README.md", readme_root(self.project_name))


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
