#!/usr/bin/env python3
"""
Unify HC dark variants to use the warm-dark background palette throughout.

The HC dark variants currently mix three background palettes:
  - pure black     #000000 / #0a0a0a / #1a1a1a   (editor, tabs, panel, minimap)
  - warm dark      #1d1a13 / #2a2518 / #3a3427   (sidebar, statusbar, titlebar)
  - near-black     #1a1a1a / #0a0a0a              (unfocused tabs, section headers)

This script collapses everything onto the warm-dark palette. The "HC" character
is preserved via the already-strong accent colors and explicit borders — VS Code
HC does not require black backgrounds, it requires strong contrast.

Only substitutes background-style keys; foreground/border keys that legitimately
use #000000 (e.g., editor.selectionForeground on light text) are left alone.

Run:  python3 scripts/unify-hc-backgrounds.py
"""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Per-family warm-dark palette (matches the non-HC dark variant of each family).
WARM_DARK_ANTIQUE = {
    "base":    "#1d1a13",   # editor.background and similar
    "surface": "#2a2518",   # slight elevation (sidebar bg, panel section header)
    "chrome":  "#3a3427",   # chrome elevation (statusbar, activitybar, inactive tab)
    "fg":      "#e8e0cc",
}

WARM_DARK_SUNSET = {
    "base":    "#1a0e12",
    "surface": "#241218",
    "chrome":  "#341a26",
    "fg":      "#ffe8d8",
}

# Substitution map: pure-black-family hex -> warm-dark-tier name.
HC_BLACK_TO_TIER = {
    "#000000": "base",     # pure black surfaces
    "#0a0a0a": "surface",  # near-black elevations
    "#1a1a1a": "chrome",   # slightly lifted chrome
    "#2a2a2a": "chrome",   # hover (fallback)
}

# Substitution map: pure-black-style overlay alphas that should become cream overlays.
# Only matters for minimapSlider where the previous fill used #ffffff15.
HC_WHITE_OVERLAY_TO_FG = {"#ffffff": "fg"}

# Background-style keys: substitution happens here. Other key categories
# (foregrounds, borders, *.foreground) preserve their values.
BG_KEY_SUFFIXES = (
    ".background", ".activeBackground", ".inactiveBackground",
    ".hoverBackground", ".dropBackground", ".unfocusedActiveBackground",
    ".unfocusedInactiveBackground", ".activeBorder",  # tab activeBorder uses bg color
)


def is_background_key(key: str) -> bool:
    """Match any key whose role is a background/surface color.

    The naive suffix check missed keys like `editorGroupHeader.tabsBackground`
    (ends with `sBackground`, not `.background`). Using a substring check on
    the segment after the last `.` catches all background-role keys.
    """
    last = key.rsplit(".", 1)[-1].lower()
    if "background" in last:
        return True
    if last in {"shadow"}:  # scrollbar.shadow
        return True
    return False


def substitute(value: str, palette: dict) -> str:
    """If `value` is a pure-black-family color used as a background, swap to
    the matching warm-dark tier (preserving alpha)."""
    if not isinstance(value, str) or not value.startswith("#"):
        return value
    raw = value.lstrip("#").lower()
    if len(raw) == 6:
        base, alpha = "#" + raw, ""
    elif len(raw) == 8:
        base, alpha = "#" + raw[:6], raw[6:]
    else:
        return value
    if base in HC_BLACK_TO_TIER:
        return palette[HC_BLACK_TO_TIER[base]] + alpha
    if base in HC_WHITE_OVERLAY_TO_FG:
        return palette[HC_WHITE_OVERLAY_TO_FG[base]] + alpha
    return value


TARGETS = [
    ("themes/antique-polychrome-dark-hc-color-theme.json", WARM_DARK_ANTIQUE),
    ("themes/antique-monochrome-dark-hc-color-theme.json", WARM_DARK_ANTIQUE),
    ("themes/antique-sunset-dark-hc-color-theme.json",     WARM_DARK_SUNSET),
]


def main() -> None:
    for rel, palette in TARGETS:
        path = ROOT / rel
        with path.open() as f:
            theme = json.load(f)
        colors = theme["colors"]

        changes = 0
        for k, v in list(colors.items()):
            if not is_background_key(k):
                continue
            new = substitute(v, palette)
            if new != v:
                colors[k] = new
                changes += 1

        with path.open("w") as f:
            json.dump(theme, f, indent="\t", ensure_ascii=False)
            f.write("\n")
        print(f"{rel}: {changes} background substitutions")


if __name__ == "__main__":
    main()
