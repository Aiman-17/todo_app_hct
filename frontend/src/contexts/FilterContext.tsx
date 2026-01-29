"use client";

/**
 * Filter Context
 *
 * Global state management for task filtering and sorting with localStorage persistence.
 * Provides filter/sort state and actions to all components.
 * Automatically saves and restores filter preferences across sessions.
 */

import React, { createContext, useContext, useState, useEffect, useCallback, ReactNode } from "react";

export interface FilterState {
  search: string;
  priority: ("high" | "medium" | "low")[] | null;
  status: "all" | "pending" | "completed";
  dueDate: "all" | "today" | "tomorrow" | "this_week" | "overdue";
  viewMode: "grid" | "list";
  sortBy: "created_at" | "due_date" | "priority" | "updated_at";
  order: "asc" | "desc";
}

interface FilterContextType {
  filters: FilterState;
  setSearch: (search: string) => void;
  setPriority: (priority: ("high" | "medium" | "low")[] | null) => void;
  setStatus: (status: "all" | "pending" | "completed") => void;
  setDueDate: (dueDate: "all" | "today" | "tomorrow" | "this_week" | "overdue") => void;
  setViewMode: (viewMode: "grid" | "list") => void;
  setSortBy: (sortBy: "created_at" | "due_date" | "priority" | "updated_at") => void;
  setOrder: (order: "asc" | "desc") => void;
  resetFilters: () => void;
}

const FilterContext = createContext<FilterContextType | undefined>(undefined);

const STORAGE_KEY = "todo_app_filter_preferences";

const DEFAULT_FILTERS: FilterState = {
  search: "",
  priority: null,
  status: "all",
  dueDate: "all",
  viewMode: "grid",
  sortBy: "created_at",
  order: "desc",
};

/**
 * Load saved filter preferences from localStorage.
 * Returns DEFAULT_FILTERS if no saved preferences or on error.
 * Safe for SSR - only accesses localStorage on client side.
 */
function loadFiltersFromStorage(): FilterState {
  // Check if we're on the client side
  if (typeof window === "undefined") {
    return DEFAULT_FILTERS;
  }

  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      // Validate the loaded data has correct structure
      return {
        search: typeof parsed.search === "string" ? parsed.search : DEFAULT_FILTERS.search,
        priority: Array.isArray(parsed.priority) ? parsed.priority : DEFAULT_FILTERS.priority,
        status: parsed.status || DEFAULT_FILTERS.status,
        dueDate: parsed.dueDate || DEFAULT_FILTERS.dueDate,
        viewMode: parsed.viewMode || DEFAULT_FILTERS.viewMode,
        sortBy: parsed.sortBy || DEFAULT_FILTERS.sortBy,
        order: parsed.order || DEFAULT_FILTERS.order,
      };
    }
  } catch (error) {
    console.error("Failed to load filter preferences from localStorage:", error);
  }
  return DEFAULT_FILTERS;
}

/**
 * Save filter preferences to localStorage.
 * Handles errors gracefully (quota exceeded, disabled storage, etc.)
 * Safe for SSR - only accesses localStorage on client side.
 */
function saveFiltersToStorage(filters: FilterState): void {
  // Check if we're on the client side
  if (typeof window === "undefined") {
    return;
  }

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(filters));
  } catch (error) {
    console.error("Failed to save filter preferences to localStorage:", error);
  }
}

export function FilterProvider({ children }: { children: ReactNode }) {
  // Initialize with saved preferences or defaults
  const [filters, setFilters] = useState<FilterState>(loadFiltersFromStorage);
  const [isInitialized, setIsInitialized] = useState(false);

  // Load preferences on mount (client-side only)
  useEffect(() => {
    setFilters(loadFiltersFromStorage());
    setIsInitialized(true);
  }, []);

  // Save to localStorage whenever filters change (after initial load)
  useEffect(() => {
    if (isInitialized) {
      saveFiltersToStorage(filters);
    }
  }, [filters, isInitialized]);

  const setSearch = useCallback((search: string) => {
    setFilters((prev) => ({ ...prev, search }));
  }, []);

  const setPriority = useCallback((priority: ("high" | "medium" | "low")[] | null) => {
    setFilters((prev) => ({ ...prev, priority }));
  }, []);

  const setStatus = useCallback((status: "all" | "pending" | "completed") => {
    setFilters((prev) => ({ ...prev, status }));
  }, []);

  const setDueDate = useCallback((dueDate: "all" | "today" | "tomorrow" | "this_week" | "overdue") => {
    setFilters((prev) => ({ ...prev, dueDate }));
  }, []);

  const setViewMode = useCallback((viewMode: "grid" | "list") => {
    setFilters((prev) => ({ ...prev, viewMode }));
  }, []);

  const setSortBy = useCallback((sortBy: "created_at" | "due_date" | "priority" | "updated_at") => {
    setFilters((prev) => ({ ...prev, sortBy }));
  }, []);

  const setOrder = useCallback((order: "asc" | "desc") => {
    setFilters((prev) => ({ ...prev, order }));
  }, []);

  const resetFilters = useCallback(() => {
    setFilters(DEFAULT_FILTERS);
    // Clear from localStorage (client-side only)
    if (typeof window !== "undefined") {
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch (error) {
        console.error("Failed to clear filter preferences from localStorage:", error);
      }
    }
  }, []);

  return (
    <FilterContext.Provider
      value={{
        filters,
        setSearch,
        setPriority,
        setStatus,
        setDueDate,
        setViewMode,
        setSortBy,
        setOrder,
        resetFilters,
      }}
    >
      {children}
    </FilterContext.Provider>
  );
}

export function useFilters() {
  const context = useContext(FilterContext);
  if (context === undefined) {
    throw new Error("useFilters must be used within a FilterProvider");
  }
  return context;
}
