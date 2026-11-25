#!/usr/bin/env python3
"""Verify the project-local SHA-256 source manifest.

This checks file integrity only. It does not verify Lean proofs or semantics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any


_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_TOP_LEVEL_KEYS = {
    "schema_version", "algorithm", "scope", "self_exclusion", "files"
}


def verify_manifest(root: Path, manifest_path: Path) -> dict[str, Any]:
    root = root.resolve()
    manifest_path = manifest_path.resolve()
    errors: list[str] = []

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {"ok": False, "checked_files": 0,
                "errors": [f"cannot read manifest: {exc}"]}

    if not isinstance(data, dict) or set(data) != _TOP_LEVEL_KEYS:
        return {"ok": False, "checked_files": 0,
                "errors": ["manifest must contain exactly the documented top-level keys"]}
    if data["schema_version"] != "1.0.0":
        errors.append("unsupported schema_version")
    if data["algorithm"] != "sha256":
        errors.append("algorithm must be sha256")
    if data["scope"] != ".":
        errors.append('scope must be "." (paths are relative to project root)')
    if data["self_exclusion"] != manifest_path.name:
        errors.append("self_exclusion must name this manifest file")
    entries = data["files"]
    if not isinstance(entries, list):
        return {"ok": False, "checked_files": 0,
                "errors": errors + ["files must be an array"]}

    seen: set[str] = set()
    checked = 0
    for index, entry in enumerate(entries):
        prefix = f"files[{index}]"
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "size_bytes"}:
            errors.append(f"{prefix}: invalid entry shape")
            continue
        rel = entry["path"]
        digest = entry["sha256"]
        size = entry["size_bytes"]
        if not isinstance(rel, str) or not rel:
            errors.append(f"{prefix}: path must be a non-empty string")
            continue
        posix = PurePosixPath(rel)
        if posix.is_absolute() or ".." in posix.parts or "." in posix.parts:
            errors.append(f"{prefix}: unsafe relative path {rel!r}")
            continue
        if rel in seen:
            errors.append(f"{prefix}: duplicate path {rel!r}")
            continue
        seen.add(rel)
        if not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest):
            errors.append(f"{prefix}: invalid SHA-256 digest")
            continue
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            errors.append(f"{prefix}: size_bytes must be a non-negative integer")
            continue

        target = root.joinpath(*posix.parts)
        try:
            resolved = target.resolve(strict=True)
            resolved.relative_to(root)
        except (OSError, ValueError):
            errors.append(f"{prefix}: missing file or path escapes project root: {rel!r}")
            continue
        if target.is_symlink() or not resolved.is_file():
            errors.append(f"{prefix}: expected a regular non-symlink file: {rel!r}")
            continue
        payload = resolved.read_bytes()
        checked += 1
        actual_size = len(payload)
        actual_digest = hashlib.sha256(payload).hexdigest()
        if actual_size != size:
            errors.append(f"{rel}: size mismatch (expected {size}, got {actual_size})")
        if actual_digest != digest:
            errors.append(f"{rel}: SHA-256 mismatch")

    return {"ok": not errors, "checked_files": checked, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1],
                        help="project root (default: parent of scripts/)")
    parser.add_argument("--manifest", type=Path, default=None,
                        help="manifest path (default: ROOT/MANIFEST.sha256.json)")
    args = parser.parse_args()
    manifest = args.manifest or (args.root / "MANIFEST.sha256.json")
    result = verify_manifest(args.root, manifest)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
