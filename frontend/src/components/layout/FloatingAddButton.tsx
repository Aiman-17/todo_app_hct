"use client";

/**
 * Floating Add Button (FAB) Component
 *
 * Floating action button for quick task creation.
 * Features:
 * - Fixed position at bottom-right
 * - Pulse animation to draw attention
 * - Smooth hover effects
 * - Opens task creation modal
 * - Accessible with keyboard navigation
 */

import { Plus } from "lucide-react";
import { useState } from "react";

interface FloatingAddButtonProps {
  onClick?: () => void;
}

export function FloatingAddButton({ onClick }: FloatingAddButtonProps) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className={`
        fixed bottom-8 right-8 z-30
        min-w-[56px] min-h-[56px] rounded-full
        bg-seal-brown text-rose-white
        shadow-lg hover:shadow-xl
        flex items-center justify-center
        transition-all duration-200 ease-in-out
        hover:scale-110
        focus:outline-none focus:ring-4 focus:ring-seal-brown/30
        ${!isHovered ? "animate-pulse-gentle" : ""}
      `}
      aria-label="Add new task"
    >
      <Plus className="w-6 h-6" aria-hidden="true" />

      {/* Tooltip */}
      {isHovered && (
        <div className="absolute bottom-full mb-2 right-0 pointer-events-none">
          <div className="bg-seal-brown text-rose-white px-3 py-2 rounded-lg shadow-lg text-sm whitespace-nowrap animate-fade-in">
            Add Task
            {/* Tooltip arrow */}
            <div className="absolute top-full right-6 -translate-x-1/2 border-8 border-transparent border-t-seal-brown" />
          </div>
        </div>
      )}
    </button>
  );
}
