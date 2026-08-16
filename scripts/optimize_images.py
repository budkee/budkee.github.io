#!/usr/bin/env python3
"""Optimize site images and enforce basic quality budgets.

Usage:
  python scripts/optimize_images.py --write
  python scripts/optimize_images.py --check
"""

from __future__ import annotations

import argparse
from pathlib import Path
from tempfile import NamedTemporaryFile

from PIL import Image

SUPPORTED = {".jpg", ".jpeg", ".png"}
SKIP_FILES = {"favicon.ico"}
MIN_MEANINGFUL_SAVINGS_BYTES = 1024


def format_bytes(size: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    value = float(size)
    idx = 0
    while value >= 1024 and idx < len(units) - 1:
        value /= 1024
        idx += 1
    return f"{value:.1f}{units[idx]}"


def resized_size(width: int, height: int, max_dim: int) -> tuple[int, int]:
    if width <= max_dim and height <= max_dim:
        return width, height
    if width >= height:
        new_w = max_dim
        new_h = int(height * (max_dim / width))
    else:
        new_h = max_dim
        new_w = int(width * (max_dim / height))
    return new_w, new_h


def optimize_one(path: Path, quality: int, max_dim: int, write: bool) -> tuple[bool, str]:
    before = path.stat().st_size

    with Image.open(path) as img:
        img.load()
        width, height = img.size
        new_w, new_h = resized_size(width, height, max_dim)
        if (new_w, new_h) != (width, height):
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        suffix = path.suffix.lower()
        if suffix in {".jpg", ".jpeg"} and img.mode not in {"RGB", "L"}:
            img = img.convert("RGB")

        with NamedTemporaryFile(delete=False, suffix=suffix, dir=path.parent) as tmp:
            tmp_path = Path(tmp.name)

        try:
            save_kwargs = {"optimize": True}
            if suffix in {".jpg", ".jpeg"}:
                save_kwargs.update({"quality": quality, "progressive": True})
            img.save(tmp_path, **save_kwargs)

            after = tmp_path.stat().st_size
            saved_bytes = before - after
            changed = saved_bytes >= MIN_MEANINGFUL_SAVINGS_BYTES or (new_w, new_h) != (width, height)

            if write and changed:
                tmp_path.replace(path)
            else:
                tmp_path.unlink(missing_ok=True)

            delta = before - after
            summary = (
                f"{path} | {format_bytes(before)} -> {format_bytes(after)} "
                f"(saved {format_bytes(max(delta, 0))})"
            )
            return changed, summary
        finally:
            if tmp_path.exists() and not write:
                tmp_path.unlink(missing_ok=True)


def ensure_webp(path: Path, quality: int, max_dim: int, write: bool) -> tuple[bool, str]:
    webp_path = path.with_suffix(".webp")
    source_mtime = path.stat().st_mtime
    webp_exists = webp_path.exists()
    webp_is_stale = webp_exists and source_mtime > webp_path.stat().st_mtime

    with Image.open(path) as img:
        img.load()
        width, height = img.size
        new_w, new_h = resized_size(width, height, max_dim)
        if (new_w, new_h) != (width, height):
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        if img.mode not in {"RGB", "RGBA", "L"}:
            img = img.convert("RGBA")

        with NamedTemporaryFile(delete=False, suffix=".webp", dir=path.parent) as tmp:
            tmp_path = Path(tmp.name)

        try:
            img.save(tmp_path, format="WEBP", quality=min(quality, 82), method=6)
            new_size = tmp_path.stat().st_size
            old_size = webp_path.stat().st_size if webp_exists else 0

            # A WebP needs refresh when it does not exist yet or the source is newer.
            needs_update = not webp_exists or webp_is_stale

            if write and needs_update:
                tmp_path.replace(webp_path)
            else:
                tmp_path.unlink(missing_ok=True)

            if webp_exists:
                summary = (
                    f"{webp_path} | {format_bytes(old_size)} -> {format_bytes(new_size)} "
                    f"({'stale' if webp_is_stale else 'ok'})"
                )
            else:
                summary = f"{webp_path} | missing -> {format_bytes(new_size)}"

            return needs_update, summary
        finally:
            if tmp_path.exists() and not write:
                tmp_path.unlink(missing_ok=True)


def iter_images(root: Path):
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in SUPPORTED and p.name not in SKIP_FILES:
            yield p


def main() -> int:
    parser = argparse.ArgumentParser(description="Optimize and validate blog images")
    parser.add_argument("--root", default="src/images", help="Image root directory")
    parser.add_argument("--quality", type=int, default=82, help="JPEG quality")
    parser.add_argument("--max-dim", type=int, default=2200, help="Max width/height in px")
    parser.add_argument(
        "--skip-webp",
        action="store_true",
        help="Disable WebP generation/validation",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Apply optimization in place")
    mode.add_argument("--check", action="store_true", help="Fail if files are not optimized")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Image root not found: {root}")
        return 2

    changed_count = 0
    processed_count = 0

    for img_path in iter_images(root):
        processed_count += 1
        changed, summary = optimize_one(
            img_path, quality=args.quality, max_dim=args.max_dim, write=args.write
        )
        if changed:
            changed_count += 1
        print(summary)

        if not args.skip_webp:
            webp_changed, webp_summary = ensure_webp(
                img_path, quality=args.quality, max_dim=args.max_dim, write=args.write
            )
            if webp_changed:
                changed_count += 1
            print(webp_summary)

    print(f"Processed: {processed_count} | Needs optimization: {changed_count}")

    if args.check and changed_count > 0:
        print(
            "Some images are not optimized or are missing stale WebP files. "
            "Run: python scripts/optimize_images.py --write"
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
