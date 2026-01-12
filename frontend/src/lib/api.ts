/**
 * API client utility for making authenticated requests to the backend.
 *
 * Provides a fetch wrapper with automatic token injection, error handling,
 * and JSON parsing. Uses cookies for token storage to work with Next.js middleware.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Set a cookie with the given name and value.
 */
function setCookie(name: string, value: string, days: number = 7): void {
  if (typeof window === 'undefined') return;
  const expires = new Date(Date.now() + days * 24 * 60 * 60 * 1000).toUTCString();
  document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Strict`;
}

/**
 * Get a cookie value by name.
 */
function getCookie(name: string): string | null {
  if (typeof window === 'undefined') return null;
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
}

/**
 * Delete a cookie by name.
 */
function deleteCookie(name: string): void {
  if (typeof window === 'undefined') return;
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

/**
 * Custom error class for API request failures.
 */
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public response?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

/**
 * Make an authenticated API request with automatic token injection.
 *
 * @param endpoint - API endpoint path (e.g., "/api/tasks")
 * @param options - Fetch options (method, headers, body, etc.)
 * @returns Parsed JSON response
 * @throws APIError if request fails or returns non-2xx status
 *
 * @example
 * ```typescript
 * // GET request
 * const tasks = await apiRequest<Task[]>('/api/tasks');
 *
 * // POST request
 * const newTask = await apiRequest<Task>('/api/tasks', {
 *   method: 'POST',
 *   body: JSON.stringify({ title: 'Buy groceries' })
 * });
 * ```
 */
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  retryCount: number = 0
): Promise<T> {
  try {
    // Get token from cookies (set after login)
    const token = getCookie('access_token');

    // Build headers with automatic token injection
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    // Make request with network error handling
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    // Parse response body (skip for 204 No Content)
    let data: any;
    if (response.status === 204) {
      // 204 No Content - no body to parse
      data = null;
    } else {
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        const text = await response.text();
        // Only set data if there's actual content
        data = text || null;
      }
    }

    // Handle JWT expiration (401) specifically
    if (response.status === 401 && retryCount === 0) {
      const errorMessage = data?.detail || data?.message || '';

      // Check if it's a token expiration error (not login/refresh endpoint)
      if (!endpoint.includes('/login') && !endpoint.includes('/refresh') &&
          (errorMessage.toLowerCase().includes('token') ||
           errorMessage.toLowerCase().includes('expired') ||
           errorMessage.toLowerCase().includes('unauthorized'))) {

        try {
          // Attempt to refresh the access token
          await refreshAccessToken();

          // Retry the original request with new token (only once)
          return apiRequest<T>(endpoint, options, retryCount + 1);
        } catch (refreshError) {
          // Refresh failed, clear tokens and redirect
          clearTokens();
          if (typeof window !== 'undefined') {
            window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
          }
          throw new APIError(
            'Session expired. Please log in again.',
            401,
            data
          );
        }
      }

      // For login/refresh endpoints or non-token errors, throw immediately
      throw new APIError(
        'Session expired. Please log in again.',
        401,
        data
      );
    }

    // Handle other errors
    if (!response.ok) {
      throw new APIError(
        data?.detail || data?.message || `Request failed with status ${response.status}`,
        response.status,
        data
      );
    }

    return data as T;
  } catch (error) {
    // Handle network errors (connection refused, timeout, etc.)
    if (error instanceof TypeError) {
      throw new APIError(
        'Unable to connect to server. Please check your internet connection and try again.',
        0,
        null
      );
    }

    // Handle JSON parsing errors (shouldn't happen after 204 fix, but just in case)
    if (error instanceof SyntaxError) {
      throw new APIError(
        'Something went wrong. Please try again.',
        0,
        null
      );
    }

    // Re-throw API errors as-is (they already have user-friendly messages)
    throw error;
  }
}

/**
 * Save authentication tokens to cookies.
 *
 * @param accessToken - JWT access token (1-hour expiry)
 * @param refreshToken - JWT refresh token (30-day expiry)
 */
export function saveTokens(accessToken: string, refreshToken: string): void {
  // Access token expires in 1 hour
  setCookie('access_token', accessToken, 1 / 24); // 1 hour in days
  // Refresh token expires in 30 days
  setCookie('refresh_token', refreshToken, 30);
}

/**
 * Clear authentication tokens from cookies (logout).
 */
export function clearTokens(): void {
  deleteCookie('access_token');
  deleteCookie('refresh_token');
}

/**
 * Check if user is authenticated (has valid access token).
 *
 * @returns true if access token exists in cookies
 */
export function isAuthenticated(): boolean {
  return !!getCookie('access_token');
}

/**
 * Get the refresh token from cookies.
 *
 * @returns Refresh token string or null if not found
 */
function getRefreshToken(): string | null {
  return getCookie('refresh_token');
}

/**
 * Refresh the access token using the refresh token.
 *
 * Makes a request to /api/auth/refresh and updates cookies with new tokens.
 * If refresh fails, clears tokens and redirects to login.
 *
 * @returns Promise that resolves when tokens are refreshed
 * @throws Error if refresh token is missing or refresh fails
 */
async function refreshAccessToken(): Promise<void> {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    // No refresh token available, redirect to login
    clearTokens();
    if (typeof window !== 'undefined') {
      window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
    }
    throw new Error('No refresh token available');
  }

  try {
    // Make refresh request WITHOUT Authorization header (uses refresh token in body)
    const response = await fetch(`${API_URL}/api/auth/refresh`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) {
      throw new Error('Token refresh failed');
    }

    const data = await response.json();

    // Save new tokens
    saveTokens(data.access_token, data.refresh_token);
  } catch (error) {
    // Refresh failed, clear tokens and redirect to login
    clearTokens();
    if (typeof window !== 'undefined') {
      window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
    }
    throw error;
  }
}
