/**
 * Dashboard Layout Component
 *
 * Protected layout for dashboard pages with premium minimalist design.
 * Features:
 * - Seal brown navbar at the top
 * - Icon-only sidebar navigation
 * - Command bar for search/filter/sort
 * - Floating action button for quick task creation
 * - Responsive layout with proper spacing
 */
"use client";

import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";
import { CommandBar, CommandBarRef } from "@/components/layout/CommandBar";
import { FloatingAddButton } from "@/components/layout/FloatingAddButton";
import { TaskForm } from "@/components/tasks/TaskForm";
import { FilterProvider } from "@/contexts/FilterContext";
import { PreferencesProvider } from "@/contexts/PreferencesContext";
import { useKeyboardShortcuts } from "@/hooks/useKeyboardShortcuts";
import { useState, useRef } from "react";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [showTaskForm, setShowTaskForm] = useState(false);
  const commandBarRef = useRef<CommandBarRef>(null);

  // Keyboard shortcuts
  useKeyboardShortcuts({
    onNewTask: () => setShowTaskForm(true),
    onFocusSearch: () => commandBarRef.current?.focusSearch(),
    onToggleFilters: () => commandBarRef.current?.toggleFilters(),
    onEscape: () => {
      // Close task form if open
      if (showTaskForm) {
        setShowTaskForm(false);
      }
    },
  });

  return (
    <PreferencesProvider>
      <FilterProvider>
        <div className="min-h-screen bg-rose-white">
          {/* Seal Brown Navbar at Top */}
          <Navbar />

          {/* Icon-only Sidebar (64px width) */}
          <Sidebar />

          {/* Main Content Area (with left margin for sidebar, top margin for navbar) */}
          <div className="ml-0 lg:ml-16 pt-0">
            {/* Command Bar */}
            <CommandBar ref={commandBarRef} />

            {/* Page Content */}
            <main className="p-6">{children}</main>
          </div>

          {/* Floating Add Button */}
          <FloatingAddButton onClick={() => setShowTaskForm(true)} />

          {/* Task Form Modal */}
          {showTaskForm && (
            <TaskForm
              open={showTaskForm}
              onOpenChange={setShowTaskForm}
            />
          )}
        </div>
      </FilterProvider>
    </PreferencesProvider>
  );
}
