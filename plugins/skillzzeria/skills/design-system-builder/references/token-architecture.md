# Token Architecture

## Tiers

| Tier | Purpose | Example | Who consumes it |
|---|---|---|---|
| **Primitive** (global, core, reference) | The palette of possible values | `color.violet.600`, `space.4`, `font.size.16`, `duration.200` | Only semantic tokens |
| **Semantic** (alias, system) | Decisions: which value serves which job | `color.text.muted`, `color.accent.default`, `space.inset.md`, `radius.control` | Components, layouts |
| **Component** (optional) | Per-component overrides for theming flexibility | `button.primary.bg`, `card.padding` | That component |

Rules:
- Components **never** reference primitives. That seam is what allows themes.
- Only add component tokens when a component genuinely needs independent theming (e.g. a white-label product). Otherwise they're indirection without value.
- A token is used **only in its role**. Don't borrow `border` color for text because the value happens to match today.
- If a role is missing, add a token; don't reach for a primitive.

## Naming grammar

`[namespace]-[category]-[concept/role]-[variant]-[state]`

```
--color-bg               --color-bg-subtle         --color-surface-raised
--color-text             --color-text-muted        --color-text-inverse
--color-border           --color-border-strong     --color-border-control
--color-accent           --color-accent-hover      --color-accent-fg       --color-accent-subtle
--color-danger           --color-danger-text       --color-danger-subtle
--space-1 … --space-16   --space-inset-sm|md|lg    --space-stack-*         --space-inline-*
--radius-sm|md|lg|full   --radius-control          --radius-container
--font-sans|serif|mono   --text-body|label|caption|h1… (composite)
--shadow-sm|md|lg        --z-dropdown|modal|toast
--duration-fast|base|slow   --ease-out|in-out|spring
```

Avoid: hue names in semantic tokens (`--color-blue-button`), component names in global semantics (`--color-sidebar-gray`), `primary` meaning two things (`--color-primary` the brand vs `--color-text-primary` — rename brand to `accent`).

Evocative primitive names (`--ink`, `--paper`, `--ember`) are a valid stylistic choice for brand-heavy products; semantic tier still names jobs.

## DTCG format (Design Tokens Format Module 2025.10 — first stable version, Oct 2025)

Key rules:
- Token = object with `$value`; optional `$type`, `$description`, `$deprecated`, `$extensions`.
- Groups are plain objects; `$type` on a group is inherited by children.
- Aliases: `"{group.subgroup.token}"` (curly-brace path).
- Names can't start with `$` or contain `{`, `}`, `.`.

Core types and value shapes:

```json
{
  "color": {
    "$type": "color",
    "violet": {
      "600": { "$value": { "colorSpace": "oklch", "components": [0.491, 0.241, 292.6], "hex": "#6d28d9" } }
    },
    "accent": { "$value": "{color.violet.600}", "$description": "Primary interactive color" }
  },
  "space": {
    "$type": "dimension",
    "4": { "$value": { "value": 16, "unit": "px" } }
  },
  "duration": { "$type": "duration", "base": { "$value": { "value": 200, "unit": "ms" } } },
  "ease": { "$type": "cubicBezier", "out": { "$value": [0.23, 1, 0.32, 1] } },
  "font": {
    "family": { "$type": "fontFamily", "sans": { "$value": ["Inter", "system-ui", "sans-serif"] } },
    "weight": { "$type": "fontWeight", "semibold": { "$value": 600 } }
  },
  "shadow": {
    "md": { "$type": "shadow", "$value": {
      "color": "{color.shadow}", "offsetX": {"value":0,"unit":"px"}, "offsetY": {"value":4,"unit":"px"},
      "blur": {"value":12,"unit":"px"}, "spread": {"value":-2,"unit":"px"} } }
  },
  "text": {
    "body": { "$type": "typography", "$value": {
      "fontFamily": "{font.family.sans}", "fontSize": {"value":16,"unit":"px"},
      "fontWeight": 400, "lineHeight": 1.5, "letterSpacing": {"value":0,"unit":"px"} } }
  }
}
```

Other types: `number`, `strokeStyle`, `border`, `transition`, `gradient`. Many tools still accept older string values (`"#6d28d9"`, `"16px"`) — check the tool's DTCG version support. The `color-theory` script emits the 2025.10 structured color format with hex fallback.

## Modes / themes

DTCG has no native "modes" yet. Common, tool-friendly patterns:
1. **One file per mode**, same token paths: `tokens/semantic.light.json`, `tokens/semantic.dark.json`; build tool emits `:root{}` and `.dark{}` (or separate platform outputs).
2. **Resolver/sets** (Tokens Studio sets, Terrazzo modes via `$extensions`) when the tool supports it.

Theme axes to anticipate (only build the ones you need): color scheme (light/dark), contrast (default/high), brand (white-label), density (comfortable/compact), platform (web/iOS/Android differences).

## Where tokens live

| Project size | Source of truth |
|---|---|
| Single web app | `app/globals.css` (`@theme` + `:root` / `.dark` vars) |
| Web + mobile / several apps | `packages/tokens/` DTCG JSON → generated outputs, committed or built in CI |
| Design-led org | Figma Variables ↔ DTCG (via Tokens Studio, Figma's native export, or the Figma MCP), code is generated |

Never hand-edit generated files; edit the source.
