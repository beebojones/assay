#!/usr/bin/env python3
"""Reveal the blind mapping. Run only after scoring is done.

Reads the key file written by shuffle.py and prints the letter->model mapping.

CLI:
    python scripts/reveal.py /path/outside/repo/assay.key.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python scripts/reveal.py <key-path>", file=sys.stderr)
        return 2

    key_path = Path(argv[1])
    if not key_path.is_file():
        print(f"key file not found: {key_path}", file=sys.stderr)
        return 2

    try:
        payload = json.loads(key_path.read_text(encoding="utf-8"))
        mapping = payload["mapping"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"could not read mapping from {key_path}: {exc}", file=sys.stderr)
        return 1

    print(f"Reveal ({len(mapping)} entries) from {key_path}:\n")
    for letter in sorted(mapping):
        entry = mapping[letter]
        model = entry.get("model", "?") if isinstance(entry, dict) else entry
        print(f"  {letter}  ->  {model}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
