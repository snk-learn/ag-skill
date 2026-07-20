---
name: react-frontend
description: >-
  Enforces React 19 + TypeScript conventions including Server vs Client
  Components, TanStack Query for data, Tailwind v4 styling, accessibility,
  and React Testing Library patterns. Use when generating or reviewing
  React (.tsx / .jsx) files or planning frontend architecture.
license: MIT
compatibility: React 19+, TypeScript 5.4+
metadata:
  author: Shariq Khan
  version: "1.0.0"
---

# React Frontend Standards

## Core rules
1. Function components only. TypeScript strict mode.
2. Default to Server Components; mark `"use client"` only when needed.
3. Data: TanStack Query on client, Server Actions for mutations. No `useEffect` for fetching.
4. State: `useState`/`useReducer` local, Zustand for shared.
5. Styling: Tailwind v4 with `@theme` tokens. Colocate `Component.tsx` + `.test.tsx`.
6. Forms: React Hook Form + Zod.
7. Testing: Vitest + RTL, prefer `getByRole` over `getByTestId`.
8. Accessibility: semantic HTML first, ARIA only when necessary.

## When to load references
- RSC decisions → `references/rsc-vs-client.md`
- A11y review → `references/a11y-checklist.md`
- New component → copy `assets/component-template.tsx`

## Definition of done
- Passes `tsc --noEmit`, ESLint clean, a11y tests pass