# Agora Backend

FastAPI backend with SQLAlchemy, Pydantic, and Supabase integration.

## Setup

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**:
   ```bash
   cd backend
   uv sync
   ```

3. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Update `DATABASE_URL` with your Supabase credentials

4. **Run database migrations**:
   ```bash
   uv run alembic upgrade head
   ```

## Running the Server

```bash
uv run uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## API Endpoints

### Health Check
- `GET /api/v1/health` - Health check endpoint

### Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users/` - List users (with pagination)
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

## Database Migrations

Create a new migration:
```bash
uv run alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
uv run alembic upgrade head
```

Rollback migration:
```bash
uv run alembic downgrade -1
```

## Code Quality

Format code:
```bash
uv run ruff format .
```

Lint code:
```bash
uv run ruff check .
```

Type check:
```bash
uv run mypy app/
```

## Frontend Integration

Generate TypeScript types from OpenAPI schema:
```bash
npx openapi-typescript http://localhost:8000/api/v1/openapi.json -o types/api.ts
```
