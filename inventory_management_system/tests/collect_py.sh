#!/usr/bin/env bash
set -euo pipefail

out="${1:-collected_python_files.txt}"
dir="${2:-.}"

if [ ! -d "$dir" ]; then
  echo "Error: not a directory: $dir" >&2
  exit 1
fi

# Truncate/create output file
: > "$out"

shopt -s nullglob 2>/dev/null || true
for f in "$dir"/*.py; do
  [ -e "$f" ] || continue
  printf '===== File: %s =====\n' "$f" >> "$out"
  cat "$f" >> "$out"
  printf '\n\n' >> "$out"
done

echo "Collected $(ls -1 "$dir"/*.py 2>/dev/null | wc -l) .py files into: $out"