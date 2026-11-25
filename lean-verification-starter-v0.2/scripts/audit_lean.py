#!/usr/bin/env python3
"""Conservative source/configuration preflight; not a Lean kernel verifier."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

PATTERNS = {
    "sorry_token": re.compile(r"\bsorry\b"),
    "admit_token": re.compile(r"\badmit\b"),
    "axiom_declaration": re.compile(r"(?m)^\s*(?:private\s+)?axiom\s+"),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    lean_files = sorted(p for p in root.rglob("*.lean") if ".lake" not in p.parts and "build" not in p.parts)
    findings = []
    for path in lean_files:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append({"file": str(path.relative_to(root)), "kind": "decode_error", "line": None})
            continue
        for kind, pattern in PATTERNS.items():
            for match in pattern.finditer(content):
                line = content.count("\n", 0, match.start()) + 1
                findings.append({"file": str(path.relative_to(root)), "kind": kind, "line": line})
    toolchain = root / "lean-toolchain"
    toolchain_value = toolchain.read_text(encoding="utf-8").strip() if toolchain.exists() else None
    placeholder = bool(toolchain_value and ("X.Y.Z" in toolchain_value or "<" in toolchain_value or "TODO" in toolchain_value))
    result = {
        "check": "lean_source_preflight",
        "classification": "static_text_scan_not_kernel_verification",
        "lean_files_scanned": len(lean_files),
        "toolchain_file_present": toolchain.exists(),
        "toolchain_value": toolchain_value,
        "toolchain_placeholder_detected": placeholder,
        "findings": findings,
        "passed": not findings and toolchain.exists() and not placeholder,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1

if __name__ == "__main__":
    sys.exit(main())
