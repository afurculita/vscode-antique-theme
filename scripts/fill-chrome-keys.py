#!/usr/bin/env python3
"""
Fill in missing tab/editor-group/panel/sidebar chrome keys in all dark themes.

When a theme omits a key, VS Code falls back to its built-in default, which for
dark themes is typically opaque #000000. That's why tab strips, panel borders,
sidebar section headers, etc. appear as pure black bands even though the rest
of the theme uses the warm-dark palette.

This script:
  1) Adds 26 missing chrome keys to each dark theme, with values drawn from
     the existing palette of that variant (so the fill harmonizes, doesn't
     introduce new shades).
  2) Fixes one outright bug: tab.unfocusedActiveBackground was #faf5e3 (bright
     cream) in every dark variant — clearly a paste error.

Variants and their base palette:
  warm-dark  (polychrome-dark, monochrome-dark): editor=#1d1a13
  hc-black   (polychrome-dark-hc, monochrome-dark-hc): editor=#000000

Run:  python3 scripts/fill-chrome-keys.py
"""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Chrome key values, parameterized by palette base.
# Palette: a dict of named shades. Each variant supplies its own.
def make_fillers(p: dict) -> dict:
    """Return a dict of {chrome_key: hex_or_rgba} given a palette dict."""
    return {
        # Editor group header (the strip behind tabs)
        "editorGroupHeader.tabsBackground":     p["base"],       # blend with editor
        "editorGroupHeader.tabsBorder":         p["chrome"],     # subtle separator
        "editorGroupHeader.noTabsBackground":   p["base"],       # when empty
        "editorGroupHeader.border":             p["chrome"],
        # Tabs
        "tab.unfocusedInactiveBackground":      p["chrome"],     # match focused inactive
        "tab.unfocusedActiveBorder":            p["accent"]+"60",
        "tab.border":                           p["chrome"],     # tab-to-tab separator
        "tab.hoverBackground":                  p["hover"],
        "tab.unfocusedHoverBackground":         p["hover"],
        "tab.unfocusedInactiveForeground":      p["muted"]+"70",
        # Editor pane / breadcrumb
        "editorPane.background":                p["base"],
        "breadcrumb.background":                p["base"],
        # Panel
        "panelTitle.activeBorder":              p["accent"],
        "panel.border":                         p["chrome"],
        "panelSection.border":                  p["chrome"],
        "panelSectionHeader.background":        p["surface"],
        "panelSectionHeader.border":            p["chrome"],
        # Status bar
        "statusBar.border":                     "#00000000",     # invisible (default)
        # Sidebar
        "sideBar.border":                       p["chrome"],
        "sideBarSectionHeader.background":      p["surface"],
        "sideBarSectionHeader.border":          p["chrome"],
        "sideBarTitle.background":              p["surface"],
        # Minimap
        "minimap.background":                   p["base"],
        "minimapSlider.background":             p["fg"] + "15",
        "minimapSlider.hoverBackground":        p["fg"] + "25",
        "minimapSlider.activeBackground":       p["fg"] + "35",
        # Scrollbar shadow
        "scrollbar.shadow":                     "#0000004d",
        # Title bar border
        "titleBar.border":                      p["chrome"],
    }


# Per-variant palettes
WARM_DARK = {
    "base":    "#1d1a13",
    "surface": "#2a2518",
    "chrome":  "#3a3427",
    "hover":   "#3f3b2e",
    "accent":  "#e89050",
    "muted":   "#a8a394",
    "fg":      "#e8e0cc",
}

HC_BLACK = {
    "base":    "#000000",
    "surface": "#0a0a0a",
    "chrome":  "#1a1a1a",
    "hover":   "#2a2a2a",
    "accent":  "#e89050",
    "muted":   "#a8a394",
    "fg":      "#ffffff",
}

# Sunset palettes (mirror what generate-sunset.py produced)
SUNSET_DARK = {
    "base":    "#1a0e12",
    "surface": "#241218",
    "chrome":  "#341a26",
    "hover":   "#3d1d2c",
    "accent":  "#ff7b54",
    "muted":   "#b08878",
    "fg":      "#ffe8d8",
}

SUNSET_DARK_HC = {
    "base":    "#000000",
    "surface": "#0a0506",
    "chrome":  "#16080c",
    "hover":   "#1a0a0f",
    "accent":  "#ff5e87",
    "muted":   "#ff9070",
    "fg":      "#ffffff",
}

SUNSET_LIGHT = {
    "base":    "#fff8f3",
    "surface": "#fff0e6",
    "chrome":  "#ffdcc4",
    "hover":   "#ffd0b0",
    "accent":  "#f18701",
    "muted":   "#705055",
    "fg":      "#2a1620",
}

SUNSET_LIGHT_HC = {
    "base":    "#ffffff",
    "surface": "#fafafa",
    "chrome":  "#eeeeee",
    "hover":   "#e8e8e8",
    "accent":  "#db3a34",
    "muted":   "#502a30",
    "fg":      "#000000",
}

# Antique Polychrome/Monochrome light variants — warm parchment palette.
WARM_LIGHT = {
    "base":    "#fcfbf0",
    "surface": "#EBE6D6",
    "chrome":  "#D2CCB8",
    "hover":   "#cbc9c3",
    "accent":  "#7a3500",
    "muted":   "#7b7664",
    "fg":      "#000000",
}

# Antique HC-light: same base/surface, but borders use stronger contrast.
WARM_LIGHT_HC = {
    "base":    "#fcfbf0",
    "surface": "#EBE6D6",
    "chrome":  "#a8a394",
    "hover":   "#cbc9c3",
    "accent":  "#7a3500",
    "muted":   "#504e44",
    "fg":      "#000000",
}

# Bug fix: this key was set to a bright cream (#faf5e3) in every dark variant.
# Replace it with a sensible per-palette dark.
TAB_UNFOCUSED_ACTIVE_BG_BUGFIX = {
    "warm-dark":      "#2a2518",
    "hc-black":       "#0a0a0a",
    "sunset-dark":    "#241218",
    "sunset-dark-hc": "#0a0506",
    "sunset-light":   "#fff0e6",
    "sunset-light-hc":"#fafafa",
    "warm-light":     "#EBE6D6",
    "warm-light-hc":  "#EBE6D6",
}

# Files to update, each with its palette identity.
TARGETS = [
    ("themes/antique-polychrome-dark-color-theme.json",     WARM_DARK,       "warm-dark"),
    ("themes/antique-monochrome-dark-color-theme.json",     WARM_DARK,       "warm-dark"),
    ("themes/antique-polychrome-dark-hc-color-theme.json",  HC_BLACK,        "hc-black"),
    ("themes/antique-monochrome-dark-hc-color-theme.json",  HC_BLACK,        "hc-black"),
    ("themes/antique-sunset-dark-color-theme.json",         SUNSET_DARK,     "sunset-dark"),
    ("themes/antique-sunset-dark-hc-color-theme.json",      SUNSET_DARK_HC,  "sunset-dark-hc"),
    ("themes/antique-sunset-light-color-theme.json",        SUNSET_LIGHT,    "sunset-light"),
    ("themes/antique-sunset-color-theme.json",              SUNSET_LIGHT_HC, "sunset-light-hc"),
    ("themes/antique-polychrome-light-color-theme.json",    WARM_LIGHT,      "warm-light"),
    ("themes/antique-monochrome-light-color-theme.json",    WARM_LIGHT,      "warm-light"),
    ("themes/antique-polychrome-color-theme.json",          WARM_LIGHT_HC,   "warm-light-hc"),
    ("themes/antique-monochrome-color-theme.json",          WARM_LIGHT_HC,   "warm-light-hc"),
]


def main() -> None:
    for rel_path, palette, palette_name in TARGETS:
        path = ROOT / rel_path
        with path.open() as f:
            theme = json.load(f)
        colors = theme["colors"]
        fillers = make_fillers(palette)

        added = 0
        for k, v in fillers.items():
            if k not in colors:
                colors[k] = v
                added += 1

        # Bug fix (dark variants only): tab.unfocusedActiveBackground was
        # set to a bright cream in every dark theme — invert intent of
        # tab.unfocusedActiveForeground. On light themes a bright value is
        # legitimate, so skip there.
        is_dark = palette_name in ("warm-dark", "hc-black", "sunset-dark", "sunset-dark-hc")
        bug_fixed = False
        if is_dark and colors.get("tab.unfocusedActiveBackground", "").lower() in ("#faf5e3", "#ffffff", "#fff5f0"):
            colors["tab.unfocusedActiveBackground"] = TAB_UNFOCUSED_ACTIVE_BG_BUGFIX[palette_name]
            bug_fixed = True

        with path.open("w") as f:
            json.dump(theme, f, indent="\t", ensure_ascii=False)
            f.write("\n")

        marker = " (+ tab.unfocusedActiveBackground bugfix)" if bug_fixed else ""
        print(f"{rel_path}: +{added} keys{marker}")


if __name__ == "__main__":
    main()
