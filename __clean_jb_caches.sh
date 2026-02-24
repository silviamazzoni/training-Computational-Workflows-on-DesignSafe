#!/usr/bin/env bash
set -euo pipefail

echo "=== Cleaning Jupyter caches ==="
echo "Repo: $(pwd)"
echo

# Root build (sometimes exists)
# if [[ -d "_build" ]]; then
#   echo "Removing ./_build"
#   rm -rf "_build"
# fi

# Per-book build + cache
if [[ -d "books" ]]; then
  for book in books/*; do
    [[ -d "$book" ]] || continue

    # if [[ -d "$book/_build" ]]; then
    #   echo "Removing $book/_build"
    #   rm -rf "$book/_build"
    # fi

    if [[ -d "$book/.jupyter_cache" ]]; then
      echo "Removing $book/.jupyter_cache"
      rm -rf "$book/.jupyter_cache"
    fi
  done
fi

# Everywhere: notebook checkpoints + jupyter_cache directories
echo
echo "Removing all .ipynb_checkpoints under ./books and ./shared"
find ./books ./shared -type d -name ".ipynb_checkpoints" -prune -print -exec rm -rf {} + 2>/dev/null || true

echo
echo "Removing all .jupyter_cache under ./books"
find ./books ./shared -type d -name ".jupyter_cache" -prune -print -exec rm -rf {} + 2>/dev/null || true

echo
echo "=== Done ==="


# chmod +x clean_jb_caches.sh
# ./clean_jb_caches.sh
