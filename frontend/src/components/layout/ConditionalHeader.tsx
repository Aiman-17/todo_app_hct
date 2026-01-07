"use client";

/**
 * Conditional Header Component
 *
 * Shows the Header only on non-dashboard routes.
 * Dashboard routes have their own layout with Sidebar/CommandBar/FAB.
 */

import { usePathname } from "next/navigation";
import { Header } from "./Header";

export function ConditionalHeader() {
  const pathname = usePathname();

  // Don't show header on dashboard routes (they have their own layout)
  if (pathname.startsWith("/dashboard")) {
    return null;
  }

  return <Header />;
}
