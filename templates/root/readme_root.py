def readme_root(project_name):
    return f"""# {project_name}

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
cp .env.local.example .env.local  # create env file and populate values
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
```bash
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
