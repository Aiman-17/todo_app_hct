import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Extract user-friendly error message from API error response.
 *
 * Handles various error formats from the backend API and returns
 * a toast-ready message for display to users.
 *
 * @param error - Error object from API request
 * @returns User-friendly error message string
 */
export function handleApiError(error: any): string {
  // Handle network errors (fetch failures)
  if (error instanceof TypeError && error.message.includes('fetch')) {
    return "Unable to connect to server. Please check your connection and try again.";
  }

  // Handle API errors with detail field (FastAPI format)
  if (error?.detail) {
    if (typeof error.detail === 'string') {
      return error.detail;
    }
    if (Array.isArray(error.detail) && error.detail.length > 0) {
      // Validation errors from Pydantic
      return error.detail.map((err: any) => err.msg).join(', ');
    }
  }

  // Handle errors with message field
  if (error?.message) {
    return error.message;
  }

  // Handle HTTP status codes
  if (error?.status) {
    switch (error.status) {
      case 400:
        return "Invalid request. Please check your input and try again.";
      case 401:
        return "Session expired. Please log in again.";
      case 403:
        return "You don't have permission to perform this action.";
      case 404:
        return "The requested resource was not found.";
      case 500:
        return "Server error. Please try again later.";
      default:
        return `Request failed with status ${error.status}`;
    }
  }

  // Generic fallback message
  return "An unexpected error occurred. Please try again.";
}
