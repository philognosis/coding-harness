---
paths:
  - "**/*.{ts,tsx}"
  - "**/next.config.*"
  - "**/globals.css"
  - "**/tailwind.config.*"
---

# UI standards (Next.js + Tailwind)

## Scaffolding a new UI

- Use `pnpm create next-app@latest <repo>-ui` (or `-dashboard` / `-app`, whichever
  fits). `@latest` is the current stable release; never a canary.
- Options: TypeScript yes, ESLint yes, Tailwind yes, App Router yes, pnpm as the
  package manager. For the `src/` directory and anything else optional, take the
  command's recommended default.
- Tailwind must be enabled at creation so `globals.css` is generated.
- `next.config.ts` sets `output: "standalone"`.

## Theme

- Dark is the default theme. The root `<html>` carries the dark class or data
  attribute, and colour tokens in `globals.css` are defined dark-first.
- Use theme tokens, never hard-coded hex values in components.

## Code

- Write for a passing `pnpm build` from the first line: no unused imports or
  variables, no implicit `any`, no unescaped entities, every hook dependency listed.
- Server Components by default. Add `"use client"` only to the leaf that needs
  state, effects or browser APIs.
- Data fetching lives in server components or route handlers. API base URLs come
  from environment variables documented in `.env.example`.
- One component per file, named exports, props typed with an explicit `type`.
- Every interactive element is keyboard-reachable and has an accessible name.

## Before you say done

- `pnpm lint`, `pnpm exec tsc --noEmit` and `pnpm build` all pass.
