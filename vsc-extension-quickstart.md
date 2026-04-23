# Antique Polychrome — Development Quickstart

## What's in this folder

- `package.json` — extension manifest. Registers 8 color themes (Polychrome /
  Monochrome × Light / Light HC / Dark / Dark HC) and 2 icon themes (Sun / Moon).
- `extension.js` — activation script. On startup and on every color-theme
  change, pairs the icon theme to the active color theme (Light → Sun, Dark → Moon).
- `themes/` — 8 color-theme JSONs, one per variant. ~280 tokens each covering
  UI chrome, editor, syntax, diff, git decorations, terminal ANSI, widgets,
  and semantic tokens.
- `fileicons/` — bundled icon themes + reference library:
  - `antique-polychrome-sun/` — Catppuccin Perfect **Latte** icons (light theme pairing)
  - `antique-polychrome-moon/` — Catppuccin Perfect **Mocha** icons (dark theme pairing)
  - `_library-vscode-icons/icons/` — vscode-icons SVG library (not registered
    as a theme; provided for cherry-picking individual icons into Sun/Moon)
  - `CATPPUCCIN-LICENSE.txt`, `VSCODE-ICONS-LICENSE.txt` — MIT attribution
- `icon.svg` / `icon.png` — extension icon shown in the Extensions panel.
  Source SVG is editable; the PNG is rendered via `rsvg-convert`.

## Live development

The extension folder is symlinked from `~/.vscode/extensions/` — edits to
files here are picked up by VS Code directly.

Change a **color token value** (in any of the 8 `themes/*.json` files) →
if that theme is the active color theme, changes apply live on save, no
reload required.

Change **structure**: edit `package.json` contributions, edit `extension.js`,
or change a theme label → **reload the window** with `Developer: Reload
Window` so VS Code re-reads the manifest / re-runs activation.

Change **icon files** (SVGs in `fileicons/*/icons/*.svg` or the theme.json
mappings) → reload required.

## Regenerating the extension icon

If you edit `icon.svg`, re-render the PNG:

```bash
rsvg-convert -w 256 -h 256 icon.svg -o icon.png
```

## Cherry-picking icons from the vscode-icons library

The `_library-vscode-icons/icons/` directory contains ~1000 SVG icons from the
vscode-icons project — they are **NOT** registered as a theme, they are
bundled as raw SVGs. To use one in the Sun or Moon theme:

1. Find the SVG in `_library-vscode-icons/icons/` (e.g.
   `file_type_python.svg`).
2. Copy it into `fileicons/antique-polychrome-sun/icons/`
   (and / or `fileicons/antique-polychrome-moon/icons/`).
3. Edit the corresponding `icon-theme.json` to point a file-type or language
   ID at the new SVG. Example:

    ```json
    "iconDefinitions": {
      "python_vsi": { "iconPath": "./icons/file_type_python.svg" }
    },
    "languageIds": {
      "python": "python_vsi"
    }
    ```

4. Reload the window.

## How the Sun / Moon pairing works

- `extension.js` keeps two sets of color theme names (light vs dark) and one
  constant per icon theme (`SUN_ICONS`, `MOON_ICONS`).
- On startup and on `workbench.colorTheme` changes, it checks the current
  color theme's membership:
  - Member of `LIGHT_ANTIQUE_THEMES` → write
    `workbench.iconTheme = "antique-polychrome-sun"`.
  - Member of `DARK_ANTIQUE_THEMES` → write
    `workbench.iconTheme = "antique-polychrome-moon"`.
  - Otherwise → no-op, user's icon theme preserved.
- Writes target `ConfigurationTarget.Global` (user settings); the sync is
  idempotent (only writes when the value would actually change).

## Inspecting scopes while iterating

To see what scope a token has under the cursor, use
`Cmd+Shift+P` → *Developer: Inspect Editor Tokens and Scopes*.

To see which `tokenColors` / `semanticTokenColors` rule is matching, the
same inspector shows the rule's foreground/fontStyle and which `scope`
entry it matched.

## Contrast invariant

Every foreground in the theme is ≥7:1 contrast (AAA WCAG) against its
theme's `editor.background` (light variants: `#fcfbf0`; dark variants:
`#1d1a13`; HC Dark: `#000000`). When adding or changing a color, verify:

```bash
python3 -c "
def lum(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    def a(c): return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*a(r) + 0.7152*a(g) + 0.0722*a(b)
def c(x, y): return (max(lum(x), lum(y))+0.05)/(min(lum(x), lum(y))+0.05)
print(f'{c(\"#YOUR_COLOR\", \"#fcfbf0\"):.2f}:1')
"
```

Replace `#YOUR_COLOR` with the candidate hex and the bg with the variant
target. AAA requires ratio ≥ 7:1.

## VS Code color theme docs

- [Color theme API reference](https://code.visualstudio.com/api/extension-guides/color-theme)
- [Icon theme API reference](https://code.visualstudio.com/api/extension-guides/file-icon-theme)
- [Color reference](https://code.visualstudio.com/api/references/theme-color) — every `*.background` / `*.foreground` token VS Code exposes
- [Extension manifest](https://code.visualstudio.com/api/references/extension-manifest) — `contributes`, `activationEvents`, `main`, etc.
