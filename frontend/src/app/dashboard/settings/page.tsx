/**
 * Settings Page
 *
 * Central hub for user preferences and profile management.
 * Features:
 * - Profile settings (name, password)
 * - Notifications preferences
 * - Keyboard shortcuts reference
 * - Code splitting for optimized loading
 */
"use client";

import { useState, lazy, Suspense } from "react";
import { Settings, Bell, Keyboard, User } from "lucide-react";

// Lazy load settings components for better performance
const ProfileSettings = lazy(() => import("@/components/settings/ProfileSettings").then(mod => ({ default: mod.ProfileSettings })));
const NotificationsSettings = lazy(() => import("@/components/settings/NotificationsSettings").then(mod => ({ default: mod.NotificationsSettings })));
const KeyboardShortcuts = lazy(() => import("@/components/settings/KeyboardShortcuts").then(mod => ({ default: mod.KeyboardShortcuts })));

// Loading component for lazy-loaded content
function SettingsLoader() {
  return (
    <div className="space-y-4 animate-pulse">
      <div className="h-8 w-48 bg-gray-200 rounded" />
      <div className="h-20 bg-gray-200 rounded" />
      <div className="h-20 bg-gray-200 rounded" />
      <div className="h-20 bg-gray-200 rounded" />
    </div>
  );
}

type SettingsTab = "profile" | "notifications" | "shortcuts";

interface TabOption {
  id: SettingsTab;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}

const tabs: TabOption[] = [
  { id: "profile", label: "Profile", icon: User },
  { id: "notifications", label: "Notifications", icon: Bell },
  { id: "shortcuts", label: "Keyboard Shortcuts", icon: Keyboard },
];

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState<SettingsTab>("profile");

  return (
    <div className="max-w-4xl mx-auto">
      {/* Page Header */}
      <div className="mb-8 animate-fade-in">
        <div className="flex items-center gap-3 mb-2">
          <Settings className="w-8 h-8 text-seal-brown" aria-hidden="true" />
          <h1 className="text-3xl font-bold text-seal-brown">Settings</h1>
        </div>
        <p className="text-seal-brown/60">
          Manage your account and preferences
        </p>
      </div>

      {/* Tabs Navigation */}
      <div className="mb-8 border-b border-seal-brown/10 animate-slide-in-up" style={{ animationDelay: "100ms", animationFillMode: "both" }}>
        <nav className="flex gap-2" role="tablist" aria-label="Settings sections">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;

            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                role="tab"
                aria-selected={isActive}
                aria-controls={`${tab.id}-panel`}
                className={`
                  flex items-center gap-2 px-4 py-3 rounded-t-lg
                  transition-all duration-200
                  min-h-[44px]
                  ${
                    isActive
                      ? "bg-rose-white text-seal-brown border-b-2 border-seal-brown"
                      : "text-seal-brown/60 hover:text-seal-brown hover:bg-rose-white/50"
                  }
                `}
              >
                <Icon className="w-5 h-5" aria-hidden="true" />
                <span className="font-medium">{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content with Lazy Loading */}
      <div className="animate-fade-in" style={{ animationDelay: "200ms", animationFillMode: "both" }}>
        <Suspense fallback={<SettingsLoader />}>
          {activeTab === "profile" && (
            <div role="tabpanel" id="profile-panel" aria-labelledby="profile-tab">
              <ProfileSettings />
            </div>
          )}

          {activeTab === "notifications" && (
            <div role="tabpanel" id="notifications-panel" aria-labelledby="notifications-tab">
              <NotificationsSettings />
            </div>
          )}

          {activeTab === "shortcuts" && (
            <div role="tabpanel" id="shortcuts-panel" aria-labelledby="shortcuts-tab">
              <KeyboardShortcuts />
            </div>
          )}
        </Suspense>
      </div>
    </div>
  );
}
