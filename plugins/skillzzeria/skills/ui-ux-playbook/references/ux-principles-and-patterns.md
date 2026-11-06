# UX Principles and Patterns

## Nielsen's 10 usability heuristics (use as a review lens; rate severity 0–4)

1. **Visibility of system status** — feedback within ~100ms; progress for waits; current location in nav.
2. **Match with the real world** — user's language, natural order, familiar metaphors.
3. **User control & freedom** — undo, cancel, back, escape; prefer undo over confirm dialogs for reversible actions.
4. **Consistency & standards** — internal (same thing looks/behaves the same) and external (platform conventions).
5. **Error prevention** — constraints, good defaults, confirmation only for destructive/irreversible actions.
6. **Recognition over recall** — visible options, recent items, autocomplete, inline hints.
7. **Flexibility & efficiency** — shortcuts, command palette, bulk actions, saved filters for experts; invisible to novices.
8. **Aesthetic & minimalist design** — every element competes for attention; remove what doesn't serve the task.
9. **Help users recover from errors** — plain language, precise problem, constructive fix, preserve input.
10. **Help & documentation** — contextual, searchable, task-focused; empty states and tooltips as micro-docs.

## Laws of UX (lawsofux.com) — the ones that change designs

| Law | Implication |
|---|---|
| **Fitts's law** | Big, close targets are faster: primary actions large and near the thumb/cursor; edges/corners are infinitely large on desktop. |
| **Hick's law** | More choices → slower decisions: progressive disclosure, sensible defaults, highlight the recommended option. |
| **Jakob's law** | Users spend most time on *other* products: follow conventions (logo top-left → home, cart top-right, search icon = magnifier). |
| **Miller / chunking** | Group information (phone numbers, card numbers, form sections); don't rely on memory across steps. |
| **Tesler's law** | Complexity is conserved: absorb it in the system (smart defaults, auto-detect), not the user. |
| **Doherty threshold** | Keep interactions < 400ms or show progress; optimistic updates. |
| **Peak-end rule** | Design the best moment and the ending (success states, completion screens). |
| **Aesthetic-usability effect** | Beautiful UIs are perceived as easier — and forgiven more. Polish matters. |
| **Von Restorff** | The distinct item is remembered: use emphasis for one thing only. |
| **Serial position** | First and last items are remembered: put key nav items at the ends. |
| **Goal-gradient** | Progress indicators motivate completion (checklists, steppers). |
| **Zeigarnik** | Incomplete tasks are remembered: show onboarding progress, drafts. |
| **Gestalt** (proximity, similarity, common region, continuity, closure) | Grouping via spacing and containers communicates structure without lines. |
| **Postel's law** | Be liberal in what you accept (input formats), conservative in what you output. |

## Patterns

### Forms
- One column; labels above inputs; group related fields with headings.
- Visible labels always (placeholders are examples, not labels). Mark optional *or* required, whichever is rarer.
- Correct `type`, `inputmode`, `autocomplete`; accept flexible formats and normalize (spaces in card numbers, phone formats).
- Validate on blur (not on every keystroke), show success sparingly, errors inline next to the field + summary at top for long forms, focus first error on submit.
- Preserve all input on error. Never clear password fields unnecessarily; never block paste.
- Primary button names the outcome ("Create project"), stays enabled until submit starts, then shows progress; prevent double submit.
- Long forms: multi-step with progress and save-as-you-go.

### Navigation
- Web apps: sidebar for 5+ sections, top nav for ≤5; breadcrumbs for deep hierarchies; URL reflects state (tabs, filters, pagination).
- Mobile: bottom tab bar (iOS) / navigation bar (Android) for 3–5 top-level destinations; stack navigation within; avoid hamburger for primary destinations.
- Always show where you are (active state not by color alone), and how to get back.
- Command palette (⌘K) for power users in productivity tools.

### Search & filtering
- Search box visible where search is primary; show recent and suggested queries; tolerate typos.
- Filters: show applied filters as removable chips, show result counts, keep filters in the URL, "clear all".
- No results: say what was searched, suggest fixes (spelling, fewer filters), offer alternatives.

### Tables & data
- Left-align text, right-align numbers (tabular figures), consistent decimal places, units in headers.
- Sticky header, sortable columns with indicator, row hover, selection with bulk actions bar.
- Density toggle for power users; virtualize large data; responsive: cards or priority columns on mobile, not horizontal scrolling of 12 columns.

### States
- **Loading**: skeletons that mirror layout for content; inline spinners for actions; avoid full-page spinners; never shift layout when content arrives.
- **Empty**: explain what goes here, why it's empty, and the primary action to fill it (first-run vs no-results vs cleared are different empty states).
- **Error**: what happened, why (if known), what to do; retry action; keep context; log details for support but don't show stack traces.
- **Partial/degraded**: offline banners, stale data indicators, partial failures in lists.
- **Success**: confirm briefly (toast) for background actions; dedicated screen only for meaningful completions (peak-end).

### Feedback & notifications
- Toasts: brief, non-critical, auto-dismiss (≥ 4–6s; pause on hover/focus), with undo when reversible; announce via live region. Errors that need action are not toasts.
- Inline messages for contextual info; banners for system-wide status; modals only for decisions that block progress.

### Destructive actions
- Prefer undo (soft delete + toast) over confirmation. When confirming, name the object and consequence ("Delete 'Q3 report'? This can't be undone."), destructive button styled as danger and labeled with the verb, for high-stakes require typing the name.

### Onboarding
- Get users to the "aha" moment fast; defer account creation when possible; progressive disclosure over upfront tours; checklists with progress; sample data in empty states; ask permissions in context (just before needed, with explanation).

### Settings
- Group by user mental model, not system architecture; search for large settings; changes apply immediately (with confirmation toast) unless risky; explain consequences inline.

### Microcopy
- Buttons: verb + object ("Save changes"), not "OK/Submit". Consistent terms (don't mix "delete/remove/trash" for the same action).
- Errors: human, specific, no blame, include the fix. Avoid jargon and codes for end users.
- Sentence case for UI text is the modern default (Title Case is a valid house style — pick one).

### Internationalization
- No concatenated strings; ICU message format for plurals/gender; room for +30–40% text expansion (German, Finnish); CSS logical properties (`margin-inline-start`) and `dir="auto"` for RTL; `Intl` for dates, numbers, currency, lists; don't flag-icon languages; locale ≠ language ≠ country.
