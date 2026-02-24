#!/usr/bin/env bash
set -euo pipefail

echo "=== Cleaning Jupyter Book build directories ==="

# 1) Remove root-level _build (if present)
if [[ -d "_build" ]]; then
  echo "Removing ./_build"
  rm -rf "_build"
fi

# 2) Remove _build inside each book
if [[ -d "books" ]]; then
  for book in books/*; do
    [[ -d "$book" ]] || continue
    if [[ -d "$book/_build" ]]; then
      echo "Removing $book/_build"
      rm -rf "$book/_build"
    fi
  done
fi

echo "=== Done ==="

# chmod +x clean_build_dirs.sh
# ./clean_build_dirs.sh
