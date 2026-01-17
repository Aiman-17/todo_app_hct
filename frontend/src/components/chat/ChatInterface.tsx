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

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages])

  // Welcome message on mount
  useEffect(() => {
    setMessages([{
      id: 'welcome',
      role: 'assistant',
      content: '👋 Hi! I can help you manage your tasks. Try:\n• "Add a task to buy groceries"\n• "Show my tasks"\n• "Mark task 1 as done"',
      timestamp: new Date()
    }])
  }, [])

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
      const response = await sendChatMessage(input, conversationId)

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
          description: 'Failed to send message. Please try again.',
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
    <div className="flex flex-col h-full bg-background">
      {/* Messages */}
      <ScrollArea className="flex-1 p-4" ref={scrollRef}>
        <div className="space-y-4 max-w-3xl mx-auto">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-muted-foreground">
              <Bot className="h-5 w-5" />
              <Loader2 className="h-4 w-4 animate-spin" />
              <span className="text-sm">Thinking...</span>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="border-t p-4">
        <div className="max-w-3xl mx-auto flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message... (e.g., 'show my tasks')"
            className="min-h-[60px] max-h-[200px] resize-none"
            disabled={loading}
          />
          <Button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            size="icon"
            className="h-[60px] w-[60px]"
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
        <div className="text-xs text-muted-foreground bg-muted px-3 py-1 rounded-full">
          {message.content}
        </div>
      </div>
    )
  }

  return (
    <div className={cn(
      "flex gap-3",
      isUser && "justify-end"
    )}>
      {!isUser && (
        <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
          <Bot className="h-5 w-5 text-primary" />
        </div>
      )}

      <div className={cn(
        "rounded-lg px-4 py-2 max-w-[70%]",
        isUser
          ? "bg-primary text-primary-foreground"
          : "bg-muted"
      )}>
        <div className="text-sm whitespace-pre-wrap break-words">
          {message.content}
        </div>
        {message.intent && (
          <div className="text-xs opacity-70 mt-1">
            {message.success ? '✓' : '⚠️'} {message.intent.replace('_', ' ')}
          </div>
        )}
      </div>

      {isUser && (
        <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
          <User className="h-5 w-5 text-primary-foreground" />
        </div>
      )}
    </div>
  )
}
