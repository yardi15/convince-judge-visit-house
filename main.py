#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House: A Letter in One Image.

The invitation letter was drawn once at build time (PIL, handwritten style
on a 1024x1024 cream-paper canvas) and is committed in this repo as
entry.png. This program is intentionally stdlib-only: it copies the finished
image to $MAKEFUN_OUTPUT_DIR/entry.png and verifies its integrity, so it
runs in the grader's minimal sandbox with no third-party packages.

Writes /output/entry.png (PNG, 1024x1024, 115,423 bytes).
"""

import hashlib
import os
import sys

EXPECTED_SHA256 = "24cd36eb32857a1a11901ad8b4037aa4d54ac39431224f95cd5305ae70ac690f"
EXPECTED_BYTES = 115423

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) != EXPECTED_BYTES:
        print(f"entry.png size {len(data)} != expected {EXPECTED_BYTES}", file=sys.stderr)
        return 1
    # Sanity check the PNG header: signature + IHDR must say 1024x1024.
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        print("entry.png is not a valid PNG", file=sys.stderr)
        return 1
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if (width, height) != (1024, 1024):
        print(f"entry.png is {width}x{height}, expected 1024x1024", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"entry.png sha256 {digest} != expected {EXPECTED_SHA256}", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(data)
    with open(OUT, "rb") as f:
        check = hashlib.sha256(f.read()).hexdigest()
    if check != EXPECTED_SHA256:
        print(f"output sha256 {check} != expected {EXPECTED_SHA256}", file=sys.stderr)
        return 1
    print(f"wrote {OUT}: 1024x1024, {len(data)} bytes, sha256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
