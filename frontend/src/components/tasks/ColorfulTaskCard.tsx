"use client";

/**
 * Colorful Task Card Component
 *
 * Beautiful task cards inspired by Pomodoro Timer app design.
 * Features:
 * - Dynamic colors (pink, purple, green, blue, orange)
 * - Small icons on the left
 * - Rounded corners with shadows
 * - Icon-based edit/delete buttons
 * - Modern checkbox styling
 * - Time duration display
 * - Optimized with React.memo to prevent unnecessary re-renders
 */

import { Pencil, Trash2, Check, Clock, Repeat } from "lucide-react";
import { useState, memo } from "react";
import type { Task } from "@/types/task";
import { isRecurring, formatRecurrenceRule } from "@/lib/recurrence";
import { getRelativeDueDate } from "@/lib/date-utils";

// Priority colors
const PRIORITY_COLORS = {
  high: "#EF4444", // Red
  medium: "#F97316", // Orange
  low: "#3B82F6", // Blue
};

interface ColorfulTaskCardProps {
  task: Task;
  onToggle: (id: number) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
}

// Color palette for different tasks
const TASK_COLORS = [
  { bg: "#FFB8D2", text: "#8B0039", icon: "#FF6B9D" }, // Pink
  { bg: "#D4B5F6", text: "#4A1E7C", icon: "#9B6DD6" }, // Purple
  { bg: "#A8E6A1", text: "#1B5E20", icon: "#66BB6A" }, // Green
  { bg: "#A8D8FF", text: "#0D47A1", icon: "#42A5F5" }, // Blue
  { bg: "#FFCC80", text: "#E65100", icon: "#FFA726" }, // Orange
  { bg: "#F8BBD0", text: "#880E4F", icon: "#EC407A" }, // Rose
  { bg: "#B39DDB", text: "#311B92", icon: "#7E57C2" }, // Deep Purple
  { bg: "#81C784", text: "#1B5E20", icon: "#4CAF50" }, // Light Green
];

export const ColorfulTaskCard = memo(function ColorfulTaskCard({
  task,
  onToggle,
  onEdit,
  onDelete,
}: ColorfulTaskCardProps) {
  const [isHovered, setIsHovered] = useState(false);

  // Assign color based on task ID (consistent coloring)
  const colorIndex = task.id % TASK_COLORS.length;
  const colors = TASK_COLORS[colorIndex];

  // Get due date info
  const dueDateInfo = getRelativeDueDate(task.due_date);

  return (
    <div
      className="group relative"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div
        role="article"
        aria-label={`Task: ${task.title}${task.completed ? " (completed)" : ""}`}
        className={`
          relative flex items-center gap-4 p-4 rounded-2xl
          transition-all duration-200 ease-in-out
          ${task.completed ? "opacity-60" : "opacity-100"}
          ${isHovered ? "scale-[1.02] shadow-lg" : "shadow-md"}
          ${dueDateInfo?.isOverdue && !task.completed ? "ring-2 ring-red-500/50" : ""}
        `}
        style={{ backgroundColor: colors.bg }}
      >
        {/* Custom Checkbox - 44px minimum for touch targets */}
        <button
          onClick={() => onToggle(task.id)}
          className={`
            flex-shrink-0 w-11 h-11 rounded-lg border-2
            flex items-center justify-center
            transition-all duration-200
            ${
              task.completed
                ? "bg-white border-white"
                : "bg-transparent border-white/50 hover:border-white active:border-white"
            }
          `}
          aria-label={task.completed ? "Mark as incomplete" : "Mark as complete"}
          style={{ borderColor: task.completed ? colors.text : undefined }}
        >
          {task.completed && (
            <Check className="w-6 h-6 animate-bounce-subtle" style={{ color: colors.text }} />
          )}
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`
              font-medium text-base
              ${task.completed ? "line-through" : ""}
            `}
            style={{ color: colors.text }}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className="text-sm mt-1 opacity-80 truncate"
              style={{ color: colors.text }}
            >
              {task.description}
            </p>
          )}

          {/* Tags Pills */}
          {task.tags && task.tags.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {task.tags.map((tag, index) => (
                <span
                  key={index}
                  className="inline-flex items-center px-2 py-0.5 text-xs rounded-full bg-white/40"
                  style={{ color: colors.text }}
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* Due Date Label */}
          {dueDateInfo && (
            <div className="flex items-center gap-1 mt-2">
              <Clock className="w-3 h-3 opacity-70" style={{ color: dueDateInfo.isOverdue ? "#EF4444" : colors.text }} aria-hidden="true" />
              <span
                className={`text-xs font-medium ${dueDateInfo.isOverdue ? "font-semibold" : ""}`}
                style={{ color: dueDateInfo.isOverdue ? "#EF4444" : colors.text }}
              >
                {dueDateInfo.label}
              </span>
            </div>
          )}

          {/* Recurrence Badge */}
          {isRecurring(task.recurrence_rule) && task.recurrence_rule && (
            <div className="flex items-center gap-1 mt-2">
              <Repeat className="w-3 h-3 opacity-70" style={{ color: colors.text }} aria-hidden="true" />
              <span className="text-xs font-medium" style={{ color: colors.text }}>
                {formatRecurrenceRule(task.recurrence_rule as any)}
              </span>
            </div>
          )}
        </div>

        {/* Action Icons - Always visible on mobile, show on hover on desktop */}
        <div
          className={`
            flex items-center gap-2
            transition-opacity duration-200
            md:${isHovered ? "opacity-100" : "opacity-0"}
            opacity-100
          `}
        >
          {/* Edit Button - 44px minimum for touch targets */}
          <button
            onClick={() => onEdit(task)}
            className="p-3 rounded-lg bg-white/50 hover:bg-white/80 active:bg-white/90 transition-colors min-w-[44px] min-h-[44px] flex items-center justify-center"
            aria-label={`Edit task: ${task.title}`}
          >
            <Pencil className="w-5 h-5" style={{ color: colors.text }} aria-hidden="true" />
          </button>

          {/* Delete Button - 44px minimum for touch targets */}
          <button
            onClick={() => onDelete(task.id)}
            className="p-3 rounded-lg bg-white/50 hover:bg-white/80 active:bg-white/90 transition-colors min-w-[44px] min-h-[44px] flex items-center justify-center"
            aria-label={`Delete task: ${task.title}`}
          >
            <Trash2 className="w-5 h-5" style={{ color: colors.text }} aria-hidden="true" />
          </button>
        </div>

        {/* Priority Indicator (small, top-right) */}
        <div
          className="absolute top-2 right-2 w-8 h-8 rounded-full flex items-center justify-center"
          style={{ backgroundColor: PRIORITY_COLORS[task.priority] + "30" }}
          role="status"
          aria-label={`Priority: ${task.priority}`}
        >
          <div
            className="w-3 h-3 rounded-full"
            style={{ backgroundColor: PRIORITY_COLORS[task.priority] }}
            aria-hidden="true"
          />
        </div>
      </div>
    </div>
  );
});
