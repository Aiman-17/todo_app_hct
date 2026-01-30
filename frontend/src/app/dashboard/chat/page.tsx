"use client"

/**
 * Phase III: Chat Page
 *
 * Main page for AI chatbot interface
 * Layout: 70% ChatInterface | 30% TaskPanel
 * Mobile: Stacked layout with drawer for tasks
 */

import { useState } from 'react'
import { ChatInterface } from '@/components/chat/ChatInterface'
import { TaskPanel } from '@/components/chat/TaskPanel'
import { Button } from '@/components/ui/button'
import { PanelRightClose, PanelRightOpen } from 'lucide-react'

export default function ChatPage() {
  const [taskRefreshTrigger, setTaskRefreshTrigger] = useState(0)
  const [showTaskPanel, setShowTaskPanel] = useState(true)

  // Called when chat performs a task operation
  const handleTaskUpdate = () => {
    setTaskRefreshTrigger(prev => prev + 1)
  }

  return (
    <div className="h-[calc(100vh-4rem)] flex bg-gradient-to-br from-rose-white to-rose-white/80">
      {/* Main Chat Area (70%) */}
      <div className={`flex-1 transition-all duration-300 ${showTaskPanel ? 'lg:w-[70%]' : 'w-full'}`}>
        <div className="h-full flex flex-col">
          {/* Header with toggle button */}
          <div className="border-b border-seal-brown/10 p-4 flex items-center justify-between bg-white/80 backdrop-blur-sm">
            <div>
              <h1 className="text-xl font-bold text-seal-brown">AI Task Assistant</h1>
              <p className="text-sm text-seal-brown/60">
                Manage your tasks with natural language—I understand typos too!
              </p>
            </div>

            {/* Toggle Task Panel (Desktop) */}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowTaskPanel(!showTaskPanel)}
              className="hidden lg:flex text-seal-brown hover:bg-seal-brown/10"
            >
              {showTaskPanel ? (
                <>
                  <PanelRightClose className="h-4 w-4 mr-2" />
                  Hide Tasks
                </>
              ) : (
                <>
                  <PanelRightOpen className="h-4 w-4 mr-2" />
                  Show Tasks
                </>
              )}
            </Button>
          </div>

          {/* Chat Interface */}
          <div className="flex-1 overflow-hidden">
            <ChatInterface onTaskUpdate={handleTaskUpdate} />
          </div>
        </div>
      </div>

      {/* Task Panel (30%) - Hidden on mobile by default */}
      {showTaskPanel && (
        <div className="hidden lg:block lg:w-[30%] lg:max-w-md border-l">
          <TaskPanel
            refreshTrigger={taskRefreshTrigger}
            onTaskAction={handleTaskUpdate}
          />
        </div>
      )}

      {/* Mobile Task Panel - Bottom Sheet (optional enhancement for later) */}
      {/* TODO: Add mobile drawer for task panel */}
    </div>
  )
}
