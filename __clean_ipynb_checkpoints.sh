#!/usr/bin/env bash
set -euo pipefail

echo "=== Removing all .ipynb_checkpoints directories (scoped) ==="

# Change these roots if you want (recommended: keep it narrow)
ROOTS=( "./books" "./shared" )

for root in "${ROOTS[@]}"; do
  [[ -d "$root" ]] || continue
  echo "--- Searching in: $root ---"
  find "$root" \
    -type d -name ".ipynb_checkpoints" -prune \
    -print -exec rm -rf {} +
done

echo "=== Done ==="


# chmod +x clean_ipynb_checkpoints.sh
# ./clean_ipynb_checkpoints.sh
