/**
 * Task item client component.
 *
 * Displays a single task with:
 * - Checkbox for completion toggle
 * - Title and description
 * - Edit button (inline editing)
 * - Delete button (with confirmation modal)
 */
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/components/ui/use-toast";
import { DeleteTaskModal } from "./DeleteTaskModal";
import { apiRequest } from "@/lib/api";
import type { Task, TaskUpdate } from "@/types/task";

interface TaskItemProps {
  task: Task;
  onDeleted: (taskId: number) => void;
  onToggled: (taskId: number) => void;
}

export function TaskItem({ task, onDeleted, onToggled }: TaskItemProps) {
  const { toast } = useToast();

  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description);
  const [isUpdating, setIsUpdating] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  /**
   * Toggle task completion status.
   *
   * Sends PATCH request to backend and notifies parent component to refresh list.
   * Displays toast on success or error.
   */
  const handleToggle = async () => {
    try {
      await apiRequest<Task>(`/api/tasks/${task.id}/toggle`, {
        method: "PATCH",
      });

      toast({
        title: "Task updated",
        description: task.completed ? "Task marked as incomplete" : "Task marked as complete",
      });

      onToggled(task.id);
    } catch (error: any) {
      toast({
        title: "Failed to update task",
        description: error.message || "An error occurred",
        variant: "destructive",
      });
    }
  };

  /**
   * Save edited task to backend.
   *
   * Validates that title is not empty, then sends PUT request with updated fields.
   * Dispatches "taskUpdated" event to notify other components.
   */
  const handleSaveEdit = async () => {
    if (!editTitle.trim()) {
      toast({
        title: "Validation error",
        description: "Title cannot be empty",
        variant: "destructive",
      });
      return;
    }

    setIsUpdating(true);

    try {
      await apiRequest<Task>(`/api/tasks/${task.id}`, {
        method: "PUT",
        body: JSON.stringify({
          title: editTitle,
          description: editDescription,
        } as TaskUpdate),
      });

      toast({
        title: "Task updated",
        description: "Your changes have been saved",
      });

      setIsEditing(false);
      window.dispatchEvent(new CustomEvent("taskUpdated"));
    } catch (error: any) {
      toast({
        title: "Failed to update task",
        description: error.message || "An error occurred",
        variant: "destructive",
      });
    } finally {
      setIsUpdating(false);
    }
  };

  /**
   * Cancel edit mode and revert changes.
   *
   * Resets edit fields to original task values and exits edit mode.
   */
  const handleCancelEdit = () => {
    setEditTitle(task.title);
    setEditDescription(task.description);
    setIsEditing(false);
  };

  /**
   * Delete task from backend.
   *
   * Sends DELETE request and notifies parent component on success.
   * Closes delete confirmation modal after deletion.
   */
  const handleDelete = async () => {
    try {
      await apiRequest(`/api/tasks/${task.id}`, {
        method: "DELETE",
      });

      toast({
        title: "Task deleted",
        description: "The task has been removed",
      });

      onDeleted(task.id);
      setShowDeleteModal(false);
    } catch (error: any) {
      toast({
        title: "Failed to delete task",
        description: error.message || "An error occurred",
        variant: "destructive",
      });
    }
  };

  return (
    <div className={`rounded-lg border p-4 transition-colors hover:bg-accent ${task.completed ? "bg-gray-50" : "bg-white"}`}>
      <div className="flex items-start gap-3">
        {/* Completion checkbox */}
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggle}
          className="mt-1 min-h-[44px] min-w-[44px] h-5 w-5 cursor-pointer rounded border-gray-300"
          aria-label={`Mark "${task.title}" as ${task.completed ? "incomplete" : "complete"}`}
        />

        {/* Task content */}
        <div className="flex-1">
          {isEditing ? (
            // Edit mode
            <div className="space-y-2">
              <Input
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                placeholder="Task title"
                maxLength={200}
                disabled={isUpdating}
              />
              <Input
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                placeholder="Task description (optional)"
                maxLength={2000}
                disabled={isUpdating}
              />
              <div className="flex gap-2">
                <Button
                  size="sm"
                  onClick={handleSaveEdit}
                  disabled={isUpdating}
                  className="min-h-[44px] min-w-[44px]"
                >
                  {isUpdating ? "Saving..." : "Save"}
                </Button>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={handleCancelEdit}
                  disabled={isUpdating}
                  className="min-h-[44px] min-w-[44px]"
                >
                  Cancel
                </Button>
              </div>
            </div>
          ) : (
            // View mode
            <>
              <h3 className={`font-medium ${task.completed ? "line-through text-gray-500" : ""}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-1 text-sm ${task.completed ? "line-through text-gray-400" : "text-gray-600"}`}>
                  {task.description}
                </p>
              )}
              <div className="mt-2 flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={() => setIsEditing(true)}
                  className="min-h-[44px] min-w-[44px]"
                >
                  Edit
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => setShowDeleteModal(true)}
                  className="min-h-[44px] min-w-[44px]"
                >
                  Delete
                </Button>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Delete confirmation modal */}
      <DeleteTaskModal
        open={showDeleteModal}
        onOpenChange={setShowDeleteModal}
        taskTitle={task.title}
        onConfirmDelete={handleDelete}
      />
    </div>
  );
}
