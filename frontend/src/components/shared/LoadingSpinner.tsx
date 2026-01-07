/**
 * Loading spinner component.
 *
 * Displays a rotating spinner icon for loading states.
 * Uses lucide-react Loader2 icon with Tailwind animate-spin.
 * Includes proper ARIA attributes for accessibility.
 */
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface LoadingSpinnerProps {
  className?: string;
  size?: number;
  label?: string;
}

export function LoadingSpinner({ className, size = 24, label = "Loading" }: LoadingSpinnerProps) {
  return (
    <Loader2
      className={cn("animate-spin text-gray-600", className)}
      size={size}
      role="status"
      aria-label={label}
      aria-live="polite"
    />
  );
}
