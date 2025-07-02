#!/usr/bin/env python3
"""
Monorepo Setup Script
Automatically creates a new monorepo with backend (Python/UV) and frontend (Next.js) setup
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


class MonorepoSetup:
    def __init__(
        self, project_name, base_path="/Users/leomartinez/Documents/PythonProjects"
    ):
        self.project_name = project_name
        self.base_path = Path(base_path)
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
│       ├── __init__.py
│       └── main.py
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

        # Add FastAPI and uvicorn
        self.run_command("uv add fastapi uvicorn", cwd=backend_path)

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
- `/backend` - Python backend service (FastAPI)
- `/frontend` - Frontend application (Next.js/React)

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
"""
        self.create_file("README.md", readme_content)


def main():
    parser = argparse.ArgumentParser(
        description="Create a new monorepo with Python backend and Next.js frontend"
    )
    parser.add_argument("project_name", help="Name of the project directory to create")
    parser.add_argument(
        "--base-path",
        default="/Users/leomartinez/Documents/PythonProjects",
        help="Base path where the project will be created (default: %(default)s)",
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
