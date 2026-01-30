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
import { Settings, Bell, Keyboard, User, ChevronLeft, ChevronRight } from "lucide-react";

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

  // Touch gesture state for mobile swipe navigation
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);
  const minSwipeDistance = 50;

  // Touch event handlers
  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;

    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    const currentIndex = tabs.findIndex(tab => tab.id === activeTab);

    if (isLeftSwipe && currentIndex < tabs.length - 1) {
      // Swipe left → go to next tab
      setActiveTab(tabs[currentIndex + 1].id);
    } else if (isRightSwipe && currentIndex > 0) {
      // Swipe right → go to previous tab
      setActiveTab(tabs[currentIndex - 1].id);
    }
  };

  // Arrow navigation functions
  const goToPrevTab = () => {
    const currentIndex = tabs.findIndex(tab => tab.id === activeTab);
    if (currentIndex > 0) {
      setActiveTab(tabs[currentIndex - 1].id);
    }
  };

  const goToNextTab = () => {
    const currentIndex = tabs.findIndex(tab => tab.id === activeTab);
    if (currentIndex < tabs.length - 1) {
      setActiveTab(tabs[currentIndex + 1].id);
    }
  };

  const currentIndex = tabs.findIndex(tab => tab.id === activeTab);
  const currentTabLabel = tabs[currentIndex]?.label || "Profile";

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

      {/* Desktop Tabs Navigation */}
      <div className="hidden md:block mb-8 border-b border-seal-brown/10 animate-slide-in-up" style={{ animationDelay: "100ms", animationFillMode: "both" }}>
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

      {/* Mobile Slider Navigation */}
      <div className="md:hidden mb-8 animate-slide-in-up" style={{ animationDelay: "100ms", animationFillMode: "both" }}>
        {/* Navigation Header with Arrows */}
        <div className="flex items-center justify-between mb-4">
          <button
            onClick={goToPrevTab}
            disabled={currentIndex === 0}
            aria-label="Previous section"
            className={`
              p-2 rounded-lg transition-all
              ${currentIndex === 0
                ? "text-seal-brown/30 cursor-not-allowed"
                : "text-seal-brown hover:bg-rose-white active:scale-95"
              }
            `}
          >
            <ChevronLeft className="w-6 h-6" />
          </button>

          <h2 className="text-lg font-semibold text-seal-brown text-center flex-1">
            {currentTabLabel}
          </h2>

          <button
            onClick={goToNextTab}
            disabled={currentIndex === tabs.length - 1}
            aria-label="Next section"
            className={`
              p-2 rounded-lg transition-all
              ${currentIndex === tabs.length - 1
                ? "text-seal-brown/30 cursor-not-allowed"
                : "text-seal-brown hover:bg-rose-white active:scale-95"
              }
            `}
          >
            <ChevronRight className="w-6 h-6" />
          </button>
        </div>

        {/* Dot Indicators */}
        <div className="flex items-center justify-center gap-2">
          {tabs.map((tab, index) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              aria-label={`Go to ${tab.label}`}
              className={`
                rounded-full transition-all duration-200
                ${index === currentIndex
                  ? "w-8 h-2 bg-seal-brown"
                  : "w-2 h-2 bg-seal-brown/30 hover:bg-seal-brown/50"
                }
              `}
            />
          ))}
        </div>
      </div>

      {/* Tab Content with Lazy Loading */}
      <div
        className="animate-fade-in"
        style={{ animationDelay: "200ms", animationFillMode: "both" }}
        onTouchStart={onTouchStart}
        onTouchMove={onTouchMove}
        onTouchEnd={onTouchEnd}
      >
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
