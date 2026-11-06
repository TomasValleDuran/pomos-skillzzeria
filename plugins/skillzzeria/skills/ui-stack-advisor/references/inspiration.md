# Inspiration & Tooling

Generic output comes from designing from memory. Look at real, excellent references for the specific screen type before designing — then extract principles (hierarchy, density, rhythm, motion), never copy.

## Reference libraries
| Source | What |
|---|---|
| **Mobbin** | Huge library of real iOS/Android/web app screens and flows, searchable by pattern (onboarding, paywall, settings…) |
| **Refero** | Web + iOS UI references with flows, good tagging |
| **Page Flows** | Recorded user flows (video) |
| **Godly**, **Land-book**, **Lapa Ninja**, **SaaS Landing Page**, **One Page Love** | Landing page galleries |
| **Awwwards**, **Siteinspire**, **Httpster** | Expressive/award-level web design |
| **Dribbble**, **Behance** | Concepts (often unrealistic — validate against real products) |
| **Collect UI**, **UI Garage** | Component-level inspiration |
| **Navbar Gallery**, **Footer Design**, **Empty States** galleries | Pattern-specific |
| **Apple HIG**, **Material 3** sites | Platform canon + component guidance |
| **Design systems gallery**: designsystemsrepo, Storybook showcase, Figma Community kits (Untitled UI, Shadcn kits, Apple/Material official kits) | How mature systems structure tokens/components |

Well-crafted products to study for product UI: Linear, Vercel, Stripe (dashboard + docs), Raycast, Arc/Dia, Notion, Things 3, Height, Cron/Notion Calendar, Craft, Superhuman, Figma, Framer, Family (wallet, for motion), Airbnb (mobile).

## Design tooling with AI agents
- **Figma MCP** (official): read designs/tokens/components into code, push code to Figma, Code Connect mapping. Use when a Figma file exists.
- **shadcn MCP / CLI**: browse and install registry items.
- **21st.dev Magic MCP**: generate components from a prompt.
- **Subframe inspiration MCP**: curated real-site references.
- **Playwright / Chrome DevTools MCP / Claude in Chrome**: render and screenshot the result at real breakpoints — always look at what you built.
- **v0**, **Lovable**, **Bolt**, **Figma Make**, **Google Stitch**: fast prototypes to explore directions; re-implement cleanly in the real stack.

## Typography & color tools
Typescale.com / Utopia (fluid type + space scales), Fontjoy (pairings), Realtime Colors, Huemint, Radix Colors, Material Theme Builder, Leonardo, oklch.com, tweakcn (shadcn theming). The `color-theory` skill's `palette.py` generates and verifies full systems locally.
