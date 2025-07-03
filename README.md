# create-monorepo 🏗️

`create-monorepo` is a tiny CLI that spins up a full-stack monorepo in **seconds**:

* FastAPI backend (Python + UV)
* Next.js / React frontend (TypeScript + Tailwind + Turbopack)
* Single shared `.gitignore` and VS Code settings
* Automatic virtual-env, Ruff, Prettier, ESLint, Tailwind, etc.

---

## Prerequisites

| Tool | Version | Why |
|------|---------|-----|
| Python | 3.11 + | runs the CLI and backend |
| [UV](https://github.com/astral-sh/uv) | latest | Python dependency manager |
| Node + npm | 18 + | Next.js frontend |
| git | any | version control |

Make sure `uv`, `npm`, and `git` are on your **PATH**.

---

## Installation

### 1. Development / editable (inside repo)
```bash
git clone https://github.com/your-name/create-monorepo.git
cd create-monorepo
pip install -e .
```

### 2. Global (via **pipx** — recommended)
```bash
# once:
pipx install ./create-monorepo     # from local clone
# or directly from GitHub:
pipx install git+https://github.com/your-name/create-monorepo.git
```
After either method you get a global command:
```bash
create-monorepo --help
```

---

## Configuration

### Default Base Path

By default, `create-monorepo` will create projects in `~/Projects`. You can customize this in three ways:

1. **Command line flag** (highest priority):
   ```bash
   create-monorepo my-project --base-path ~/code
   ```

2. **Environment variable** (persistent):
   ```bash
   # Add to ~/.zshrc or ~/.bashrc
   export MONOREPO_BASE_PATH="$HOME/Documents/PythonProjects"
   
   # Then use normally
   create-monorepo my-project
   ```

3. **Default** (lowest priority):
   - If no flag or environment variable is set, defaults to `~/Projects`

---

## Usage

```bash
# create a new project directory under ~/Projects (or your configured base path)
create-monorepo my-awesome-project

# specify a custom base path
create-monorepo my-awesome-project --base-path ~/code
```

When it finishes you'll see something like:
```
📂 Project location: /path/to/my-awesome-project

🔧 Next steps:
  1. cd /path/to/my-awesome-project
  2. git add . && git commit -m 'Initial commit'
  3. Backend: cd backend && source .venv/bin/activate && python -m uvicorn app.main:app --reload
  4. Frontend: cd frontend && npm run dev
```

---

## "One-click" / single-command options

### Shell alias (simplest)
Add to `~/.zshrc` or `~/.bashrc`:
```bash
alias cm='create-monorepo'
```
Reload (`source ~/.zshrc`) and then:
```bash
cm my-project
```

### macOS Quick Action button
1. Open **Automator** → *New* → *Quick Action* (or *App* if you want a dock icon).
2. Add **"Run Shell Script"**.
3. Script contents:
   ```bash
   /usr/local/bin/create-monorepo "$@"
   ```
   (Find the path with `which create-monorepo`.)
4. Save as "Create Monorepo".
5. Optionally add a keyboard shortcut in **System Settings → Keyboard → Shortcuts → Services**.

Now you can trigger the quick action, enter a project name, and your monorepo is scaffolded automatically.
