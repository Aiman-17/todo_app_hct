"use client"

/**
 * Phase III: TaskPanel Component
 *
 * Displays live task list in right sidebar (30% width)
 * - Shows all user tasks
 * - Quick actions (complete, delete)
 * - Syncs with chat operations
 */

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Checkbox } from '@/components/ui/checkbox'
import { Trash2, Loader2 } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { Task } from '@/types/task'

interface TaskPanelProps {
  refreshTrigger: number // Increment to trigger refresh
  onTaskAction?: () => void // Callback after task action
}

export function TaskPanel({ refreshTrigger, onTaskAction }: TaskPanelProps) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Fetch tasks
  const fetchTasks = async () => {
    try {
      setLoading(true)
      setError(null)

      const token = localStorage.getItem('auth_token')
      if (!token) {
        throw new Error('Not authenticated')
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/tasks`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      )

      if (!response.ok) {
        throw new Error('Failed to fetch tasks')
      }

      const data = await response.json()
      setTasks(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  // Fetch on mount and when refreshTrigger changes
  useEffect(() => {
    fetchTasks()
  }, [refreshTrigger])

  // Toggle task completion
  const handleToggle = async (taskId: number) => {
    try {
      const token = localStorage.getItem('auth_token')
      if (!token) return

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/tasks/${taskId}/toggle`,
        {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      )

      if (!response.ok) {
        throw new Error('Failed to toggle task')
      }

      // Update local state
      setTasks(prev =>
        prev.map(task =>
          task.id === taskId ? { ...task, completed: !task.completed } : task
        )
      )

      onTaskAction?.()
    } catch (err) {
      console.error('Failed to toggle task:', err)
    }
  }

  // Delete task
  const handleDelete = async (taskId: number) => {
    if (!confirm('Delete this task?')) return

    try {
      const token = localStorage.getItem('auth_token')
      if (!token) return

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/tasks/${taskId}`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      )

      if (!response.ok) {
        throw new Error('Failed to delete task')
      }

      // Remove from local state
      setTasks(prev => prev.filter(task => task.id !== taskId))

      onTaskAction?.()
    } catch (err) {
      console.error('Failed to delete task:', err)
    }
  }

  const pendingTasks = tasks.filter(t => !t.completed)
  const completedTasks = tasks.filter(t => t.completed)

  return (
    <Card className="h-full flex flex-col border-l rounded-none">
      <CardHeader className="border-b">
        <CardTitle className="text-lg">Your Tasks ({tasks.length})</CardTitle>
      </CardHeader>

      <CardContent className="flex-1 p-0">
        <ScrollArea className="h-full">
          {loading && (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          )}

          {error && (
            <div className="p-4 text-sm text-destructive">
              {error}
            </div>
          )}

          {!loading && !error && tasks.length === 0 && (
            <div className="p-4 text-sm text-muted-foreground text-center">
              No tasks yet. Create one via chat!
            </div>
          )}

          {!loading && !error && (
            <div className="p-4 space-y-6">
              {/* Pending Tasks */}
              {pendingTasks.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-3">
                    Pending ({pendingTasks.length})
                  </h3>
                  <div className="space-y-2">
                    {pendingTasks.map(task => (
                      <TaskItem
                        key={task.id}
                        task={task}
                        onToggle={handleToggle}
                        onDelete={handleDelete}
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* Completed Tasks */}
              {completedTasks.length > 0 && (
                <div>
                  <h3 className="text-sm font-medium text-muted-foreground mb-3">
                    Completed ({completedTasks.length})
                  </h3>
                  <div className="space-y-2">
                    {completedTasks.map(task => (
                      <TaskItem
                        key={task.id}
                        task={task}
                        onToggle={handleToggle}
                        onDelete={handleDelete}
                      />
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </ScrollArea>
      </CardContent>
    </Card>
  )
}

interface TaskItemProps {
  task: Task
  onToggle: (id: number) => void
  onDelete: (id: number) => void
}

function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <div className="flex items-start gap-2 p-2 rounded-lg hover:bg-muted/50 transition-colors group">
      <Checkbox
        checked={task.completed}
        onCheckedChange={() => onToggle(task.id)}
        className="mt-0.5"
      />

      <div className="flex-1 min-w-0">
        <p className={cn(
          "text-sm font-medium",
          task.completed && "line-through text-muted-foreground"
        )}>
          {task.title}
        </p>
        {task.description && (
          <p className="text-xs text-muted-foreground mt-0.5 line-clamp-2">
            {task.description}
          </p>
        )}
      </div>

      <Button
        variant="ghost"
        size="icon"
        className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
        onClick={() => onDelete(task.id)}
      >
        <Trash2 className="h-3.5 w-3.5" />
      </Button>
    </div>
  )
}
