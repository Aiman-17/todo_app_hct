/**
 * Task creation dialog component.
 *
 * Handles task creation with title and description fields in a dialog.
 * Implements keyboard navigation:
 * - Escape key closes dialog
 * - Enter key submits form (when in input fields)
 * - Auto-focus on title input when opened
 */
"use client";

import { useState, useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { LoadingSpinner } from "@/components/shared/LoadingSpinner";
import { useToast } from "@/components/ui/use-toast";
import { apiRequest } from "@/lib/api";
import { useScreenReaderAnnouncement, ScreenReaderAnnouncer } from "@/hooks/useScreenReaderAnnouncement";
import type { TaskCreate, Task } from "@/types/task";

interface TaskFormProps {
  trigger?: React.ReactNode;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  task?: Task; // Optional: if provided, form is in edit mode
}

const DRAFT_KEY = "task_form_draft";

export function TaskForm({ trigger, open: controlledOpen, onOpenChange, task }: TaskFormProps) {
  const { toast } = useToast();
  const { announce, message } = useScreenReaderAnnouncement();
  const titleInputRef = useRef<HTMLInputElement>(null);

  const isEditMode = !!task;
  const [internalOpen, setInternalOpen] = useState(false);
  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [priority, setPriority] = useState<"high" | "medium" | "low">(task?.priority || "medium");
  const [tags, setTags] = useState<string[]>(task?.tags || []);
  const [tagInput, setTagInput] = useState("");
  const [dueDate, setDueDate] = useState<string>(
    task?.due_date ? new Date(task.due_date).toISOString().split('T')[0] : ""
  );
  const [recurrenceEnabled, setRecurrenceEnabled] = useState<boolean>(!!task?.recurrence_rule);
  const [recurrenceFrequency, setRecurrenceFrequency] = useState<string>(
    task?.recurrence_rule?.frequency || "daily"
  );
  const [recurrenceInterval, setRecurrenceInterval] = useState<number>(
    task?.recurrence_rule?.interval || 1
  );
  const [isLoading, setIsLoading] = useState(false);
  const [draftSaved, setDraftSaved] = useState(false);

  const isOpen = controlledOpen !== undefined ? controlledOpen : internalOpen;
  const setIsOpen = onOpenChange || setInternalOpen;

  /**
   * Load draft from localStorage when component mounts.
   *
   * Restores any unsaved work from a previous session to prevent data loss.
   */
  useEffect(() => {
    try {
      const savedDraft = localStorage.getItem(DRAFT_KEY);
      if (savedDraft) {
        const draft = JSON.parse(savedDraft);
        setTitle(draft.title || "");
        setDescription(draft.description || "");
        setDraftSaved(true);
      }
    } catch (error) {
      // Ignore localStorage errors (e.g., quota exceeded, disabled)
      console.error("Failed to load draft:", error);
    }
  }, []);

  /**
   * Save draft to localStorage whenever title or description changes.
   *
   * Prevents work loss due to session expiration or accidental browser closure.
   * Draft is automatically cleared after successful task creation.
   */
  useEffect(() => {
    if (title || description) {
      try {
        localStorage.setItem(DRAFT_KEY, JSON.stringify({ title, description }));
        setDraftSaved(true);
        // Hide "draft saved" indicator after 2 seconds
        const timer = setTimeout(() => setDraftSaved(false), 2000);
        return () => clearTimeout(timer);
      } catch (error) {
        // Ignore localStorage errors
        console.error("Failed to save draft:", error);
      }
    }
  }, [title, description]);

  /**
   * Auto-focus title input when dialog opens.
   *
   * Uses setTimeout to wait for dialog animation to complete before focusing.
   */
  useEffect(() => {
    if (isOpen && titleInputRef.current) {
      setTimeout(() => {
        titleInputRef.current?.focus();
      }, 100);
    }
  }, [isOpen]);

  /**
   * Handle form submission to create or update a task.
   *
   * Sends POST (create) or PUT (update) request to backend with task data,
   * clears form on success, closes dialog, and dispatches event to notify TaskList.
   *
   * @param e - Form submission event
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (isEditMode && task) {
        // Update existing task
        await apiRequest<Task>(`/api/tasks/${task.id}`, {
          method: "PUT",
          body: JSON.stringify({
            title,
            description,
            priority,
            tags: tags.length > 0 ? tags : null,
            due_date: dueDate ? new Date(dueDate).toISOString() : null,
            recurrence_rule: recurrenceEnabled ? { frequency: recurrenceFrequency, interval: recurrenceInterval } : null,
          }),
        });

        toast({
          title: "Task updated",
          description: "Your task has been updated successfully",
        });

        // Announce to screen readers
        announce("Task updated successfully");

        window.dispatchEvent(new CustomEvent("taskUpdated"));
      } else {
        // Create new task
        await apiRequest<Task>("/api/tasks", {
          method: "POST",
          body: JSON.stringify({
            title,
            description,
            priority,
            tags: tags.length > 0 ? tags : null,
            due_date: dueDate ? new Date(dueDate).toISOString() : null,
            recurrence_rule: recurrenceEnabled ? { frequency: recurrenceFrequency, interval: recurrenceInterval } : null,
          } as TaskCreate),
        });

        toast({
          title: "Task created",
          description: "Your task has been added successfully",
        });

        // Announce to screen readers
        announce("Task created successfully");

        window.dispatchEvent(new CustomEvent("taskCreated"));
      }

      // Clear form state
      setTitle("");
      setDescription("");

      // Clear saved draft from localStorage
      try {
        localStorage.removeItem(DRAFT_KEY);
      } catch (error) {
        console.error("Failed to clear draft:", error);
      }

      setIsOpen(false);
    } catch (error: any) {
      toast({
        title: isEditMode ? "Failed to update task" : "Failed to create task",
        description: error.message || "An error occurred",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handle keyboard events for dialog navigation.
   *
   * - Escape key: Close dialog
   * - Enter key (in input fields): Submit form
   *
   * @param e - Keyboard event
   */
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape") {
      e.preventDefault();
      setIsOpen(false);
    } else if (e.key === "Enter" && (e.target as HTMLElement).tagName === "INPUT") {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const dialogContent = (
    <DialogContent onKeyDown={handleKeyDown} className="sm:max-w-[500px] max-h-[85vh] flex flex-col p-0">
      <DialogHeader className="px-6 pt-6 pb-4 shrink-0">
        <DialogTitle>{isEditMode ? "Edit Task" : "Add New Task"}</DialogTitle>
        <DialogDescription>
          {isEditMode ? "Update your task details" : "Create a new task to add to your list"}
        </DialogDescription>
      </DialogHeader>

      {/* Screen Reader Announcer */}
      <ScreenReaderAnnouncer message={message} />

      <form onSubmit={handleSubmit} className="space-y-4 overflow-y-auto px-6 pb-6 flex-1">
        <div className="space-y-2">
          <Label htmlFor="title">Title</Label>
          <Input
            ref={titleInputRef}
            id="title"
            type="text"
            placeholder="Enter task title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            maxLength={200}
            disabled={isLoading}
          />
          <p className="text-xs text-gray-500">
            {title.length}/200 characters
          </p>
        </div>

        <div className="space-y-2">
          <Label htmlFor="description">Description (optional)</Label>
          <Input
            id="description"
            type="text"
            placeholder="Enter task description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            maxLength={2000}
            disabled={isLoading}
          />
          <p className="text-xs text-gray-500">
            {description.length}/2000 characters
          </p>
        </div>

        {/* Priority Selector */}
        <div className="space-y-2">
          <Label htmlFor="priority">Priority</Label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value as "high" | "medium" | "low")}
            disabled={isLoading}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-seal-brown/30 focus:border-seal-brown"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        {/* Due Date Picker */}
        <div className="space-y-2">
          <Label htmlFor="due_date">Due Date (optional)</Label>
          <Input
            id="due_date"
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            disabled={isLoading}
            min={new Date().toISOString().split('T')[0]}
          />
        </div>

        {/* Recurrence Rule Selector */}
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <input
              id="recurrence_enabled"
              type="checkbox"
              checked={recurrenceEnabled}
              onChange={(e) => setRecurrenceEnabled(e.target.checked)}
              disabled={isLoading}
              className="w-4 h-4 rounded border-gray-300 text-seal-brown focus:ring-seal-brown/30"
            />
            <Label htmlFor="recurrence_enabled" className="cursor-pointer">
              Repeat this task
            </Label>
          </div>

          {recurrenceEnabled && (
            <div className="ml-6 space-y-2 border-l-2 border-seal-brown/20 pl-4">
              <div className="space-y-2">
                <Label htmlFor="recurrence_frequency">Frequency</Label>
                <select
                  id="recurrence_frequency"
                  value={recurrenceFrequency}
                  onChange={(e) => setRecurrenceFrequency(e.target.value)}
                  disabled={isLoading}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-seal-brown/30 focus:border-seal-brown"
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="yearly">Yearly</option>
                </select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="recurrence_interval">Repeat every</Label>
                <div className="flex items-center gap-2">
                  <Input
                    id="recurrence_interval"
                    type="number"
                    min="1"
                    max="365"
                    value={recurrenceInterval}
                    onChange={(e) => setRecurrenceInterval(parseInt(e.target.value) || 1)}
                    disabled={isLoading}
                    className="w-20"
                  />
                  <span className="text-sm text-gray-500">
                    {recurrenceFrequency === 'daily' && (recurrenceInterval === 1 ? 'day' : 'days')}
                    {recurrenceFrequency === 'weekly' && (recurrenceInterval === 1 ? 'week' : 'weeks')}
                    {recurrenceFrequency === 'monthly' && (recurrenceInterval === 1 ? 'month' : 'months')}
                    {recurrenceFrequency === 'yearly' && (recurrenceInterval === 1 ? 'year' : 'years')}
                  </span>
                </div>
              </div>

              <p className="text-xs text-gray-500 italic">
                {recurrenceFrequency === 'daily' && `Task will repeat every ${recurrenceInterval} day${recurrenceInterval > 1 ? 's' : ''}`}
                {recurrenceFrequency === 'weekly' && `Task will repeat every ${recurrenceInterval} week${recurrenceInterval > 1 ? 's' : ''}`}
                {recurrenceFrequency === 'monthly' && `Task will repeat every ${recurrenceInterval} month${recurrenceInterval > 1 ? 's' : ''}`}
                {recurrenceFrequency === 'yearly' && `Task will repeat every ${recurrenceInterval} year${recurrenceInterval > 1 ? 's' : ''}`}
              </p>
            </div>
          )}
        </div>

        {/* Tags Input */}
        <div className="space-y-2">
          <Label htmlFor="tags">Tags (optional)</Label>
          <div className="flex gap-2">
            <Input
              id="tags"
              type="text"
              placeholder="Add a tag"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  if (tagInput.trim() && tags.length < 10) {
                    setTags([...tags, tagInput.trim()]);
                    setTagInput("");
                  }
                }
              }}
              disabled={isLoading}
              maxLength={50}
            />
            <Button
              type="button"
              onClick={() => {
                if (tagInput.trim() && tags.length < 10) {
                  setTags([...tags, tagInput.trim()]);
                  setTagInput("");
                }
              }}
              disabled={isLoading || !tagInput.trim() || tags.length >= 10}
              variant="outline"
            >
              Add
            </Button>
          </div>
          {tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-2">
              {tags.map((tag, index) => (
                <span
                  key={index}
                  className="inline-flex items-center gap-1 px-2 py-1 text-xs bg-seal-brown/10 text-seal-brown rounded-full"
                >
                  {tag}
                  <button
                    type="button"
                    onClick={() => setTags(tags.filter((_, i) => i !== index))}
                    disabled={isLoading}
                    className="hover:text-red-600"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
          <p className="text-xs text-gray-500">
            {tags.length}/10 tags • Press Enter or click Add
          </p>
        </div>

        <div className="flex gap-2 justify-between items-center">
          <div className="text-xs text-gray-500 italic">
            {draftSaved && (title || description) && "Draft saved"}
          </div>
          <div className="flex gap-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => setIsOpen(false)}
              disabled={isLoading}
              className="min-h-[44px] min-w-[44px]"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={isLoading}
              className="min-h-[44px] min-w-[44px]"
            >
              {isLoading ? (
                <>
                  <LoadingSpinner size={16} className="mr-2" />
                  {isEditMode ? "Updating..." : "Creating..."}
                </>
              ) : (
                isEditMode ? "Update Task" : "Create Task"
              )}
            </Button>
          </div>
        </div>
      </form>
    </DialogContent>
  );

  if (trigger) {
    return (
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogTrigger asChild>{trigger}</DialogTrigger>
        {dialogContent}
      </Dialog>
    );
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      {dialogContent}
    </Dialog>
  );
}
