/**
 * Browser notification utilities for task due date reminders.
 *
 * Handles permission requests, notification scheduling, and notification preferences.
 */

export type NotificationPermissionStatus = "granted" | "denied" | "default";

export interface NotificationPreferences {
  enabled: boolean;
  reminderMinutes: number; // Minutes before due date to send notification
}

const DEFAULT_REMINDER_MINUTES = 60; // 1 hour before due date

/**
 * Check if browser supports notifications.
 *
 * @returns True if Notification API is available, false otherwise
 */
export function isNotificationSupported(): boolean {
  return typeof window !== "undefined" && "Notification" in window;
}

/**
 * Get current notification permission status.
 *
 * @returns Permission status: "granted", "denied", or "default"
 */
export function getNotificationPermission(): NotificationPermissionStatus {
  if (!isNotificationSupported()) return "denied";
  return Notification.permission as NotificationPermissionStatus;
}

/**
 * Request notification permission from the user.
 *
 * Shows browser's native permission dialog.
 *
 * @returns Promise that resolves to the permission status
 *
 * @example
 * const permission = await requestNotificationPermission();
 * if (permission === "granted") {
 *   console.log("Notifications enabled!");
 * }
 */
export async function requestNotificationPermission(): Promise<NotificationPermissionStatus> {
  if (!isNotificationSupported()) {
    console.warn("Notifications are not supported in this browser");
    return "denied";
  }

  if (Notification.permission === "granted") {
    return "granted";
  }

  try {
    const permission = await Notification.requestPermission();
    return permission as NotificationPermissionStatus;
  } catch (error) {
    console.error("Failed to request notification permission:", error);
    return "denied";
  }
}

/**
 * Show a browser notification.
 *
 * Requires notification permission to be granted.
 *
 * @param title - Notification title
 * @param options - Notification options (body, icon, etc.)
 * @returns Notification instance or null if permission denied
 *
 * @example
 * showNotification("Task Due Soon", {
 *   body: "Buy groceries is due in 1 hour",
 *   icon: "/icon.png"
 * });
 */
export function showNotification(
  title: string,
  options?: NotificationOptions
): Notification | null {
  if (!isNotificationSupported()) {
    console.warn("Notifications are not supported in this browser");
    return null;
  }

  if (Notification.permission !== "granted") {
    console.warn("Notification permission not granted");
    return null;
  }

  try {
    return new Notification(title, options);
  } catch (error) {
    console.error("Failed to show notification:", error);
    return null;
  }
}

/**
 * Schedule a notification for a task due date.
 *
 * Sets up a timer to show a notification before the task is due.
 *
 * @param taskTitle - Task title
 * @param dueDate - ISO 8601 due date string
 * @param reminderMinutes - Minutes before due date to notify (default: 60)
 * @returns Timer ID that can be used to cancel the notification, or null if scheduling failed
 *
 * @example
 * const timerId = scheduleTaskNotification(
 *   "Buy groceries",
 *   "2025-01-04T15:00:00Z",
 *   30 // 30 minutes before
 * );
 *
 * // Later, to cancel:
 * if (timerId) clearTimeout(timerId);
 */
export function scheduleTaskNotification(
  taskTitle: string,
  dueDate: string,
  reminderMinutes: number = DEFAULT_REMINDER_MINUTES
): number | null {
  if (!isNotificationSupported() || Notification.permission !== "granted") {
    return null;
  }

  const due = new Date(dueDate);
  const now = new Date();

  // Calculate notification time (reminderMinutes before due date)
  const notificationTime = new Date(due.getTime() - reminderMinutes * 60 * 1000);
  const timeUntilNotification = notificationTime.getTime() - now.getTime();

  // Don't schedule if notification time has passed
  if (timeUntilNotification <= 0) {
    return null;
  }

  // Schedule notification
  const timerId = window.setTimeout(() => {
    showNotification("Task Due Soon", {
      body: `"${taskTitle}" is due in ${reminderMinutes} minutes`,
      icon: "/icon.png",
      badge: "/badge.png",
      tag: `task-${taskTitle}`, // Prevents duplicate notifications for same task
      requireInteraction: false,
      silent: false
    });
  }, timeUntilNotification);

  return timerId;
}

/**
 * Cancel a scheduled notification.
 *
 * @param timerId - Timer ID returned from scheduleTaskNotification
 *
 * @example
 * const timerId = scheduleTaskNotification("Buy groceries", dueDate);
 * // Later, cancel the notification
 * cancelScheduledNotification(timerId);
 */
export function cancelScheduledNotification(timerId: number): void {
  clearTimeout(timerId);
}

/**
 * Load notification preferences from localStorage.
 *
 * @returns NotificationPreferences object with enabled and reminderMinutes
 */
export function loadNotificationPreferences(): NotificationPreferences {
  if (typeof window === "undefined") {
    return { enabled: false, reminderMinutes: DEFAULT_REMINDER_MINUTES };
  }

  try {
    const saved = localStorage.getItem("todo_app_notification_preferences");
    if (saved) {
      const parsed = JSON.parse(saved);
      return {
        enabled: typeof parsed.enabled === "boolean" ? parsed.enabled : false,
        reminderMinutes: typeof parsed.reminderMinutes === "number"
          ? parsed.reminderMinutes
          : DEFAULT_REMINDER_MINUTES
      };
    }
  } catch (error) {
    console.error("Failed to load notification preferences:", error);
  }

  return { enabled: false, reminderMinutes: DEFAULT_REMINDER_MINUTES };
}

/**
 * Save notification preferences to localStorage.
 *
 * @param preferences - NotificationPreferences to save
 */
export function saveNotificationPreferences(preferences: NotificationPreferences): void {
  if (typeof window === "undefined") return;

  try {
    localStorage.setItem(
      "todo_app_notification_preferences",
      JSON.stringify(preferences)
    );
  } catch (error) {
    console.error("Failed to save notification preferences:", error);
  }
}
