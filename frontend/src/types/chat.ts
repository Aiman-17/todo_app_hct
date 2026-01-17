/**
 * Phase III: Chat-related TypeScript types
 */

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
  intent?: string
  success?: boolean
}

export interface ChatRequest {
  message: string
  conversation_id?: string
}

export interface ChatResponse {
  response: string
  conversation_id: string
  intent: string
  success: boolean
  correlation_id: string
}

export interface TaskActionMetadata {
  type: 'create' | 'update' | 'delete' | 'complete' | 'list'
  task_id?: number
  task_ids?: number[]
}
