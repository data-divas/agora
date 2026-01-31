.PHONY: help install dev-install clean test lint format typecheck run migrate migrate-auto migrate-rollback db-upgrade db-downgrade server dev docs api-types health check all

# Default target
help:
	@echo "Agora - Available Make targets:"
	@echo ""
	@echo "  Setup & Installation:"
	@echo "    install          - Install production dependencies"
	@echo "    dev-install      - Install all dependencies including dev tools"
	@echo "    clean            - Remove cache files and virtual environment"
	@echo ""
	@echo "  Development:"
	@echo "    run              - Run the FastAPI server with hot reload"
	@echo "    dev              - Alias for run"
	@echo "    server           - Run server without reload (production mode)"
	@echo "    docs             - Open API documentation in browser"
	@echo ""
	@echo "  Database:"
	@echo "    migrate          - Run all pending database migrations"
	@echo "    migrate-auto     - Create a new auto-generated migration"
	@echo "    migrate-rollback - Rollback the last migration"
	@echo "    db-upgrade       - Alias for migrate"
	@echo "    db-downgrade     - Downgrade database by one revision"
	@echo ""
	@echo "  Code Quality:"
	@echo "    test             - Run tests with pytest"
	@echo "    lint             - Run ruff linter"
	@echo "    format           - Format code with ruff"
	@echo "    typecheck        - Run mypy type checking"
	@echo "    check            - Run all checks (lint + typecheck + test)"
	@echo ""
	@echo "  Frontend Integration:"
	@echo "    api-types        - Generate TypeScript types from OpenAPI schema"
	@echo ""
	@echo "  Utilities:"
	@echo "    health           - Check if the API server is running"
	@echo "    all              - Install deps, migrate DB, and run server"

# Setup & Installation
install:
	cd backend && uv sync --no-dev

dev-install:
	cd backend && uv sync

clean:
	cd backend && rm -rf .venv
	cd backend && find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	cd backend && find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	cd backend && find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	cd backend && find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	cd backend && find . -type f -name "*.pyc" -delete

# Development
run:
	cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev: run

server:
	cd backend && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

docs:
	@echo "Opening API documentation..."
	@open http://localhost:8000/docs 2>/dev/null || xdg-open http://localhost:8000/docs 2>/dev/null || echo "Please open http://localhost:8000/docs in your browser"

# Database
migrate:
	cd backend && uv run alembic upgrade head

migrate-auto:
	@read -p "Enter migration message: " msg; \
	cd backend && uv run alembic revision --autogenerate -m "$$msg"

migrate-rollback:
	cd backend && uv run alembic downgrade -1

db-upgrade: migrate

db-downgrade:
	cd backend && uv run alembic downgrade -1

# Code Quality
test:
	cd backend && uv run pytest -v

lint:
	cd backend && uv run ruff check .

format:
	cd backend && uv run ruff format .
	cd backend && uv run ruff check --fix .

typecheck:
	cd backend && uv run mypy app/

check: lint typecheck test

# Frontend Integration
api-types:
	@echo "Make sure the server is running first (make run)"
	@echo "Generating TypeScript types..."
	npx openapi-typescript http://localhost:8000/api/v1/openapi.json -o types/api.ts

# Utilities
health:
	@curl -s http://localhost:8000/api/v1/health | python3 -m json.tool || echo "Server is not running"

# Combined workflow
all: dev-install migrate run
