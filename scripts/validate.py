#!/usr/bin/env python3
"""Validate the hosted challenge JSON before it is published.

Checks that:
  * the JSON parses;
  * every node uses a known type and carries the fields that type requires;
  * every image `src` points at this site and at a file that actually exists
    in `public/`, so a candidate never hits a 404 mid-challenge.

Usage: python3 scripts/validate.py
Exits non-zero (and prints every problem it found) if anything is wrong.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
JSON_PATH = PUBLIC / "code-challenge" / "challenge.json"

# Change these two if the repository is ever renamed or transferred; the image
# URLs inside challenge.json must keep matching the site they are served from.
OWNER = "aruana-lumiform"
REPO = "mobile-code-challenge-tools"
BASE_URL = f"https://{OWNER}.github.io/{REPO}/"

CONTAINER_TYPES = {"page", "section"}
LEAF_TYPES = {"text", "question", "image"}

errors: list[str] = []


def fail(path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def check_node(node: object, path: str) -> None:
    if not isinstance(node, dict):
        fail(path, f"expected an object, got {type(node).__name__}")
        return

    node_type = node.get("type")
    if node_type in CONTAINER_TYPES:
        if not node.get("title"):
            fail(path, f"{node_type} is missing a non-empty 'title'")
        items = node.get("items")
        if not isinstance(items, list) or not items:
            fail(path, f"{node_type} is missing a non-empty 'items' array")
            return
        for index, child in enumerate(items):
            child_type = child.get("type") if isinstance(child, dict) else "?"
            check_node(child, f"{path}.items[{index}]({child_type})")

    elif node_type in {"text", "question"}:
        if not node.get("content"):
            fail(path, f"{node_type} is missing a non-empty 'content'")

    elif node_type == "image":
        if not node.get("title"):
            fail(path, "image is missing a non-empty 'title'")
        check_image_src(node.get("src"), path)

    else:
        known = ", ".join(sorted(CONTAINER_TYPES | LEAF_TYPES))
        fail(path, f"unknown type {node_type!r} (expected one of: {known})")


def check_image_src(src: object, path: str) -> None:
    if not isinstance(src, str) or not src:
        fail(path, "image is missing a non-empty 'src'")
        return
    if not src.startswith(BASE_URL):
        fail(path, f"image src {src!r} does not start with {BASE_URL!r}")
        return
    asset = PUBLIC / src[len(BASE_URL):]
    if not asset.is_file():
        fail(path, f"image src {src!r} has no file at public/{src[len(BASE_URL):]}")


def main() -> int:
    if not JSON_PATH.is_file():
        print(f"error: {JSON_PATH.relative_to(ROOT)} does not exist")
        return 1

    try:
        document = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: {JSON_PATH.relative_to(ROOT)} is not valid JSON: {exc}")
        return 1

    if document.get("type") != "page":
        fail("$", "the document root must be a page")
    check_node(document, "$")

    if errors:
        print(f"{JSON_PATH.relative_to(ROOT)} is invalid:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"{JSON_PATH.relative_to(ROOT)} is valid; all image assets resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
