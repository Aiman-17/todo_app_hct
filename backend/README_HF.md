---
title: Todo App Backend API
emoji: ✅
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Todo App Backend API

FastAPI backend for the Todo Application with JWT authentication.

## Features

- User authentication (signup/login)
- Task CRUD operations
- User isolation
- PostgreSQL database
- JWT tokens
- Full API documentation at `/docs`

## Environment Variables Required

Set these in your Hugging Face Space settings:

```
DATABASE_URL=your_neon_postgres_url
SECRET_KEY=your_secret_key_min_32_chars
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
CORS_ORIGINS=https://your-frontend-url.vercel.app,http://localhost:3000
```

## API Documentation

Once deployed, visit `https://your-space-url.hf.space/docs` for interactive API documentation.
