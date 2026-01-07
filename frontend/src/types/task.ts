/**
 * TypeScript type definitions for task-related data structures.
 *
 * Mirrors backend Pydantic schemas (TaskCreate, TaskUpdate, TaskResponse).
 */

/**
 * Task data (response from backend).
 */
export interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  priority: "high" | "medium" | "low";
  due_date: string | null; // ISO 8601 datetime or null
  tags: string[] | null;
  recurrence_rule: Record<string, any> | null;
  created_at: string; // ISO 8601 datetime
  updated_at: string; // ISO 8601 datetime
  deleted_at: string | null; // ISO 8601 datetime or null (soft delete)
}

/**
 * Task creation request payload.
 */
export interface TaskCreate {
  title: string;
  description?: string;
  priority?: "high" | "medium" | "low";
  due_date?: string | null;
  tags?: string[] | null;
  recurrence_rule?: Record<string, any> | null;
}

/**
 * Task update request payload (all fields optional).
 */
export interface TaskUpdate {
  title?: string;
  description?: string;
  priority?: "high" | "medium" | "low";
  due_date?: string | null;
  tags?: string[] | null;
  recurrence_rule?: Record<string, any> | null;
}
