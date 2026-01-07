"use client";

/**
 * Icon-only Sidebar Component
 *
 * Premium minimalist sidebar with icon navigation.
 * Features:
 * - Icon-only design (64px width when collapsed)
 * - Smooth hover states with seal-brown accents
 * - Tooltips on hover to show labels
 * - Fixed positioning on left side
 * - Responsive: hidden on mobile with hamburger menu toggle
 */

import { Home, CheckSquare, Calendar, Settings, LogOut, Menu, X } from "lucide-react";
import { usePathname, useRouter } from "next/navigation";
import { clearTokens } from "@/lib/api";
import { useState } from "react";

interface NavItem {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  href: string;
  action?: () => void;
}

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    clearTokens();
    router.push("/login");
  };

  const navItems: NavItem[] = [
    { icon: Home, label: "Dashboard", href: "/dashboard" },
    { icon: CheckSquare, label: "Tasks", href: "/dashboard" },
    { icon: Calendar, label: "Calendar", href: "/dashboard/calendar" },
    { icon: Settings, label: "Settings", href: "/dashboard/settings" },
  ];

  const isActive = (href: string) => pathname === href;

  const closeMobileMenu = () => setIsMobileMenuOpen(false);

  return (
    <>
      {/* Mobile Menu Button (visible on small screens) */}
      <button
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        className="fixed top-4 left-4 z-50 lg:hidden bg-seal-brown text-rose-white p-3 rounded-lg shadow-lg hover:bg-seal-brown/90 transition-colors min-h-[44px] min-w-[44px]"
        aria-label={isMobileMenuOpen ? "Close menu" : "Open menu"}
        aria-expanded={isMobileMenuOpen}
      >
        {isMobileMenuOpen ? (
          <X className="w-6 h-6" aria-hidden="true" />
        ) : (
          <Menu className="w-6 h-6" aria-hidden="true" />
        )}
      </button>

      {/* Mobile Overlay */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={closeMobileMenu}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed left-0 top-0 z-40 h-screen w-16 bg-seal-brown flex flex-col items-center py-6 shadow-lg
          transition-transform duration-300 ease-in-out
          lg:translate-x-0
          ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
        role="complementary"
        aria-label="Sidebar navigation"
      >
        {/* Logo/Brand */}
        <div className="mb-8 text-rose-white font-bold text-xl" aria-hidden="true">T</div>

      {/* Navigation Items */}
      <nav className="flex-1 flex flex-col gap-2 w-full px-2" role="navigation" aria-label="Main menu">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.href);

          return (
            <div key={item.label} className="relative">
              <button
                onClick={() => {
                  router.push(item.href);
                  closeMobileMenu();
                }}
                onMouseEnter={() => setHoveredItem(item.label)}
                onMouseLeave={() => setHoveredItem(null)}
                className={`
                  w-full min-h-[44px] rounded-lg flex items-center justify-center
                  transition-all duration-200 ease-in-out
                  ${
                    active
                      ? "bg-rose-white text-seal-brown shadow-md"
                      : "text-rose-white hover:bg-rose-white/10 hover:text-rose-white"
                  }
                `}
                aria-label={item.label}
                aria-current={active ? "page" : undefined}
              >
                <Icon className="w-5 h-5" aria-hidden="true" />
              </button>

              {/* Tooltip on hover */}
              {hoveredItem === item.label && (
                <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 pointer-events-none">
                  <div className="bg-seal-brown text-rose-white px-3 py-2 rounded-lg shadow-lg text-sm whitespace-nowrap animate-fade-in">
                    {item.label}
                    {/* Tooltip arrow */}
                    <div className="absolute right-full top-1/2 -translate-y-1/2 border-8 border-transparent border-r-seal-brown" />
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </nav>

      {/* Logout Button */}
      <div className="relative mt-auto">
        <button
          onClick={() => {
            handleLogout();
            closeMobileMenu();
          }}
          onMouseEnter={() => setHoveredItem("Logout")}
          onMouseLeave={() => setHoveredItem(null)}
          className="
            w-12 min-h-[44px] rounded-lg flex items-center justify-center
            text-rose-white hover:bg-rose-white/10 hover:text-rose-white
            transition-all duration-200 ease-in-out
          "
          aria-label="Logout"
        >
          <LogOut className="w-5 h-5" aria-hidden="true" />
        </button>

        {/* Logout Tooltip */}
        {hoveredItem === "Logout" && (
          <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 pointer-events-none">
            <div className="bg-seal-brown text-rose-white px-3 py-2 rounded-lg shadow-lg text-sm whitespace-nowrap animate-fade-in">
              Logout
              <div className="absolute right-full top-1/2 -translate-y-1/2 border-8 border-transparent border-r-seal-brown" />
            </div>
          </div>
        )}
      </div>
      </aside>
    </>
  );
}
