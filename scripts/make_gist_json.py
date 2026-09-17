#!/usr/bin/env python3
"""Produce a copy of challenge.json whose image URLs point somewhere else.

The committed challenge.json points its images at the GitHub Pages site. If the
JSON is served from a Gist instead, the images still need a host, and it will
not be Pages unless Pages is enabled. This rewrites the image base so the two
halves agree, without hand-editing the document.

  # images straight from the repo, no Pages needed
  python3 scripts/make_gist_json.py --image-base \
      https://raw.githubusercontent.com/aruana-lumiform/mobile-code-challenge-tools/main/public/code-challenge/

Then paste the result into the Gist. Re-run it whenever challenge.json changes:
the Gist is a copy, and copies drift.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "public" / "code-challenge" / "challenge.json"
DEFAULT_OUT = ROOT / "dist" / "challenge.gist.json"


def rewrite(node: dict, image_base: str) -> int:
    """Repoint every image src at image_base, keeping its filename. Returns the count."""
    rewritten = 0
    if node.get("type") == "image" and isinstance(node.get("src"), str):
        node["src"] = image_base + node["src"].rsplit("/", 1)[-1]
        rewritten += 1
    for child in node.get("items", []):
        if isinstance(child, dict):
            rewritten += rewrite(child, image_base)
    return rewritten


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--image-base", required=True,
                        help="URL prefix for the images; must end with a slash")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help=f"where to write (default: {DEFAULT_OUT.relative_to(ROOT)})")
    args = parser.parse_args()

    if not args.image_base.endswith("/"):
        print("error: --image-base must end with a slash", file=sys.stderr)
        return 2

    document = json.loads(SOURCE.read_text(encoding="utf-8"))
    count = rewrite(document, args.image_base)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out} ({count} image URLs repointed at {args.image_base})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
