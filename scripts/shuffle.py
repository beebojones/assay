#!/usr/bin/env python3
"""Blinding step for the bake-off.

Takes the model-named builds in builds/, randomly assigns each to a letter
(a, b, c, ... continuing past d for larger N), copies them to the repo root
as <letter>.html, and regenerates index.html and SCORECARD.md for the current
N. The secret letter->model mapping is written to a key path you pass on the
command line; that path MUST live outside the repo so it can never be
committed.

Nothing about the mapping is printed. stdout gets only the count and the key
location.

CLI:
    python scripts/shuffle.py /path/outside/repo/assay.key.json
"""

from __future__ import annotations

import json
import random
import shutil
import string
import sys
from pathlib import Path

import check  # same directory; imported, never shelled out to

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILDS_DIR = REPO_ROOT / "builds"
BUILD_PREFIX = "cosmic-pinball-"

CRITERIA = ["Joy", "Feel", "Vox OS fidelity", "Code quality", "Cleverness", "Total"]


def model_label(path: Path) -> str:
    """Derive the model label from cosmic-pinball-<model>.html."""
    stem = path.stem  # filename without .html
    if stem.startswith(BUILD_PREFIX):
        return stem[len(BUILD_PREFIX):]
    return stem


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def parse_key_path(argv: list[str]) -> Path:
    if len(argv) != 2:
        die("usage: python scripts/shuffle.py <key-path-outside-repo>", 2)
    return Path(argv[1])


def guard_key_outside_repo(key_path: Path) -> None:
    """Refuse if the key would land inside the repo. Uses resolved absolute
    paths, not string matching."""
    resolved = key_path.resolve()
    repo = REPO_ROOT.resolve()
    if resolved == repo or resolved.is_relative_to(repo):
        die(
            "refusing to write the key inside the repo:\n"
            f"  key : {resolved}\n"
            f"  repo: {repo}\n"
            "Pass a path outside the repo so the mapping can never be committed.",
            2,
        )


def wipe_stale_letters() -> None:
    """Remove any single-letter .html files left at the repo root by a prior,
    possibly larger, run so a smaller N cannot leave orphans behind."""
    for letter in string.ascii_lowercase:
        stale = REPO_ROOT / f"{letter}.html"
        if stale.exists():
            stale.unlink()


def generate_index(letters: list[str]) -> None:
    """Scaffolding page: one link per letter, letters only, phone-friendly.
    Deliberately plain; not part of the test."""
    items = "\n".join(
        f'    <li><a href="{ltr}.html">{ltr.upper()}</a></li>' for ltr in letters
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bake-off</title>
<style>
  :root {{ color-scheme: dark; }}
  html, body {{ margin: 0; padding: 0; background: #0a0a0b; color: #f2f2f4;
    font: 500 18px/1.4 system-ui, -apple-system, sans-serif; }}
  main {{ max-width: 640px; margin: 0 auto; padding: 24px 16px 64px; }}
  ul {{ list-style: none; margin: 0; padding: 0; }}
  li {{ margin: 0 0 16px; }}
  a {{ display: block; padding: 24px; text-align: center; text-decoration: none;
    color: #f2f2f4; background: #17171a; border: 1px solid #2a2a2e;
    border-radius: 12px; font-size: 28px; letter-spacing: 0.02em; }}
  a:active {{ background: #202024; }}
</style>
</head>
<body>
<main>
  <ul>
{items}
  </ul>
</main>
</body>
</html>
"""
    (REPO_ROOT / "index.html").write_text(html, encoding="utf-8")


def generate_scorecard(letters: list[str]) -> None:
    """Blind scorecard: one column per letter, one row per criterion, plus an
    empty notes subsection per letter. Letters only."""
    header = "| Criterion | " + " | ".join(letters) + " |"
    divider = "|" + "---|" * (len(letters) + 1)
    rows = [f"| {c} | " + " | ".join("" for _ in letters) + " |" for c in CRITERIA]

    notes = "\n".join(f"### {ltr}\n" for ltr in letters)

    md = (
        "# Scorecard\n\n"
        "Score each entry blind. Letters only — no model names.\n\n"
        f"{header}\n{divider}\n" + "\n".join(rows) + "\n\n"
        "## Notes\n\n"
        f"{notes}"
    )
    (REPO_ROOT / "SCORECARD.md").write_text(md, encoding="utf-8")


def write_key(key_path: Path, mapping: dict[str, dict[str, str]]) -> None:
    payload = {
        "note": "Secret letter->model mapping for the bake-off. Keep outside the repo.",
        "count": len(mapping),
        "mapping": mapping,
    }
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    key_path = parse_key_path(argv)
    guard_key_outside_repo(key_path)

    if not BUILDS_DIR.is_dir():
        die(f"builds directory not found: {BUILDS_DIR}", 2)

    builds = sorted(BUILDS_DIR.glob("*.html"))
    n = len(builds)
    if n < 2:
        die(
            f"need at least 2 builds to shuffle, found {n} in {BUILDS_DIR}.\n"
            "Drop the model builds in as cosmic-pinball-<model>.html first.",
            2,
        )
    if n > 26:
        die(f"too many builds ({n}); only 26 letters a-z are available.", 2)

    # Gate on leaks first. Import the logic, do not shell out.
    findings = check.scan_builds(BUILDS_DIR)
    if findings:
        print(f"aborting shuffle: {len(findings)} leak(s) found. Fix these first:",
              file=sys.stderr)
        for f in findings:
            print(f"  {f}", file=sys.stderr)
        return 1

    # Randomly assign builds to letters.
    letters = list(string.ascii_lowercase[:n])
    shuffled = builds[:]
    random.shuffle(shuffled)

    wipe_stale_letters()

    mapping: dict[str, dict[str, str]] = {}
    for letter, build in zip(letters, shuffled):
        shutil.copyfile(build, REPO_ROOT / f"{letter}.html")
        mapping[letter] = {"model": model_label(build), "source": build.name}

    generate_index(letters)
    generate_scorecard(letters)
    write_key(key_path, mapping)

    print(f"shuffled {n} build(s) into letters {letters[0]}..{letters[-1]}")
    print(f"key written to {key_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
