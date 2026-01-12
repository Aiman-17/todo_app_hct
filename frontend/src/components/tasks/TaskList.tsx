/**
 * Task list client component.
 *
 * Fetches and displays all tasks for the authenticated user.
 * Listens for task creation/update events to refresh the list.
 * Implements loading states with spinner and skeleton loaders.
 * Supports filtering by all/pending/completed status.
 */
"use client";

import { useEffect, useState, useCallback } from "react";
import { ColorfulTaskCard } from "./ColorfulTaskCard";
import { TaskForm } from "./TaskForm";
import { SkeletonTaskList } from "@/components/shared/SkeletonTaskCard";
import { useToast } from "@/components/ui/use-toast";
import { apiRequest } from "@/lib/api";
import { useFilters } from "@/contexts/FilterContext";
import { useScreenReaderAnnouncement, ScreenReaderAnnouncer } from "@/hooks/useScreenReaderAnnouncement";
import type { Task } from "@/types/task";

export function TaskList() {
  const { toast } = useToast();
  const { filters } = useFilters();
  const { announce, message } = useScreenReaderAnnouncement();

  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  /**
   * Fetch tasks with current filters from the API.
   *
   * Builds query parameters from FilterContext and fetches filtered tasks.
   * Memoized with useCallback to prevent infinite re-render loops.
   */
  const fetchTasks = useCallback(async () => {
    try {
      // Build query parameters from filters
      const params = new URLSearchParams();

      // Priority filter (comma-separated if multiple)
      if (filters.priority && filters.priority.length > 0) {
        // Backend expects single priority value, so we'll fetch each priority separately
        // For now, just use the first priority (can be enhanced later)
        params.append("priority", filters.priority[0]);
      }

      // Status filter (convert to completed boolean)
      if (filters.status === "pending") {
        params.append("completed", "false");
      } else if (filters.status === "completed") {
        params.append("completed", "true");
      }
      // "all" doesn't add any filter

      // Sort parameters
      params.append("sort_by", filters.sortBy);
      params.append("order", filters.order);

      const queryString = params.toString();
      const url = queryString ? `/api/tasks?${queryString}` : "/api/tasks";

      const data = await apiRequest<Task[]>(url);

      // Apply client-side search filter if search query exists
      const filteredData = filters.search
        ? data.filter(
            (task) =>
              task.title.toLowerCase().includes(filters.search.toLowerCase()) ||
              task.description.toLowerCase().includes(filters.search.toLowerCase())
          )
        : data;

      setTasks(filteredData);
    } catch (error: any) {
      toast({
        title: "Failed to load tasks",
        description: error.message || "An error occurred",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  }, [filters.priority, filters.status, filters.sortBy, filters.order, filters.search, toast]);

  // Refetch when filters change
  useEffect(() => {
    setIsLoading(true);
    fetchTasks();
  }, [fetchTasks]);

  // Listen for task creation/update events
  useEffect(() => {
    const handleTaskCreated = () => {
      setIsLoading(true);
      fetchTasks();
    };

    window.addEventListener("taskCreated", handleTaskCreated);
    window.addEventListener("taskUpdated", handleTaskCreated);

    return () => {
      window.removeEventListener("taskCreated", handleTaskCreated);
      window.removeEventListener("taskUpdated", handleTaskCreated);
    };
  }, [fetchTasks]);

  /**
   * Handle task deletion by removing it from local state.
   *
   * @param taskId - ID of the task that was deleted
   */
  const handleTaskDeleted = (taskId: number) => {
    setTasks((prev) => prev.filter((task) => task.id !== taskId));
  };

  /**
   * Handle task toggle by updating local state.
   */
  const handleTaskToggle = async (taskId: number) => {
    try {
      const task = tasks.find((t) => t.id === taskId);
      if (!task) return;

      await apiRequest(`/api/tasks/${taskId}/toggle`, { method: "PATCH" });

      // Update local state
      setTasks((prev) =>
        prev.map((t) =>
          t.id === taskId ? { ...t, completed: !t.completed } : t
        )
      );

      // Announce to screen readers
      announce(task.completed ? "Task marked as incomplete" : "Task marked as complete");
    } catch (error: any) {
      toast({
        title: "Failed to update task",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  /**
   * Handle task deletion with undo capability.
   *
   * Soft deletes the task and shows an undo toast for 5 seconds.
   * Task is restored if user clicks Undo within the timeout.
   */
  const handleTaskDelete = async (taskId: number) => {
    const deletedTask = tasks.find((t) => t.id === taskId);
    if (!deletedTask) return;

    try {
      // Soft delete the task
      await apiRequest(`/api/tasks/${taskId}`, { method: "DELETE" });

      // Remove from local state immediately
      setTasks((prev) => prev.filter((task) => task.id !== taskId));

      // Announce to screen readers
      announce("Task deleted");

      // Show undo toast
      toast({
        title: "Task deleted",
        description: (
          <div className="flex items-center justify-between gap-2">
            <span>{deletedTask.title}</span>
            <button
              onClick={async () => {
                try {
                  // Restore the task via API
                  await apiRequest(`/api/tasks/${taskId}/restore`, { method: "POST" });

                  // Refresh the task list
                  fetchTasks();

                  // Announce restoration
                  announce("Task restored");

                  toast({
                    title: "Task restored",
                    description: "Task has been successfully restored",
                  });
                } catch (error: any) {
                  toast({
                    title: "Failed to restore task",
                    description: error.message,
                    variant: "destructive",
                  });
                }
              }}
              className="px-3 py-1 text-sm font-medium text-seal-brown bg-white/20 hover:bg-white/30 rounded-lg transition-colors"
            >
              Undo
            </button>
          </div>
        ),
        duration: 5000, // 5 second timeout
      });
    } catch (error: any) {
      toast({
        title: "Failed to delete task",
        description: error.message,
        variant: "destructive",
      });
    }
  };

  /**
   * Handle task edit.
   */
  const handleTaskEdit = (task: Task) => {
    setEditingTask(task);
  };

  if (isLoading) {
    return <SkeletonTaskList count={5} />;
  }

  // Empty state messages based on filters
  const getEmptyMessage = () => {
    if (tasks.length === 0) {
      if (filters.search) return "No tasks match your search.";
      if (filters.status === "pending") return "No pending tasks. Great job! 🎉";
      if (filters.status === "completed") return "No completed tasks yet. Let's get started!";
      return "No tasks yet. Create one to get started!";
    }
    return "No tasks found.";
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-seal-brown/60 text-lg">
          {getEmptyMessage()}
        </p>
      </div>
    );
  }

  return (
    <>
      <div className="space-y-4 animate-fade-in">
        {tasks.map((task, index) => (
          <div
            key={task.id}
            className="animate-slide-in-up"
            style={{
              animationDelay: `${index * 50}ms`,
              animationFillMode: "both"
            }}
          >
            <ColorfulTaskCard
              task={task}
              onToggle={handleTaskToggle}
              onEdit={handleTaskEdit}
              onDelete={handleTaskDelete}
            />
          </div>
        ))}
      </div>

      {/* Edit Task Modal */}
      {editingTask && (
        <TaskForm
          task={editingTask}
          open={!!editingTask}
          onOpenChange={(open) => !open && setEditingTask(null)}
        />
      )}

      {/* Screen Reader Announcer */}
      <ScreenReaderAnnouncer message={message} />
    </>
  );
}
