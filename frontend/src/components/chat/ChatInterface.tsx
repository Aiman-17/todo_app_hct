"use client"

/**
 * Phase III: ChatInterface Component
 *
 * Main chat interface using custom implementation
 * - Sends to POST /api/chat (our backend)
 * - Renders chat messages
 * - Notifies parent on task operations
 */

import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Send, Bot, User, Loader2 } from 'lucide-react'
import { cn } from '@/lib/utils'
import { sendChatMessage, ChatAPIError } from '@/lib/api/chat'
import { useToast } from '@/components/ui/use-toast'
import type { ChatMessage } from '@/types/chat'

interface ChatInterfaceProps {
  onTaskUpdate: () => void // Callback when task is created/updated/deleted
}

export function ChatInterface({ onTaskUpdate }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string | undefined>()
  const scrollRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  // Load conversation from localStorage on mount (MEMORY FIX)
  useEffect(() => {
    const savedConversationId = localStorage.getItem('chat_conversation_id')
    const savedMessages = localStorage.getItem('chat_messages')

    if (savedConversationId) {
      setConversationId(savedConversationId)
    }

    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages)
        setMessages(parsed)
      } catch (e) {
        console.error('Failed to parse saved messages:', e)
        // Show welcome message if parsing fails
        setMessages([{
          id: 'welcome',
          role: 'assistant',
          content: '👋 Hi! I\'m your friendly AI task assistant. I understand natural language!\n\nTry saying:\n• "Add task buy groceries tomorrow"\n• "Show my urgent tasks"\n• "Mark id [number]" to complete a task\n• "View tasks" to see your list',
          timestamp: new Date()
        }])
      }
    } else {
      // Show welcome message on first visit
      setMessages([{
        id: 'welcome',
        role: 'assistant',
        content: '👋 Hi! I\'m your friendly AI task assistant. I understand natural language!\n\nTry saying:\n• "Add task buy groceries tomorrow"\n• "Show my urgent tasks"\n• "Mark id [number]" to complete a task\n• "View tasks" to see your list',
        timestamp: new Date()
      }])
    }
  }, [])

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  // Save conversation to localStorage whenever it changes (MEMORY FIX)
  useEffect(() => {
    if (conversationId) {
      localStorage.setItem('chat_conversation_id', conversationId)
    }
  }, [conversationId])

  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('chat_messages', JSON.stringify(messages))
    }
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    // Add user message immediately
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      // Send to backend
      console.log('🚀 Sending message to backend:', input)
      console.log('📍 API URL:', process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')

      // Check for auth token in cookies (where it's actually stored)
      const getCookie = (name: string) => {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
        return match ? match[2] : null
      }
      const token = getCookie('access_token')
      console.log('🔑 Auth token exists:', !!token, token ? `(${token.substring(0, 20)}...)` : '')

      const response = await sendChatMessage(input, conversationId)

      console.log('✅ Response received:', response)

      // Update conversation ID
      if (response.conversation_id) {
        setConversationId(response.conversation_id)
      }

      // Add assistant response
      const assistantMessage: ChatMessage = {
        id: Date.now().toString() + '-assistant',
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
        intent: response.intent,
        success: response.success
      }

      setMessages(prev => [...prev, assistantMessage])

      // If task operation was successful, notify parent to refresh task list
      if (response.success && ['create_task', 'update_task', 'delete_task', 'complete_task'].includes(response.intent)) {
        onTaskUpdate()
      }

    } catch (error) {
      console.error('❌ Chat error:', error)
      console.error('❌ Error details:', {
        type: error?.constructor?.name,
        message: error instanceof Error ? error.message : String(error),
        statusCode: error instanceof ChatAPIError ? error.statusCode : 'N/A',
        stack: error instanceof Error ? error.stack : undefined
      })

      if (error instanceof ChatAPIError) {
        if (error.statusCode === 429) {
          // Rate limit
          toast({
            title: 'Rate Limit Exceeded',
            description: error.message,
            variant: 'destructive'
          })
        } else if (error.statusCode === 401) {
          // Already handled by redirect in API
          console.log('🔒 Auth error - should redirect to login')
        } else {
          toast({
            title: 'Error',
            description: error.message,
            variant: 'destructive'
          })
        }
      } else {
        toast({
          title: 'Error',
          description: 'Failed to send message. Please try again in a moment.',
          variant: 'destructive'
        })
      }

      // Add error message to chat
      setMessages(prev => [...prev, {
        id: Date.now().toString() + '-error',
        role: 'system',
        content: '❌ Failed to send message. Please try again.',
        timestamp: new Date()
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-rose-white to-rose-white/50">
      {/* Messages */}
      <ScrollArea className="flex-1 p-4" ref={scrollRef}>
        <div className="space-y-4 max-w-3xl mx-auto">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-seal-brown/60">
              <Bot className="h-5 w-5 text-seal-brown" />
              <Loader2 className="h-4 w-4 animate-spin text-seal-brown" />
              <span className="text-sm">Thinking...</span>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="border-t border-seal-brown/10 p-4 bg-white/50 backdrop-blur-sm">
        <div className="max-w-3xl mx-auto flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message... (e.g., 'show my tasks')"
            className="min-h-[60px] max-h-[200px] resize-none bg-white border-seal-brown/20 focus:border-seal-brown/40 text-seal-brown placeholder:text-seal-brown/40"
            disabled={loading}
          />
          <Button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            size="icon"
            className="h-[60px] w-[60px] bg-seal-brown hover:bg-seal-brown/90 text-rose-white shadow-lg"
          >
            <Send className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </div>
  )
}

function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === 'user'
  const isSystem = message.role === 'system'

  if (isSystem) {
    return (
      <div className="flex justify-center">
        <div className="text-xs text-seal-brown/60 bg-seal-brown/5 px-3 py-1 rounded-full border border-seal-brown/10">
          {message.content}
        </div>
      </div>
    )
  }

  return (
    <div className={cn(
      "flex gap-3 items-start",
      isUser && "justify-end"
    )}>
      {!isUser && (
        <div className="h-8 w-8 rounded-full bg-seal-brown/10 flex items-center justify-center flex-shrink-0 shadow-sm">
          <Bot className="h-5 w-5 text-seal-brown" />
        </div>
      )}

      <div className={cn(
        "rounded-2xl px-4 py-3 max-w-[70%] shadow-md",
        isUser
          ? "bg-seal-brown text-rose-white"
          : "bg-white text-seal-brown border border-seal-brown/10"
      )}>
        <div className="text-sm whitespace-pre-wrap break-words leading-relaxed">
          {message.content}
        </div>
        {message.intent && (
          <div className={cn(
            "text-xs mt-2 pt-2 border-t",
            isUser ? "border-rose-white/20" : "border-seal-brown/10"
          )}>
            <span className={isUser ? "text-rose-white/80" : "text-seal-brown/60"}>
              {message.success ? '✓' : '⚠️'} {message.intent.replace('_', ' ')}
            </span>
          </div>
        )}
      </div>

      {isUser && (
        <div className="h-8 w-8 rounded-full bg-seal-brown flex items-center justify-center flex-shrink-0 shadow-md">
          <User className="h-5 w-5 text-rose-white" />
        </div>
      )}
    </div>
  )
}
