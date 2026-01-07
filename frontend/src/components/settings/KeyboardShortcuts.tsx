/**
 * Keyboard Shortcuts Reference Panel
 *
 * Displays all available keyboard shortcuts in the application.
 * Helps users discover and learn keyboard navigation.
 */
"use client";

import { Keyboard } from "lucide-react";

interface ShortcutItem {
  key: string;
  description: string;
  category: string;
}

const shortcuts: ShortcutItem[] = [
  // Navigation
  { key: "N", description: "Create new task", category: "Navigation" },
  { key: "/", description: "Focus search input", category: "Navigation" },
  { key: "F", description: "Toggle filters panel", category: "Navigation" },
  { key: "Esc", description: "Close modals/dropdowns", category: "Navigation" },
  { key: "Tab", description: "Navigate between elements", category: "Navigation" },

  // Task Actions
  { key: "Enter", description: "Submit forms/confirm actions", category: "Task Actions" },
  { key: "Space", description: "Toggle checkboxes", category: "Task Actions" },
];

export function KeyboardShortcuts() {
  // Group shortcuts by category
  const groupedShortcuts = shortcuts.reduce((acc, shortcut) => {
    if (!acc[shortcut.category]) {
      acc[shortcut.category] = [];
    }
    acc[shortcut.category].push(shortcut);
    return acc;
  }, {} as Record<string, ShortcutItem[]>);

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <Keyboard className="w-5 h-5 text-seal-brown" />
        <h2 className="text-xl font-semibold text-seal-brown">Keyboard Shortcuts</h2>
      </div>

      <div className="space-y-6">
        {Object.entries(groupedShortcuts).map(([category, items]) => (
          <div key={category}>
            <h3 className="text-sm font-semibold text-seal-brown/70 mb-3">
              {category}
            </h3>
            <div className="space-y-2">
              {items.map((item) => (
                <div
                  key={item.key}
                  className="flex items-center justify-between p-3 bg-rose-white rounded-lg border border-seal-brown/10"
                >
                  <span className="text-sm text-seal-brown">{item.description}</span>
                  <kbd className="px-3 py-1.5 text-sm font-semibold text-seal-brown bg-white border border-seal-brown/20 rounded shadow-sm min-w-[44px] text-center">
                    {item.key}
                  </kbd>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="p-4 bg-seal-brown/5 rounded-lg border border-seal-brown/10">
        <p className="text-sm text-seal-brown/70">
          <strong>Tip:</strong> These shortcuts work from anywhere in the app unless you're typing in an input field.
        </p>
      </div>
    </div>
  );
}
