"use client";

/**
 * Completion Circle Component
 *
 * Circular progress indicator for task completion analytics.
 * Features:
 * - Animated circular progress bar
 * - Percentage display in center
 * - Color-coded progress (green for high completion)
 * - Smooth animations
 */

import { useEffect, useState } from "react";

interface CompletionCircleProps {
  completed: number;
  total: number;
  size?: number;
  strokeWidth?: number;
}

export function CompletionCircle({
  completed,
  total,
  size = 120,
  strokeWidth = 8,
}: CompletionCircleProps) {
  const [progress, setProgress] = useState(0);
  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

  // Calculate circle properties
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (progress / 100) * circumference;

  // Determine color based on completion percentage
  const getColor = () => {
    if (percentage >= 80) return "#66BB6A"; // Green
    if (percentage >= 50) return "#FFA726"; // Orange
    if (percentage >= 25) return "#FFB8D2"; // Pink
    return "#A8D8FF"; // Blue
  };

  // Animate progress on mount and when percentage changes
  useEffect(() => {
    const timer = setTimeout(() => {
      setProgress(percentage);
    }, 100);
    return () => clearTimeout(timer);
  }, [percentage]);

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg
        width={size}
        height={size}
        className="transform -rotate-90"
      >
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#E0E0E0"
          strokeWidth={strokeWidth}
          fill="transparent"
        />

        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={getColor()}
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
      </svg>

      {/* Center text */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-bold text-seal-brown">
          {percentage}%
        </span>
        <span className="text-xs text-seal-brown/60 mt-1">
          {completed}/{total} tasks
        </span>
      </div>
    </div>
  );
}
