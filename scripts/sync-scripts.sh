#!/bin/bash
# scripts/sync-scripts.sh
# Sync canonical ZooData shared runtime files to all amazon-* skill directories.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT_SOURCE="$REPO_ROOT/zoodata/scripts/zoodata.py"
CONTRACT_SOURCE="$REPO_ROOT/zoodata/references/cli-contract.md"
CHECK_ONLY=0

if [[ ${1:-} == "--check" ]]; then
  CHECK_ONLY=1
elif [[ $# -gt 0 ]]; then
  echo "Usage: $0 [--check]"
  exit 2
fi

# Doc-only skills that do not embed the ZooData CLI/runtime contract.
SKIP_SKILLS=()

for source in "$SCRIPT_SOURCE" "$CONTRACT_SOURCE"; do
  if [[ ! -f "$source" ]]; then
    echo "ERROR: Canonical source file does not exist: $source"
    exit 1
  fi
done

changed=0
total=0
conflict=0
skipped=0

sync_managed_file() {
  local source=$1
  local target=$2
  local skill_name=$3
  local relative_target=$4

  if [[ ! -f "$target" ]]; then
    if [[ $CHECK_ONLY -eq 1 ]]; then
      echo "  MISSING $skill_name/$relative_target"
      conflict=$((conflict + 1))
    else
      mkdir -p "$(dirname "$target")"
      cp "$source" "$target"
      echo "  SYNC $skill_name/$relative_target"
      changed=$((changed + 1))
    fi
    return
  fi

  if diff -q "$source" "$target" &>/dev/null; then
    echo "  OK   $skill_name/$relative_target"
    return
  fi

  if [[ $CHECK_ONLY -eq 1 ]]; then
    echo "  OUT-OF-SYNC $skill_name/$relative_target"
    conflict=$((conflict + 1))
  elif grep -q "Canonical source - do not edit copies" "$target"; then
    cp "$source" "$target"
    echo "  SYNC $skill_name/$relative_target"
    changed=$((changed + 1))
  else
    echo "  CONFLICT $skill_name/$relative_target has no managed-copy marker"
    echo "           Edit the canonical source and run scripts/sync-scripts.sh"
    conflict=$((conflict + 1))
  fi
}

for skill_dir in "$REPO_ROOT"/amazon-*/; do
  skill_name=$(basename "$skill_dir")

  if [[ ${#SKIP_SKILLS[@]} -gt 0 && " ${SKIP_SKILLS[*]} " == *" $skill_name "* ]]; then
    echo "  SKIP $skill_name (doc-only)"
    skipped=$((skipped + 1))
    continue
  fi

  total=$((total + 1))
  sync_managed_file \
    "$SCRIPT_SOURCE" \
    "$skill_dir/scripts/zoodata.py" \
    "$skill_name" \
    "scripts/zoodata.py"
  sync_managed_file \
    "$CONTRACT_SOURCE" \
    "$skill_dir/references/cli-contract.md" \
    "$skill_name" \
    "references/cli-contract.md"
done

echo ""
if [[ $conflict -gt 0 ]]; then
  echo "ERROR: $conflict shared-file copies are missing, out of sync, or unmanaged."
  echo "Run: bash scripts/sync-scripts.sh"
  exit 1
fi

if [[ $CHECK_ONLY -eq 1 ]]; then
  echo "Shared-file check passed: $total skills, 0 mismatches, $skipped skipped."
else
  echo "Done: $total skills processed, $changed files updated, $skipped skipped."
fi
