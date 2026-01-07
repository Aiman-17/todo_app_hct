"use client";

/**
 * User Preferences Context
 *
 * Global state management for user preferences including notifications,
 * theme, and other app settings. Provides persistence via localStorage.
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import {
  loadNotificationPreferences,
  saveNotificationPreferences,
  type NotificationPreferences
} from "@/lib/notifications";

export interface UserPreferences {
  notifications: NotificationPreferences;
  // Future preferences can be added here:
  // theme: "light" | "dark" | "auto";
  // language: string;
  // viewMode: "grid" | "list";
}

interface PreferencesContextType {
  preferences: UserPreferences;
  setNotificationPreferences: (prefs: NotificationPreferences) => void;
  // Future setters:
  // setTheme: (theme: "light" | "dark" | "auto") => void;
  // setLanguage: (language: string) => void;
}

const PreferencesContext = createContext<PreferencesContextType | undefined>(undefined);

const DEFAULT_PREFERENCES: UserPreferences = {
  notifications: {
    enabled: false,
    reminderMinutes: 60
  }
};

/**
 * Load user preferences from localStorage.
 * Returns DEFAULT_PREFERENCES if no saved preferences or on error.
 * Safe for SSR - only accesses localStorage on client side.
 */
function loadPreferencesFromStorage(): UserPreferences {
  if (typeof window === "undefined") {
    return DEFAULT_PREFERENCES;
  }

  try {
    // Load notification preferences
    const notifications = loadNotificationPreferences();

    return {
      notifications,
      // Load other preferences here in the future
    };
  } catch (error) {
    console.error("Failed to load user preferences from localStorage:", error);
    return DEFAULT_PREFERENCES;
  }
}

export function PreferencesProvider({ children }: { children: ReactNode }) {
  const [preferences, setPreferences] = useState<UserPreferences>(loadPreferencesFromStorage);
  const [isInitialized, setIsInitialized] = useState(false);

  // Load preferences on mount (client-side only)
  useEffect(() => {
    setPreferences(loadPreferencesFromStorage());
    setIsInitialized(true);
  }, []);

  // Save notification preferences when they change
  useEffect(() => {
    if (isInitialized) {
      saveNotificationPreferences(preferences.notifications);
    }
  }, [preferences.notifications, isInitialized]);

  const setNotificationPreferences = (prefs: NotificationPreferences) => {
    setPreferences((prev) => ({ ...prev, notifications: prefs }));
  };

  return (
    <PreferencesContext.Provider
      value={{
        preferences,
        setNotificationPreferences,
      }}
    >
      {children}
    </PreferencesContext.Provider>
  );
}

export function usePreferences() {
  const context = useContext(PreferencesContext);
  if (context === undefined) {
    throw new Error("usePreferences must be used within a PreferencesProvider");
  }
  return context;
}
