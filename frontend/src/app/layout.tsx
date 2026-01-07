/**
 * Root layout component for Next.js App Router.
 *
 * Wraps all pages with:
 * - HTML structure
 * - Global CSS (Tailwind + shadcn/ui theme)
 * - Font configuration (Inter)
 * - Toast notification provider
 */
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";
import { ConditionalHeader } from "@/components/layout/ConditionalHeader";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Todo Application",
  description: "Full-stack todo application with authentication and user isolation",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans antialiased`}>
        <ConditionalHeader />
        {children}
        <Toaster />
      </body>
    </html>
  );
}
