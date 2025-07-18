GITIGNORE = """# Common file types to be ignored

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
