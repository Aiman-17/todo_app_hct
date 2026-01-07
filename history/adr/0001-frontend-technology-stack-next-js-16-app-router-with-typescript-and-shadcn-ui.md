# ADR-0001: Frontend Technology Stack - Next.js 16 App Router with TypeScript and shadcn/ui

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-30
- **Feature:** 002-fullstack-web-auth
- **Context:** Phase II requires a production-grade web frontend with user authentication, responsive design, and interactive task management. The frontend must consume a RESTful backend API without direct database access.

## Decision

**Adopt Next.js 16+ App Router with TypeScript 5+, Tailwind CSS, shadcn/ui, and Better Auth React SDK as the integrated frontend technology stack.**

Stack Components:
- **Framework:** Next.js 16+ (App Router mandatory, not Pages Router)
- **Language:** TypeScript 5+ with strict mode enabled
- **Styling:** Tailwind CSS 3.4+ (utility-first CSS framework)
- **Component Library:** shadcn/ui (Radix UI primitives + Tailwind components)
- **Icons:** lucide-react
- **Authentication:** Better Auth React SDK (@better-auth/react)
- **Runtime:** Node.js 20+ with React 19+
- **State Management:** React Context + Server Components (no Redux/Zustand needed for MVP)
- **Form Handling:** Controlled components with Pydantic-validated backend schemas

## Consequences

### Positive

- **Server Components by Default:** Next.js 16 App Router enables server-side rendering for faster initial page loads, reducing client-side JavaScript bundle size.
- **Type Safety:** TypeScript strict mode + Pydantic backend schemas provide end-to-end type safety from API to UI.
- **Integrated Tooling:** Next.js provides built-in routing, middleware, API routes, and hot reload without configuration.
- **Responsive UI Out-of-the-Box:** Tailwind CSS + shadcn/ui components are mobile-first and accessible by default (Radix UI ARIA primitives).
- **No Component Library Lock-In:** shadcn/ui copies components into project source, allowing full customization without dependency bloat.
- **Authentication SDK Integration:** Better Auth React SDK provides automatic token refresh, httpOnly cookie management, and session handling aligned with backend.
- **Developer Experience:** Excellent DX with hot reload, TypeScript IntelliSense, and Tailwind IntelliSense extensions.
- **Future-Proof:** Next.js 16 App Router is the current stable architecture (Pages Router is legacy), ensuring long-term support and ecosystem compatibility.

### Negative

- **Learning Curve:** App Router introduces Server Components vs Client Components mental model, requiring team to understand when to use `"use client"` directive.
- **Framework Coupling:** Next.js conventions (app/ directory, middleware.ts, layout.tsx) tightly couple code to framework (migration to Remix/Astro would require significant refactoring).
- **Build Complexity:** Next.js build process is more complex than vanilla React (requires understanding of SSR, hydration, and caching strategies).
- **shadcn/ui Maintenance:** Components are copied into project, requiring manual updates when shadcn/ui releases new versions (tradeoff for customization control).
- **Tailwind CSS Verbosity:** Utility classes can become verbose in JSX (mitigated by extracting reusable components).

## Alternatives Considered

### Alternative Stack A: Remix + styled-components + Netlify
- **Components:** Remix (SSR framework), styled-components (CSS-in-JS), Netlify (deployment), Better Auth React SDK
- **Pros:** Remix has excellent data loading patterns (loaders/actions), styled-components provide scoped CSS, Netlify has generous free tier.
- **Cons:** Smaller ecosystem than Next.js (fewer tutorials/libraries), styled-components add runtime overhead, Remix App Router is less mature than Next.js 16.
- **Why Rejected:** Next.js has larger community, better TypeScript support, and shadcn/ui is designed specifically for Tailwind (not styled-components).

### Alternative Stack B: Vite + React + Material-UI (MUI) + Vanilla CSS
- **Components:** Vite (build tool), React 19, Material-UI v6 (component library), vanilla CSS modules, Better Auth React SDK
- **Pros:** Vite has faster build times, MUI provides comprehensive component library, no framework lock-in (vanilla React).
- **Cons:** No SSR/SSG out-of-the-box (requires manual setup with Vite SSR plugin), MUI is heavier (larger bundle size), less control over component styling, routing requires manual setup (React Router).
- **Why Rejected:** Lack of SSR for initial page load performance, MUI bundle size exceeds shadcn/ui lightweight approach, manual routing setup increases boilerplate.

### Alternative Stack C: SvelteKit + TailwindCSS + Skeleton UI
- **Components:** SvelteKit (Svelte framework), Tailwind CSS, Skeleton UI (Svelte component library), Better Auth SDK (requires custom integration)
- **Pros:** Svelte compiles to vanilla JS (smaller bundles), SvelteKit has excellent SSR support, Skeleton UI provides Tailwind-based components for Svelte.
- **Cons:** Smaller ecosystem than React, Better Auth SDK requires custom integration (no official Svelte SDK), team lacks Svelte experience, fewer third-party libraries.
- **Why Rejected:** React ecosystem maturity (larger talent pool, more libraries), Better Auth has first-class React support, team familiarity with React reduces onboarding time.

## References

- Feature Spec: `specs/002-fullstack-web-auth/spec.md` (FR-014 to FR-020, FR-025 for responsive UI)
- Implementation Plan: `specs/002-fullstack-web-auth/plan.md` (Technical Context section, Project Structure frontend/)
- Research: `specs/002-fullstack-web-auth/research.md` (Section 3: Next.js 16 App Router Patterns, Section 5: shadcn/ui)
- Related ADRs: ADR-0003 (Authentication Architecture - Frontend uses Better Auth React SDK)
- OpenAPI Contract: `specs/002-fullstack-web-auth/contracts/openapi.yaml` (defines API endpoints frontend consumes)
