/**
 * Keyboard shortcuts hook for global hotkeys.
 *
 * Provides keyboard shortcuts for common actions:
 * - N: New task
 * - /: Focus search
 * - F: Toggle filters
 * - Escape: Close modals/dropdowns
 */

import { useEffect } from "react";

export interface KeyboardShortcutHandlers {
  onNewTask?: () => void;
  onFocusSearch?: () => void;
  onToggleFilters?: () => void;
  onEscape?: () => void;
}

/**
 * Hook to enable global keyboard shortcuts.
 *
 * @param handlers - Object containing callback functions for each shortcut
 * @param enabled - Whether shortcuts are enabled (default: true)
 *
 * @example
 * useKeyboardShortcuts({
 *   onNewTask: () => setShowTaskForm(true),
 *   onFocusSearch: () => searchInputRef.current?.focus(),
 *   onToggleFilters: () => setShowFilters(prev => !prev),
 *   onEscape: () => closeAllModals()
 * });
 */
export function useKeyboardShortcuts(
  handlers: KeyboardShortcutHandlers,
  enabled: boolean = true
) {
  useEffect(() => {
    if (!enabled) return;

    const handleKeyDown = (event: KeyboardEvent) => {
      // Don't trigger shortcuts when user is typing in an input/textarea
      const target = event.target as HTMLElement;
      const isInputField =
        target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.isContentEditable;

      // Exception: Allow '/' to focus search even when not in input
      // Exception: Allow Escape to work everywhere
      const isSlashKey = event.key === "/";
      const isEscapeKey = event.key === "Escape";

      if (isInputField && !isSlashKey && !isEscapeKey) {
        return;
      }

      // N: New task
      if (event.key === "n" || event.key === "N") {
        if (!isInputField) {
          event.preventDefault();
          handlers.onNewTask?.();
        }
      }

      // /: Focus search
      if (event.key === "/") {
        event.preventDefault();
        handlers.onFocusSearch?.();
      }

      // F: Toggle filters
      if (event.key === "f" || event.key === "F") {
        if (!isInputField) {
          event.preventDefault();
          handlers.onToggleFilters?.();
        }
      }

      // Escape: Close modals/dropdowns
      if (event.key === "Escape") {
        event.preventDefault();
        handlers.onEscape?.();
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [handlers, enabled]);
}

/**
 * Format keyboard shortcut for display.
 *
 * @param key - The keyboard key
 * @returns Formatted string for display
 *
 * @example
 * formatShortcut("N") // Returns: "N"
 * formatShortcut("/") // Returns: "/"
 */
export function formatShortcut(key: string): string {
  return key.toUpperCase();
}

/**
 * Get keyboard shortcut hints for UI display.
 *
 * @returns Array of shortcut hints with key and description
 */
export function getKeyboardShortcuts() {
  return [
    { key: "N", description: "New task" },
    { key: "/", description: "Focus search" },
    { key: "F", description: "Toggle filters" },
    { key: "Esc", description: "Close modals" },
  ];
}
