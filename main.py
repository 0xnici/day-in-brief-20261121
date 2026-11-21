#!/usr/bin/env python3
"""Entry point for the 21 November 2026 front page.

The front page is composed ahead of time by tools/render.py and stored
beside this file as entry.png. At grade time there is no network and no
clock to consult, so the whole job here is a careful copy: verify the
asset really is the page we shipped, then place it at /output/entry.png
byte for byte.
"""
import os
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
TARGET = os.path.join(TARGET_DIR, "entry.png")


def read_page() -> bytes:
    with open(SOURCE, "rb") as fh:
        blob = fh.read()
    if not blob.startswith(PNG_SIGNATURE):
        raise SystemExit("entry.png is not a PNG file")
    if len(blob) > 1024 * 1024:
        raise SystemExit("entry.png exceeds the 1 MiB limit")
    # The IHDR chunk follows the signature: width and height are the two
    # big-endian uint32s at bytes 16..24. The rules cap the page at
    # 1024x1024, so refuse anything larger before it is published.
    width = int.from_bytes(blob[16:20], "big")
    height = int.from_bytes(blob[20:24], "big")
    if width > 1024 or height > 1024:
        raise SystemExit(f"entry.png is {width}x{height}, over the 1024x1024 cap")
    return blob


def publish(blob: bytes) -> None:
    os.makedirs(TARGET_DIR, exist_ok=True)
    # Write the page directly with ordinary permissions. A grader-side
    # reader may run as a different user than this process, so the file
    # must stay world-readable: no mkstemp (its 0600 mode made an earlier
    # edition's run fail) and an explicit chmod to be sure.
    with open(TARGET, "wb") as fh:
        fh.write(blob)
    os.chmod(TARGET, 0o644)
    with open(TARGET, "rb") as fh:
        if fh.read() != blob:
            raise SystemExit("published page does not match the source")


def main() -> int:
    blob = read_page()
    publish(blob)
    print(f"published {TARGET} ({len(blob)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
