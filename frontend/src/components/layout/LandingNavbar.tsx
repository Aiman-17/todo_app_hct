"use client";

/**
 * Modern Landing Page Navbar Component
 *
 * Features:
 * - Responsive navigation menu
 * - Logo with AI branding
 * - CTA buttons (Login/Signup)
 * - Mobile hamburger menu
 * - Futuristic gradient background
 */

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Menu, X, Bot } from "lucide-react";

export function LandingNavbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { href: "#features", label: "Features" },
    { href: "#how-it-works", label: "How It Works" },
    { href: "#pricing", label: "Pricing" },
    { href: "#about", label: "About" },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-r from-seal-brown/95 to-seal-brown/90 backdrop-blur-md shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <Bot className="w-8 h-8 text-rose-white" />
            <span className="text-xl font-bold text-rose-white">AI TaskMaster</span>
          </Link>

          {/* Desktop Navigation - Only visible on large screens */}
          <div className="hidden lg:flex items-center gap-8">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="text-rose-white/80 hover:text-rose-white transition-colors font-medium"
              >
                {link.label}
              </a>
            ))}
          </div>

          {/* Desktop CTA Buttons - Only visible on large screens */}
          <div className="hidden lg:flex items-center gap-3">
            <Link href="/login">
              <Button
                variant="ghost"
                className="text-rose-white hover:bg-rose-white/10 hover:text-rose-white"
              >
                Log In
              </Button>
            </Link>
            <Link href="/signup">
              <Button className="bg-rose-white text-seal-brown hover:bg-rose-white/90 font-semibold">
                Get Started Free
              </Button>
            </Link>
          </div>

          {/* Mobile Menu Button - Visible on mobile and tablet */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden p-2 rounded-md text-rose-white hover:bg-rose-white/10 transition-colors"
            aria-label="Toggle mobile menu"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu - Navigation links only (mobile and tablet) */}
        {mobileMenuOpen && (
          <div className="lg:hidden py-4 border-t border-rose-white/20 animate-fade-in">
            <div className="flex flex-col gap-4">
              {navLinks.map((link) => (
                <a
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-rose-white/80 hover:text-rose-white transition-colors font-medium py-2"
                >
                  {link.label}
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
