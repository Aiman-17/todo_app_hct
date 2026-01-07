# Research: Phase II Technology Integration

**Feature**: 002-fullstack-web-auth
**Date**: 2025-12-30
**Research Areas**: Better Auth integration, SQLModel best practices, Next.js 16 App Router patterns, Neon PostgreSQL connection, shadcn/ui setup, password validation

## 1. Better Auth Integration (Python + TypeScript SDK)

### Overview
Better Auth is a framework-agnostic authentication library with first-class support for both backend and frontend. It provides JWT token management, session handling, and secure password hashing.

### Backend (Python/FastAPI)
- **Installation**: `pip install better-auth-python`
- **JWT Token Generation**:
  ```python
  from better_auth import BetterAuth

  auth = BetterAuth(secret=os.getenv("BETTER_AUTH_SECRET"))
  access_token = auth.create_access_token(
      user_id=user.id,
      expires_in=timedelta(minutes=15)
  )
  refresh_token = auth.create_refresh_token(
      user_id=user.id,
      expires_in=timedelta(days=7)
  )
  ```
- **JWT Validation Middleware**:
  ```python
  from fastapi import Depends, HTTPException, status
  from fastapi.security import HTTPBearer

  security = HTTPBearer()

  async def get_current_user(token: str = Depends(security)) -> User:
      try:
          payload = auth.verify_token(token.credentials)
          user_id = payload.get("user_id")
          # Query user from database using SQLModel
          return user
      except Exception:
          raise HTTPException(status_code=401, detail="Invalid token")
  ```

### Frontend (TypeScript/Next.js)
- **Installation**: `npm install @better-auth/react`
- **Client Configuration**:
  ```typescript
  // src/lib/auth.ts
  import { createAuthClient } from '@better-auth/react';

  export const authClient = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    credentials: 'include', // For httpOnly cookies
  });
  ```
- **Token Storage**: Store access token in httpOnly cookies for security (prevents XSS attacks). Refresh token also stored in httpOnly cookies.
- **Automatic Token Refresh**: Better Auth SDK handles refresh token flow automatically when access token expires.

### Key Decisions
- **Shared Secret**: Both frontend and backend MUST use the same `BETTER_AUTH_SECRET` environment variable for JWT signing/verification.
- **Token Expiry**: Access token: 15 minutes (short-lived, reduces compromise risk), Refresh token: 7 days (balances security and UX).
- **Password Hashing**: Use `bcrypt` with salt rounds = 12 (industry standard).

---

## 2. SQLModel Best Practices (Neon PostgreSQL)

### Overview
SQLModel is a library that combines SQLAlchemy and Pydantic, providing type-safe database models with automatic validation.

### Connection Pooling for Neon
Neon is a serverless PostgreSQL database that benefits from connection pooling to avoid cold starts.

```python
# backend/src/database.py
from sqlmodel import create_engine, Session, SQLModel
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # postgresql://user:pass@host/db?sslmode=require

# Connection pooling configuration for Neon
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries in development
    pool_size=5,  # Max 5 connections in pool
    max_overflow=10,  # Allow 10 overflow connections
    pool_pre_ping=True,  # Verify connection before use (handles Neon cold starts)
    pool_recycle=3600,  # Recycle connections after 1 hour
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

### CRUD Patterns with User Isolation

**Create Task**:
```python
# backend/src/services/task_service.py
from sqlmodel import Session, select
from models.task import Task

def create_task(session: Session, user_id: str, title: str, description: str = "") -> Task:
    task = Task(
        user_id=user_id,  # From JWT token
        title=title,
        description=description,
        completed=False
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**Read Tasks (User Isolated)**:
```python
def get_user_tasks(session: Session, user_id: str) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id).order_by(
        Task.completed.asc(),  # Incomplete first
        Task.created_at.desc()  # Newest first within each group
    )
    tasks = session.exec(statement).all()
    return tasks
```

**Update Task (with Authorization Check)**:
```python
def update_task(session: Session, task_id: int, user_id: str, title: str = None, description: str = None) -> Task:
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    if not task:
        raise ValueError("Task not found or access denied")

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description

    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Key Decisions
- **NO raw SQL**: All queries MUST use SQLModel `select()`, `where()`, `order_by()` methods.
- **Session Management**: Use FastAPI dependency injection with `Depends(get_session)` to manage sessions.
- **Authorization**: ALWAYS filter by `user_id` in queries to prevent cross-user access.

---

## 3. Next.js 16 App Router Patterns

### Overview
Next.js 16 introduces the App Router (`app/` directory) with Server Components by default, enabling server-side rendering and improved performance.

### Server Components vs Client Components

**Server Components** (default):
- Render on server, send HTML to client
- Can directly query databases (but we won't—backend API handles this)
- Cannot use React hooks (useState, useEffect) or browser APIs
- Use for: layouts, static content, data fetching from backend API

**Client Components** (`"use client"` directive):
- Render on client, enable interactivity
- Can use React hooks and browser APIs
- Use for: forms, interactive UI, state management

### Example: Dashboard Page (Hybrid Approach)

```typescript
// app/dashboard/page.tsx (Server Component)
import { TaskList } from '@/components/tasks/TaskList';

export default async function DashboardPage() {
  // Fetch tasks server-side (reduces client-side loading)
  // BUT: still calls backend API, NOT direct DB access
  const tasks = await fetch(`${process.env.API_URL}/api/tasks`, {
    cache: 'no-store', // Always fetch fresh data
    headers: {
      Authorization: `Bearer ${getServerSideToken()}` // From cookies
    }
  }).then(res => res.json());

  return (
    <div>
      <h1>Your Tasks</h1>
      <TaskList initialTasks={tasks} /> {/* Client Component for interactions */}
    </div>
  );
}
```

```typescript
// components/tasks/TaskList.tsx (Client Component)
"use client";

import { useState } from 'react';
import { Task } from '@/types/task';

export function TaskList({ initialTasks }: { initialTasks: Task[] }) {
  const [tasks, setTasks] = useState(initialTasks);

  // Handle create, update, delete, toggle with API calls
  // Update local state optimistically for better UX

  return (
    <div>
      {tasks.map(task => (
        <TaskItem key={task.id} task={task} onUpdate={handleUpdate} />
      ))}
    </div>
  );
}
```

### Protected Routes with Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('access_token')?.value;

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*']
};
```

### Key Decisions
- **Default to Server Components**: Use Client Components only when needed (forms, interactive state).
- **API Calls from Server Components**: Fetch initial data server-side for faster page loads.
- **Middleware for Auth**: Check JWT token in middleware to protect routes before rendering.

---

## 4. Neon PostgreSQL Connection

### Overview
Neon is a serverless PostgreSQL database with automatic scaling, branching, and instant provisioning.

### Connection String Format
```
postgresql://[user]:[password]@[endpoint]/[database]?sslmode=require
```

Example:
```
postgresql://todo_user:SecurePass123@ep-cool-meadow-123456.us-east-2.aws.neon.tech/todo_db?sslmode=require
```

### Serverless Considerations
- **Connection Pooling**: Essential for serverless environments to avoid exhausting connections. Use `pool_size=5` and `max_overflow=10` in SQLModel engine.
- **Cold Starts**: Neon may take 1-2 seconds to wake up from idle. Use `pool_pre_ping=True` to verify connections before use.
- **SSL Required**: Neon enforces SSL connections. Always include `?sslmode=require` in connection string.

### Environment Variables
```bash
# backend/.env
DATABASE_URL=postgresql://user:pass@endpoint/db?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
CORS_ORIGINS=http://localhost:3000
```

### Database Initialization
```python
# backend/src/main.py
from database import create_db_and_tables

@app.on_event("startup")
async def startup():
    create_db_and_tables()  # Creates tables if not exist
```

### Key Decisions
- **SSL Mode**: Always use `sslmode=require` for security.
- **Connection Pooling**: Use SQLModel's built-in pooling with Neon-optimized settings.
- **Environment Variables**: Store connection string in `.env`, never commit to version control.

---

## 5. shadcn/ui Component Library

### Overview
shadcn/ui is a collection of re-usable components built with Radix UI and Tailwind CSS. Unlike traditional component libraries, you copy components into your project (full control, no NPM bloat).

### Installation & Setup
```bash
# Initialize shadcn/ui in Next.js project
npx shadcn-ui@latest init

# Install specific components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add form
npx shadcn-ui@latest add label
npx shadcn-ui@latest add toast
```

Components are installed to `src/components/ui/` and can be customized.

### Component Customization Example: Delete Confirmation Modal

```typescript
// components/tasks/DeleteConfirmModal.tsx
"use client";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

export function DeleteConfirmModal({
  open,
  onClose,
  onConfirm
}: {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
}) {
  return (
    <AlertDialog open={open} onOpenChange={onClose}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete Task</AlertDialogTitle>
          <AlertDialogDescription>
            Are you sure you want to delete this task? This action cannot be undone.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            onClick={onConfirm}
            className="bg-destructive text-destructive-foreground"
          >
            Delete
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
```

### Responsive Design
shadcn/ui components are built with Tailwind CSS and are responsive by default. Use Tailwind responsive prefixes:

```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Stacks on mobile, 2 columns on tablet, 3 on desktop */}
</div>
```

### Key Decisions
- **Component Selection**: Use AlertDialog for delete confirmation (matches spec requirement for modal dialog).
- **Customization**: Copy components to `src/components/ui/` for full control (can modify styles, behavior).
- **Accessibility**: shadcn/ui uses Radix UI primitives with built-in ARIA attributes and keyboard navigation.

---

## 6. Password Validation (Frontend + Backend)

### Validation Rules (from spec.md)
- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one number (0-9)

### Frontend Validation (TypeScript/React)

```typescript
// lib/validation.ts
export function validatePassword(password: string): {
  valid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  if (password.length < 8) {
    errors.push("Password must be at least 8 characters");
  }
  if (!/[A-Z]/.test(password)) {
    errors.push("Password must include an uppercase letter");
  }
  if (!/[a-z]/.test(password)) {
    errors.push("Password must include a lowercase letter");
  }
  if (!/[0-9]/.test(password)) {
    errors.push("Password must include a number");
  }

  return {
    valid: errors.length === 0,
    errors
  };
}
```

**Usage in Signup Form**:
```typescript
// components/auth/SignupForm.tsx
const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault();

  const passwordValidation = validatePassword(password);
  if (!passwordValidation.valid) {
    setErrors(passwordValidation.errors);
    return;
  }

  // Submit to backend
  api.post('/api/auth/signup', { email, name, password });
};
```

### Backend Validation (Python/Pydantic)

```python
# backend/src/schemas/auth.py
from pydantic import BaseModel, validator
import re

class UserCreate(BaseModel):
    email: str
    name: str
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must include an uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must include a lowercase letter")
        if not re.search(r'[0-9]', v):
            raise ValueError("Password must include a number")
        return v
```

**Password Hashing**:
```python
# backend/src/services/auth_service.py
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

### Key Decisions
- **Regex Patterns**: Use simple character class regex `[A-Z]`, `[a-z]`, `[0-9]` for clarity.
- **Client + Server Validation**: Frontend validates first (better UX), backend enforces (security).
- **bcrypt Salt Rounds**: 12 rounds (industry standard, balances security and performance).

---

## Summary of Key Technical Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Authentication** | Better Auth with JWT (15 min access, 7 day refresh) | Industry-standard token lifetimes balance security and UX |
| **Password Hashing** | bcrypt with 12 salt rounds | Industry standard, resistant to brute-force attacks |
| **ORM** | SQLModel with NO raw SQL | Type-safe, Pydantic validation, prevents SQL injection |
| **Database** | Neon PostgreSQL with connection pooling | Serverless, auto-scaling, connection pooling for performance |
| **Frontend Framework** | Next.js 16 App Router (Server + Client Components) | SSR for performance, Client Components for interactivity |
| **UI Library** | shadcn/ui + Tailwind CSS | Full control, accessible, responsive by default |
| **API Pattern** | RESTful with domain-grouped APIRouters | Clear separation (/auth, /tasks), scalable for future domains |
| **Authorization** | JWT middleware + user_id filtering on all queries | Enforces user isolation at both route and data layer |

---

## References
- Better Auth Documentation: https://better-auth.com
- SQLModel Documentation: https://sqlmodel.tiangolo.com
- Next.js 16 App Router: https://nextjs.org/docs/app
- Neon PostgreSQL: https://neon.tech/docs
- shadcn/ui: https://ui.shadcn.com
- bcrypt Best Practices: OWASP Password Storage Cheat Sheet
