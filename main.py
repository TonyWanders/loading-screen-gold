#!/usr/bin/env python3
"""Write one loading-screen tip to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The tip is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 200 characters, one line, not only white space.
"""

import os
import sys
from pathlib import Path

TIP = (
    "Tip: your agent just rewrote your code while you blinked. "
    "Read the diff, keep what works. "
    "You are the senior now, and your intern never sleeps."
)

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def check_one_line(text: str) -> None:
    """Reject text that is not a single line or that holds an em dash."""
    if "\n" in text or "\r" in text:
        raise ValueError("tip is not one line")
    if "\u2014" in text:
        raise ValueError("tip contains an em dash")


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 200 chars, one line.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"tip is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("tip is only white space")
    check_one_line(text)
    return chars


def main() -> int:
    try:
        chars = validate(TIP)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TIP, encoding="utf-8")
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
