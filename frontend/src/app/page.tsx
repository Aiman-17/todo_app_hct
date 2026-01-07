"use client";

/**
 * Modern Landing Page with AI-Powered Task Management Theme
 *
 * Features:
 * - Futuristic hero section with AI messaging
 * - 3D robot illustration (left side)
 * - Responsive design (mobile-first)
 * - Modern navbar and footer
 * - CTA buttons with gradient effects
 */

import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { LandingNavbar } from "@/components/layout/LandingNavbar";
import { LandingFooter } from "@/components/layout/LandingFooter";
import {
  Bot,
  Sparkles,
  Zap,
  CheckCircle2,
  Calendar,
  Bell,
  TrendingUp,
  Shield,
  Smartphone,
  Globe
} from "lucide-react";
import { isAuthenticated } from "@/lib/api";

export default function HomePage() {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setAuthenticated(isAuthenticated());
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-rose-white to-seal-brown/5">
        <div className="text-seal-brown/60">Loading...</div>
      </div>
    );
  }

  const features = [
    {
      icon: Sparkles,
      title: "AI-Powered Intelligence",
      description: "Smart task suggestions and priority recommendations powered by advanced AI"
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Instant sync across all devices with real-time updates"
    },
    {
      icon: Shield,
      title: "Secure & Private",
      description: "Bank-level encryption keeps your data safe and private"
    },
    {
      icon: Calendar,
      title: "Smart Scheduling",
      description: "Intelligent due date reminders and recurring task automation"
    },
    {
      icon: Bell,
      title: "Smart Notifications",
      description: "Never miss a deadline with AI-optimized alerts"
    },
    {
      icon: TrendingUp,
      title: "Productivity Analytics",
      description: "Track your progress with insightful dashboards"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-rose-white via-rose-white to-seal-brown/5">
      {/* Navbar */}
      <LandingNavbar />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Robot Image/Illustration - First on mobile, Right on desktop */}
            <div className="order-1 lg:order-2 flex justify-center lg:justify-end animate-fade-in">
              <div className="relative w-full max-w-md aspect-square">
                {/* 3D Robot Placeholder with modern styling */}
                <div className="absolute inset-0 bg-gradient-to-br from-seal-brown/10 to-seal-brown/5 rounded-3xl shadow-2xl flex items-center justify-center overflow-hidden">
                  {/* Animated gradient background */}
                  <div className="absolute inset-0 bg-gradient-to-tr from-seal-brown/20 via-transparent to-seal-brown/10 animate-pulse"></div>

                  {/* Robot Icon (placeholder for 3D model) */}
                  <div className="relative z-10 flex flex-col items-center gap-4">
                    <Bot className="w-48 h-48 text-seal-brown animate-bounce-subtle" strokeWidth={1.5} />
                    <div className="flex gap-2">
                      <div className="w-3 h-3 bg-seal-brown/40 rounded-full animate-pulse"></div>
                      <div className="w-3 h-3 bg-seal-brown/40 rounded-full animate-pulse delay-100"></div>
                      <div className="w-3 h-3 bg-seal-brown/40 rounded-full animate-pulse delay-200"></div>
                    </div>
                  </div>

                  {/* Floating particles effect */}
                  <div className="absolute top-10 left-10 w-2 h-2 bg-seal-brown/30 rounded-full animate-float"></div>
                  <div className="absolute bottom-20 right-10 w-3 h-3 bg-seal-brown/20 rounded-full animate-float delay-100"></div>
                  <div className="absolute top-32 right-20 w-2 h-2 bg-seal-brown/25 rounded-full animate-float delay-200"></div>
                </div>

                {/* Decorative elements */}
                <div className="absolute -top-4 -right-4 w-24 h-24 bg-seal-brown/10 rounded-full blur-2xl"></div>
                <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-seal-brown/5 rounded-full blur-3xl"></div>
              </div>
            </div>

            {/* Hero Content - Second on mobile, Left on desktop */}
            <div className="order-2 lg:order-1 text-center lg:text-left animate-slide-in">
              {/* Badge */}
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-seal-brown/10 rounded-full mb-6">
                <Sparkles className="w-4 h-4 text-seal-brown" />
                <span className="text-sm font-medium text-seal-brown">AI-Powered Task Management</span>
              </div>

              {/* Main Heading */}
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-seal-brown mb-6 leading-tight">
                Your AI Assistant for
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-seal-brown to-seal-brown/60">
                  Effortless Productivity
                </span>
              </h1>

              {/* Subheading */}
              <p className="text-lg sm:text-xl text-seal-brown/70 mb-8 max-w-xl mx-auto lg:mx-0">
                Experience the future of task management with intelligent automation,
                smart scheduling, and seamless collaboration. Get more done, stress less.
              </p>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                {authenticated ? (
                  <Link href="/dashboard">
                    <Button
                      size="lg"
                      className="w-full sm:w-auto bg-seal-brown hover:bg-seal-brown/90 text-rose-white font-semibold px-8 py-6 text-lg shadow-xl hover:shadow-2xl transition-all duration-300 group"
                    >
                      Go to Dashboard
                      <Zap className="ml-2 w-5 h-5 group-hover:rotate-12 transition-transform" />
                    </Button>
                  </Link>
                ) : (
                  <>
                    <Link href="/signup">
                      <Button
                        size="lg"
                        className="w-full sm:w-auto bg-seal-brown hover:bg-seal-brown/90 text-rose-white font-semibold px-8 py-6 text-lg shadow-xl hover:shadow-2xl transition-all duration-300 group"
                      >
                        Start Free Today
                        <Sparkles className="ml-2 w-5 h-5 group-hover:scale-110 transition-transform" />
                      </Button>
                    </Link>
                    <Link href="/login">
                      <Button
                        variant="outline"
                        size="lg"
                        className="w-full sm:w-auto border-2 border-seal-brown text-seal-brown hover:bg-seal-brown hover:text-rose-white font-semibold px-8 py-6 text-lg transition-all duration-300"
                      >
                        Log In
                      </Button>
                    </Link>
                  </>
                )}
              </div>

              {/* Trust Indicators */}
              <div className="mt-8 flex flex-wrap items-center justify-center lg:justify-start gap-6 text-sm text-seal-brown/60">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown" />
                  <span>Free forever plan</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown" />
                  <span>No credit card required</span>
                </div>
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown" />
                  <span>Cancel anytime</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-white/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-seal-brown mb-4">
              Powerful Features, Simple Experience
            </h2>
            <p className="text-lg text-seal-brown/70 max-w-2xl mx-auto">
              Everything you need to manage tasks efficiently, all powered by intelligent automation
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div
                  key={index}
                  className="p-6 bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 border border-seal-brown/10 hover:border-seal-brown/30 group"
                >
                  <div className="w-12 h-12 bg-seal-brown/10 rounded-xl flex items-center justify-center mb-4 group-hover:bg-seal-brown group-hover:scale-110 transition-all duration-300">
                    <Icon className="w-6 h-6 text-seal-brown group-hover:text-rose-white transition-colors" />
                  </div>
                  <h3 className="text-xl font-semibold text-seal-brown mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-seal-brown/70">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-seal-brown mb-4">
              How It Works
            </h2>
            <p className="text-lg text-seal-brown/70 max-w-2xl mx-auto">
              Get started in minutes with our simple, intuitive workflow
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            {/* Step 1 */}
            <div className="text-center">
              <div className="w-20 h-20 bg-seal-brown rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl font-bold text-rose-white">1</span>
              </div>
              <h3 className="text-xl font-semibold text-seal-brown mb-3">
                Create Your Account
              </h3>
              <p className="text-seal-brown/70">
                Sign up in seconds with just your email. No credit card required, no complicated setup.
              </p>
            </div>

            {/* Step 2 */}
            <div className="text-center">
              <div className="w-20 h-20 bg-seal-brown rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl font-bold text-rose-white">2</span>
              </div>
              <h3 className="text-xl font-semibold text-seal-brown mb-3">
                Add Your Tasks
              </h3>
              <p className="text-seal-brown/70">
                Create tasks with titles, descriptions, priorities, and due dates. Our AI helps organize them automatically.
              </p>
            </div>

            {/* Step 3 */}
            <div className="text-center">
              <div className="w-20 h-20 bg-seal-brown rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl font-bold text-rose-white">3</span>
              </div>
              <h3 className="text-xl font-semibold text-seal-brown mb-3">
                Get Things Done
              </h3>
              <p className="text-seal-brown/70">
                Track progress, collaborate with your team, and achieve your goals with intelligent reminders.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white/50">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-seal-brown mb-2">10K+</div>
              <div className="text-seal-brown/70">Active Users</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-seal-brown mb-2">1M+</div>
              <div className="text-seal-brown/70">Tasks Completed</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-seal-brown mb-2">99.9%</div>
              <div className="text-seal-brown/70">Uptime</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-seal-brown mb-2">4.9★</div>
              <div className="text-seal-brown/70">User Rating</div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-seal-brown mb-4">
              Simple, Transparent Pricing
            </h2>
            <p className="text-lg text-seal-brown/70 max-w-2xl mx-auto">
              Choose the plan that fits your needs. All plans include our core AI-powered features.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {/* Free Plan */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-seal-brown/10 hover:border-seal-brown/30 transition-all duration-300">
              <h3 className="text-2xl font-bold text-seal-brown mb-2">Free</h3>
              <div className="text-4xl font-bold text-seal-brown mb-6">
                $0<span className="text-lg font-normal text-seal-brown/60">/month</span>
              </div>
              <ul className="space-y-4 mb-8">
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown mt-0.5 flex-shrink-0" />
                  <span className="text-seal-brown/70">Up to 50 tasks</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown mt-0.5 flex-shrink-0" />
                  <span className="text-seal-brown/70">Basic AI suggestions</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown mt-0.5 flex-shrink-0" />
                  <span className="text-seal-brown/70">Mobile & web access</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown mt-0.5 flex-shrink-0" />
                  <span className="text-seal-brown/70">Email support</span>
                </li>
              </ul>
              <Link href="/signup">
                <Button className="w-full bg-seal-brown/10 text-seal-brown hover:bg-seal-brown hover:text-rose-white">
                  Get Started
                </Button>
              </Link>
            </div>

            {/* Pro Plan */}
            <div className="bg-gradient-to-br from-seal-brown to-seal-brown/90 rounded-2xl shadow-2xl p-8 border-4 border-seal-brown transform scale-105 relative">
              <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-rose-white text-seal-brown px-4 py-1 rounded-full text-sm font-semibold">
                Most Popular
              </div>
              <h3 className="text-2xl font-bold text-rose-white mb-2">Pro</h3>
              <div className="text-4xl font-bold text-rose-white mb-6">
                $9<span className="text-lg font-normal text-rose-white/60">/month</span>
              </div>
              <ul className="space-y-4 mb-8">
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-rose-white mt-0.5 flex-shrink-0" />
                  <span className="text-rose-white/90">Unlimited tasks</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-rose-white mt-0.5 flex-shrink-0" />
                  <span className="text-rose-white/90">Advanced AI automation</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-rose-white mt-0.5 flex-shrink-0" />
                  <span className="text-rose-white/90">Team collaboration</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-rose-white mt-0.5 flex-shrink-0" />
                  <span className="text-rose-white/90">Priority support</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-rose-white mt-0.5 flex-shrink-0" />
                  <span className="text-rose-white/90">Custom integrations</span>
                </li>
              </ul>
              <Link href="/signup">
                <Button className="w-full bg-rose-white text-seal-brown hover:bg-rose-white/90">
                  Start Free Trial
                </Button>
              </Link>
            </div>

            {/* Enterprise Plan */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-seal-brown/10 hover:border-seal-brown/30 transition-all duration-300">
              <h3 className="text-2xl font-bold text-seal-brown mb-2">Enterprise</h3>
              <div className="text-4xl font-bold text-seal-brown mb-6">
                Custom
              </div>
              <ul className="space-y-4 mb-8">
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown mt-0.5 flex-shrink-0" />
                  <span className="text-seal-brown/70">Everything in Pro</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown mt-0.5 flex-shrink-0" />
                  <span className="text-seal-brown/70">Dedicated account manager</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown mt-0.5 flex-shrink-0" />
                  <span className="text-seal-brown/70">Advanced security & compliance</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown mt-0.5 flex-shrink-0" />
                  <span className="text-seal-brown/70">Custom AI training</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-seal-brown mt-0.5 flex-shrink-0" />
                  <span className="text-seal-brown/70">SLA guarantee</span>
                </li>
              </ul>
              <Button className="w-full bg-seal-brown/10 text-seal-brown hover:bg-seal-brown hover:text-rose-white">
                Contact Sales
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 px-4 sm:px-6 lg:px-8 bg-white/50">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Left: Content */}
            <div>
              <h2 className="text-3xl sm:text-4xl font-bold text-seal-brown mb-6">
                About AI TaskMaster
              </h2>
              <p className="text-lg text-seal-brown/70 mb-6">
                AI TaskMaster was born from a simple idea: task management should be effortless, not another task on your list.
              </p>
              <p className="text-lg text-seal-brown/70 mb-6">
                We combine cutting-edge AI technology with beautiful, intuitive design to help individuals and teams achieve more. Our platform learns from your habits, suggests optimal workflows, and automates the tedious parts of task management.
              </p>
              <p className="text-lg text-seal-brown/70 mb-8">
                Whether you're managing personal projects, coordinating a team, or running a business, AI TaskMaster adapts to your needs and grows with you.
              </p>

              <div className="space-y-4">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-seal-brown/10 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Zap className="w-6 h-6 text-seal-brown" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-seal-brown mb-1">Our Mission</h3>
                    <p className="text-seal-brown/70">
                      Empower everyone to achieve their goals through intelligent task management.
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-seal-brown/10 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Shield className="w-6 h-6 text-seal-brown" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-seal-brown mb-1">Our Values</h3>
                    <p className="text-seal-brown/70">
                      Privacy-first, user-centric design, and continuous innovation.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Right: Stats/Visual */}
            <div className="grid grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-2xl shadow-lg text-center">
                <Globe className="w-10 h-10 text-seal-brown mx-auto mb-3" />
                <div className="text-3xl font-bold text-seal-brown mb-1">120+</div>
                <div className="text-seal-brown/70">Countries</div>
              </div>
              <div className="bg-white p-6 rounded-2xl shadow-lg text-center">
                <Smartphone className="w-10 h-10 text-seal-brown mx-auto mb-3" />
                <div className="text-3xl font-bold text-seal-brown mb-1">5M+</div>
                <div className="text-seal-brown/70">Downloads</div>
              </div>
              <div className="bg-white p-6 rounded-2xl shadow-lg text-center">
                <TrendingUp className="w-10 h-10 text-seal-brown mx-auto mb-3" />
                <div className="text-3xl font-bold text-seal-brown mb-1">98%</div>
                <div className="text-seal-brown/70">Satisfaction</div>
              </div>
              <div className="bg-white p-6 rounded-2xl shadow-lg text-center">
                <CheckCircle2 className="w-10 h-10 text-seal-brown mx-auto mb-3" />
                <div className="text-3xl font-bold text-seal-brown mb-1">24/7</div>
                <div className="text-seal-brown/70">Support</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-seal-brown to-seal-brown/90">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-rose-white mb-6">
            Ready to Transform Your Productivity?
          </h2>
          <p className="text-lg text-rose-white/80 mb-8">
            Join thousands of users who are getting more done with AI TaskMaster
          </p>
          {!authenticated && (
            <Link href="/signup">
              <Button
                size="lg"
                className="bg-rose-white text-seal-brown hover:bg-rose-white/90 font-semibold px-12 py-6 text-lg shadow-2xl hover:scale-105 transition-all duration-300"
              >
                Start Free Today
                <Sparkles className="ml-2 w-5 h-5" />
              </Button>
            </Link>
          )}
        </div>
      </section>

      {/* Footer */}
      <LandingFooter />
    </div>
  );
}
