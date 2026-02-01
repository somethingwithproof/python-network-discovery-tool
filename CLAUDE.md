# python-network-discovery-tool

## Purpose
Nmap-based network discovery tool with async scanning, multiple report formats, and optional Redis/DB backends.

## Stack
- Python 3.10+, setuptools, uv for dependency management
- Dependencies: python-nmap, paramiko, pydantic, typer, fastapi, uvicorn, jinja2, openpyxl
- Optional: pymysql, pg8000, snimpy/pysnmp, redis, dnspython, fpdf2
- Dev: ruff, mypy, pytest, pytest-asyncio, pre-commit
- Docker + docker-compose support

## Build / Test
```bash
pip install -e ".[dev]"
pytest tests/
ruff check .
mypy src/
# Docker
docker build -t network-discovery .
docker-compose run network-discovery 192.168.1.0/24
```

## Standards
- Python 3.12+, strict mypy, ruff (line-length 100)
- Google Python Style Guide docstrings
- Type hints required, pydantic for models
- Clean Architecture (domain/infrastructure/interfaces)

## Conventions
- `src/network_discovery/` for package source
- `tests/` for test suite
- `docs/` for MkDocs documentation
- `scripts/` and `tools/` for helper scripts
- `templates/` for report templates
- CLI entry point: `network-discovery` via typer
- `uv.lock` committed for reproducible builds
