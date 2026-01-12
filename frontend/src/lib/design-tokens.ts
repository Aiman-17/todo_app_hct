/**
 * Design Tokens for Premium Minimalist UI
 *
 * Centralized design system constants for colors, spacing, shadows, and animations.
 * Use these tokens throughout the application for consistent visual design.
 */

/**
 * Color Palette
 */
export const colors = {
  // Primary brand colors
  roseWhite: "#F5EDE6", // Updated from #FFF0EB
  sealBrown: "#2D0B00",

  // Priority indicators
  priority: {
    high: "#9C1F1F",
    medium: "#FFB8A6",
    low: "#FFE5DB",
  },

  // Status colors
  status: {
    active: "#2D0B00",
    completed: "#8B7E77",
    overdue: "#9C1F1F",
  },
} as const;

/**
 * Typography
 */
export const typography = {
  fontFamily: {
    sans: "var(--font-inter), -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
  },
  fontSize: {
    xs: "0.75rem",    // 12px
    sm: "0.875rem",   // 14px
    base: "1rem",     // 16px
    lg: "1.125rem",   // 18px
    xl: "1.25rem",    // 20px
    "2xl": "1.5rem",  // 24px
    "3xl": "1.875rem", // 30px
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  lineHeight: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75,
  },
} as const;

/**
 * Spacing
 */
export const spacing = {
  xs: "0.25rem",   // 4px
  sm: "0.5rem",    // 8px
  md: "1rem",      // 16px
  lg: "1.5rem",    // 24px
  xl: "2rem",      // 32px
  "2xl": "3rem",   // 48px
  "3xl": "4rem",   // 64px
} as const;

/**
 * Border Radius
 */
export const borderRadius = {
  none: "0",
  sm: "0.25rem",   // 4px
  md: "0.5rem",    // 8px
  lg: "0.75rem",   // 12px
  xl: "1rem",      // 16px
  full: "9999px",
} as const;

/**
 * Shadows - Soft, subtle elevations
 */
export const shadows = {
  none: "none",
  sm: "0 1px 2px 0 rgba(45, 11, 0, 0.05)",
  md: "0 4px 6px -1px rgba(45, 11, 0, 0.1), 0 2px 4px -1px rgba(45, 11, 0, 0.06)",
  lg: "0 10px 15px -3px rgba(45, 11, 0, 0.1), 0 4px 6px -2px rgba(45, 11, 0, 0.05)",
  xl: "0 20px 25px -5px rgba(45, 11, 0, 0.1), 0 10px 10px -5px rgba(45, 11, 0, 0.04)",
  inner: "inset 0 2px 4px 0 rgba(45, 11, 0, 0.06)",
} as const;

/**
 * Transitions - Smooth, calm animations
 */
export const transitions = {
  fast: "150ms cubic-bezier(0.4, 0, 0.2, 1)",
  base: "200ms cubic-bezier(0.4, 0, 0.2, 1)",
  slow: "300ms cubic-bezier(0.4, 0, 0.2, 1)",
  slowest: "500ms cubic-bezier(0.4, 0, 0.2, 1)",
} as const;

/**
 * Z-Index Layers
 */
export const zIndex = {
  base: 0,
  dropdown: 10,
  sticky: 20,
  modal: 30,
  popover: 40,
  tooltip: 50,
} as const;

/**
 * Breakpoints (matches Tailwind defaults)
 */
export const breakpoints = {
  sm: "640px",
  md: "768px",
  lg: "1024px",
  xl: "1280px",
  "2xl": "1536px",
} as const;

/**
 * Layout constraints
 */
export const layout = {
  maxWidth: {
    sm: "640px",
    md: "768px",
    lg: "1024px",
    xl: "1280px",
    "2xl": "1536px",
    full: "100%",
  },
  sidebar: {
    collapsed: "4rem",   // 64px (icon-only)
    expanded: "16rem",   // 256px (with labels)
  },
  header: {
    height: "4rem",      // 64px
  },
} as const;

/**
 * Icon sizes
 */
export const iconSize = {
  xs: "1rem",    // 16px
  sm: "1.25rem", // 20px
  md: "1.5rem",  // 24px
  lg: "2rem",    // 32px
  xl: "2.5rem",  // 40px
} as const;

/**
 * Touch targets (minimum 44px for accessibility)
 */
export const touchTarget = {
  min: "44px",
} as const;

/**
 * Animation keyframes
 */
export const animations = {
  pulse: {
    from: { opacity: 1 },
    "50%": { opacity: 0.5 },
    to: { opacity: 1 },
  },
  fadeIn: {
    from: { opacity: 0 },
    to: { opacity: 1 },
  },
  fadeOut: {
    from: { opacity: 1 },
    to: { opacity: 0 },
  },
  slideInRight: {
    from: { transform: "translateX(100%)" },
    to: { transform: "translateX(0)" },
  },
  slideInLeft: {
    from: { transform: "translateX(-100%)" },
    to: { transform: "translateX(0)" },
  },
  scaleIn: {
    from: { transform: "scale(0.95)", opacity: 0 },
    to: { transform: "scale(1)", opacity: 1 },
  },
  scaleOut: {
    from: { transform: "scale(1)", opacity: 1 },
    to: { transform: "scale(0.95)", opacity: 0 },
  },
} as const;

/**
 * Helper function to get priority color
 */
export function getPriorityColor(priority: "high" | "medium" | "low"): string {
  return colors.priority[priority];
}

/**
 * Helper function to check if user prefers reduced motion
 */
export function prefersReducedMotion(): boolean {
  if (typeof window === "undefined") return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/**
 * Helper function to apply transition with reduced motion check
 */
export function transition(speed: keyof typeof transitions = "base"): string {
  if (prefersReducedMotion()) return "none";
  return transitions[speed];
}
