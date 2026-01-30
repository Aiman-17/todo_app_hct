/**
 * Phase III: Chat API client
 *
 * Handles communication with POST /api/chat endpoint
 */

import { ChatRequest, ChatResponse } from '@/types/chat'
import { apiRequest, APIError } from '@/lib/api'

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
 * Send chat message to backend
 */
export async function sendChatMessage(
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  const requestBody: ChatRequest = {
    message,
    conversation_id: conversationId
  }

  try {
    const data = await apiRequest<ChatResponse>('/api/chat', {
      method: 'POST',
      body: JSON.stringify(requestBody)
    })

    return data

  } catch (error) {
    // Convert APIError to ChatAPIError for backward compatibility
    if (error instanceof APIError) {
      // Handle rate limiting (429)
      if (error.status === 429) {
        throw new ChatAPIError(
          error.response?.detail?.message || 'Rate limit exceeded. Please try again later.',
          429,
          error.response?.detail
        )
      }

      // Convert other API errors
      throw new ChatAPIError(
        error.message,
        error.status,
        error.response
      )
    }

    // Network error or other issues
    throw new ChatAPIError(
      'Network error. Please check your connection.',
      0,
      error
    )
  }
}
