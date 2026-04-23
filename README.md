# Antique Polychrome

A warm-parchment theme family for [Visual Studio Code](https://code.visualstudio.com/)
with an 8-color polychrome syntax palette, AAA WCAG contrast, and auto-paired
file icons.

## Eight variants

| | Light (`vs`) | Light HC (`hc-light`) | Dark (`vs-dark`) | Dark HC (`hc-black`) |
|---|---|---|---|---|
| **Polychrome** | `Antique Polychrome Light` | `Antique Polychrome` | `Antique Polychrome Dark` | `Antique Polychrome Dark HC` |
| **Monochrome** | `Antique Monochrome Light` | `Antique Monochrome` | `Antique Monochrome Dark` | `Antique Monochrome Dark HC` |

- **Polychrome** — full 8-color syntax grammar (amber / green / indigo / red / teal / navy / purple / magenta)
- **Monochrome** — syntax stripped down to amber for strings + red for comments; everything else uses structural font style (bold / italic / underline) to carry meaning

## Color grammar (polychrome variants)

| Color | Hex (light / dark) | Semantic meaning |
|-------|---------------------|------------------|
| **Black / cream** | `#000` / `#e8e0cc` | Identifiers, variables, parameters — default "content" |
| **Amber** | `#7a3500` / `#e89050` | Functions, methods, property access, tags, regex, decorators, CSS selectors, inline code |
| **Green** | `#094d29` / `#7fd49c` | Numbers, constants, `this`/`self`, enum members, JSON/YAML keys, CSS properties |
| **Indigo** | `#471acc` / `#a58fef` | Strings, links |
| **Red** | `#990e2d` / `#eb8097` | Comments, JSDoc |
| **Teal** | `#0a5c5c` / `#7ec5c5` | Types, interfaces, classes, primitives |
| **Navy** | `#1e4e9e` / `#97b8e5` | Namespaces, modules, info-level diagnostics |
| **Purple** | `#6a2b8e` / `#c8a3e0` | Control-flow keywords (`if`, `else`, `return`, `try`, `catch`) |
| **Magenta** | `#991757` / `#eb9bbf` | Storage modifiers (`async`, `static`, `public`, `readonly`), `new` |
| **Muted brown** | `#504e44` / `#a8a394` | Operators, subordinate punctuation — "scaffolding" |

Every foreground hits AAA (≥7:1) on its theme's background.

## Bundled icon themes (Sun / Moon)

| ID | Label | Source | Used by |
|----|-------|--------|---------|
| `antique-polychrome-sun` | Antique Polychrome Sun | Catppuccin Perfect — **Latte** variant | All light color themes |
| `antique-polychrome-moon` | Antique Polychrome Moon | Catppuccin Perfect — **Mocha** variant | All dark color themes |

An activation script (`extension.js`) pairs the icon theme to the active color
theme:

- **Selecting an Antique *Light* / *Light HC* variant** → Sun (Latte) icons auto-activate
- **Selecting an Antique *Dark* / *Dark HC* variant** → Moon (Mocha) icons auto-activate
- **Selecting a non-Antique color theme** → your previous icon theme is left untouched

Both icon sets are from
[`thang-nm/catppuccin-perfect-icons`](https://github.com/thang-nm/catppuccin-perfect-icons)
(MIT) — copied into `fileicons/` to keep the extension self-contained.

The extension also bundles
[`vscode-icons-team/vscode-icons`](https://github.com/vscode-icons/vscode-icons)
(MIT) as a reference library under `fileicons/_library-vscode-icons/icons/` so
individual icons can be cherry-picked into the Sun/Moon themes if we want to
swap specific file-type icons.

## Activate

1. `Cmd+Shift+P` → *Preferences: Color Theme* → pick any **Antique Polychrome** or **Antique Monochrome** variant
2. Sun or Moon icons activate automatically based on whether the selected theme is light or dark

## Installation (local only)

This extension lives as a symlink from your project's `.vscode/` into
`~/.vscode/extensions/`:

```text
~/.vscode/extensions/local.antique-polychrome-1.4.1/
```

To register it with a VS Code profile that doesn't already have it, add an
entry to `~/Library/Application Support/Code/User/profiles/<id>/extensions.json`:

```json
{
  "identifier": { "id": "local.antique-polychrome" },
  "version": "1.4.1",
  "location": { "$mid": 1, "path": "/Users/<you>/.vscode/extensions/local.antique-polychrome-1.4.1", "scheme": "file" },
  "relativeLocation": "local.antique-polychrome-1.4.1",
  "metadata": { "source": "resource", "targetPlatform": "undefined" }
}
```

Reload the window (`Developer: Reload Window`) and the theme appears in the pickers.

## Credits

Color theme is a derivative of
[`solarized-high-contrast-light`](https://github.com/tinytinytinytiny/solarized-high-contrast-light)
by **tinytinytinytiny** (MIT). Substantial modifications include the 8-color
polychrome expansion, semantic token highlighting, full 8-variant family
(light / dark × HC, polychrome / monochrome), UI-chrome re-tuning, git / diff
visibility fixes, widget-family coverage (checkbox / radio / inputOption /
button), and the Sun/Moon icon auto-pairing.

Icons:
- **Sun / Moon** — [Catppuccin Perfect Icons](https://github.com/thang-nm/catppuccin-perfect-icons) (MIT) — Latte and Mocha variants
- **Reference library** — [vscode-icons](https://github.com/vscode-icons/vscode-icons) (MIT) — bundled as SVGs for cherry-picking

Both license files preserved at `fileicons/CATPPUCCIN-LICENSE.txt` and
`fileicons/VSCODE-ICONS-LICENSE.txt`.
