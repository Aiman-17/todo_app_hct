/**
 * Phase III: Chat API client
 *
 * Handles communication with POST /api/chat endpoint
 */

import { ChatRequest, ChatResponse } from '@/types/chat'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export class ChatAPIError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public details?: any
  ) {
    super(message)
    this.name = 'ChatAPIError'
  }
}

/**
 * Get access token from cookies (same as main API)
 */
function getCookie(name: string): string | null {
  if (typeof window === 'undefined') return null
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
  return match ? match[2] : null
}

/**
 * Send chat message to backend
 */
export async function sendChatMessage(
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  // Get token from cookies (same as rest of the app)
  const token = getCookie('access_token')

  if (!token) {
    throw new ChatAPIError('Not authenticated', 401)
  }

  const requestBody: ChatRequest = {
    message,
    conversation_id: conversationId
  }

  try {
    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(requestBody)
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))

      if (response.status === 401) {
        // Token expired or invalid - redirect to login
        localStorage.removeItem('auth_token')
        window.location.href = '/login'
        throw new ChatAPIError('Session expired', 401)
      }

      if (response.status === 429) {
        // Rate limit exceeded
        throw new ChatAPIError(
          errorData.detail?.message || 'Rate limit exceeded. Please try again later.',
          429,
          errorData.detail
        )
      }

      throw new ChatAPIError(
        errorData.detail || 'Failed to send message',
        response.status,
        errorData
      )
    }

    const data: ChatResponse = await response.json()
    return data

  } catch (error) {
    if (error instanceof ChatAPIError) {
      throw error
    }

    // Network error or other issues
    throw new ChatAPIError(
      'Network error. Please check your connection.',
      0,
      error
    )
  }
}
