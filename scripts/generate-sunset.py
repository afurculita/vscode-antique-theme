#!/usr/bin/env python3
"""
Generate the four Antique Sunset themes (light, light-hc, dark, dark-hc) from
the existing antique-polychrome-dark theme as a structural template.

The Sunset gradient is the 8-stop palette:
    #ff5e87  #ff7b54  #ffa45c  #ffd166  #f7b801  #f18701  #ee5e51  #db3a34

Strategy: take the role each source-color plays in the polychrome-dark theme
(deepest bg, primary accent, error, etc.) and remap to a warm equivalent for
each variant. Cool accents in source (green/blue/purple) collapse onto warm
gradient stops so the theme has a single visual identity.

Run:  python3 scripts/generate-sunset.py
"""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "themes" / "antique-polychrome-dark-color-theme.json"

# Sunset gradient stops (8 points along pink → amber).
SUNSET = {
    "pink":     "#ff5e87",
    "coral":    "#ff7b54",
    "orange":   "#ffa45c",
    "amber":    "#ffd166",
    "gold":     "#f7b801",
    "burnt":    "#f18701",
    "vermil":   "#ee5e51",
    "crimson":  "#db3a34",
}

# Maps source-theme color → new color for each of the 4 variants.
# Keys are the base hex (no alpha) from antique-polychrome-dark post-consolidation.
# Values are dicts: variant → new base hex.
#
# Variants:
#   "dark"     — warm dark backgrounds, gradient accents
#   "dark-hc"  — pure-black backgrounds, max-chroma accents, white borders
#   "light"    — warm cream backgrounds, deeper accents
#   "light-hc" — pure-white backgrounds, deepest accents, black borders
REMAP = {
    # === BACKGROUND TIERS ===
    "#1d1a13": {"dark": "#1a0e12", "dark-hc": "#000000", "light": "#fff8f3", "light-hc": "#ffffff"},
    "#2a2518": {"dark": "#241218", "dark-hc": "#0a0506", "light": "#fff0e6", "light-hc": "#fafafa"},
    "#302a1d": {"dark": "#2a1620", "dark-hc": "#0e0709", "light": "#ffe8d8", "light-hc": "#f5f5f5"},
    "#3a3427": {"dark": "#341a26", "dark-hc": "#16080c", "light": "#ffdcc4", "light-hc": "#eeeeee"},
    "#3f3b2e": {"dark": "#3d1d2c", "dark-hc": "#1a0a0f", "light": "#ffd0b0", "light-hc": "#e8e8e8"},
    "#4a4233": {"dark": "#4a2334", "dark-hc": "#220d13", "light": "#ffc095", "light-hc": "#dddddd"},
    # === FOREGROUND TIERS ===
    "#faf5e3": {"dark": "#fff5f0", "dark-hc": "#ffffff", "light": "#1a0e12", "light-hc": "#000000"},
    "#e8e0cc": {"dark": "#ffe8d8", "dark-hc": "#ffe0c8", "light": "#2a1620", "light-hc": "#0a0506"},
    "#c0b8a0": {"dark": "#d8a896", "dark-hc": "#ffa080", "light": "#5a3a40", "light-hc": "#3a2026"},
    "#a8a394": {"dark": "#b08878", "dark-hc": "#ff9070", "light": "#705055", "light-hc": "#502a30"},
    "#8a8474": {"dark": "#8a6068", "dark-hc": "#c87060", "light": "#8a5a60", "light-hc": "#6a3540"},
    "#ffffff": {"dark": "#ffffff", "dark-hc": "#ffffff", "light": "#000000", "light-hc": "#000000"},
    # === PRIMARY ACCENT (gradient middle: coral) ===
    "#e89050": {"dark": SUNSET["coral"],   "dark-hc": SUNSET["pink"],    "light": SUNSET["burnt"],   "light-hc": SUNSET["crimson"]},
    "#d48040": {"dark": SUNSET["burnt"],   "dark-hc": SUNSET["crimson"], "light": SUNSET["vermil"],  "light-hc": SUNSET["crimson"]},
    # === SEMANTIC ACCENTS (cool ones collapse to warm equivalents) ===
    # green/success → gold
    "#4ec48a": {"dark": SUNSET["gold"],    "dark-hc": SUNSET["amber"],   "light": "#a87800",          "light-hc": "#806000"},
    # blue/info → orange
    "#5ab8d4": {"dark": SUNSET["orange"],  "dark-hc": SUNSET["amber"],   "light": SUNSET["burnt"],   "light-hc": "#a05400"},
    # yellow/warning → amber
    "#f0c058": {"dark": SUNSET["amber"],   "dark-hc": SUNSET["gold"],    "light": "#b88000",          "light-hc": "#805500"},
    # link / light blue → pink
    "#97b8e5": {"dark": SUNSET["pink"],    "dark-hc": SUNSET["coral"],   "light": SUNSET["crimson"], "light-hc": "#a02030"},
    # purple → crimson
    "#a58fef": {"dark": SUNSET["crimson"], "dark-hc": SUNSET["vermil"],  "light": "#a02835",          "light-hc": "#702028"},
    # error/red — keep crimson
    "#e85e7d": {"dark": SUNSET["crimson"], "dark-hc": SUNSET["crimson"], "light": "#a02030",          "light-hc": "#600018"},
    # black (used in 00-alpha overlays mostly) — leave alone
    "#000000": {"dark": "#000000", "dark-hc": "#000000", "light": "#000000", "light-hc": "#000000"},
}

# Variant metadata.
VARIANTS = {
    "dark":      {"type": "dark",  "ui": "vs-dark",  "label": "Antique Sunset Dark"},
    "dark-hc":   {"type": "dark",  "ui": "hc-black", "label": "Antique Sunset Dark HC"},
    "light":     {"type": "light", "ui": "vs",       "label": "Antique Sunset Light"},
    "light-hc":  {"type": "light", "ui": "hc-light", "label": "Antique Sunset"},
}


def remap_value(value: str, variant: str) -> str:
    """Substitute a #RRGGBB or #RRGGBBAA value into the variant's palette."""
    if not isinstance(value, str) or not value.startswith("#"):
        return value
    raw = value.lstrip("#").lower()
    if len(raw) == 6:
        base, alpha = "#" + raw, ""
    elif len(raw) == 8:
        base, alpha = "#" + raw[:6], raw[6:]
    else:
        return value
    if base in REMAP and variant in REMAP[base]:
        return REMAP[base][variant] + alpha
    return value


def walk(node, variant: str):
    if isinstance(node, dict):
        for k, v in list(node.items()):
            if isinstance(v, str):
                node[k] = remap_value(v, variant)
            else:
                walk(v, variant)
    elif isinstance(node, list):
        for item in node:
            walk(item, variant)


def main() -> None:
    with SRC.open() as f:
        template = json.load(f)

    out_files = {
        "dark":     ROOT / "themes" / "antique-sunset-dark-color-theme.json",
        "dark-hc":  ROOT / "themes" / "antique-sunset-dark-hc-color-theme.json",
        "light":    ROOT / "themes" / "antique-sunset-light-color-theme.json",
        "light-hc": ROOT / "themes" / "antique-sunset-color-theme.json",
    }

    for variant, out in out_files.items():
        theme = json.loads(json.dumps(template))  # deep copy
        theme["type"] = VARIANTS[variant]["type"]
        walk(theme, variant)
        with out.open("w") as f:
            json.dump(theme, f, indent="\t", ensure_ascii=False)
            f.write("\n")
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
