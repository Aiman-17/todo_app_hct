/**
 * Next.js middleware for route protection and authentication.
 *
 * Protects /dashboard route by checking for access_token in cookies.
 * Redirects unauthenticated users to /login.
 */
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * Middleware function that runs on every request matching the config.matcher.
 *
 * @param request - Next.js request object
 * @returns NextResponse (redirect or continue)
 */
export function middleware(request: NextRequest) {
  // Check for access token in cookies (will be set after login)
  const token = request.cookies.get('access_token')?.value;

  // Get the pathname from the request
  const { pathname } = request.nextUrl;

  // If trying to access protected route without token, redirect to login
  if (pathname.startsWith('/dashboard')) {
    if (!token) {
      const loginUrl = new URL('/login', request.url);
      loginUrl.searchParams.set('redirect', pathname); // Preserve redirect URL
      return NextResponse.redirect(loginUrl);
    }
  }

  // If authenticated user tries to access login/signup, redirect to dashboard
  if ((pathname === '/login' || pathname === '/signup') && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Allow request to proceed
  return NextResponse.next();
}

/**
 * Matcher configuration for middleware.
 *
 * Only runs middleware on specified routes (dashboard, login, signup).
 * Excludes API routes, static files, and Next.js internals.
 */
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api routes (/api/*)
     * - static files (/_next/static/*)
     * - image optimization (/_next/image/*)
     * - favicon.ico
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
