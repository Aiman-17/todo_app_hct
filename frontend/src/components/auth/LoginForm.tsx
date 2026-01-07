/**
 * Login form client component.
 *
 * Handles user authentication with email and password fields.
 * Submits credentials to POST /api/auth/login, saves tokens to localStorage,
 * and redirects to /dashboard on success.
 */
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";
import { apiRequest, saveTokens } from "@/lib/api";
import type { LoginRequest, TokenResponse } from "@/types/auth";

export function LoginForm() {
  const router = useRouter();
  const { toast } = useToast();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Handle form submission for user login.
   *
   * Sends POST request to /api/auth/login with credentials,
   * saves JWT tokens to cookies on success, and redirects to dashboard.
   *
   * @param e - Form submission event
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const data = await apiRequest<TokenResponse>("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({
          email,
          password,
        } as LoginRequest),
      });

      saveTokens(data.access_token, data.refresh_token);

      toast({
        title: "Login successful",
        description: "Welcome back!",
      });

      router.push("/dashboard");
    } catch (error: any) {
      toast({
        title: "Login failed",
        description: error.message || "Invalid email or password",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          placeholder="alice@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          disabled={isLoading}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          disabled={isLoading}
        />
      </div>

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? "Logging in..." : "Log in"}
      </Button>

      <div className="text-center text-sm text-gray-600">
        Don&apos;t have an account?{" "}
        <Link href="/signup" className="text-blue-600 hover:underline">
          Sign up
        </Link>
      </div>
    </form>
  );
}
