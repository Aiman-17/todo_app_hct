"use client";

/**
 * Notifications Settings Component
 *
 * Allows users to enable/disable browser notifications and configure
 * reminder timing for task due dates.
 *
 * Features:
 * - Enable/disable notifications toggle
 * - Reminder time selector (15min, 30min, 1hr, 2hr, 1day)
 * - Permission request button
 * - Permission status indicator
 */

import { useState, useEffect } from "react";
import { Bell, BellOff, Check, X, AlertCircle } from "lucide-react";
import {
  isNotificationSupported,
  getNotificationPermission,
  requestNotificationPermission,
  type NotificationPermissionStatus
} from "@/lib/notifications";
import { usePreferences } from "@/contexts/PreferencesContext";

const REMINDER_OPTIONS = [
  { label: "15 minutes before", value: 15 },
  { label: "30 minutes before", value: 30 },
  { label: "1 hour before", value: 60 },
  { label: "2 hours before", value: 120 },
  { label: "1 day before", value: 1440 }
];

export function NotificationsSettings() {
  const { preferences, setNotificationPreferences } = usePreferences();
  const [permission, setPermission] = useState<NotificationPermissionStatus>("default");
  const [isRequesting, setIsRequesting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  // Check permission on mount
  useEffect(() => {
    if (isNotificationSupported()) {
      setPermission(getNotificationPermission());
    }
  }, []);

  const handleRequestPermission = async () => {
    setIsRequesting(true);

    try {
      const result = await requestNotificationPermission();
      setPermission(result);

      if (result === "granted") {
        setNotificationPreferences({ ...preferences.notifications, enabled: true });
        setShowSuccess(true);
        setTimeout(() => setShowSuccess(false), 3000);
      }
    } catch (error) {
      console.error("Failed to request notification permission:", error);
    } finally {
      setIsRequesting(false);
    }
  };

  const handleToggleEnabled = () => {
    if (!preferences.notifications.enabled && permission !== "granted") {
      // Need to request permission first
      handleRequestPermission();
    } else {
      setNotificationPreferences({
        ...preferences.notifications,
        enabled: !preferences.notifications.enabled
      });
    }
  };

  const handleReminderChange = (minutes: number) => {
    setNotificationPreferences({
      ...preferences.notifications,
      reminderMinutes: minutes
    });
  };

  // Don't render if notifications not supported
  if (!isNotificationSupported()) {
    return (
      <div className="bg-white rounded-2xl p-6 shadow-md">
        <div className="flex items-center gap-3 mb-4">
          <BellOff className="w-5 h-5 text-seal-brown/60" />
          <h3 className="text-lg font-semibold text-seal-brown">
            Notifications
          </h3>
        </div>
        <p className="text-sm text-seal-brown/60">
          Browser notifications are not supported on this device.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl p-6 shadow-md">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          {preferences.notifications.enabled ? (
            <Bell className="w-5 h-5 text-seal-brown" />
          ) : (
            <BellOff className="w-5 h-5 text-seal-brown/60" />
          )}
          <h3 className="text-lg font-semibold text-seal-brown">
            Notifications
          </h3>
        </div>

        {/* Permission Status Indicator */}
        {permission === "granted" && (
          <div className="flex items-center gap-1 text-xs text-green-600">
            <Check className="w-3 h-3" />
            <span>Enabled</span>
          </div>
        )}
        {permission === "denied" && (
          <div className="flex items-center gap-1 text-xs text-red-600">
            <X className="w-3 h-3" />
            <span>Blocked</span>
          </div>
        )}
      </div>

      {/* Success Message */}
      {showSuccess && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2">
          <Check className="w-4 h-4 text-green-600" />
          <span className="text-sm text-green-700">
            Notifications enabled successfully!
          </span>
        </div>
      )}

      {/* Permission Denied Warning */}
      {permission === "denied" && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2">
          <AlertCircle className="w-4 h-4 text-red-600 mt-0.5 flex-shrink-0" />
          <div className="text-sm text-red-700">
            <p className="font-medium">Notifications blocked</p>
            <p className="mt-1 text-xs">
              To enable notifications, please allow them in your browser settings.
            </p>
          </div>
        </div>
      )}

      {/* Enable/Disable Toggle */}
      <div className="mb-6">
        <label className="flex items-center justify-between cursor-pointer">
          <span className="text-sm font-medium text-seal-brown">
            Enable task reminders
          </span>
          <button
            onClick={handleToggleEnabled}
            disabled={isRequesting || permission === "denied"}
            className={`
              relative inline-flex h-6 w-11 items-center rounded-full
              transition-colors duration-200 ease-in-out
              ${
                preferences.notifications.enabled
                  ? "bg-seal-brown"
                  : "bg-seal-brown/20"
              }
              ${isRequesting || permission === "denied" ? "opacity-50 cursor-not-allowed" : ""}
            `}
          >
            <span
              className={`
                inline-block h-4 w-4 transform rounded-full bg-white
                transition duration-200 ease-in-out
                ${preferences.notifications.enabled ? "translate-x-6" : "translate-x-1"}
              `}
            />
          </button>
        </label>
        <p className="text-xs text-seal-brown/60 mt-1">
          Get notified before your tasks are due
        </p>
      </div>

      {/* Request Permission Button (if permission not granted) */}
      {permission === "default" && (
        <div className="mb-6">
          <button
            onClick={handleRequestPermission}
            disabled={isRequesting}
            className="w-full px-4 py-2 bg-seal-brown/10 hover:bg-seal-brown/20 text-seal-brown rounded-lg transition-colors duration-200 text-sm font-medium disabled:opacity-50"
          >
            {isRequesting ? "Requesting permission..." : "Allow notifications"}
          </button>
        </div>
      )}

      {/* Reminder Time Selector */}
      {preferences.notifications.enabled && permission === "granted" && (
        <div>
          <label className="block text-sm font-medium text-seal-brown mb-3">
            Remind me
          </label>
          <div className="space-y-2">
            {REMINDER_OPTIONS.map((option) => (
              <label
                key={option.value}
                className="flex items-center gap-3 cursor-pointer group"
              >
                <input
                  type="radio"
                  name="reminder-time"
                  value={option.value}
                  checked={preferences.notifications.reminderMinutes === option.value}
                  onChange={() => handleReminderChange(option.value)}
                  className="w-4 h-4 text-seal-brown border-seal-brown/30 focus:ring-seal-brown/30"
                />
                <span className="text-sm text-seal-brown group-hover:text-seal-brown/80">
                  {option.label}
                </span>
              </label>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
