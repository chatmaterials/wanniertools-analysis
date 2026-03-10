#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


TASK_MAP = {
    "bulk-band": "BulkBand_calc = T",
    "surface-state": "SlabSS_calc = T",
    "fermi-arc": "SlabArc_calc = T",
    "wilson-loop": "WannierCenter_calc = T",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a conservative WannierTools input template.")
    parser.add_argument("directory", help="Output directory for the workflow.")
    parser.add_argument("--task", choices=sorted(TASK_MAP), required=True)
    parser.add_argument("--hr-file", default="wannier90_hr.dat")
    parser.add_argument("--num-occupied", type=int, required=True)
    parser.add_argument("--surface", default="1 0 0")
    parser.add_argument("--system", default="WannierTools analysis")
    return parser.parse_args()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n")


def write_workflow_plan(root: Path, task: str, notes: list[str]) -> None:
    lines = [
        "# Workflow Plan",
        "",
        f"- Task: `{task}`",
        "",
        "## Stages",
        "",
        "### WannierTools Setup",
        "- Directory: `.`",
        "- Purpose: Finalize wt.in against a validated Wannier model before launching WannierTools.",
        "- Depends on: A trustworthy `wannier90_hr.dat` model and physically justified path or plane settings",
        "- Files: `wt.in.template`, `README.next-steps`",
        "",
        "## Notes",
        "",
    ]
    lines.extend(f"- {note}" for note in notes)
    write(root / "WORKFLOW_PLAN.md", "\n".join(lines))


def template(args: argparse.Namespace) -> str:
    lines = [
        "&TB_FILE",
        f" Hrfile = '{args.hr_file}'",
        "/",
        "",
        "&CONTROL",
        f" {TASK_MAP[args.task]}",
        "/",
        "",
        "&SYSTEM",
        f" NumOccupied = {args.num_occupied}",
        "/",
        "",
        "# Replace the placeholders below with a physically justified setup.",
        f"# System: {args.system}",
        f"SURFACE = {args.surface}",
    ]
    if args.task == "bulk-band":
        lines.extend(
            [
                "KPATH_BULK = 0.0 0.0 0.0   0.5 0.0 0.0",
            ]
        )
    elif args.task == "surface-state":
        lines.extend(
            [
                "KPATH_SLAB = 0.0 0.0   0.5 0.0",
            ]
        )
    elif args.task == "fermi-arc":
        lines.extend(
            [
                "KPLANE_SLAB = 0.0 0.0   1.0 0.0   0.0 1.0",
            ]
        )
    else:
        lines.extend(
            [
                "KPLANE_BULK = 0.0 0.0 0.0   1.0 0.0 0.0   0.0 1.0 0.0",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    if args.num_occupied <= 0:
        raise SystemExit("--num-occupied must be a positive integer")
    root = Path(args.directory).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    write(root / "wt.in.template", template(args))
    notes = [
        f"Task: {args.task}",
        f"HR file assumption: {args.hr_file}",
        f"NumOccupied assumption: {args.num_occupied}",
        "Do not run the template until the surface and k-space placeholders are replaced with physically justified values.",
    ]
    if args.task in {"surface-state", "fermi-arc"}:
        notes.append("Confirm the chosen surface normal is physically intended before running slab-related analysis.")
    write(root / "README.next-steps", "\n".join(f"- {line}" for line in notes))
    write_workflow_plan(root, args.task, notes)


if __name__ == "__main__":
    main()
