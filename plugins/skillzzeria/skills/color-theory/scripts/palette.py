#!/usr/bin/env python3
"""
palette.py — zero-dependency color toolkit for UI work (Python 3.8+).

Everything is computed in OKLab/OKLCH (perceptually uniform) and gamut-mapped
to sRGB so every value it prints is renderable on every screen.

Commands
  convert  <color>                       hex / rgb / hsl / oklch for one color
  contrast <fg> <bg>                     WCAG 2.x ratio + pass levels, APCA Lc
  ramp     <color> [--name N]            11-step ramp (50..950) holding the hue
  neutral  <color> [--tint 0.012]        tinted gray ramp from a brand hue
  harmony  <color> [--scheme S]          complementary|analogous|triadic|split|tetradic
  cvd      <color> [<color> ...]         color-vision-deficiency simulation + confusable pairs
  system   <color> [--neutral-tint T]    full starter system: accent, neutral and status
                                         ramps + light/dark semantic tokens, every text
                                         pair verified (auto-moves along the ramp to pass)

Common flags
  --format table|css|tailwind|json       (ramp, neutral, system)   default: table
  --notation oklch|hex                   value notation in css/tailwind output (default oklch)
  --no-anchor                            ramp: don't snap the nearest step to the exact input
  --hue-shift DEG                        ramp: drift hue across the dark steps (yellow: -15)

Colors accepted: #rgb, #rrggbb, rgb(r g b), oklch(L C H) with L in 0..1 or %.

Examples
  python3 palette.py system "#6d28d9" --format css > tokens.css
  python3 palette.py contrast "#ffffff" "#7c3aed"
  python3 palette.py cvd "#16a34a" "#dc2626" "#2563eb"
"""
import argparse
import json
import math
import re
import sys

# ---------------------------------------------------------------- conversions

def _srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c):
    if c <= 0.0031308:
        return 12.92 * c
    return 1.055 * (c ** (1 / 2.4)) - 0.055


def linear_rgb_to_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def oklab_to_linear_rgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def oklch_to_oklab(L, C, H):
    h = math.radians(H)
    return L, C * math.cos(h), C * math.sin(h)


def oklab_to_oklch(L, a, b):
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360
    return L, C, H


class Color:
    """Stored as gamma-encoded sRGB floats 0..1."""

    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b

    # -- constructors
    @classmethod
    def parse(cls, s):
        s = s.strip().lower()
        m = re.fullmatch(r"#?([0-9a-f]{3}|[0-9a-f]{6})", s)
        if m:
            h = m.group(1)
            if len(h) == 3:
                h = "".join(ch * 2 for ch in h)
            return cls(*(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)))
        m = re.fullmatch(r"rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+).*\)", s)
        if m:
            return cls(*(float(v) / 255 for v in m.groups()))
        m = re.fullmatch(r"oklch\(\s*([\d.]+)(%?)\s+([\d.]+)\s+([\d.]+)(?:deg)?\s*(?:/.*)?\)", s)
        if m:
            L = float(m.group(1)) / (100 if m.group(2) else 1)
            return cls.from_oklch(L, float(m.group(3)), float(m.group(4)))
        raise ValueError(f"Can't parse color: {s!r}")

    @classmethod
    def from_oklch(cls, L, C, H):
        """Gamut-map into sRGB by reducing chroma (keeps L and H fixed)."""
        L = min(max(L, 0.0), 1.0)
        if not in_gamut(L, C, H):
            lo, hi = 0.0, C
            for _ in range(30):
                mid = (lo + hi) / 2
                if in_gamut(L, mid, H):
                    lo = mid
                else:
                    hi = mid
            C = lo
        lr, lg, lb = oklab_to_linear_rgb(*oklch_to_oklab(L, C, H))
        return cls(*(min(max(_linear_to_srgb(max(v, 0.0)), 0.0), 1.0) for v in (lr, lg, lb)))

    # -- views
    @property
    def linear(self):
        return tuple(_srgb_to_linear(v) for v in (self.r, self.g, self.b))

    @property
    def oklab(self):
        return linear_rgb_to_oklab(*self.linear)

    @property
    def oklch(self):
        return oklab_to_oklch(*self.oklab)

    @property
    def hex(self):
        return "#" + "".join(f"{round(v * 255):02x}" for v in (self.r, self.g, self.b))

    @property
    def rgb255(self):
        return tuple(round(v * 255) for v in (self.r, self.g, self.b))

    @property
    def hsl(self):
        r, g, b = self.r, self.g, self.b
        mx, mn = max(r, g, b), min(r, g, b)
        l = (mx + mn) / 2
        if mx == mn:
            return 0.0, 0.0, l * 100
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        return h * 60, s * 100, l * 100

    def css_oklch(self):
        L, C, H = self.oklch
        if C < 0.0005:
            return f"oklch({L * 100:.1f}% 0 0)"
        return f"oklch({L * 100:.1f}% {C:.3f} {H:.1f})"

    def css(self, notation):
        return self.hex if notation == "hex" else self.css_oklch()


def in_gamut(L, C, H, eps=1e-6):
    rgb = oklab_to_linear_rgb(*oklch_to_oklab(L, C, H))
    return all(-eps <= v <= 1 + eps for v in rgb)


def max_chroma(L, H):
    lo, hi = 0.0, 0.4
    for _ in range(28):
        mid = (lo + hi) / 2
        if in_gamut(L, mid, H):
            lo = mid
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------- contrast

def relative_luminance(c):
    r, g, b = c.linear
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def wcag_ratio(fg, bg):
    a, b = relative_luminance(fg), relative_luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def apca_lc(txt, bg):
    """APCA-W3 0.0.98G-4g. Positive = dark text on light bg; negative = light on dark."""
    def y(c):
        r, g, b = c.r, c.g, c.b
        Y = 0.2126729 * r ** 2.4 + 0.7151522 * g ** 2.4 + 0.0721750 * b ** 2.4
        return Y + (0.022 - Y) ** 1.414 if Y < 0.022 else Y

    yt, yb = y(txt), y(bg)
    if abs(yb - yt) < 0.0005:
        return 0.0
    if yb > yt:
        sapc = (yb ** 0.56 - yt ** 0.57) * 1.14
        out = 0.0 if sapc < 0.1 else sapc - 0.027
    else:
        sapc = (yb ** 0.65 - yt ** 0.62) * 1.14
        out = 0.0 if sapc > -0.1 else sapc + 0.027
    return out * 100


def wcag_levels(ratio):
    return {
        "AA body (4.5)": ratio >= 4.5,
        "AA large/UI (3.0)": ratio >= 3.0,
        "AAA body (7.0)": ratio >= 7.0,
    }


def apca_hint(lc):
    a = abs(lc)
    if a >= 90:
        return "preferred for body text"
    if a >= 75:
        return "minimum for body text"
    if a >= 60:
        return "ok for large/bold text and UI labels"
    if a >= 45:
        return "headlines / large text only"
    if a >= 30:
        return "non-text UI, placeholders, disabled at best"
    return "insufficient for anything readable"


# ---------------------------------------------------------------- ramps

STEPS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
# Target OKLCH lightness per step. Finer at the light end (where the eye is
# most sensitive and UI backgrounds live), 500 sits near mid-gray, 950 is a
# deep shade usable as a dark-mode background.
TARGET_L = [0.975, 0.945, 0.895, 0.825, 0.735, 0.645, 0.565, 0.490, 0.420, 0.355, 0.265]
# Chroma as a share of (seed's relative vividness × the gamut max at that L/H).
# The sRGB gamut already narrows toward white, so the light end stays high in
# relative terms; the dark end tapers so shades don't go muddy/neon.
CHROMA_SHAPE = [0.85, 0.82, 0.80, 0.85, 0.92, 1.0, 1.0, 0.95, 0.85, 0.72, 0.58]
# Absolute chroma caps for the tint steps. Hues whose gamut stays wide near
# white (yellow, lime, cyan) would otherwise produce neon "subtle" backgrounds.
CHROMA_CAP = [0.028, 0.055, 0.095, 0.145, None, None, None, None, None, None, None]


def make_ramp(seed, anchor=True, chroma_scale=1.0, hue_shift=0.0):
    L0, C0, H0 = seed.oklch
    rel = C0 / max(max_chroma(L0, H0), 1e-6)  # how vivid the seed is for its L/H
    rel = min(rel, 1.0) * chroma_scale
    ramp = []
    H = H0
    for k, (L, shape, cap) in enumerate(zip(TARGET_L, CHROMA_SHAPE, CHROMA_CAP)):
        # optional hue drift on the shade side (e.g. yellows toward orange so
        # dark steps read golden instead of olive): 0 at step 500, full at 950
        H = (H0 + hue_shift * max(0, k - 5) / 5) % 360
        C = rel * shape * max_chroma(L, H)
        if cap is not None:
            C = min(C, cap * min(rel * 1.15, 1.0))
        ramp.append(Color.from_oklch(L, C, H))
    anchored = None
    if anchor and C0 > 0.01:
        i = min(range(len(TARGET_L)), key=lambda k: abs(TARGET_L[k] - L0))
        ramp[i] = seed
        anchored = STEPS[i]
    return ramp, anchored


# Neutrals span a wider lightness range than chromatic ramps: near-white
# page backgrounds at the top, a genuinely dark dark-mode canvas at 950.
NEUTRAL_L = [0.985, 0.965, 0.920, 0.870, 0.710, 0.555, 0.445, 0.370, 0.275, 0.210, 0.150]


def make_neutral(seed, tint=0.012):
    _, _, H = seed.oklch
    out = []
    for L, shape in zip(NEUTRAL_L, CHROMA_SHAPE):
        # keep the tint subtle and slightly stronger mid-ramp
        out.append(Color.from_oklch(L, tint * (0.6 + 0.4 * shape), H))
    return out


# ---------------------------------------------------------------- CVD

# Machado, Oliveira & Fernandes (2009), severity 1.0, applied to linear RGB.
CVD = {
    "protanopia": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deuteranopia": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritanopia": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}


def simulate(c, kind):
    if kind == "achromatopsia":
        y = relative_luminance(c)
        v = _linear_to_srgb(y)
        return Color(v, v, v)
    lin = c.linear
    m = CVD[kind]
    out = [sum(m[i][j] * lin[j] for j in range(3)) for i in range(3)]
    return Color(*(min(max(_linear_to_srgb(max(v, 0)), 0), 1) for v in out))


def delta_e_ok(a, b):
    return math.dist(a.oklab, b.oklab)


# ---------------------------------------------------------------- system

STATUS_HUES = {"success": 150.0, "warning": 75.0, "danger": 27.0, "info": 245.0}


def hue_dist(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def status_seeds(accent_h):
    seeds = {}
    for name, h in STATUS_HUES.items():
        # Keep status hues at least 25° away from the accent so "brand" never
        # reads as "error"/"success". If the brand IS that hue, nudge status.
        if hue_dist(h, accent_h) < 25:
            h = (accent_h + 25 * (1 if (h - accent_h) % 360 < 180 else -1)) % 360
        L = 0.62 if name != "warning" else 0.76
        seeds[name] = Color.from_oklch(L, 0.17, h)
    return seeds


# role -> (ramp, light step, dark step, min WCAG ratio vs bg or None)
# Fills (accent + statuses) and their -fg / -hover are resolved separately.
ROLES = [
    ("bg",            "neutral",  50, 950, None),
    ("bg-subtle",     "neutral", 100, 900, None),
    ("surface",       "neutral", None, 900, None),   # light: pure white
    ("border",        "neutral", 200, 800, None),
    ("border-strong", "neutral", 300, 700, None),
    ("border-control","neutral", 500, 500, 3.0),    # inputs/checkboxes: WCAG 1.4.11
    ("text",          "neutral", 950,  50, 7.0),
    ("text-muted",    "neutral", 600, 400, 4.5),
    ("accent-subtle", "accent",  100, 950, None),
    ("accent-text",   "accent",  700, 300, 4.5),
    ("focus-ring",    "accent",  500, 400, 3.0),
]
STATUS_ROLES = [
    ("{s}-subtle", 100, 950, None),
    ("{s}-text",   700, 300, 4.5),
]


def build_system(accent_seed, neutral_tint=0.012, anchor=True):
    accent, anchored = make_ramp(accent_seed, anchor=anchor)
    ramps = {"accent": accent, "neutral": make_neutral(accent_seed, neutral_tint)}
    _, _, ah = accent_seed.oklch
    for name, seed in status_seeds(ah).items():
        ramps[name], _ = make_ramp(seed, anchor=False)

    white = Color(1, 1, 1)
    themes, notes = {}, []
    for mode in ("light", "dark"):
        toks = {}
        bg = ramps["neutral"][STEPS.index(50 if mode == "light" else 950)]

        def pick(ramp_name, step, min_ratio, role):
            if step is None:
                return ("white", None, white)
            ramp = ramps[ramp_name]
            i = STEPS.index(step)
            if min_ratio:
                # walk away from the bg until the pair passes
                d = 1 if mode == "light" else -1
                start = i
                while 0 <= i < len(STEPS) and wcag_ratio(ramp[i], bg) < min_ratio:
                    i += d
                i = min(max(i, 0), len(STEPS) - 1)
                if i != start:
                    notes.append(f"{mode}: {role} moved {ramp_name}-{STEPS[start]} -> {STEPS[i]} to reach {min_ratio}:1")
            return (ramp_name, STEPS[i], ramp[i])

        for role, rn, ls, ds, mr in ROLES:
            toks[role] = pick(rn, ls if mode == "light" else ds, mr, role)
        for s in STATUS_HUES:
            for tmpl, ls, ds, mr in STATUS_ROLES:
                role = tmpl.format(s=s)
                toks[role] = pick(s, ls if mode == "light" else ds, mr, role)

        # Solid fills (buttons, badges): pick the fill step + foreground pair.
        # Try the preferred step first, then neighbours, and take the first
        # where white or the ramp's 950 reaches 4.5:1 on the fill and the fill
        # itself reaches 3:1 against the page (WCAG 1.4.11 non-text contrast).
        base_order = [6, 7, 5] if mode == "light" else [5, 4, 6]   # indices into STEPS
        for fill in ["accent"] + list(STATUS_HUES):
            ramp = ramps[fill]
            order = list(base_order)
            # light mode: if the exact brand color can be the primary fill, use it
            if fill == "accent" and mode == "light" and anchored in (500, 600, 700, 800):
                ai = STEPS.index(anchored)
                order = [ai] + [k for k in order if k != ai]
            chosen = None
            for i in order:
                c = ramp[i]
                fg = max([("white", None, white), (fill, 950, ramp[-1])], key=lambda t: wcag_ratio(t[2], c))
                if wcag_ratio(fg[2], c) >= 4.5 and wcag_ratio(c, bg) >= 3.0:
                    chosen = (i, fg)
                    break
            if chosen is None:
                i = order[0]
                fg = max([("white", None, white), (fill, 950, ramp[-1])], key=lambda t: wcag_ratio(t[2], ramp[i]))
                chosen = (i, fg)
                notes.append(f"{mode}: {fill}-fg on {fill} is {wcag_ratio(fg[2], ramp[i]):.2f}:1 (<4.5) — "
                             "use it for large/bold labels only, or adjust the seed")
            elif chosen[0] != order[0]:
                notes.append(f"{mode}: {fill} fill moved {fill}-{STEPS[order[0]]} -> {STEPS[chosen[0]]} so its label passes 4.5:1")
            i, fg = chosen
            toks[fill] = (fill, STEPS[i], ramp[i])
            toks[f"{fill}-fg"] = fg
            if fill == "accent":
                h = min(i + 1, 10) if mode == "light" else max(i - 1, 0)
                toks["accent-hover"] = ("accent", STEPS[h], ramp[h])
        themes[mode] = toks
    return ramps, themes, notes, anchored


# ---------------------------------------------------------------- output

def fmt_ramp_table(name, ramp, anchored=None):
    lines = [f"{name}  (step · hex · oklch · contrast vs white / vs black)"]
    white, black = Color(1, 1, 1), Color(0, 0, 0)
    for s, c in zip(STEPS, ramp):
        mark = "  ← input" if s == anchored else ""
        lines.append(
            f"  {s:>4}  {c.hex}  {c.css_oklch():<26} {wcag_ratio(c, white):5.2f} / {wcag_ratio(c, black):5.2f}{mark}"
        )
    return "\n".join(lines)


def ramps_css(ramps, notation, prefix=""):
    out = []
    for name, ramp in ramps.items():
        for s, c in zip(STEPS, ramp):
            out.append(f"  --{prefix}{name}-{s}: {c.css(notation)};")
    return out


def role_ref(t, notation, use_vars, prefix=""):
    rn, step, c = t
    if rn == "white":
        return "#fff" if notation == "hex" else "oklch(100% 0 0)"
    if use_vars and step is not None:
        return f"var(--{prefix}{rn}-{step})"
    return c.css(notation)


def dtcg_color(c):
    """DTCG Format Module 2025.10 color value (structured, with hex fallback)."""
    L, C, H = c.oklch
    return {"colorSpace": "oklch", "components": [round(L, 4), round(C, 4), round(H, 2) if C >= 0.0005 else 0],
            "hex": c.hex}


def emit_system(ramps, themes, fmt, notation):
    if fmt == "json":
        # DTCG 2025.10-style: primitives + semantic aliases per mode
        prim = {name: {str(s): {"$value": dtcg_color(c)} for s, c in zip(STEPS, r)}
                for name, r in ramps.items()}
        prim["$type"] = "color"
        prim["white"] = {"$value": dtcg_color(Color(1, 1, 1))}
        sem = {}
        for mode, toks in themes.items():
            sem[mode] = {"$type": "color"}
            sem[mode].update({
                role: {"$value": "{color.white}" if t[0] == "white" else "{color.%s.%s}" % (t[0], t[1])}
                for role, t in toks.items()
            })
        return json.dumps({"color": prim, "semantic": sem}, indent=2)

    lines = []
    if fmt == "tailwind":
        lines.append("/* Tailwind v4 — paste into your main CSS after @import \"tailwindcss\"; */")
        lines.append("@custom-variant dark (&:where(.dark, .dark *));\n")
        lines.append("/* primitives -> utilities like bg-accent-600, text-neutral-500 */")
        lines.append("@theme {")
        lines += ramps_css(ramps, notation, prefix="color-")
        lines.append("}\n")
        lines.append(":root {")
        lines += [f"  --{r}: {role_ref(t, notation, True, 'color-')};" for r, t in themes["light"].items()]
        lines.append("}\n.dark {")
        lines += [f"  --{r}: {role_ref(t, notation, True, 'color-')};" for r, t in themes["dark"].items()]
        lines.append("}\n")
        lines.append("/* expose semantic roles as utilities: bg-bg, text-text-muted, border-border, bg-accent ... */")
        lines.append("@theme inline {")
        lines += [f"  --color-{r}: var(--{r});" for r in themes["light"]]
        lines.append("}")
        return "\n".join(lines)

    # plain CSS
    lines.append(":root {")
    lines.append("  color-scheme: light;")
    lines += ramps_css(ramps, notation)
    lines.append("")
    lines += [f"  --color-{r}: {role_ref(t, notation, True)};" for r, t in themes["light"].items()]
    lines.append("}\n")
    dark_body = ["  color-scheme: dark;"] + [
        f"  --color-{r}: {role_ref(t, notation, True)};" for r, t in themes["dark"].items()]
    lines.append("/* pick ONE switching mechanism; class-based shown, media query alternative below */")
    lines.append(".dark {")
    lines += dark_body
    lines.append("}")
    lines.append("/* @media (prefers-color-scheme: dark) { :root:not(.light) { ...same as .dark... } } */")
    return "\n".join(lines)


def system_report(themes, notes):
    lines = []
    for mode, toks in themes.items():
        bg = toks["bg"][2]
        lines.append(f"\n{mode.upper()} THEME  (bg = {bg.hex})")
        for role, (rn, step, c) in toks.items():
            ref = "white" if rn == "white" else f"{rn}-{step}"
            if role.endswith("-fg"):
                base = toks[role[:-3]][2]
                r, lc = wcag_ratio(c, base), apca_lc(c, base)
                lines.append(f"  {role:<16} {ref:<14} {c.hex}   on {role[:-3]}: {r:5.2f}:1  Lc {lc:6.1f}")
            elif role in ("bg", "bg-subtle", "surface") or role.endswith("-subtle"):
                lines.append(f"  {role:<16} {ref:<14} {c.hex}")
            else:
                r, lc = wcag_ratio(c, bg), apca_lc(c, bg)
                lines.append(f"  {role:<16} {ref:<14} {c.hex}   vs bg: {r:5.2f}:1  Lc {lc:6.1f}")
    if notes:
        lines.append("\nAdjustments / warnings:")
        lines += [f"  - {n}" for n in notes]
    return "\n".join(lines)


# ---------------------------------------------------------------- CLI

def cmd_convert(a):
    c = Color.parse(a.color)
    L, C, H = c.oklch
    h, s, l = c.hsl
    print(f"hex    {c.hex}")
    print(f"rgb    rgb({' '.join(map(str, c.rgb255))})")
    print(f"hsl    hsl({h:.0f} {s:.0f}% {l:.0f}%)")
    print(f"oklch  {c.css_oklch()}")
    print(f"chroma {C:.3f} of max {max_chroma(L, H):.3f} at this L/H ({C / max(max_chroma(L, H), 1e-6):.0%} vivid)")
    print(f"vs white {wcag_ratio(c, Color(1, 1, 1)):.2f}:1   vs black {wcag_ratio(c, Color(0, 0, 0)):.2f}:1")


def cmd_contrast(a):
    fg, bg = Color.parse(a.fg), Color.parse(a.bg)
    r = wcag_ratio(fg, bg)
    lc = apca_lc(fg, bg)
    print(f"{fg.hex} on {bg.hex}")
    print(f"WCAG 2.x  {r:.2f}:1")
    for k, v in wcag_levels(r).items():
        print(f"  {'PASS' if v else 'fail'}  {k}")
    print(f"APCA      Lc {lc:.1f}  ({apca_hint(lc)})  [advisory — WCAG 3 is not final]")


def _ramp_out(name, ramp, anchored, a):
    if a.format == "table":
        print(fmt_ramp_table(name, ramp, anchored))
    elif a.format == "json":
        group = {"$type": "color"}
        group.update({str(s): {"$value": dtcg_color(c)} for s, c in zip(STEPS, ramp)})
        print(json.dumps({"color": {name: group}}, indent=2))
    elif a.format == "tailwind":
        print("@theme {")
        print("\n".join(f"  --color-{name}-{s}: {c.css(a.notation)};" for s, c in zip(STEPS, ramp)))
        print("}")
    else:
        print(":root {")
        print("\n".join(f"  --{name}-{s}: {c.css(a.notation)};" for s, c in zip(STEPS, ramp)))
        print("}")


def cmd_ramp(a):
    ramp, anchored = make_ramp(Color.parse(a.color), anchor=not a.no_anchor, hue_shift=a.hue_shift)
    _ramp_out(a.name, ramp, anchored, a)


def cmd_neutral(a):
    _ramp_out(a.name, make_neutral(Color.parse(a.color), a.tint), None, a)


def cmd_harmony(a):
    c = Color.parse(a.color)
    L, C, H = c.oklch
    offs = {
        "complementary": [0, 180],
        "analogous": [-30, 0, 30],
        "triadic": [0, 120, 240],
        "split": [0, 150, 210],
        "tetradic": [0, 90, 180, 270],
    }[a.scheme]
    print(f"{a.scheme} from {c.hex} (OKLCH hue rotation, same L and relative chroma)")
    rel = C / max(max_chroma(L, H), 1e-6)
    for o in offs:
        h = (H + o) % 360
        x = c if o == 0 else Color.from_oklch(L, rel * max_chroma(L, h), h)
        print(f"  {o:+4d}°  {x.hex}  {x.css_oklch()}")
    print("\nTip: in UI, use one of these as the accent and the rest sparingly (charts, illustrations,"
          " tags) — a harmony is a source of hues, not a mandate to use them all equally.")


def cmd_cvd(a):
    cols = [Color.parse(x) for x in a.colors]
    kinds = ["protanopia", "deuteranopia", "tritanopia", "achromatopsia"]
    print("color     " + "  ".join(f"{k[:12]:<12}" for k in kinds))
    for c in cols:
        print(f"{c.hex}   " + "  ".join(f"{simulate(c, k).hex:<12}" for k in kinds))
    if len(cols) > 1:
        print("\nPairs that become hard to tell apart (OKLab ΔE < 0.06; ≥0.10 is comfortable):")
        flagged = False
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                for k in ["normal"] + kinds:
                    x = cols[i] if k == "normal" else simulate(cols[i], k)
                    y = cols[j] if k == "normal" else simulate(cols[j], k)
                    d = delta_e_ok(x, y)
                    if d < 0.06:
                        flagged = True
                        print(f"  {cols[i].hex} vs {cols[j].hex} under {k}: ΔE {d:.3f}")
        if not flagged:
            print("  none — all pairs stay distinguishable")
        print("\nRegardless: never let color be the only signal (add icon, label, pattern or position).")


def cmd_system(a):
    seed = Color.parse(a.color)
    ramps, themes, notes, anchored = build_system(seed, a.neutral_tint, anchor=not a.no_anchor)
    if a.format == "table":
        for name, r in ramps.items():
            print(fmt_ramp_table(name, r, anchored if name == "accent" else None))
            print()
        print(system_report(themes, notes))
    else:
        print(emit_system(ramps, themes, a.format, a.notation))
        if notes:
            print("\n/* adjustments:\n" + "\n".join(f"   {n}" for n in notes) + "\n*/", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, name_default):
        sp.add_argument("--format", choices=["table", "css", "tailwind", "json"], default="table")
        sp.add_argument("--notation", choices=["oklch", "hex"], default="oklch")
        sp.add_argument("--name", default=name_default)

    sp = sub.add_parser("convert"); sp.add_argument("color"); sp.set_defaults(fn=cmd_convert)
    sp = sub.add_parser("contrast"); sp.add_argument("fg"); sp.add_argument("bg"); sp.set_defaults(fn=cmd_contrast)
    sp = sub.add_parser("ramp"); sp.add_argument("color"); common(sp, "brand")
    sp.add_argument("--no-anchor", action="store_true")
    sp.add_argument("--hue-shift", type=float, default=0.0,
                    help="degrees of hue drift from step 500 to 950 (e.g. -15 for yellow -> golden)")
    sp.set_defaults(fn=cmd_ramp)
    sp = sub.add_parser("neutral"); sp.add_argument("color"); common(sp, "neutral")
    sp.add_argument("--tint", type=float, default=0.012); sp.set_defaults(fn=cmd_neutral)
    sp = sub.add_parser("harmony"); sp.add_argument("color")
    sp.add_argument("--scheme", choices=["complementary", "analogous", "triadic", "split", "tetradic"],
                    default="complementary"); sp.set_defaults(fn=cmd_harmony)
    sp = sub.add_parser("cvd"); sp.add_argument("colors", nargs="+"); sp.set_defaults(fn=cmd_cvd)
    sp = sub.add_parser("system"); sp.add_argument("color"); common(sp, "accent")
    sp.add_argument("--neutral-tint", type=float, default=0.012)
    sp.add_argument("--no-anchor", action="store_true"); sp.set_defaults(fn=cmd_system)

    a = p.parse_args()
    try:
        a.fn(a)
    except ValueError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
