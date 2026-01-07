# Quickstart: Phase II Local Development

**Feature**: 002-fullstack-web-auth
**Last Updated**: 2025-12-30
**Estimated Setup Time**: 15-20 minutes

This guide walks you through setting up the Phase II full-stack todo application on your local machine.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13+** (check: `python --version`)
- **Node.js 20+** (check: `node --version`)
- **npm 10+** (check: `npm --version`)
- **Git** (for cloning the repository)
- **Neon PostgreSQL Account** (free tier available at https://neon.tech)

---

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd todo_app_hct
git checkout 002-fullstack-web-auth
```

---

## Step 2: Backend Setup (Python/FastAPI)

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt** should include:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-dotenv==1.0.0
bcrypt==4.1.2
pyjwt==2.8.0
pydantic[email]==2.5.3
```

### 2.4 Create Environment File

Create `backend/.env` with the following content:

```bash
# Database
DATABASE_URL=postgresql://[user]:[password]@[endpoint]/[database]?sslmode=require

# Authentication
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-long-change-this-in-production

# CORS
CORS_ORIGINS=http://localhost:3000
```

**Getting DATABASE_URL from Neon**:
1. Go to https://neon.tech and sign up (free tier)
2. Create a new project named "todo_app"
3. Copy the connection string from the dashboard
4. Replace `[user]`, `[password]`, `[endpoint]`, and `[database]` in `.env`

**Example**:
```
DATABASE_URL=postgresql://todo_user:AbCdEfGh@ep-cool-meadow-123456.us-east-2.aws.neon.tech/todo_db?sslmode=require
```

**Generating BETTER_AUTH_SECRET**:
```bash
# On Linux/macOS:
openssl rand -hex 32

# On Windows (PowerShell):
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

### 2.5 Initialize Database

```bash
# Run database initialization (creates tables)
python -m src.main
```

This will create the `users` and `tasks` tables in your Neon database.

### 2.6 Start Backend Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Backend**:
Open http://localhost:8000/api/health in your browser. You should see:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-30T10:00:00Z"
}
```

---

## Step 3: Frontend Setup (Next.js/TypeScript)

### 3.1 Open New Terminal

Keep the backend server running in the first terminal. Open a new terminal window.

### 3.2 Navigate to Frontend Directory

```bash
cd frontend  # From project root
```

### 3.3 Install Dependencies

```bash
npm install
```

**package.json** should include:
```json
{
  "dependencies": {
    "next": "^15.1.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "tailwindcss": "^3.4.0",
    "@radix-ui/react-alert-dialog": "^1.0.5",
    "@radix-ui/react-dialog": "^1.1.15",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-toast": "^1.1.5",
    "lucide-react": "^0.300.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "tailwindcss-animate": "^1.0.7"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "@types/node": "^20.10.6",
    "@types/react": "^18.2.46",
    "@types/react-dom": "^18.2.18",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "eslint": "^8.56.0",
    "eslint-config-next": "^15.1.0"
  }
}
```

### 3.4 Create Environment File

Create `frontend/.env.local` with the following content:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Note**: The frontend does not need the `BETTER_AUTH_SECRET`. JWT verification is done server-side by the backend.

### 3.5 Start Frontend Development Server

```bash
npm run dev
```

**Expected Output**:
```
   ▲ Next.js 15.1.0
   - Local:        http://localhost:3000
   - Ready in 2.1s
```

---

## Step 4: Access the Application

1. **Open Browser**: Navigate to http://localhost:3000
2. **Create Account**:
   - Click "Sign Up"
   - Enter email: `test@example.com`
   - Enter name: `Test User`
   - Enter password: `TestPass123` (min 8 chars, 1 uppercase, 1 lowercase, 1 number)
   - Click "Create Account"
   - You should be automatically logged in and redirected to the dashboard
3. **Task Dashboard**:
   - You should now see the task dashboard
   - Click "Add Task" to create your first task
   - Enter title: `Buy groceries`
   - Enter description: `Milk, eggs, bread`
   - Click "Create Task"
4. **Test Operations**:
   - **Toggle**: Click checkbox to mark task as complete
   - **Edit**: Click "Edit" button, update title/description, click "Save"
   - **Delete**: Click "Delete" button, confirm in modal dialog
5. **Test Persistence**:
   - Logout (click "Logout" button in top-right header)
   - Login again with the same credentials
   - Verify tasks are still present

---

## Step 5: Verify Setup

### Backend Health Check

```bash
curl http://localhost:8000/api/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-30T10:00:00Z"
}
```

### Create User via API (Optional)

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "api-test@example.com",
    "name": "API Test User",
    "password": "ApiTest123"
  }'
```

**Expected Response** (201 Created):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "api-test@example.com",
    "name": "API Test User",
    "created_at": "2025-12-30T10:00:00Z"
  },
  "tokens": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 900
  }
}
```

### Login via API (Optional)

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "api-test@example.com",
    "password": "ApiTest123"
  }'
```

**Expected Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

---

## Troubleshooting

### Issue: Backend won't start - "ModuleNotFoundError"

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
# Activate venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Database connection error

**Solution**: Verify `DATABASE_URL` in `backend/.env`:
- Check Neon dashboard for correct connection string
- Ensure `?sslmode=require` is appended
- Test connection manually:
  ```bash
  psql "postgresql://user:pass@endpoint/db?sslmode=require"
  ```

### Issue: Frontend API calls fail (CORS error)

**Solution**: Ensure backend `CORS_ORIGINS` includes `http://localhost:3000`:
```bash
# backend/.env
CORS_ORIGINS=http://localhost:3000
```

Restart backend server after changing `.env`.

### Issue: JWT token errors (401 Unauthorized)

**Solution**: Ensure `BETTER_AUTH_SECRET` is IDENTICAL in both `backend/.env` and `frontend/.env.local`.

### Issue: Frontend shows "Network Error"

**Solution**: Verify backend is running on http://localhost:8000:
```bash
curl http://localhost:8000/api/health
```

If not responding, restart backend server.

### Issue: Tasks not persisting after logout

**Solution**: Check database tables exist:
```bash
# Connect to Neon database
psql "postgresql://user:pass@endpoint/db?sslmode=require"

# List tables
\dt

# Should show: users, tasks
```

If tables don't exist, run database initialization:
```bash
python -m src.main
```

---

## Next Steps

- **Run Tests**: See `backend/tests/` and `frontend/tests/` for test suites
- **API Documentation**: View OpenAPI spec at http://localhost:8000/docs (FastAPI auto-generates Swagger UI)
- **Customize UI**: Modify shadcn/ui components in `frontend/src/components/ui/`
- **Add Features**: Refer to `specs/002-fullstack-web-auth/tasks.md` for implementation tasks

---

## Development Tips

1. **Hot Reload**: Both backend (`--reload`) and frontend (`npm run dev`) support hot reload
2. **Database Browser**: Use Neon's web-based SQL editor to query database
3. **API Testing**: Use FastAPI's built-in Swagger UI at http://localhost:8000/docs
4. **Logs**: Backend logs SQL queries when `echo=True` in `database.py`
5. **Port Conflicts**: If ports 3000 or 8000 are in use, update `.env` and restart servers

---

## Environment Summary

| Component | URL | Port |
|-----------|-----|------|
| Frontend | http://localhost:3000 | 3000 |
| Backend API | http://localhost:8000 | 8000 |
| API Docs (Swagger) | http://localhost:8000/docs | 8000 |
| Database | Neon PostgreSQL (remote) | 5432 (via SSL) |

---

## Support

For issues or questions:
1. Check `specs/002-fullstack-web-auth/spec.md` for requirements
2. Review `specs/002-fullstack-web-auth/plan.md` for architecture
3. Consult `specs/002-fullstack-web-auth/research.md` for technology integration details
