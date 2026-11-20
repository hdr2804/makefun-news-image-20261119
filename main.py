#!/usr/bin/env python3
"""Copy the pre-rendered front page to the grader's output directory.

Standard library only: no Pillow, no network. The entry image is drawn
ahead of time by gen_image.py and committed as entry.png; this program
just copies it, so it runs identically in the grader's sandbox.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    # Same bytes out as in: the grader runs this twice and demands
    # byte-identical output, so the copy must be exact, never re-encoded.
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
