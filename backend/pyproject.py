def pyproject_toml(project_name):
    return f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "backend"
version = "0.1.0"
description = "Backend service for {project_name}"
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
