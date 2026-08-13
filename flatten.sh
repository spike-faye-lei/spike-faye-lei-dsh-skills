#!/usr/bin/env bash
# Flatten categorized skills into a flat directory for DSH installation.
# DSH discovers skills one level deep (<root>/<name>/SKILL.md), so the
# categorized layout (skills/<category>/<name>/SKILL.md) must be flattened.
#
# Usage: ./flatten.sh [target-dir]   (default: ~/.dsh/skills)
set -u
TARGET="${1:-$HOME/.dsh/skills}"
mkdir -p "$TARGET"

count=0
for d in skills/*/*/; do
  name="$(basename "$d")"
  if [ -d "$TARGET/$name" ]; then
    echo "skip (exists): $name"
    continue
  fi
  cp -r "$d" "$TARGET/$name"
  count=$((count+1))
done
echo "flattened $count skills into $TARGET"
