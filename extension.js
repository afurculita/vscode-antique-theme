// Auto-pairs the bundled icon theme (Sun / Moon) with the active Antique color theme.
//
//   • Light color themes   → antique-polychrome-sun (Catppuccin Latte icons)
//   • Dark color themes    → antique-polychrome-moon (Catppuccin Mocha icons)
//
// Non-Antique color themes are ignored — we don't hijack the user's icon theme
// when they switch away from the family.

const vscode = require('vscode');

const LIGHT_ANTIQUE_THEMES = new Set([
    'Antique Polychrome',           // hc-light
    'Antique Polychrome Light',     // vs
    'Antique Monochrome',           // hc-light
    'Antique Monochrome Light',     // vs
]);

const DARK_ANTIQUE_THEMES = new Set([
    'Antique Polychrome Dark',      // vs-dark
    'Antique Polychrome Dark HC',   // hc-black
    'Antique Monochrome Dark',      // vs-dark
    'Antique Monochrome Dark HC',   // hc-black
]);

const SUN_ICONS = 'antique-polychrome-sun';
const MOON_ICONS = 'antique-polychrome-moon';

async function syncIconTheme() {
    const cfg = vscode.workspace.getConfiguration();
    const currentColorTheme = cfg.get('workbench.colorTheme');

    let desiredIconTheme;
    if (LIGHT_ANTIQUE_THEMES.has(currentColorTheme)) {
        desiredIconTheme = SUN_ICONS;
    } else if (DARK_ANTIQUE_THEMES.has(currentColorTheme)) {
        desiredIconTheme = MOON_ICONS;
    } else {
        return; // not one of ours — leave the user's icon theme alone
    }

    const currentIconTheme = cfg.get('workbench.iconTheme');
    if (currentIconTheme !== desiredIconTheme) {
        await cfg.update(
            'workbench.iconTheme',
            desiredIconTheme,
            vscode.ConfigurationTarget.Global
        );
    }
}

function activate(context) {
    syncIconTheme();

    const disposable = vscode.workspace.onDidChangeConfiguration(event => {
        if (event.affectsConfiguration('workbench.colorTheme')) {
            syncIconTheme();
        }
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };
