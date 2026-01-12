/**
 * Recurrence utility for calculating next occurrence dates and formatting recurrence rules.
 *
 * Supports daily, weekly, monthly, and yearly recurrence patterns with custom intervals.
 */

export type RecurrenceFrequency = "daily" | "weekly" | "monthly" | "yearly";

export interface RecurrenceRule {
  frequency: RecurrenceFrequency;
  interval: number; // 1 = every day/week/month, 2 = every 2 days/weeks/months, etc.
}

/**
 * Calculate the next occurrence date from a given date based on recurrence rule.
 *
 * @param fromDate - Starting date (typically the current due_date)
 * @param rule - Recurrence rule with frequency and interval
 * @returns Next occurrence date
 *
 * @example
 * const nextDate = calculateNextOccurrence(
 *   new Date('2025-01-01'),
 *   { frequency: 'weekly', interval: 2 }
 * );
 * // Returns: 2025-01-15 (2 weeks later)
 */
export function calculateNextOccurrence(
  fromDate: Date,
  rule: RecurrenceRule
): Date {
  const nextDate = new Date(fromDate);

  switch (rule.frequency) {
    case "daily":
      nextDate.setDate(nextDate.getDate() + rule.interval);
      break;

    case "weekly":
      nextDate.setDate(nextDate.getDate() + rule.interval * 7);
      break;

    case "monthly":
      nextDate.setMonth(nextDate.getMonth() + rule.interval);
      break;

    case "yearly":
      nextDate.setFullYear(nextDate.getFullYear() + rule.interval);
      break;

    default:
      throw new Error(`Unknown recurrence frequency: ${rule.frequency}`);
  }

  return nextDate;
}

/**
 * Format recurrence rule for display as a human-readable string.
 *
 * @param rule - Recurrence rule with frequency and interval
 * @returns Formatted string (e.g., "Daily", "Weekly", "Every 2 weeks", "Monthly")
 *
 * @example
 * formatRecurrenceRule({ frequency: 'weekly', interval: 1 }); // "Weekly"
 * formatRecurrenceRule({ frequency: 'daily', interval: 2 }); // "Every 2 days"
 * formatRecurrenceRule({ frequency: 'monthly', interval: 1 }); // "Monthly"
 */
export function formatRecurrenceRule(rule: RecurrenceRule): string {
  const { frequency, interval } = rule;

  // Singular/plural forms for each frequency
  const labels: Record<RecurrenceFrequency, { singular: string; plural: string }> = {
    daily: { singular: "day", plural: "days" },
    weekly: { singular: "week", plural: "weeks" },
    monthly: { singular: "month", plural: "months" },
    yearly: { singular: "year", plural: "years" },
  };

  if (interval === 1) {
    // Simple case: "Daily", "Weekly", "Monthly", "Yearly"
    return frequency.charAt(0).toUpperCase() + frequency.slice(1);
  }

  // Complex case: "Every 2 days", "Every 3 weeks", etc.
  const label = labels[frequency];
  return `Every ${interval} ${label.plural}`;
}

/**
 * Check if a task has a recurrence rule.
 *
 * @param recurrenceRule - Recurrence rule object or null
 * @returns True if task is recurring, false otherwise
 */
export function isRecurring(recurrenceRule: Record<string, any> | null): boolean {
  return recurrenceRule !== null && recurrenceRule.frequency !== undefined;
}

/**
 * Validate recurrence rule structure.
 *
 * @param rule - Recurrence rule to validate
 * @returns True if valid, false otherwise
 */
export function isValidRecurrenceRule(rule: any): rule is RecurrenceRule {
  if (!rule || typeof rule !== "object") return false;

  const validFrequencies: RecurrenceFrequency[] = ["daily", "weekly", "monthly", "yearly"];

  return (
    validFrequencies.includes(rule.frequency) &&
    typeof rule.interval === "number" &&
    rule.interval >= 1
  );
}
