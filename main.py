#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House: A Letter in One Image.

The invitation letter was drawn once at build time — a warm, funny,
handwritten-style letter to the AI judge on a 1024x1024 cream-paper canvas,
with a small drawn house scene on top — and is committed in this repo as
entry.png.

This program is deliberately stdlib-only. It copies the finished image to
$MAKEFUN_OUTPUT_DIR/entry.png and checks it on the way through, so it runs
in the grader's minimal sandbox with no third-party packages installed.
The earlier version redrew the picture at run time with PIL; the grader's
image has no PIL, so that version exited with code 1. Copying the finished
image is the fix.
"""

import hashlib
import os
import sys

# The finished invitation letter, as committed in this repo.
EXPECTED_SHA256 = "24cd36eb32857a1a11901ad8b4037aa4d54ac39431224f95cd5305ae70ac690f"
EXPECTED_SIZE = 115423
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(SCRIPT_DIR, "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DESTINATION = os.path.join(OUTPUT_DIR, "entry.png")


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def check_png(data):
    """Check the bytes are a 1024x1024 PNG; return an error string or None."""
    if len(data) != EXPECTED_SIZE:
        return f"size is {len(data)} bytes, expected {EXPECTED_SIZE}"
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return "missing PNG signature"
    if data[12:16] != b"IHDR":
        return "first chunk is not IHDR"
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        return "missing or truncated IEND chunk"
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        return f"dimensions are {width}x{height}, expected 1024x1024"
    return None


def main():
    try:
        with open(SOURCE, "rb") as handle:
            image = handle.read()
    except OSError as exc:
        return fail(f"cannot read {SOURCE}: {exc}")

    problem = check_png(image)
    if problem is not None:
        return fail(f"entry.png failed its checks: {problem}")

    digest = hashlib.sha256(image).hexdigest()
    if digest != EXPECTED_SHA256:
        return fail(f"sha256 {digest} does not match the committed image")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        with open(DESTINATION, "wb") as handle:
            handle.write(image)
        with open(DESTINATION, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        return fail(f"cannot write {DESTINATION}: {exc}")

    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        return fail("the written file does not match the source image")

    print(f"wrote {DESTINATION}: 1024x1024, {len(image)} bytes, sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
