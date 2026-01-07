/**
 * TypeScript type definitions for authentication-related data structures.
 *
 * Mirrors backend Pydantic schemas (UserCreate, UserLogin, UserResponse, TokenResponse).
 */

/**
 * User profile data (response from backend).
 */
export interface User {
  id: string; // UUID
  email: string;
  name: string;
  created_at: string; // ISO 8601 datetime
}

/**
 * User signup request payload.
 */
export interface SignupRequest {
  email: string;
  name: string;
  password: string;
}

/**
 * User login request payload.
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * JWT token response from login/signup endpoints.
 */
export interface TokenResponse {
  access_token: string; // JWT with 15-min expiry
  refresh_token: string; // JWT with 7-day expiry
  token_type: string; // "bearer"
  expires_in: number; // 900 seconds (15 minutes)
}

/**
 * Combined response for successful signup (user + tokens).
 */
export interface SignupResponse {
  user: User;
  tokens: TokenResponse;
}
