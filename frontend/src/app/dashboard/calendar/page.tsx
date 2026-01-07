/**
 * Calendar Page
 *
 * Calendar view of tasks organized by due dates.
 * Features:
 * - Monthly calendar view
 * - Tasks displayed on their due dates
 * - Navigate between months
 * - Click dates to see tasks
 */
"use client";

import { useState, useEffect } from "react";
import { Calendar as CalendarIcon, ChevronLeft, ChevronRight } from "lucide-react";
import { apiRequest } from "@/lib/api";
import type { Task } from "@/types/task";

export default function CalendarPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Fetch all tasks
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await apiRequest<Task[]>("/api/tasks");
        setTasks(data);
      } catch (error) {
        console.error("Failed to load tasks:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTasks();
  }, []);

  // Get tasks for a specific date
  const getTasksForDate = (date: Date) => {
    return tasks.filter((task) => {
      if (!task.due_date) return false;
      const taskDate = new Date(task.due_date);
      return (
        taskDate.getDate() === date.getDate() &&
        taskDate.getMonth() === date.getMonth() &&
        taskDate.getFullYear() === date.getFullYear()
      );
    });
  };

  // Generate calendar days
  const getDaysInMonth = (date: Date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    const days: (Date | null)[] = [];

    // Add empty cells for days before month starts
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(null);
    }

    // Add all days in month
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(new Date(year, month, day));
    }

    return days;
  };

  const days = getDaysInMonth(currentDate);
  const monthName = currentDate.toLocaleString("default", { month: "long", year: "numeric" });

  const goToPreviousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1));
  };

  const goToNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1));
  };

  const goToToday = () => {
    setCurrentDate(new Date());
  };

  const isToday = (date: Date | null) => {
    if (!date) return false;
    const today = new Date();
    return (
      date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear()
    );
  };

  const isSelected = (date: Date | null) => {
    if (!date || !selectedDate) return false;
    return (
      date.getDate() === selectedDate.getDate() &&
      date.getMonth() === selectedDate.getMonth() &&
      date.getFullYear() === selectedDate.getFullYear()
    );
  };

  const selectedDateTasks = selectedDate ? getTasksForDate(selectedDate) : [];

  return (
    <div className="max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <CalendarIcon className="w-8 h-8 text-seal-brown" aria-hidden="true" />
          <h1 className="text-3xl font-bold text-seal-brown">Calendar</h1>
        </div>
        <p className="text-seal-brown/60">View your tasks by due date</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendar View */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-3xl p-6 shadow-lg">
            {/* Calendar Header */}
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-seal-brown">{monthName}</h2>
              <div className="flex items-center gap-2">
                <button
                  onClick={goToToday}
                  className="px-4 py-2 text-sm font-medium text-seal-brown hover:bg-seal-brown/5 rounded-lg transition-colors"
                >
                  Today
                </button>
                <button
                  onClick={goToPreviousMonth}
                  className="p-2 hover:bg-seal-brown/5 rounded-lg transition-colors"
                  aria-label="Previous month"
                >
                  <ChevronLeft className="w-5 h-5 text-seal-brown" />
                </button>
                <button
                  onClick={goToNextMonth}
                  className="p-2 hover:bg-seal-brown/5 rounded-lg transition-colors"
                  aria-label="Next month"
                >
                  <ChevronRight className="w-5 h-5 text-seal-brown" />
                </button>
              </div>
            </div>

            {/* Weekday Headers */}
            <div className="grid grid-cols-7 gap-2 mb-2">
              {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((day) => (
                <div key={day} className="text-center text-sm font-semibold text-seal-brown/60 py-2">
                  {day}
                </div>
              ))}
            </div>

            {/* Calendar Grid */}
            <div className="grid grid-cols-7 gap-2">
              {days.map((date, index) => {
                if (!date) {
                  return <div key={`empty-${index}`} className="aspect-square" />;
                }

                const dayTasks = getTasksForDate(date);
                const hasTask = dayTasks.length > 0;
                const today = isToday(date);
                const selected = isSelected(date);

                return (
                  <button
                    key={index}
                    onClick={() => setSelectedDate(date)}
                    className={`
                      aspect-square p-2 rounded-lg transition-all duration-200
                      flex flex-col items-center justify-center
                      ${today ? "bg-seal-brown text-rose-white font-bold" : ""}
                      ${selected && !today ? "bg-seal-brown/10 ring-2 ring-seal-brown" : ""}
                      ${!today && !selected ? "hover:bg-seal-brown/5" : ""}
                    `}
                  >
                    <span className="text-sm">{date.getDate()}</span>
                    {hasTask && (
                      <div className="mt-1 flex gap-0.5">
                        {dayTasks.slice(0, 3).map((task, i) => (
                          <div
                            key={i}
                            className={`w-1.5 h-1.5 rounded-full ${
                              task.priority === "high"
                                ? "bg-red-500"
                                : task.priority === "medium"
                                ? "bg-yellow-500"
                                : "bg-blue-500"
                            }`}
                          />
                        ))}
                      </div>
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Selected Date Tasks */}
        <div className="space-y-4">
          <div className="bg-white rounded-3xl p-6 shadow-lg">
            <h3 className="text-xl font-bold text-seal-brown mb-4">
              {selectedDate
                ? selectedDate.toLocaleDateString("default", {
                    weekday: "long",
                    month: "long",
                    day: "numeric",
                  })
                : "Select a date"}
            </h3>

            {selectedDate && (
              <div className="space-y-3">
                {selectedDateTasks.length === 0 ? (
                  <p className="text-seal-brown/60 text-sm">No tasks for this date</p>
                ) : (
                  selectedDateTasks.map((task) => (
                    <div
                      key={task.id}
                      className={`
                        p-4 rounded-lg border-l-4
                        ${
                          task.priority === "high"
                            ? "border-red-500 bg-red-50"
                            : task.priority === "medium"
                            ? "border-yellow-500 bg-yellow-50"
                            : "border-blue-500 bg-blue-50"
                        }
                      `}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1">
                          <h4
                            className={`font-semibold text-seal-brown ${
                              task.completed ? "line-through opacity-50" : ""
                            }`}
                          >
                            {task.title}
                          </h4>
                          {task.description && (
                            <p className="text-sm text-seal-brown/60 mt-1">{task.description}</p>
                          )}
                        </div>
                        <span
                          className={`
                            text-xs font-medium px-2 py-1 rounded-full
                            ${
                              task.priority === "high"
                                ? "bg-red-100 text-red-700"
                                : task.priority === "medium"
                                ? "bg-yellow-100 text-yellow-700"
                                : "bg-blue-100 text-blue-700"
                            }
                          `}
                        >
                          {task.priority}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>

          {/* Tasks Summary */}
          <div className="bg-white rounded-3xl p-6 shadow-lg">
            <h3 className="text-lg font-bold text-seal-brown mb-4">This Month</h3>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm text-seal-brown/60">Total Tasks</span>
                <span className="font-semibold text-seal-brown">
                  {tasks.filter((t) => t.due_date && new Date(t.due_date).getMonth() === currentDate.getMonth()).length}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-seal-brown/60">Completed</span>
                <span className="font-semibold text-green-600">
                  {
                    tasks.filter(
                      (t) =>
                        t.completed &&
                        t.due_date &&
                        new Date(t.due_date).getMonth() === currentDate.getMonth()
                    ).length
                  }
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-seal-brown/60">Pending</span>
                <span className="font-semibold text-orange-600">
                  {
                    tasks.filter(
                      (t) =>
                        !t.completed &&
                        t.due_date &&
                        new Date(t.due_date).getMonth() === currentDate.getMonth()
                    ).length
                  }
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
