// 🧂 Tiny SSR-safe hooks for media queries. useSyncExternalStore = no tearing, no effects dance.
import { useSyncExternalStore } from "react";

export function useMediaQuery(query: string, serverFallback = false): boolean {
  return useSyncExternalStore(
    (onChange) => {
      const mql = window.matchMedia(query);
      mql.addEventListener("change", onChange);
      return () => mql.removeEventListener("change", onChange);
    },
    () => window.matchMedia(query).matches,
    () => serverFallback,
  );
}

/** true when the user asked the OS to reduce motion — swap movement for opacity, don't drop feedback. */
export const usePrefersReducedMotion = () => useMediaQuery("(prefers-reduced-motion: reduce)");

/** true on devices with a real hover pointer (mouse/trackpad) — gate hover-only affordances on this. */
export const useCanHover = () => useMediaQuery("(hover: hover) and (pointer: fine)");

/** Tailwind-default breakpoints; prefer CSS/container queries for layout, use this for behavior only. */
export const useIsDesktop = () => useMediaQuery("(min-width: 1024px)");
