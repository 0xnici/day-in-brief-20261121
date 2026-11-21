#!/usr/bin/env python3
"""Place this repository's entry image at the grader's output path.

The image in this repository is the entry. This program only copies it
to /output/entry.png, using nothing but the standard library, and it
touches no network at all.
"""

import hashlib
import os
import shutil
import sys


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo_dir, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    if _sha256(source) != _sha256(target):
        print("error: copied file differs from source", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (target, os.path.getsize(target)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
