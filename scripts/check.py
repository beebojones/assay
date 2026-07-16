#!/usr/bin/env python3
"""Leak scanner for blinded HTML builds.

Scans every .html file under builds/ for vendor tells and for any <title>
that is not exactly the expected value. It reports findings (file, line,
matched string) and never modifies a build. Run it before shuffling, and
shuffle.py imports scan_builds() to gate the blinding step.

CLI:
    python scripts/check.py [builds_dir]

Exit code is nonzero if any finding is reported.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Extend this list as new models enter the bake-off. Matching is
# case-insensitive and bounded to whole tokens (so "gpt" does not fire on a
# random base64 blob, but "GPT", "claude-opus", and "z.ai" all do).
VENDOR_TELLS = [
    "claude", "anthropic",
    "glm", "z.ai", "zhipu",
    "warp",
    "manus",
    "gpt", "openai", "codex",
    "gemini", "google",
    "llama", "meta",
    "mistral",
    "deepseek",
    "qwen",
    "grok", "xai",
    "copilot",
]

# The <title> of every build must be exactly this. Anything else is a tell.
EXPECTED_TITLE = "Cosmic Pinball"

# Whole-token match: the tell may not be flanked by another letter/digit.
# This keeps "meta" from matching "metadata" while still catching "meta,"
# "<meta", "Meta" and "z.ai".
_TELL_PATTERNS = [
    (tell, re.compile(r"(?<![A-Za-z0-9])" + re.escape(tell) + r"(?![A-Za-z0-9])",
                      re.IGNORECASE))
    for tell in VENDOR_TELLS
]

_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


class Finding:
    """A single leak: which file, which line, what matched, and why."""

    def __init__(self, path: Path, line: int, matched: str, reason: str):
        self.path = path
        self.line = line
        self.matched = matched
        self.reason = reason

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.reason}: {self.matched!r}"


def scan_text(path: Path, text: str) -> list[Finding]:
    """Return all findings for one file's contents."""
    findings: list[Finding] = []
    lines = text.splitlines()

    # Vendor tells, anywhere in the file, any casing.
    for lineno, line in enumerate(lines, start=1):
        for _tell, pattern in _TELL_PATTERNS:
            for m in pattern.finditer(line):
                # "meta" (the Meta/Llama tell) collides with the HTML <meta>
                # element, which every mobile build legitimately uses for the
                # viewport/charset tags. Suppress only when it is the tag NAME
                # (preceded by "<" or "</"); "Meta" in text, attribute values,
                # or comments still flags. No other tell is an HTML element.
                if m.group(0).lower() == "meta":
                    before = line[: m.start()]
                    if before.endswith("<") or before.endswith("</"):
                        continue
                findings.append(
                    Finding(path, lineno, m.group(0), "vendor tell")
                )

    # Title check. A missing title is also a tell (the build should have one).
    match = _TITLE_RE.search(text)
    if match is None:
        findings.append(
            Finding(path, 1, "<no title>",
                    f"missing <title> (expected {EXPECTED_TITLE!r})")
        )
    else:
        title = match.group(1).strip()
        if title != EXPECTED_TITLE:
            lineno = text[: match.start()].count("\n") + 1
            findings.append(
                Finding(path, lineno, title,
                        f"unexpected <title> (expected {EXPECTED_TITLE!r})")
            )

    return findings


def scan_file(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return scan_text(path, text)


def scan_builds(builds_dir: Path) -> list[Finding]:
    """Scan every .html under builds_dir. Returns all findings, sorted."""
    findings: list[Finding] = []
    for html in sorted(builds_dir.glob("*.html")):
        findings.extend(scan_file(html))
    return findings


def main(argv: list[str]) -> int:
    builds_dir = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent.parent / "builds"
    if not builds_dir.is_dir():
        print(f"builds directory not found: {builds_dir}", file=sys.stderr)
        return 2

    findings = scan_builds(builds_dir)
    if not findings:
        n = len(list(builds_dir.glob("*.html")))
        print(f"clean: no leaks in {n} build(s) under {builds_dir}")
        return 0

    print(f"LEAKS FOUND ({len(findings)}):", file=sys.stderr)
    for f in findings:
        print(f"  {f}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
