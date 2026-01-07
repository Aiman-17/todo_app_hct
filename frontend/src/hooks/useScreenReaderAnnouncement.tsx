/**
 * Screen reader announcement hook for accessibility.
 *
 * Provides a way to announce dynamic content changes to screen readers
 * using ARIA live regions.
 */

import { useEffect, useRef, useState } from "react";

/**
 * Hook to announce messages to screen readers.
 *
 * Creates an invisible ARIA live region that announces messages.
 *
 * @returns announce function to trigger announcements
 *
 * @example
 * const announce = useScreenReaderAnnouncement();
 * announce("Task created successfully");
 * announce("Task deleted");
 */
export function useScreenReaderAnnouncement() {
  const [message, setMessage] = useState("");
  const timeoutRef = useRef<NodeJS.Timeout>();

  // Clear message after announcement
  useEffect(() => {
    if (message) {
      // Clear after 1 second to allow for re-announcement of same message
      timeoutRef.current = setTimeout(() => {
        setMessage("");
      }, 1000);
    }

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [message]);

  const announce = (text: string) => {
    setMessage(text);
  };

  return { announce, message };
}

/**
 * ScreenReaderAnnouncer component for the live region.
 *
 * Should be placed once in the app root or layout.
 *
 * @param message - The message to announce
 *
 * @example
 * <ScreenReaderAnnouncer message={message} />
 */
export function ScreenReaderAnnouncer({ message }: { message: string }) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {message}
    </div>
  );
}
