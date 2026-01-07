/**
 * Signup form client component.
 *
 * Handles user registration with email, name, and password fields.
 * Submits data to POST /api/auth/signup, saves tokens to localStorage,
 * and redirects to /dashboard on success.
 * Includes real-time password validation feedback.
 */
"use client";

import { useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";
import { apiRequest, saveTokens } from "@/lib/api";
import { Check, X } from "lucide-react";
import type { SignupRequest, SignupResponse } from "@/types/auth";

export function SignupForm() {
  const router = useRouter();
  const { toast } = useToast();

  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Real-time password validation.
   *
   * Checks password requirements and updates validation state on each password change:
   * - Minimum 8 characters
   * - At least one uppercase letter
   * - At least one lowercase letter
   * - At least one number
   */
  const passwordValidation = useMemo(() => {
    return {
      minLength: password.length >= 8,
      hasUppercase: /[A-Z]/.test(password),
      hasLowercase: /[a-z]/.test(password),
      hasNumber: /[0-9]/.test(password),
    };
  }, [password]);

  const isPasswordValid = Object.values(passwordValidation).every(Boolean);

  /**
   * Handle form submission for user signup.
   *
   * Sends POST request to /api/auth/signup with user data,
   * saves JWT tokens to cookies on success, and redirects to dashboard.
   *
   * @param e - Form submission event
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const data = await apiRequest<SignupResponse>("/api/auth/signup", {
        method: "POST",
        body: JSON.stringify({
          email,
          name,
          password,
        } as SignupRequest),
      });

      saveTokens(data.tokens.access_token, data.tokens.refresh_token);

      toast({
        title: "Account created",
        description: `Welcome, ${data.user.name}!`,
      });

      router.push("/dashboard");
    } catch (error: any) {
      toast({
        title: "Signup failed",
        description: error.message || "Failed to create account",
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
        <Label htmlFor="name">Name</Label>
        <Input
          id="name"
          type="text"
          placeholder="Alice Smith"
          value={name}
          onChange={(e) => setName(e.target.value)}
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
          className={password && !isPasswordValid ? "border-red-500 focus:ring-red-500" : ""}
        />

        {/* Real-time password requirements checklist */}
        {password && (
          <div className="space-y-1 p-3 bg-gray-50 rounded-md">
            <p className="text-xs font-medium text-gray-700 mb-2">Password requirements:</p>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                {passwordValidation.minLength ? (
                  <Check className="h-4 w-4 text-green-600" />
                ) : (
                  <X className="h-4 w-4 text-red-500" />
                )}
                <span className={`text-xs ${passwordValidation.minLength ? "text-green-600" : "text-gray-600"}`}>
                  At least 8 characters
                </span>
              </div>
              <div className="flex items-center gap-2">
                {passwordValidation.hasUppercase ? (
                  <Check className="h-4 w-4 text-green-600" />
                ) : (
                  <X className="h-4 w-4 text-red-500" />
                )}
                <span className={`text-xs ${passwordValidation.hasUppercase ? "text-green-600" : "text-gray-600"}`}>
                  One uppercase letter
                </span>
              </div>
              <div className="flex items-center gap-2">
                {passwordValidation.hasLowercase ? (
                  <Check className="h-4 w-4 text-green-600" />
                ) : (
                  <X className="h-4 w-4 text-red-500" />
                )}
                <span className={`text-xs ${passwordValidation.hasLowercase ? "text-green-600" : "text-gray-600"}`}>
                  One lowercase letter
                </span>
              </div>
              <div className="flex items-center gap-2">
                {passwordValidation.hasNumber ? (
                  <Check className="h-4 w-4 text-green-600" />
                ) : (
                  <X className="h-4 w-4 text-red-500" />
                )}
                <span className={`text-xs ${passwordValidation.hasNumber ? "text-green-600" : "text-gray-600"}`}>
                  One number
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? "Creating account..." : "Sign up"}
      </Button>

      <div className="text-center text-sm text-gray-600">
        Already have an account?{" "}
        <Link href="/login" className="text-blue-600 hover:underline">
          Log in
        </Link>
      </div>
    </form>
  );
}
