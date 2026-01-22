/**
 * Header component with authentication-aware navigation.
 *
 * Displays:
 * - User profile and logout button (if authenticated)
 * - Login/Signup links (if not authenticated)
 */
"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { isAuthenticated, clearTokens, apiRequest } from "@/lib/api";
import { useToast } from "@/components/ui/use-toast";
import type { User } from "@/types/auth";

export function Header() {
  const router = useRouter();
  const { toast } = useToast();

  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check authentication status and fetch user profile
    const fetchUser = async () => {
      if (isAuthenticated()) {
        try {
          const userData = await apiRequest<User>("/api/auth/profile");
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
      <header className="border-b bg-white">
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <Link href="/" className="text-xl font-bold">
            Todo App
          </Link>
        </div>
      </header>
    );
  }

  return (
    <header className="border-b bg-white" role="banner">
      <div className="container mx-auto flex flex-col sm:flex-row sm:h-16 items-center justify-between px-4 py-4 sm:py-0 gap-4 sm:gap-0">
        <Link href="/" className="text-xl font-bold" aria-label="Todo App home">
          Todo App
        </Link>

        <nav className="flex flex-col sm:flex-row items-center gap-4" role="navigation" aria-label="Main navigation">
          {user ? (
            // Authenticated user
            <>
              <Link href="/dashboard" className="text-sm hover:underline">
                Dashboard
              </Link>
              <Link href="/dashboard/chat" className="text-sm hover:underline">
                AI Chat
              </Link>
              <span className="text-sm text-gray-600 hidden sm:inline" aria-label={`Logged in as ${user.name}`}>
                {user.name}
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={handleLogout}
                className="min-h-[44px] min-w-[44px]"
                aria-label="Log out of your account"
              >
                Logout
              </Button>
            </>
          ) : (
            // Unauthenticated user
            <>
              <Link href="/login">
                <Button variant="outline" size="sm" className="min-h-[44px] min-w-[44px]">
                  Log in
                </Button>
              </Link>
              <Link href="/signup">
                <Button size="sm" className="min-h-[44px] min-w-[44px]">
                  Sign up
                </Button>
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
