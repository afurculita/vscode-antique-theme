#!/usr/bin/env python3
"""
Boost border contrast across all themes.

Earlier `fill-chrome-keys.py` populated `*.border` keys using the "chrome"
palette tier — a slight surface elevation. That puts borders 1.04–1.48:1
contrast against the background, well below the 3:1 floor for non-text UI
elements (WCAG 1.4.11). Borders become invisible.

This pass walks every theme and overwrites the chrome-tier border values
with a per-palette "border" color, chosen for ~3:1+ contrast against the
background. Non-chrome borders that already use accent colors (e.g.,
button.border, tab.activeBorderTop) are left alone — only the 26 chrome
border keys are touched.

Run:  python3 scripts/boost-border-contrast.py
"""

from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Border-color set to overwrite the previously-filled chrome border values
# in each theme. The PREV_CHROME hex is what fill-chrome-keys.py wrote.
# The NEW_BORDER is what we want now.
PALETTES = {
    # warm dark antique (polychrome-dark, monochrome-dark, polychrome-dark-hc,
    # monochrome-dark-hc): bg ranges #1d1a13..#3a3427, border ~3.5:1
    "warm-dark": {
        "prev_chrome": "#3a3427",
        "new_border":  "#7b7664",  # muted mid-tan
    },
    "hc-black": {
        # fill-chrome-keys.py used HC_BLACK chrome=#1a1a1a; unify did not
        # touch *.border keys, so the chrome border value persists.
        "prev_chrome": "#1a1a1a",
        "new_border":  "#c0b8a0",  # bright tan border for HC visibility
    },
    "warm-light": {
        "prev_chrome": "#D2CCB8",
        "new_border":  "#7b7664",  # mid-tan border
    },
    "warm-light-hc": {
        "prev_chrome": "#a8a394",
        "new_border":  "#504e44",  # dark border for HC light
    },
    "sunset-dark": {
        "prev_chrome": "#341a26",
        "new_border":  "#b08878",  # muted pink-tan
    },
    "sunset-dark-hc": {
        # fill-chrome-keys.py used SUNSET_DARK_HC chrome=#16080c
        "prev_chrome": "#16080c",
        "new_border":  "#ff9070",  # bright coral for HC visibility
    },
    "sunset-light": {
        "prev_chrome": "#ffdcc4",
        "new_border":  "#705055",  # dark plum-tan
    },
    "sunset-light-hc": {
        "prev_chrome": "#eeeeee",
        "new_border":  "#502a30",  # very dark for HC light
    },
}

TARGETS = [
    ("themes/antique-polychrome-dark-color-theme.json",     "warm-dark"),
    ("themes/antique-monochrome-dark-color-theme.json",     "warm-dark"),
    ("themes/antique-polychrome-dark-hc-color-theme.json",  "hc-black"),
    ("themes/antique-monochrome-dark-hc-color-theme.json",  "hc-black"),
    ("themes/antique-polychrome-light-color-theme.json",    "warm-light"),
    ("themes/antique-monochrome-light-color-theme.json",    "warm-light"),
    ("themes/antique-polychrome-color-theme.json",          "warm-light-hc"),
    ("themes/antique-monochrome-color-theme.json",          "warm-light-hc"),
    ("themes/antique-sunset-dark-color-theme.json",         "sunset-dark"),
    ("themes/antique-sunset-dark-hc-color-theme.json",      "sunset-dark-hc"),
    ("themes/antique-sunset-light-color-theme.json",        "sunset-light"),
    ("themes/antique-sunset-color-theme.json",              "sunset-light-hc"),
]

# Chrome border keys added by fill-chrome-keys.py — these are what we
# overwrite. Other *.border keys (button.border, focusBorder, etc.) that
# already use accent colors are left untouched.
CHROME_BORDER_KEYS = {
    "editorGroupHeader.tabsBorder", "editorGroupHeader.border",
    "tab.border", "tab.unfocusedActiveBorder",
    "panel.border", "panelSection.border", "panelSectionHeader.border",
    "statusBar.border", "sideBar.border", "sideBarSectionHeader.border",
    "titleBar.border",
}


def main() -> None:
    for rel, palette_name in TARGETS:
        path = ROOT / rel
        p = PALETTES[palette_name]
        with path.open() as f:
            theme = json.load(f)
        colors = theme["colors"]

        changes = 0
        for k in CHROME_BORDER_KEYS:
            v = colors.get(k)
            if not isinstance(v, str):
                continue
            base = "#" + v.lstrip("#").lower()[:6]
            # Only overwrite if it's the previous (low-contrast) chrome value.
            if base == p["prev_chrome"].lower():
                # Preserve alpha if present (e.g., tab.unfocusedActiveBorder had "60")
                raw = v.lstrip("#").lower()
                alpha = raw[6:] if len(raw) == 8 else ""
                colors[k] = p["new_border"] + alpha
                changes += 1

        with path.open("w") as f:
            json.dump(theme, f, indent="\t", ensure_ascii=False)
            f.write("\n")
        print(f"{rel}: {changes} border substitutions ({palette_name})")


if __name__ == "__main__":
    main()
