/**
 * Dashboard page component (protected route).
 *
 * Displays the user's task list with premium minimalist design.
 * Requires authentication (middleware redirects if not logged in).
 * Layout provides Sidebar, CommandBar, and FloatingAddButton.
 *
 * Features:
 * - Task list with colorful cards
 * - Completion analytics (circular progress)
 * - Pomodoro timer for focus sessions
 */
"use client";

import { useState, useEffect } from "react";
import { TaskList } from "@/components/tasks/TaskList";
import { CompletionCircle } from "@/components/analytics/CompletionCircle";
import { PomodoroTimer } from "@/components/timer/PomodoroTimer";
import { useFilters } from "@/contexts/FilterContext";
import { apiRequest } from "@/lib/api";
import type { Task } from "@/types/task";

export default function DashboardPage() {
  const { filters, setStatus } = useFilters();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoadingStats, setIsLoadingStats] = useState(true);

  // Fetch tasks for analytics
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await apiRequest<Task[]>("/api/tasks");
        setTasks(data);
      } catch (error) {
        console.error("Failed to load tasks for analytics:", error);
      } finally {
        setIsLoadingStats(false);
      }
    };

    fetchTasks();

    // Listen for task updates to refresh analytics
    const handleTaskUpdated = () => fetchTasks();
    window.addEventListener("taskCreated", handleTaskUpdated);
    window.addEventListener("taskUpdated", handleTaskUpdated);

    return () => {
      window.removeEventListener("taskCreated", handleTaskUpdated);
      window.removeEventListener("taskUpdated", handleTaskUpdated);
    };
  }, []);

  const completedCount = tasks.filter((t) => t.completed).length;
  const totalCount = tasks.length;

  return (
    <div className="max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-seal-brown">My Tasks</h1>
        <p className="text-seal-brown/60 mt-1">
          Manage and organize your tasks
        </p>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Task List - Takes 2 columns on large screens */}
        <div className="lg:col-span-2">
          {/* Filter Tabs */}
          <div className="mb-6 bg-white rounded-2xl p-2 shadow-md flex gap-2">
            <button
              onClick={() => setStatus("all")}
              className={`
                flex-1 px-6 py-3 rounded-xl font-semibold transition-all duration-200
                ${
                  filters.status === "all"
                    ? "bg-seal-brown text-rose-white shadow-lg"
                    : "text-seal-brown hover:bg-seal-brown/5"
                }
              `}
            >
              All Tasks
              <span className="ml-2 text-sm">({tasks.length})</span>
            </button>
            <button
              onClick={() => setStatus("pending")}
              className={`
                flex-1 px-6 py-3 rounded-xl font-semibold transition-all duration-200
                ${
                  filters.status === "pending"
                    ? "bg-seal-brown text-rose-white shadow-lg"
                    : "text-seal-brown hover:bg-seal-brown/5"
                }
              `}
            >
              Pending
              <span className="ml-2 text-sm">({tasks.filter(t => !t.completed).length})</span>
            </button>
            <button
              onClick={() => setStatus("completed")}
              className={`
                flex-1 px-6 py-3 rounded-xl font-semibold transition-all duration-200
                ${
                  filters.status === "completed"
                    ? "bg-seal-brown text-rose-white shadow-lg"
                    : "text-seal-brown hover:bg-seal-brown/5"
                }
              `}
            >
              Completed
              <span className="ml-2 text-sm">({tasks.filter(t => t.completed).length})</span>
            </button>
          </div>

          <section aria-labelledby="tasks-heading">
            <h2 id="tasks-heading" className="sr-only">Your Tasks</h2>
            <TaskList />
          </section>
        </div>

        {/* Right Sidebar - Analytics & Timer */}
        <div className="space-y-6">
          {/* Completion Analytics */}
          <div className="bg-white rounded-3xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-seal-brown mb-4 text-center">
              Progress
            </h3>
            <div className="flex justify-center">
              {!isLoadingStats && (
                <CompletionCircle
                  completed={completedCount}
                  total={totalCount}
                  size={160}
                  strokeWidth={12}
                />
              )}
            </div>
            <div className="mt-4 text-center">
              <p className="text-sm text-seal-brown/60">
                Keep up the great work!
              </p>
            </div>
          </div>

          {/* Pomodoro Timer */}
          <PomodoroTimer
            onComplete={() => {
              // Optional: Show notification or toast on timer completion
              console.log("Focus session completed!");
            }}
          />
        </div>
      </div>
    </div>
  );
}
