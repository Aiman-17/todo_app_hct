/**
 * Profile Settings Component
 *
 * Allows users to view and update their profile information.
 * Includes name, email display, and password change functionality.
 */
"use client";

import { useState, useEffect } from "react";
import { User, Mail, Lock, Save } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";
import { apiRequest } from "@/lib/api";
import type { User as UserType } from "@/types/auth";

export function ProfileSettings() {
  const { toast } = useToast();
  const [user, setUser] = useState<UserType | null>(null);
  const [name, setName] = useState("");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingProfile, setIsLoadingProfile] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const userData = await apiRequest<UserType>("/api/auth/profile");
        setUser(userData);
        setName(userData.name);
      } catch (error) {
        toast({
          title: "Failed to load profile",
          description: "Please try refreshing the page",
          variant: "destructive",
        });
      } finally {
        setIsLoadingProfile(false);
      }
    };

    fetchProfile();
  }, []);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await apiRequest("/api/auth/profile", {
        method: "PUT",
        body: JSON.stringify({ name }),
      });

      toast({
        title: "Profile updated",
        description: "Your profile has been updated successfully",
      });

      // Update local user state
      if (user) {
        setUser({ ...user, name });
      }
    } catch (error: any) {
      toast({
        title: "Failed to update profile",
        description: error.message,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      toast({
        title: "Passwords don't match",
        description: "Please make sure your passwords match",
        variant: "destructive",
      });
      return;
    }

    if (newPassword.length < 8) {
      toast({
        title: "Password too short",
        description: "Password must be at least 8 characters",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);

    try {
      await apiRequest("/api/auth/change-password", {
        method: "POST",
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });

      toast({
        title: "Password changed",
        description: "Your password has been changed successfully",
      });

      // Clear password fields
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (error: any) {
      toast({
        title: "Failed to change password",
        description: error.message,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoadingProfile) {
    return (
      <div className="space-y-6">
        <div className="h-8 w-48 bg-gray-200 rounded animate-pulse" />
        <div className="space-y-4">
          <div className="h-20 bg-gray-200 rounded animate-pulse" />
          <div className="h-20 bg-gray-200 rounded animate-pulse" />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2">
        <User className="w-5 h-5 text-seal-brown" />
        <h2 className="text-xl font-semibold text-seal-brown">Profile</h2>
      </div>

      {/* Profile Information */}
      <form onSubmit={handleUpdateProfile} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="name">Name</Label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-seal-brown/40" />
            <Input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={isLoading}
              className="pl-10"
              required
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-seal-brown/40" />
            <Input
              id="email"
              type="email"
              value={user?.email || ""}
              disabled
              className="pl-10 bg-gray-50"
            />
          </div>
          <p className="text-xs text-seal-brown/60">
            Email cannot be changed
          </p>
        </div>

        <Button
          type="submit"
          disabled={isLoading || name === user?.name}
          className="min-h-[44px]"
        >
          <Save className="w-4 h-4 mr-2" />
          Save Changes
        </Button>
      </form>

      {/* Password Change */}
      <div className="pt-6 border-t border-seal-brown/10">
        <div className="flex items-center gap-2 mb-4">
          <Lock className="w-5 h-5 text-seal-brown" />
          <h3 className="text-lg font-semibold text-seal-brown">Change Password</h3>
        </div>

        <form onSubmit={handleChangePassword} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="current-password">Current Password</Label>
            <Input
              id="current-password"
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              disabled={isLoading}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="new-password">New Password</Label>
            <Input
              id="new-password"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              disabled={isLoading}
              minLength={8}
              required
            />
            <p className="text-xs text-seal-brown/60">
              Must be at least 8 characters
            </p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="confirm-password">Confirm New Password</Label>
            <Input
              id="confirm-password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              disabled={isLoading}
              minLength={8}
              required
            />
          </div>

          <Button
            type="submit"
            disabled={isLoading}
            variant="outline"
            className="min-h-[44px]"
          >
            Change Password
          </Button>
        </form>
      </div>
    </div>
  );
}
