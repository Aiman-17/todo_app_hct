# Frontend - Next.js Todo Application

Modern, responsive Next.js 15 frontend for the Todo application with JWT authentication and real-time task management.

## Features

- **Next.js 15 App Router**: File-based routing with Server and Client Components
- **Cookie-based Authentication**: Secure JWT token storage compatible with middleware
- **Responsive Design**: Mobile-first design with Tailwind CSS breakpoints
- **Keyboard Navigation**: Full keyboard support (Escape, Enter, Tab) for accessibility
- **shadcn/ui Components**: Beautiful, accessible components built on Radix UI
- **Real-time Validation**: Instant feedback for form inputs and password requirements
- **Loading States**: Visual feedback with spinners during async operations
- **Error Handling**: Centralized error handling with user-friendly toast notifications
- **Type Safety**: Full TypeScript with strict mode enabled
- **Accessibility**: ARIA labels, semantic HTML, and screen reader support

## Prerequisites

- Node.js 18.0 or higher
- npm (Node package manager)
- Backend server running (see `../backend/README.md`)

## Quick Start

### 1. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install packages
npm install
```

### 2. Configure Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

The application will be available at:
- **Frontend**: http://localhost:3000 (or http://localhost:3001 if port 3000 is in use)
- **Backend Required**: Ensure backend is running at http://localhost:8000

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── (auth)/             # Auth route group (public)
│   │   │   ├── login/          # Login page
│   │   │   └── signup/         # Signup page
│   │   ├── dashboard/          # Dashboard page (protected)
│   │   ├── layout.tsx          # Root layout with toast provider
│   │   ├── middleware.ts       # Route protection middleware
│   │   └── page.tsx            # Home page (redirects to dashboard)
│   ├── components/
│   │   ├── auth/               # Authentication components
│   │   │   ├── LoginForm.tsx   # Login form with validation
│   │   │   └── SignupForm.tsx  # Signup with password requirements
│   │   ├── layout/             # Layout components
│   │   │   └── Header.tsx      # Responsive header with logout
│   │   ├── shared/             # Shared components
│   │   │   └── LoadingSpinner.tsx  # Reusable loading indicator
│   │   ├── tasks/              # Task management components
│   │   │   ├── TaskList.tsx    # Responsive task grid
│   │   │   ├── TaskItem.tsx    # Individual task card
│   │   │   ├── TaskForm.tsx    # Create/edit task dialog
│   │   │   └── DeleteTaskModal.tsx # Delete confirmation
│   │   └── ui/                 # shadcn/ui components
│   │       ├── button.tsx      # Button component
│   │       ├── card.tsx        # Card component
│   │       ├── dialog.tsx      # Dialog/modal component
│   │       ├── input.tsx       # Input component
│   │       ├── label.tsx       # Label component
│   │       └── toast.tsx       # Toast notification system
│   ├── lib/
│   │   ├── api.ts              # API client with auth and error handling
│   │   └── utils.ts            # Utility functions (cn, handleApiError)
│   └── types/
│       └── index.ts            # TypeScript type definitions
├── public/                     # Static assets
├── .env.local                  # Environment variables (create this)
├── .env.example                # Environment template
├── next.config.mjs             # Next.js configuration
├── tailwind.config.ts          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
└── package.json                # Dependencies and scripts
```

## Available Scripts

```bash
# Development server with hot reload
npm run dev

# Production build
npm run build

# Start production server (after build)
npm start

# Run ESLint
npm run lint
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | Yes | - |

**Note**: Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. Never put secrets here.

## Component Architecture

### Authentication Components

**LoginForm** (`src/components/auth/LoginForm.tsx`)
- Email and password validation
- JWT token storage in cookies
- Error handling with toast notifications
- Loading states during authentication

**SignupForm** (`src/components/auth/SignupForm.tsx`)
- Real-time password validation with visual checklist
- Password requirements: 8+ chars, uppercase, lowercase, number
- Character counters for inputs
- Duplicate email detection

### Task Components

**TaskList** (`src/components/tasks/TaskList.tsx`)
- Responsive grid layout (1/2/3 columns)
- Real-time task fetching with React hooks
- Empty state with motivational message
- Loading spinner during fetch

**TaskItem** (`src/components/tasks/TaskItem.tsx`)
- Touch-friendly checkboxes (44px × 44px)
- Inline editing with save/cancel
- Delete with confirmation modal
- Hover states and transitions

**TaskForm** (`src/components/tasks/TaskForm.tsx`)
- Dialog-based creation
- Auto-focus on open
- Keyboard navigation (Escape to close, Enter to submit)
- Character limits (title: 200, description: 2000)

### Layout Components

**Header** (`src/components/layout/Header.tsx`)
- Responsive layout (stacks on mobile)
- User name display (hidden on mobile)
- Logout button with confirmation

## Authentication Flow

1. **Login/Signup**: User submits credentials → Backend validates → Returns JWT tokens
2. **Token Storage**: `saveTokens()` stores tokens in cookies with proper expiry:
   - Access token: 15 minutes
   - Refresh token: 7 days
3. **Middleware Protection**: `middleware.ts` checks for `access_token` cookie on protected routes
4. **API Requests**: `apiRequest()` automatically injects `Authorization: Bearer <token>` header
5. **Token Expiration**: On 401 response, `clearTokens()` removes cookies and redirects to `/login`
6. **Logout**: `clearTokens()` removes cookies → Middleware redirects to `/login`

## API Client

The `src/lib/api.ts` module provides:

```typescript
// Make authenticated request
const tasks = await apiRequest<Task[]>('/api/tasks');

// POST with body
const newTask = await apiRequest<Task>('/api/tasks', {
  method: 'POST',
  body: JSON.stringify({ title: 'Buy groceries', description: 'Milk, eggs, bread' })
});

// Save tokens (called after login/signup)
saveTokens(accessToken, refreshToken);

// Check authentication status
const isLoggedIn = isAuthenticated();

// Logout
clearTokens();
```

**Features**:
- Automatic token injection from cookies
- JWT expiration detection and auto-redirect
- Network error handling with user-friendly messages
- JSON parsing with content-type detection
- TypeScript generics for type-safe responses

## Error Handling

Centralized error handling with `handleApiError()` utility:

```typescript
try {
  await apiRequest('/api/tasks', { method: 'POST', body: JSON.stringify(taskData) });
  toast({ title: "Success", description: "Task created!" });
} catch (error) {
  const message = handleApiError(error);
  toast({ title: "Error", description: message, variant: "destructive" });
}
```

**Error Types Handled**:
- Network errors (fetch failures)
- FastAPI validation errors (Pydantic)
- HTTP status codes (400, 401, 403, 404, 500)
- Generic fallback messages

## Responsive Design

**Breakpoints** (Tailwind defaults):
- Mobile: < 640px
- Tablet: 640px - 1023px (sm: and md:)
- Desktop: 1024px+ (lg:)

**Touch Targets**: All interactive elements have minimum 44px × 44px for mobile usability.

**Layout Patterns**:
```typescript
// Stack on mobile, row on desktop
className="flex flex-col sm:flex-row"

// 1 column on mobile, 2 on tablet, 3 on desktop
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3"

// Hide on mobile, show on desktop
className="hidden sm:inline"
```

## Accessibility

- **Semantic HTML**: Proper use of `<main>`, `<section>`, `<nav>`, `<header>`
- **ARIA Labels**: All interactive elements have descriptive labels
- **Keyboard Navigation**: Full keyboard support (Tab, Escape, Enter)
- **Screen Reader Support**: Status announcements with `aria-live`
- **Focus Management**: Auto-focus on dialog open, focus trap in modals
- **Heading Hierarchy**: Proper h1 → h2 → h3 structure

## Building for Production

```bash
# Create optimized production build
npm run build

# Start production server
npm start
```

The build process:
1. Type-checks with TypeScript
2. Lints with ESLint
3. Optimizes images and fonts
4. Generates static pages where possible
5. Creates serverless functions for dynamic routes

**Output**: `.next/` directory with optimized bundles.

## Deployment

### Vercel (Recommended)

1. Push code to GitHub/GitLab/Bitbucket
2. Import project in Vercel dashboard
3. Set environment variable: `NEXT_PUBLIC_API_URL=https://your-api.com`
4. Deploy

### Other Platforms

For Docker, AWS, or self-hosted deployment:

1. Build the application: `npm run build`
2. Set `NEXT_PUBLIC_API_URL` environment variable
3. Start server: `npm start` (runs on port 3000)
4. Ensure backend API is accessible from frontend
5. Configure reverse proxy (nginx/Apache) if needed

**CORS Configuration**: Ensure backend `CORS_ORIGINS` includes your frontend URL.

See `../specs/002-fullstack-web-auth/deployment.md` for detailed deployment instructions.

## Development Workflow

1. **Start Backend**: `cd backend && uvicorn src.main:app --reload`
2. **Start Frontend**: `cd frontend && npm run dev`
3. **Make Changes**: Edit files in `src/`
4. **Hot Reload**: Changes appear automatically
5. **Test**: Manual testing at http://localhost:3000
6. **Build**: `npm run build` to verify production build
7. **Commit**: Git commit with descriptive message

## Troubleshooting

### Port Already in Use

**Error**: `Port 3000 is already in use`

**Solution**: Next.js will automatically use port 3001. Or kill the process:
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9
```

### Cannot Connect to Backend

**Error**: "Unable to connect to server"

**Solution**:
- Verify backend is running: http://localhost:8000/api/health
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Ensure CORS is configured in backend `.env`: `CORS_ORIGINS=http://localhost:3000`

### Authentication Not Working

**Error**: Redirected to login after successful login

**Solution**:
- Clear cookies: DevTools → Application → Cookies → Delete all
- Verify backend `BETTER_AUTH_SECRET` is set
- Check browser console for errors
- Ensure tokens are saved to cookies (not localStorage)

### Build Errors

**Error**: Type errors or webpack issues

**Solution**:
```bash
# Clean build cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

### Missing UI Components

**Error**: `Cannot find module '@/components/ui/...'`

**Solution**: Missing shadcn/ui component. Either:
- Install via CLI: `npx shadcn@latest add <component>`
- Create manually in `src/components/ui/` (see existing components)

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Radix UI Documentation](https://www.radix-ui.com/)
- [Project Quickstart Guide](../specs/002-fullstack-web-auth/quickstart.md)
- [Backend API Documentation](../backend/README.md)

## License

See root README.md for license information.
