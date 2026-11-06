# Building Blocks — specialized widgets (snapshot Nov 2026)

Default = first listed. Prefer what the chosen kit already provides (e.g. Mantine dates, MUI X pickers, shadcn calendar) before adding a library.

## Icons
| Set | Notes |
|---|---|
| **Lucide** | shadcn default, 1.5k+ consistent stroke icons, every framework + RN |
| **Phosphor** | 6 weights (thin→fill, duotone) — great for expressive brands |
| **Tabler** | 5k+ stroke icons |
| **Heroicons** | Tailwind Labs, small and refined |
| **Hugeicons** | Very large set, multiple styles (free + pro) |
| **Material Symbols** | Variable font (fill, weight, grade, optical size) — Android/Material |
| **SF Symbols** | iOS/macOS native (`expo-symbols` in RN); use them on Apple platforms |
| **Iconify** | Meta-library: 200k+ icons from all sets, on-demand |
Rules: one family per product; match stroke width to text weight; icon-only buttons need accessible labels; never emoji as UI icons.

## Fonts (free, high quality)
UI sans: Inter (and Inter Display), Geist, IBM Plex Sans, Manrope, Figtree, DM Sans, Plus Jakarta Sans, Public Sans, Instrument Sans, Onest, Schibsted Grotesk. Display/editorial: Fraunces, Instrument Serif, Newsreader, Playfair, Bricolage Grotesque, Space Grotesk, Syne, Unbounded. Mono: Geist Mono, JetBrains Mono, IBM Plex Mono, Berkeley Mono (paid). Sources: Google Fonts, Fontshare (free quality grotesks: Satoshi, General Sans, Cabinet Grotesk, Clash Display), Fontsource (npm self-hosting). System stacks are a valid choice for tools. Native: SF Pro (iOS default), Roboto/Google Sans Flex (Android).

## Charts
| Library | Notes |
|---|---|
| **Recharts 3** | SVG, React-idiomatic; powers shadcn charts |
| **Tremor** (Vercel) | Dashboard components on Recharts + Tailwind, copy-in |
| **visx** (Airbnb) | Low-level D3 + React primitives for custom viz |
| **Nivo** | Many chart types, SVG/Canvas |
| **Apache ECharts** | Canvas, huge datasets, very complete |
| **Observable Plot** / D3 | Exploratory, custom |
| **uPlot** | Tiny, fast time series |
| **MUI X Charts**, **Mantine Charts** | If already on those kits |
| **Liveline** | Real-time streaming lines |
Pair with the `dataviz` skill for chart design.

## Tables & data grids
TanStack Table (headless, default), TanStack Virtual for rows; AG Grid (enterprise grids, community + paid), MUI X Data Grid, Glide Data Grid (canvas, millions of cells).

## Forms & validation
React Hook Form (default) or TanStack Form; schema with Zod 4 / Valibot / ArkType (Standard Schema compatible); Conform for server actions/progressive enhancement. Inputs: input-otp (OTP), react-phone-number-input, `@internationalized/date` (via React Aria) for locale-aware dates.

## Dates & calendars
react-day-picker (shadcn calendar), React Aria DatePicker/Calendar (best a11y + i18n), Mantine Dates, MUI X Date Pickers. Big calendars: Schedule-X, FullCalendar, MUI X Scheduler (alpha). Date math: date-fns, Temporal (polyfill) / Day.js.

## Overlays & feedback
Toasts: **Sonner** (web), sonner-native / Burnt (RN). Command palette: **cmdk**. Drawers/sheets (web): Base UI/Radix dialog-based sheets; Vaul (check maintenance status first). Tooltips/popovers: from primitives (Floating UI underneath).

## Drag & drop
dnd kit (`@dnd-kit/react` new API or `@dnd-kit/core`), **Pragmatic drag and drop** (Atlassian; replaces react-beautiful-dnd), React Aria DnD (most accessible), SortableJS (vanilla). RN: react-native-reanimated-dnd / sortable libs built on Reanimated + Gesture Handler.

## Virtualization
TanStack Virtual (headless), Virtuoso (batteries-included, chat/reverse lists), virtua (tiny). RN: FlashList, LegendList.

## Rich text & editors
Tiptap (ProseMirror; extensible, collab), Lexical (Meta), Plate (shadcn-styled Slate), BlockNote (Notion-like), Milkdown (markdown). Code editors: CodeMirror 6, Monaco. Syntax highlighting: Shiki.

## Carousels, media, misc
Embla Carousel (shadcn carousel), Swiper (feature-rich), Keen Slider. Media: Vidstack / Media Chrome. Maps: MapLibre GL, react-map-gl, Mapbox. Confetti: canvas-confetti. QR: qrcode / react-qr-code. OG images: Satori / `next/og`. Resizable panels: react-resizable-panels. Color picker: react-colorful. File upload: Uppy, react-dropzone, FilePond. State: Zustand, Jotai, TanStack Query (server state), nuqs (URL state). Theme switching: next-themes.

## AI / chat interfaces
shadcn **AI Elements** (copy-in chat/agent UI patterns: messages, prompt input, tool calls, reasoning, code blocks; replaces deprecated AI SDK Elements), Vercel AI SDK UI hooks, assistant-ui, CopilotKit. MUI X Chat (alpha).
