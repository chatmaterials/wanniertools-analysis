#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def inspect(path: Path) -> dict[str, object]:
    root = path if path.is_dir() else path.parent
    input_file = root / "wt.in"
    template_file = root / "wt.in.template"
    active = input_file if input_file.exists() else template_file if template_file.exists() else None
    missing = []
    warnings = []
    if active is None:
        missing.append("wt.in or wt.in.template")
        return {"path": str(root), "missing_files": missing, "warnings": warnings}
    text = active.read_text(errors="ignore")
    match = re.search(r"Hrfile\s*=\s*'([^']+)'", text)
    if match:
        hr_path = root / match.group(1)
        if not hr_path.exists():
            warnings.append(f"Referenced HR file not found in this directory: {match.group(1)}")
    if "SURFACE = 1 0 0" in text and "# Replace the placeholders below with a physically justified setup." in text:
        warnings.append("Surface orientation still looks like the default placeholder.")
    if "KPATH_BULK = 0.0 0.0 0.0   0.5 0.0 0.0" in text:
        warnings.append("Bulk-band path still contains the placeholder example.")
    if "KPATH_SLAB = 0.0 0.0   0.5 0.0" in text:
        warnings.append("Surface-state path still contains the placeholder example.")
    if "KPLANE_SLAB = 0.0 0.0   1.0 0.0   0.0 1.0" in text:
        warnings.append("Fermi-arc plane still contains the placeholder example.")
    if "KPLANE_BULK = 0.0 0.0 0.0   1.0 0.0 0.0   0.0 1.0 0.0" in text:
        warnings.append("Wilson-loop plane still contains the placeholder example.")
    if "BulkBand_calc = T" in text and "KPATH_BULK" not in text:
        warnings.append("Bulk-band mode is active but no KPATH_BULK definition was found.")
    if "SlabSS_calc = T" in text and "KPATH_SLAB" not in text:
        warnings.append("Surface-state mode is active but no KPATH_SLAB definition was found.")
    if "SlabArc_calc = T" in text and "KPLANE_SLAB" not in text:
        warnings.append("Fermi-arc mode is active but no KPLANE_SLAB definition was found.")
    if "WannierCenter_calc = T" in text and "KPLANE_BULK" not in text:
        warnings.append("Wilson-loop mode is active but no KPLANE_BULK definition was found.")
    if ".template" in active.name:
        warnings.append("The active input is still a template, not a finalized wt.in file.")
    return {"path": str(root), "missing_files": missing, "warnings": warnings}


def main() -> None:
    parser = argparse.ArgumentParser(description="Check a WannierTools directory for missing inputs and model files.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    record = inspect(Path(args.path).expanduser().resolve())
    if args.json:
        print(json.dumps(record, indent=2))
        return
    print(f"Path: {record['path']}")
    if record["missing_files"]:
        print("Missing files: " + ", ".join(record["missing_files"]))
    if record["warnings"]:
        print("Warnings: " + "; ".join(record["warnings"]))


if __name__ == "__main__":
    main()
