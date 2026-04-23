# Icon libraries

This directory bundles the two active icon themes (Sun / Moon) plus two
**reference libraries** used for cherry-picking individual icons into the
active themes.

## Folder layout

```text
fileicons/
├── antique-polychrome-sun/         — active light icon theme (Catppuccin Latte base)
├── antique-polychrome-moon/        — active dark icon theme (Catppuccin Mocha base)
├── _library-vscode-icons/          — MIT-licensed SVG library
│   └── icons/*.svg
├── _library-monokai-pro-light-filter-sun/  — Monokai Pro icons (SVGs + original font)
│   ├── icons/*.svg                         — 123 SVGs extracted from the font
│   ├── monokai-pro-icons.woff              — original font (kept for re-extraction)
│   ├── monokai-pro-light-filter-sun-icon-theme.json
│   ├── monokai-pro-light-filter-sun-monochrome-icon-theme.json
│   └── MONOKAI-PRO-LICENSE.txt
├── CATPPUCCIN-LICENSE.txt          — MIT
└── VSCODE-ICONS-LICENSE.txt        — MIT
```

## Libraries summary

| Library | License | Format | Used for |
|---------|---------|--------|----------|
| Catppuccin (built into Sun/Moon) | MIT | SVG | Most file-type + folder icons (native) |
| `_library-vscode-icons/` | MIT | SVG | All folder-type icons (`_fd_*`) + cherry-picks for files Catppuccin misses |
| `_library-monokai-pro-light-filter-sun/` | **Commercial — personal-use-only** | Font (woff) + JSON | Cherry-picks when the Monokai Pro aesthetic matches better |

## Cherry-picking from vscode-icons (SVG)

SVG cherry-pick is straightforward:

1. Find the SVG: `ls _library-vscode-icons/icons/ | grep -i <name>`
2. Copy into the active theme's icons dir with `vsi_` prefix:
   `cp _library-vscode-icons/icons/file_type_X.svg antique-polychrome-sun/icons/vsi_file_type_X.svg`
3. Add to the theme's `icon-theme.json`:
    - `iconDefinitions`: `"vsi_X": { "iconPath": "./icons/vsi_file_type_X.svg" }`
    - `fileNames` / `fileExtensions` / `languageIds`: point the name at `"vsi_X"`
4. Reload VS Code.

## Cherry-picking from Monokai Pro (SVG — preferred)

All 123 Monokai Pro glyphs have been pre-extracted from the font as individual
SVGs in `_library-monokai-pro-light-filter-sun/icons/` with their Filter Sun
colors baked in. Cherry-pick them the same way as vscode-icons:

1. Find the SVG: `ls _library-monokai-pro-light-filter-sun/icons/ | grep -i <name>`
   (e.g. `python.svg`, `claude.svg`, `typescript.svg`)
2. Copy into the active theme's `icons/` dir with an `mp_` prefix:
   `cp _library-monokai-pro-light-filter-sun/icons/python.svg antique-polychrome-sun/icons/mp_python.svg`
3. Add to the theme's `icon-theme.json`:
    - `iconDefinitions`: `"mp_python": { "iconPath": "./icons/mp_python.svg" }`
    - `fileNames` / `fileExtensions` / `languageIds`: point at `"mp_python"`
4. Reload VS Code.

## Re-extracting glyphs from the font (if you need to)

The 123 SVGs in `_library-monokai-pro-light-filter-sun/icons/` were extracted
from `monokai-pro-icons.woff` via `fontTools`. If Monokai updates the font in a
future Monokai Pro extension version, re-run the extractor:

```bash
/opt/homebrew/opt/python@3.10/bin/python3.10 \
  -c "$(cat <<'PY'
import json, pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

LIB = pathlib.Path('<path-to-library>')
font = TTFont(LIB / 'monokai-pro-icons.woff')
gs = font.getGlyphSet()
cmap = font['cmap'].getBestCmap()
theme = json.loads((LIB / 'monokai-pro-light-filter-sun-icon-theme.json').read_text())
ascender = font['hhea'].ascender
descender = font['hhea'].descender

for icon_id, d in theme['iconDefinitions'].items():
    cp = int(d['fontCharacter'].lstrip('\\\\'), 16)
    gname = cmap[cp]
    pen = SVGPathPen(gs); gs[gname].draw(pen)
    w = font['hmtx'][gname][0]
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-ascender} {w} {ascender - descender}"><path transform="scale(1,-1)" d="{pen.getCommands()}" fill="{d["fontColor"]}"/></svg>'
    (LIB / 'icons' / f'{icon_id.lstrip("_")}.svg').write_text(svg)
PY
)"
```

## ⚠ License — this extension is NOT distributable

The `_library-monokai-pro-light-filter-sun/` assets are licensed by Monokai
under a **commercial license that prohibits redistribution** (see
`_library-monokai-pro-light-filter-sun/MONOKAI-PRO-LICENSE.txt`).

This extension therefore must not be:

- Published to the VS Code Marketplace
- Pushed to a public GitHub repository
- Shared with teammates or other users
- Copied to machines that don't belong to the current licensed user

To make the extension shareable in the future, delete:

- `_library-monokai-pro-light-filter-sun/` (entire directory)
- any `mp_*` entries from `antique-polychrome-sun/icon-theme.json` and
  `antique-polychrome-moon/icon-theme.json`
- the `monokai-pro-icons` entry from each theme's `fonts` array
- any Monokai-derived icon references in `fileNames` / `fileExtensions` / `languageIds`

After deletion, the remaining assets (Catppuccin + vscode-icons) are all MIT-
licensed and freely distributable.
