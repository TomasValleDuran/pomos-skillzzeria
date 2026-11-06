# Components: API, States, Docs, Governance

## API conventions

| Prop | Meaning | Values (example) |
|---|---|---|
| `variant` | visual emphasis | `solid` (primary), `soft`, `outline`, `ghost`, `link` |
| `tone` (or `color`) | semantic intent, only if needed | `neutral`, `accent`, `danger`, `success` |
| `size` | dimensions tied to control-height tokens | `sm`, `md`, `lg` (avoid more than 3–4) |
| `asChild` / `render` | polymorphism / composition (Radix `asChild`, Base UI `render`) | element or component |
| state props | controlled/uncontrolled pairs | `open`/`defaultOpen`/`onOpenChange`, `value`/`defaultValue`/`onValueChange` |

- **Composition over configuration**: `<Card><CardHeader/><CardContent/></Card>` beats `<Card title subtitle footer actions …/>`. Compound components share context.
- **Style states with data attributes** set by primitives (`data-state="open"`, `data-disabled`, `data-highlighted`) instead of boolean class juggling.
- Forward refs, spread rest props onto the root, merge `className` (`cn()`), never swallow `aria-*` or event handlers.
- Typed variants with **cva** / **tailwind-variants**; export the variant types.
- Don't make `danger` a variant *and* a tone; one axis per concept.
- Name by function, not appearance (`Callout`, not `YellowBox`).

## State matrix (every interactive component)

| State | Visual | A11y |
|---|---|---|
| default | base tokens | correct role, accessible name |
| hover | one step of emphasis; pointer devices only (`@media (hover: hover)`) | — |
| active/pressed | darker/scale(0.97–0.98) | `aria-pressed` for toggles |
| focus-visible | 2px ring, 2px offset, ≥3:1 | keyboard reachable, logical order |
| disabled | reduced contrast, no hover | `disabled` or `aria-disabled` (keeps it focusable when it needs a tooltip explaining why) |
| loading | spinner/skeleton, keep width stable, block double submit | `aria-busy`, announce completion |
| error / invalid | danger border + message + icon | `aria-invalid`, `aria-describedby` → message |
| selected / checked | indicator beyond color | `aria-selected`/`aria-checked`/`aria-current` |
| read-only | looks like text, still selectable | `readonly` |
| empty | designed empty state (what + why + next action) | — |

Plus content stress: very long text, no text, huge numbers, RTL, 200% zoom / largest Dynamic Type. The `break`, `state-machine` and `variant` skills help render and stress-test states.

## Component inventory (typical order of building)

1. Primitives of the system: Text/Heading, Icon, Button, IconButton, Link, Stack/Inline/Grid (layout), Separator
2. Forms: Label, Input, Textarea, Select, Combobox, Checkbox, Radio, Switch, Slider, Field (label + control + description + error)
3. Feedback: Toast, Alert/Callout, Badge, Spinner, Skeleton, Progress, Empty state
4. Overlays: Dialog, Sheet/Drawer, Popover, Tooltip, Dropdown menu, Context menu, Command palette
5. Navigation: Tabs, Breadcrumbs, Pagination, Sidebar, Navbar, Bottom tabs (mobile)
6. Data: Table, List, Card, Avatar, Description list, Chart wrappers
7. Patterns (compositions): Page header, Settings section, Auth forms, Filters bar, Onboarding

## Documentation

Per component: purpose (one line), when to use / when not, anatomy, variants, sizes, states (rendered), props table, accessibility notes (keyboard map, roles), do/don't examples, related components. Tools: Storybook (de facto), Ladle, Histoire (Vue); for small projects, a single `/design` route that renders every component and state is enough and doubles as a visual test page.

`DESIGN.md` at repo root summarizes direction + tokens + inventory + rules for humans and AI agents. Keep it under ~200 lines; link out for detail.

## Testing

- Visual regression: Chromatic, Playwright screenshots, Lost Pixel.
- A11y: axe (via Storybook a11y addon, `@axe-core/playwright`), keyboard walkthroughs, screen reader spot checks (VoiceOver, NVDA, TalkBack).
- Interaction tests for complex components (Storybook play functions / Testing Library).

## Governance

- **Semver** for the package; changelog (Changesets). Breaking = renamed/removed token or prop, changed default.
- Deprecate before removal: `$deprecated` in DTCG, console warnings in dev, codemods for big changes.
- Contribution path: propose (issue) → design review → build with docs/states → a11y + visual tests → release.
- Detached/one-off components in product code are signals: either promote to the system or document as a local pattern.
- Measure adoption (grep imports, lint rules banning raw values: stylelint `declaration-strict-value`, ESLint tailwind plugin restrictions, `no-restricted-syntax` for hex literals).
