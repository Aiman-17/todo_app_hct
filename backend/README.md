# Backend - FastAPI Todo Application

FastAPI backend for the Todo application with JWT authentication and PostgreSQL/SQLite database support.

## Features

- **JWT Authentication**: Secure user authentication with access and refresh tokens
- **User Isolation**: Tasks are isolated by user_id for data security
- **SQLModel ORM**: Type-safe database operations with Pydantic validation
- **PostgreSQL/SQLite**: Supports both PostgreSQL (production) and SQLite (development)
- **API Documentation**: Auto-generated OpenAPI/Swagger docs at `/docs`
- **CORS Support**: Configurable cross-origin resource sharing
- **Password Hashing**: bcrypt with 12 rounds for secure password storage
- **Comprehensive Testing**: Unit and integration tests with pytest

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- PostgreSQL (for production) or SQLite (for development)

## Quick Start

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database URL
# For SQLite (development):
DATABASE_URL=sqlite:///./test.db
# For PostgreSQL (production):
# DATABASE_URL=postgresql://user:password@host:5432/dbname

# Authentication Secret (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
BETTER_AUTH_SECRET=your-secret-key-here

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Generate a secure secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Run Database Migrations

The application automatically creates tables on startup. No manual migrations needed for initial setup.

### 5. Start Development Server

```bash
uvicorn src.main:app --reload --port 8000
```

The API will be available at:
- **API Base**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/api/health

## Project Structure

```
backend/
├── src/
│   ├── api/           # API route handlers
│   │   ├── auth.py    # Authentication endpoints
│   │   └── tasks.py   # Task CRUD endpoints
│   ├── models/        # SQLModel database models
│   │   ├── user.py    # User model
│   │   └── task.py    # Task model
│   ├── schemas/       # Pydantic request/response schemas
│   │   ├── auth.py    # Auth schemas
│   │   └── task.py    # Task schemas
│   ├── services/      # Business logic layer
│   │   ├── auth_service.py    # Authentication logic
│   │   ├── user_service.py    # User operations
│   │   └── task_service.py    # Task operations
│   ├── config.py      # Configuration management
│   ├── database.py    # Database connection setup
│   ├── dependencies.py # Dependency injection
│   └── main.py        # FastAPI application entry point
├── tests/             # Test suite
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── conftest.py    # Pytest fixtures
├── .env               # Environment variables (create this)
├── .env.example       # Environment template
└── requirements.txt   # Python dependencies
```

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/signup` | Register new user | No |
| POST | `/api/auth/login` | Login user | No |
| GET | `/api/auth/profile` | Get user profile | Yes |

### Tasks

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/tasks` | Get all user's tasks | Yes |
| POST | `/api/tasks` | Create new task | Yes |
| PUT | `/api/tasks/{id}` | Update task | Yes |
| DELETE | `/api/tasks/{id}` | Delete task | Yes |
| PATCH | `/api/tasks/{id}/toggle` | Toggle task completion | Yes |

### Health Check

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/health` | Health check | No |

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

- **Access Token**: 15-minute expiry (for API requests)
- **Refresh Token**: 7-day expiry (for obtaining new access tokens)

Include the access token in the `Authorization` header:
```
Authorization: Bearer <access_token>
```

## Running Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_models.py -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
```

## Database Schema

### Users Table
- `id` (UUID): Primary key
- `email` (String): Unique, indexed
- `name` (String): User's display name
- `password_hash` (String): bcrypt hashed password
- `created_at` (DateTime): Account creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Tasks Table
- `id` (Integer): Primary key, auto-increment
- `user_id` (UUID): Foreign key to users.id, indexed
- `title` (String, max 200): Task title
- `description` (String, max 2000): Task description
- `completed` (Boolean): Completion status, default False
- `created_at` (DateTime): Task creation timestamp
- `updated_at` (DateTime): Last update timestamp
- Composite index on (user_id, completed, created_at DESC)

## Security Features

- Password hashing with bcrypt (12 rounds)
- JWT token-based authentication
- User data isolation (users can only access their own tasks)
- CORS configuration for frontend access
- Input validation with Pydantic
- SQL injection prevention via SQLModel ORM

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | Database connection string | Yes | - |
| `BETTER_AUTH_SECRET` | JWT signing secret (min 32 chars) | Yes | - |
| `CORS_ORIGINS` | Allowed origins (comma-separated) | Yes | - |

## Deployment

For production deployment:

1. Use PostgreSQL instead of SQLite
2. Set strong `BETTER_AUTH_SECRET` (32+ characters)
3. Configure `CORS_ORIGINS` to production frontend URL
4. Use a production ASGI server (already using uvicorn)
5. Enable HTTPS/SSL
6. Set up proper logging and monitoring
7. Configure database connection pooling

See `../specs/002-fullstack-web-auth/deployment.md` for detailed deployment instructions.

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` in `.env` is correct
- For PostgreSQL, ensure the database exists and credentials are valid
- For SQLite, check file permissions

### Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Authentication Errors
- Verify `BETTER_AUTH_SECRET` is set in `.env`
- Check token expiration (access tokens expire in 15 minutes)

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Project Quickstart Guide](../specs/002-fullstack-web-auth/quickstart.md)
- [API Specification](../specs/002-fullstack-web-auth/contracts/openapi.yaml)

## License

See root README.md for license information.
