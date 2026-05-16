#!/usr/bin/env bash
# Update the Antique Polychrome VS Code extension from git across all profiles.
#
# What it does:
#   1. Refuses to run while VS Code is open (install would fail anyway).
#   2. git fetch + fast-forward pull from origin/main.
#   3. Packages a fresh .vsix with vsce.
#   4. Installs to the default profile, then to every named profile that
#      doesn't already share extensions with default (useDefaultFlags.extensions).
#
# Usage:   ./scripts/update.sh
# Repo:    git@github.com:afurculita/vscode-antique-theme.git

set -euo pipefail

readonly REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly STORAGE_JSON="$HOME/Library/Application Support/Code/User/globalStorage/storage.json"
readonly EXTENSIONS_JSON="$HOME/.vscode/extensions/extensions.json"
readonly EXT_ID="local.antique-polychrome"
readonly VSCODE_PROC_PATTERN='Visual Studio Code.app/Contents/MacOS/Code$'

log()  { printf '\033[1;34m→\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m!\033[0m %s\n' "$*" >&2; }
err()  { printf '\033[1;31m✗\033[0m %s\n' "$*" >&2; }
ok()   { printf '\033[1;32m✓\033[0m %s\n' "$*"; }

ensure_vscode_closed() {
  if ps ax -o comm | grep -qE "$VSCODE_PROC_PATTERN"; then
    err "VS Code is running. Quit it (Cmd+Q) before running this script."
    err "  (Install would fail with: 'Please restart VS Code before reinstalling...')"
    exit 1
  fi
}

# Removes any dangling entry for $EXT_ID whose on-disk path no longer exists.
# Without this, `code --install-extension` errors with "Please restart VS Code
# before reinstalling..." because VS Code can't reconcile the missing folder.
# SAFE ONLY when VS Code is fully closed (it owns this file at runtime).
repair_extensions_json() {
  [[ -f "$EXTENSIONS_JSON" ]] || return 0
  python3 - "$EXTENSIONS_JSON" "$EXT_ID" <<'PY'
import json, os, sys, shutil, tempfile
path, ext_id = sys.argv[1], sys.argv[2]
with open(path) as f:
    exts = json.load(f)
removed = []
kept = []
for e in exts:
    eid = e.get('identifier', {}).get('id', '')
    loc = e.get('location', {}).get('path', '')
    if eid == ext_id and loc and not os.path.exists(loc):
        removed.append((eid, e.get('version'), loc))
        continue
    kept.append(e)
if not removed:
    print(f'  no stale {ext_id} entries')
    sys.exit(0)
shutil.copy(path, path + '.bak')
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
with os.fdopen(fd, 'w') as f:
    json.dump(kept, f)
os.replace(tmp, path)
for eid, ver, loc in removed:
    print(f'  removed dangling: {eid}@{ver} -> {loc}')
PY
}

pull_latest() {
  cd "$REPO_DIR"
  log "Pulling from origin/main..."
  git fetch origin
  git pull --ff-only origin main
}

build_vsix() {
  cd "$REPO_DIR"
  rm -f ./*.vsix
  log "Packaging VSIX..." >&2
  npx --yes @vscode/vsce package \
    --allow-missing-repository \
    --skip-license \
    --no-dependencies >&2
  ls -t ./*.vsix | head -1
}

# Emits one profile name per line, excluding profiles that share extensions
# with the default profile (useDefaultFlags.extensions = true).
list_installable_profiles() {
  [[ -f "$STORAGE_JSON" ]] || return 0
  python3 - "$STORAGE_JSON" <<'PY'
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
for p in data.get('userDataProfiles', []):
    if p.get('useDefaultFlags', {}).get('extensions'):
        continue
    print(p['name'])
PY
}

install_to_profile() {
  local vsix="$1" profile="${2:-}"
  if [[ -z "$profile" ]]; then
    log "Installing to default profile..."
    code --install-extension "$vsix" --force
  else
    log "Installing to profile: $profile"
    if ! code --profile "$profile" --install-extension "$vsix" --force; then
      warn "Install to '$profile' failed (continuing)"
      return 1
    fi
  fi
}

main() {
  ensure_vscode_closed
  pull_latest

  local vsix
  vsix=$(build_vsix)
  log "Built: $(basename "$vsix")"

  log "Repairing extensions.json (removing dangling entries)..."
  repair_extensions_json

  install_to_profile "$vsix"

  local failed=0
  while IFS= read -r profile; do
    [[ -z "$profile" ]] && continue
    install_to_profile "$vsix" "$profile" || failed=$((failed + 1))
  done < <(list_installable_profiles)

  echo
  ok "VSIX: $(basename "$vsix")"
  ok "Reopen VS Code to load the updated theme/icons."
  if (( failed > 0 )); then
    warn "$failed profile install(s) failed; check output above."
    exit 1
  fi
}

main "$@"
