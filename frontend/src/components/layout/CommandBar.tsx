"use client";

/**
 * Command Bar Component
 *
 * Top bar with search, filter, and sort controls.
 * Features:
 * - Live search input
 * - Priority filter (multi-select)
 * - Status filter (all/pending/completed)
 * - Sort selector (created_at/due_date/priority/updated_at)
 * - Responsive design
 */

import { Search, Filter, ArrowUpDown, X } from "lucide-react";
import { useState, useEffect, useRef, forwardRef, useImperativeHandle } from "react";
import { useFilters } from "@/contexts/FilterContext";
import { useDebounce } from "@/hooks/useDebounce";

export interface CommandBarRef {
  focusSearch: () => void;
  toggleFilters: () => void;
  toggleSort: () => void;
}

export const CommandBar = forwardRef<CommandBarRef, {}>((props, ref) => {
  const searchInputRef = useRef<HTMLInputElement>(null);
  const {
    filters,
    setSearch,
    setPriority,
    setStatus,
    setDueDate,
    setSortBy,
    setOrder,
    resetFilters,
  } = useFilters();

  const [showFilters, setShowFilters] = useState(false);
  const [showSort, setShowSort] = useState(false);

  // Local state for search input (for immediate UI feedback)
  const [localSearch, setLocalSearch] = useState(filters.search);

  // Debounced search value (reduces API calls)
  const debouncedSearch = useDebounce(localSearch, 300);

  // Local state for priority checkboxes
  const [selectedPriorities, setSelectedPriorities] = useState<("high" | "medium" | "low")[]>([]);

  // Update global search when debounced value changes
  useEffect(() => {
    setSearch(debouncedSearch);
  }, [debouncedSearch, setSearch]);

  // Update local search when external filters change
  useEffect(() => {
    setLocalSearch(filters.search);
  }, [filters.search]);

  const handleSearchChange = (value: string) => {
    setLocalSearch(value);
  };

  const handlePriorityToggle = (priority: "high" | "medium" | "low") => {
    const newPriorities = selectedPriorities.includes(priority)
      ? selectedPriorities.filter((p) => p !== priority)
      : [...selectedPriorities, priority];

    setSelectedPriorities(newPriorities);
    setPriority(newPriorities.length > 0 ? newPriorities : null);
  };

  const handleStatusChange = (status: "all" | "pending" | "completed") => {
    setStatus(status);
  };

  const handleDueDateChange = (dueDate: "all" | "today" | "tomorrow" | "this_week" | "overdue") => {
    setDueDate(dueDate);
  };

  const handleSortChange = (sortBy: "created_at" | "due_date" | "priority" | "updated_at") => {
    setSortBy(sortBy);
  };

  const handleOrderToggle = () => {
    setOrder(filters.order === "asc" ? "desc" : "asc");
  };

  const handleResetFilters = () => {
    setSelectedPriorities([]);
    resetFilters();
  };

  // Expose methods via ref for keyboard shortcuts
  useImperativeHandle(ref, () => ({
    focusSearch: () => {
      searchInputRef.current?.focus();
    },
    toggleFilters: () => {
      setShowFilters((prev) => !prev);
    },
    toggleSort: () => {
      setShowSort((prev) => !prev);
    },
  }));

  return (
    <div className="bg-white border-b border-seal-brown/10 px-6 py-4 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center gap-4">
        {/* Search Input */}
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-seal-brown/40" />
          <input
            ref={searchInputRef}
            type="text"
            value={localSearch}
            onChange={(e) => handleSearchChange(e.target.value)}
            placeholder="Search tasks... (Press / to focus)"
            className="
              w-full pl-10 pr-4 py-2.5
              bg-rose-white border border-seal-brown/20 rounded-lg
              text-seal-brown placeholder:text-seal-brown/40
              focus:outline-none focus:ring-2 focus:ring-seal-brown/30 focus:border-seal-brown
              transition-all duration-200
            "
            aria-label="Search tasks"
          />
        </div>

        {/* Filter Button */}
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="
            px-4 py-2.5 rounded-lg
            bg-rose-white border border-seal-brown/20
            text-seal-brown hover:bg-seal-brown/5
            transition-all duration-200
            flex items-center gap-2
          "
          aria-label="Filter tasks"
        >
          <Filter className="w-5 h-5" />
          <span className="hidden sm:inline">Filter</span>
        </button>

        {/* Sort Button */}
        <button
          onClick={() => setShowSort(!showSort)}
          className="
            px-4 py-2.5 rounded-lg
            bg-rose-white border border-seal-brown/20
            text-seal-brown hover:bg-seal-brown/5
            transition-all duration-200
            flex items-center gap-2
          "
          aria-label="Sort tasks"
        >
          <ArrowUpDown className="w-5 h-5" />
          <span className="hidden sm:inline">Sort</span>
        </button>
      </div>

      {/* Filter Dropdown */}
      {showFilters && (
        <div className="mt-4 p-6 pl-[20px] bg-rose-white rounded-lg border border-seal-brown/20 shadow-sm animate-fade-in">
          <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Priority Filter */}
            <div>
              <h3 className="text-sm font-semibold text-seal-brown mb-3">Priority</h3>
              <div className="space-y-2">
                {(["high", "medium", "low"] as const).map((priority) => (
                  <label key={priority} className="flex items-center gap-2 cursor-pointer group">
                    <input
                      type="checkbox"
                      checked={selectedPriorities.includes(priority)}
                      onChange={() => handlePriorityToggle(priority)}
                      className="w-4 h-4 rounded border-seal-brown/30 text-seal-brown focus:ring-seal-brown/30"
                    />
                    <span className="text-sm text-seal-brown capitalize group-hover:text-seal-brown/80">
                      {priority}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            {/* Status Filter */}
            <div>
              <h3 className="text-sm font-semibold text-seal-brown mb-3">Status</h3>
              <div className="space-y-2">
                {(["all", "pending", "completed"] as const).map((status) => (
                  <label key={status} className="flex items-center gap-2 cursor-pointer group">
                    <input
                      type="radio"
                      name="status"
                      checked={filters.status === status}
                      onChange={() => handleStatusChange(status)}
                      className="w-4 h-4 border-seal-brown/30 text-seal-brown focus:ring-seal-brown/30"
                    />
                    <span className="text-sm text-seal-brown capitalize group-hover:text-seal-brown/80">
                      {status}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            {/* Due Date Filter */}
            <div>
              <h3 className="text-sm font-semibold text-seal-brown mb-3">Due Date</h3>
              <div className="space-y-2">
                {([
                  { value: "all", label: "All" },
                  { value: "today", label: "Today" },
                  { value: "tomorrow", label: "Tomorrow" },
                  { value: "this_week", label: "This Week" },
                  { value: "overdue", label: "Overdue" },
                ] as const).map((option) => (
                  <label key={option.value} className="flex items-center gap-2 cursor-pointer group">
                    <input
                      type="radio"
                      name="dueDate"
                      checked={filters.dueDate === option.value}
                      onChange={() => handleDueDateChange(option.value)}
                      className="w-4 h-4 border-seal-brown/30 text-seal-brown focus:ring-seal-brown/30"
                    />
                    <span className="text-sm text-seal-brown group-hover:text-seal-brown/80">
                      {option.label}
                    </span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          {/* Reset Button */}
          <div className="mt-4 pt-4 border-t border-seal-brown/10">
            <button
              onClick={handleResetFilters}
              className="text-sm text-seal-brown/60 hover:text-seal-brown flex items-center gap-1"
            >
              <X className="w-4 h-4" />
              Reset Filters
            </button>
          </div>
        </div>
      )}

      {/* Sort Dropdown */}
      {showSort && (
        <div className="mt-4 p-6 bg-rose-white rounded-lg border border-seal-brown/20 shadow-sm animate-fade-in">
          <div className="max-w-7xl mx-auto">
            <h3 className="text-sm font-semibold text-seal-brown mb-3">Sort By</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Sort Field */}
              <div className="space-y-2">
                {([
                  { value: "created_at", label: "Date Created" },
                  { value: "due_date", label: "Due Date" },
                  { value: "priority", label: "Priority" },
                  { value: "updated_at", label: "Last Updated" },
                ] as const).map((option) => (
                  <label key={option.value} className="flex items-center gap-2 cursor-pointer group">
                    <input
                      type="radio"
                      name="sortBy"
                      checked={filters.sortBy === option.value}
                      onChange={() => handleSortChange(option.value)}
                      className="w-4 h-4 border-seal-brown/30 text-seal-brown focus:ring-seal-brown/30"
                    />
                    <span className="text-sm text-seal-brown group-hover:text-seal-brown/80">
                      {option.label}
                    </span>
                  </label>
                ))}
              </div>

              {/* Sort Order */}
              <div className="space-y-2">
                <label className="flex items-center gap-2 cursor-pointer group">
                  <input
                    type="radio"
                    name="order"
                    checked={filters.order === "asc"}
                    onChange={() => setOrder("asc")}
                    className="w-4 h-4 border-seal-brown/30 text-seal-brown focus:ring-seal-brown/30"
                  />
                  <span className="text-sm text-seal-brown group-hover:text-seal-brown/80">
                    Ascending (A→Z, Old→New)
                  </span>
                </label>
                <label className="flex items-center gap-2 cursor-pointer group">
                  <input
                    type="radio"
                    name="order"
                    checked={filters.order === "desc"}
                    onChange={() => setOrder("desc")}
                    className="w-4 h-4 border-seal-brown/30 text-seal-brown focus:ring-seal-brown/30"
                  />
                  <span className="text-sm text-seal-brown group-hover:text-seal-brown/80">
                    Descending (Z→A, New→Old)
                  </span>
                </label>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
});

CommandBar.displayName = "CommandBar";
