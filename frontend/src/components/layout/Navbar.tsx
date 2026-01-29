"use client";

/**
 * Navbar Component
 *
 * Horizontal navigation bar at the top of the dashboard.
 * Features:
 * - Seal brown (#2D0B00) background
 * - App branding/logo
 * - User profile display
 * - Logout button
 * - Responsive design
 */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { LogOut, User, CheckSquare } from "lucide-react";
import { isAuthenticated, clearTokens, apiRequest } from "@/lib/api";
import { useToast } from "@/components/ui/use-toast";
import type { User as UserType } from "@/types/auth";

export function Navbar() {
  const router = useRouter();
  const { toast } = useToast();

  const [user, setUser] = useState<UserType | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check authentication status and fetch user profile
    const fetchUser = async () => {
      if (isAuthenticated()) {
        try {
          const userData = await apiRequest<UserType>("/api/auth/profile");
          setUser(userData);
        } catch (error) {
          // Token expired or invalid - clear tokens
          clearTokens();
          setUser(null);
        }
      }
      setLoading(false);
    };

    fetchUser();
  }, []);

  const handleLogout = () => {
    // Clear tokens from localStorage
    clearTokens();
    setUser(null);

    // Show success toast
    toast({
      title: "Logged out",
      description: "You have been successfully logged out",
    });

    // Redirect to login page
    router.push("/login");
  };

  if (loading) {
    return (
      <nav className="bg-seal-brown border-b border-seal-brown/20 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3 pl-12 lg:pl-0">
              <CheckSquare className="w-6 h-6 text-rose-white" />
              <span className="text-rose-white font-bold text-xl">Todo App</span>
            </div>
          </div>
        </div>
      </nav>
    );
  }

  return (
    <nav className="bg-seal-brown border-b border-seal-brown/20 shadow-lg" role="navigation" aria-label="Main navigation">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Left: App Branding */}
          <div className="flex items-center gap-3 pl-12 lg:pl-0" role="banner">
            <CheckSquare className="w-6 h-6 text-rose-white" aria-hidden="true" />
            <h1 className="text-rose-white font-bold text-base sm:text-xl">Todo App</h1>
          </div>

          {/* Right: User Info & Actions */}
          {user && (
            <div className="flex items-center gap-4">
              {/* User Profile */}
              <div className="hidden sm:flex items-center gap-2 px-3 py-2 rounded-lg bg-rose-white/10" role="status" aria-label={`Logged in as ${user.name}`}>
                <User className="w-5 h-5 text-rose-white" aria-hidden="true" />
                <span className="text-rose-white text-sm font-medium">
                  {user.name}
                </span>
              </div>

              {/* Logout Button */}
              <button
                onClick={handleLogout}
                className="
                  flex items-center gap-2 px-4 py-2 rounded-lg
                  bg-rose-white/10 hover:bg-rose-white/20
                  text-rose-white font-medium
                  transition-all duration-200
                  border border-rose-white/20
                  min-h-[44px] min-w-[44px]
                "
                aria-label="Log out"
              >
                <LogOut className="w-5 h-5" aria-hidden="true" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
