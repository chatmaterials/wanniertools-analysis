#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


def find_output(path: Path) -> Path | None:
    if path.is_file():
        return path
    for name in ("WT.out", "wt.out"):
        candidate = path / name
        if candidate.exists():
            return candidate
    files = sorted(path.glob("*.out"))
    return files[0] if files else None


def summarize(path: Path) -> dict[str, object]:
    output = find_output(path)
    text = output.read_text(errors="ignore") if output else ""
    lower = text.lower()
    warnings = []
    if "warning" in lower:
        warnings.append("WannierTools output contains warning lines.")
    if "error" in lower:
        warnings.append("WannierTools output contains error lines.")
    if output is None:
        warnings.append("No WT.out-style file was found in this path yet.")
    produced = [item.name for item in path.iterdir()] if path.is_dir() else [path.name]
    return {
        "path": str(path),
        "output_file": str(output) if output else None,
        "completed": "Congratulations" in text or "program ends normally" in lower,
        "warnings": warnings,
        "notable_outputs": [name for name in produced if name.endswith((".dat", ".gnu", ".bxsf"))][:10],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a WannierTools working directory or output file.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    record = summarize(Path(args.path).expanduser().resolve())
    if args.json:
        print(json.dumps(record, indent=2))
        return
    print(f"Path: {record['path']}")
    print(f"Output: {record['output_file']}")
    print(f"Completed: {record['completed']}")
    if record["warnings"]:
        print("Warnings: " + "; ".join(record["warnings"]))
    if record["notable_outputs"]:
        print("Notable outputs: " + ", ".join(record["notable_outputs"]))


if __name__ == "__main__":
    main()
