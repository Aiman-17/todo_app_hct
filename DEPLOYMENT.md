# Deployment Guide - AI TaskMaster

Complete guide for deploying AI TaskMaster to production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Vercel Deployment (Recommended)](#vercel-deployment-recommended)
- [Railway Deployment](#railway-deployment)
- [Render Deployment](#render-deployment)
- [Docker Deployment](#docker-deployment)
- [Self-Hosted Deployment](#self-hosted-deployment)
- [Post-Deployment Checklist](#post-deployment-checklist)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- ✅ GitHub account with repository access
- ✅ Neon PostgreSQL database (or other PostgreSQL provider)
- ✅ Production-ready environment variables
- ✅ SSL/TLS certificates (provided by hosting platform)
- ✅ Domain name (optional but recommended)

**Important Notes**:
- ⚠️ This app requires **Server-Side Rendering (SSR)** - static export will NOT work
- ⚠️ Both backend and frontend must be deployed separately
- ⚠️ CORS must be configured correctly for frontend-backend communication
- ⚠️ HTTPS is required for secure cookie-based authentication

---

## Environment Variables

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require

# Authentication Secret (min 32 characters)
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
BETTER_AUTH_SECRET=your-secret-key-here-min-32-chars

# CORS Origins (comma-separated, no spaces)
CORS_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com

# Optional: Environment indicator
ENVIRONMENT=production

# Optional: Log level
LOG_LEVEL=INFO
```

**Security Notes**:
- Never commit `.env` files to version control
- Use different secrets for development and production
- Keep `BETTER_AUTH_SECRET` highly secure (32+ characters, random)
- Only include trusted domains in `CORS_ORIGINS`

### Frontend Environment Variables

Create a `.env.local` file in the `frontend` directory:

```bash
# Backend API URL (no trailing slash)
NEXT_PUBLIC_API_URL=https://your-backend-domain.com

# Authentication Secret (must match backend)
BETTER_AUTH_SECRET=same-secret-as-backend

# Better Auth Base URL
BETTER_AUTH_URL=https://your-frontend-domain.com

# Optional: Environment indicator
NEXT_PUBLIC_ENV=production
```

---

## Vercel Deployment (Recommended)

Vercel provides the best experience for Next.js applications with automatic SSR support.

### Step 1: Prepare Your Repository

```bash
# Commit all changes
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

### Step 2: Deploy Backend (FastAPI)

1. **Create New Project on Vercel**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Select `backend` as the root directory

2. **Configure Backend Build Settings**:
   ```
   Framework Preset: Other
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Output Directory: (leave empty)
   Install Command: pip install -r requirements.txt
   ```

3. **Add Environment Variables**:
   - Go to Project Settings → Environment Variables
   - Add all backend environment variables:
     - `DATABASE_URL`
     - `BETTER_AUTH_SECRET`
     - `CORS_ORIGINS` (add frontend domain after frontend deployment)

4. **Configure API Route**:
   - Create `vercel.json` in `backend` directory:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "src/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "src/main.py"
       }
     ]
   }
   ```

5. **Deploy**:
   - Click "Deploy"
   - Note the deployment URL (e.g., `https://your-backend.vercel.app`)

### Step 3: Deploy Frontend (Next.js)

1. **Create New Project on Vercel**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Select `frontend` as the root directory

2. **Configure Frontend Build Settings**:
   ```
   Framework Preset: Next.js (auto-detected)
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   Node.js Version: 18.x or higher
   ```

3. **Add Environment Variables**:
   - Go to Project Settings → Environment Variables
   - Add all frontend environment variables:
     - `NEXT_PUBLIC_API_URL` → Backend URL from Step 2
     - `BETTER_AUTH_SECRET` → Same as backend
     - `BETTER_AUTH_URL` → Frontend URL (update after first deploy)

4. **Deploy**:
   - Click "Deploy"
   - Note the deployment URL (e.g., `https://your-app.vercel.app`)

### Step 4: Update CORS Configuration

1. Go to backend project settings on Vercel
2. Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,https://your-app.vercel.app
   ```
3. Redeploy backend

### Step 5: Verify Deployment

1. Visit your frontend URL
2. Test signup/login functionality
3. Create a task and verify backend communication
4. Check browser console for any CORS errors

---

## Railway Deployment

Railway provides excellent support for both Python and Node.js applications.

### Backend Deployment

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Create New Project**:
   ```bash
   cd backend
   railway init
   ```

3. **Add Environment Variables**:
   ```bash
   railway variables set DATABASE_URL="postgresql://..."
   railway variables set BETTER_AUTH_SECRET="your-secret"
   railway variables set CORS_ORIGINS="https://your-frontend.up.railway.app"
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

5. **Get Deployment URL**:
   ```bash
   railway status
   ```

### Frontend Deployment

1. **Create New Project**:
   ```bash
   cd frontend
   railway init
   ```

2. **Add Environment Variables**:
   ```bash
   railway variables set NEXT_PUBLIC_API_URL="https://your-backend.up.railway.app"
   railway variables set BETTER_AUTH_SECRET="same-as-backend"
   railway variables set BETTER_AUTH_URL="https://your-frontend.up.railway.app"
   ```

3. **Deploy**:
   ```bash
   railway up
   ```

---

## Render Deployment

Render supports both web services (backend) and static sites with SSR (frontend).

### Backend Deployment

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure:
   - **Name**: `aitaskmaster-backend`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in dashboard
6. Deploy

### Frontend Deployment

1. Click "New +" → "Web Service"
2. Connect GitHub repository
3. Configure:
   - **Name**: `aitaskmaster-frontend`
   - **Root Directory**: `frontend`
   - **Environment**: Node
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
4. Add environment variables
5. Deploy

---

## Docker Deployment

For self-hosted or containerized deployments.

### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy application code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:18-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production

# Copy built application
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Expose port
EXPOSE 3000

# Run application
CMD ["npm", "start"]
```

### Docker Compose

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - CORS_ORIGINS=http://localhost:3000
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - BETTER_AUTH_URL=http://localhost:3000
    depends_on:
      - backend

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=todouser
      - POSTGRES_PASSWORD=todopass
      - POSTGRES_DB=tododb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Deploy with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Self-Hosted Deployment

For deploying on your own server (VPS, dedicated server, etc.).

### Prerequisites

- Ubuntu 22.04+ or similar Linux distribution
- Nginx installed
- Domain name with DNS configured
- SSL certificate (Let's Encrypt recommended)

### Backend Setup

1. **Install Python and dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3.13 python3-pip python3-venv nginx
   ```

2. **Clone repository and setup**:
   ```bash
   cd /opt
   sudo git clone <your-repo-url>
   cd todo_app_hct/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create systemd service** (`/etc/systemd/system/aitaskmaster-backend.service`):
   ```ini
   [Unit]
   Description=AI TaskMaster Backend
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/todo_app_hct/backend
   Environment="PATH=/opt/todo_app_hct/backend/venv/bin"
   ExecStart=/opt/todo_app_hct/backend/venv/bin/uvicorn src.main:app --host 127.0.0.1 --port 8000 --workers 4
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

4. **Start backend service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable aitaskmaster-backend
   sudo systemctl start aitaskmaster-backend
   ```

### Frontend Setup

1. **Install Node.js**:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt install nodejs
   ```

2. **Build frontend**:
   ```bash
   cd /opt/todo_app_hct/frontend
   npm install
   npm run build
   ```

3. **Create systemd service** (`/etc/systemd/system/aitaskmaster-frontend.service`):
   ```ini
   [Unit]
   Description=AI TaskMaster Frontend
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/todo_app_hct/frontend
   ExecStart=/usr/bin/npm start
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

4. **Start frontend service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable aitaskmaster-frontend
   sudo systemctl start aitaskmaster-frontend
   ```

### Nginx Configuration

Create `/etc/nginx/sites-available/aitaskmaster`:

```nginx
# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site and reload Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/aitaskmaster /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL Configuration with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d api.yourdomain.com
```

---

## Post-Deployment Checklist

After deployment, verify:

- [ ] Frontend loads without errors
- [ ] Backend API is accessible (visit `/docs` endpoint)
- [ ] User signup works correctly
- [ ] User login works correctly
- [ ] Tasks can be created, updated, deleted
- [ ] Filters and search work correctly
- [ ] Authentication persists across page reloads
- [ ] CORS errors are resolved
- [ ] HTTPS is working (secure cookies)
- [ ] Database connections are stable
- [ ] Logs show no critical errors
- [ ] Environment variables are set correctly
- [ ] Health check endpoint responds (`/health` if implemented)

### Testing Checklist

Run through the [MANUAL_TESTING.md](MANUAL_TESTING.md) guide to ensure all features work correctly in production.

---

## Troubleshooting

### CORS Errors

**Symptom**: `Access to fetch at 'https://api.domain.com' blocked by CORS policy`

**Solution**:
1. Check `CORS_ORIGINS` in backend environment variables
2. Ensure frontend domain is included (with correct protocol: https://)
3. Redeploy backend after updating CORS_ORIGINS
4. Clear browser cache and test again

### Authentication Failures

**Symptom**: Login works but redirects to login again

**Solution**:
1. Ensure `BETTER_AUTH_SECRET` matches on both frontend and backend
2. Verify HTTPS is enabled (required for secure cookies)
3. Check `BETTER_AUTH_URL` matches your frontend domain
4. Ensure cookies are not blocked by browser settings

### Database Connection Issues

**Symptom**: `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution**:
1. Verify `DATABASE_URL` is correct
2. Check database is accessible from deployment server
3. Ensure SSL mode is set: `?sslmode=require` for Neon
4. Verify database user has proper permissions
5. Check firewall rules allow connections

### Build Failures

**Symptom**: Deployment fails during build step

**Solution**:
1. Check build logs for specific error messages
2. Verify all dependencies are in `requirements.txt`/`package.json`
3. Ensure Node.js version is 18+ for frontend
4. Ensure Python version is 3.13+ for backend
5. Check for syntax errors or import issues

### 404 Errors on API Routes

**Symptom**: `404 Not Found` when accessing API endpoints

**Solution**:
1. Verify `NEXT_PUBLIC_API_URL` points to correct backend domain
2. Check backend is running and accessible
3. Ensure API endpoints are correctly configured
4. Check Nginx/proxy configuration if self-hosting

### Performance Issues

**Symptom**: Slow page loads or API responses

**Solution**:
1. Enable database connection pooling
2. Add Redis caching for frequent queries
3. Optimize database indexes
4. Enable CDN for static assets
5. Use production builds (not development mode)
6. Monitor server resources (CPU, memory, disk)

---

## Support

For deployment assistance:
- Open an issue on GitHub: [Issues](https://github.com/your-repo/issues)
- Check [Manual Testing Guide](MANUAL_TESTING.md)
- Review [README.md](README.md) for project overview

---

**Last Updated**: January 6, 2026
**Version**: 2.1.0
