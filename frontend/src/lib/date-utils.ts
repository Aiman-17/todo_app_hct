/**
 * Date formatting utilities for task due dates.
 *
 * Provides human-readable relative date labels (Today, Tomorrow, In X days, etc.)
 * and overdue detection for tasks.
 */

export interface RelativeDueDateInfo {
  label: string;
  isOverdue: boolean;
  daysUntilDue: number; // Negative if overdue, 0 if today, positive if future
}

/**
 * Get relative due date label and overdue status.
 *
 * @param dueDate - ISO 8601 date string or null
 * @returns RelativeDueDateInfo object with label, isOverdue flag, and days until due, or null if no due date
 *
 * @example
 * // Task due today
 * getRelativeDueDate("2025-01-04T10:00:00Z");
 * // Returns: { label: "Due Today", isOverdue: false, daysUntilDue: 0 }
 *
 * // Task overdue by 2 days
 * getRelativeDueDate("2025-01-02T10:00:00Z");
 * // Returns: { label: "Overdue by 2 days", isOverdue: true, daysUntilDue: -2 }
 *
 * // Task due in 3 days
 * getRelativeDueDate("2025-01-07T10:00:00Z");
 * // Returns: { label: "Due in 3 days", isOverdue: false, daysUntilDue: 3 }
 */
export function getRelativeDueDate(dueDate: string | null): RelativeDueDateInfo | null {
  if (!dueDate) return null;

  const due = new Date(dueDate);
  const now = new Date();

  // Normalize to start of day for accurate day comparisons
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const dueDay = new Date(due.getFullYear(), due.getMonth(), due.getDate());

  const diffTime = dueDay.getTime() - today.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  if (diffDays < 0) {
    // Overdue
    const daysOverdue = Math.abs(diffDays);
    return {
      label: `Overdue by ${daysOverdue} day${daysOverdue !== 1 ? 's' : ''}`,
      isOverdue: true,
      daysUntilDue: diffDays
    };
  } else if (diffDays === 0) {
    // Due today
    return {
      label: "Due Today",
      isOverdue: false,
      daysUntilDue: 0
    };
  } else if (diffDays === 1) {
    // Due tomorrow
    return {
      label: "Due Tomorrow",
      isOverdue: false,
      daysUntilDue: 1
    };
  } else if (diffDays <= 7) {
    // Due within a week
    return {
      label: `Due in ${diffDays} days`,
      isOverdue: false,
      daysUntilDue: diffDays
    };
  } else {
    // Due later (show formatted date)
    return {
      label: `Due ${formatDate(due)}`,
      isOverdue: false,
      daysUntilDue: diffDays
    };
  }
}

/**
 * Format a date as a readable string (e.g., "Jan 4, 2025").
 *
 * @param date - Date object to format
 * @returns Formatted date string
 *
 * @example
 * formatDate(new Date("2025-01-04"));
 * // Returns: "Jan 4, 2025"
 */
export function formatDate(date: Date): string {
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
}

/**
 * Format a date and time as a readable string (e.g., "Jan 4, 2025 at 10:30 AM").
 *
 * @param date - Date object to format
 * @returns Formatted date and time string
 *
 * @example
 * formatDateTime(new Date("2025-01-04T10:30:00Z"));
 * // Returns: "Jan 4, 2025 at 10:30 AM"
 */
export function formatDateTime(date: Date): string {
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });
}

/**
 * Check if a task is overdue based on its due date.
 *
 * @param dueDate - ISO 8601 date string or null
 * @returns True if task is overdue, false otherwise
 *
 * @example
 * isOverdue("2025-01-02T10:00:00Z"); // Returns: true (if today is after Jan 2)
 * isOverdue("2025-01-10T10:00:00Z"); // Returns: false (if today is before Jan 10)
 * isOverdue(null); // Returns: false (no due date)
 */
export function isOverdue(dueDate: string | null): boolean {
  if (!dueDate) return false;
  const info = getRelativeDueDate(dueDate);
  return info?.isOverdue ?? false;
}

/**
 * Get a color class for styling based on how soon a task is due.
 *
 * @param dueDate - ISO 8601 date string or null
 * @returns Tailwind color class string
 *
 * @example
 * getDueDateColor("2025-01-02T10:00:00Z"); // Returns: "text-red-600" (overdue)
 * getDueDateColor("2025-01-04T10:00:00Z"); // Returns: "text-orange-600" (today)
 * getDueDateColor("2025-01-05T10:00:00Z"); // Returns: "text-yellow-600" (tomorrow)
 * getDueDateColor("2025-01-10T10:00:00Z"); // Returns: "text-gray-600" (later)
 */
export function getDueDateColor(dueDate: string | null): string {
  const info = getRelativeDueDate(dueDate);
  if (!info) return "text-gray-600";

  if (info.isOverdue) return "text-red-600";
  if (info.daysUntilDue === 0) return "text-orange-600";
  if (info.daysUntilDue === 1) return "text-yellow-600";
  return "text-gray-600";
}
