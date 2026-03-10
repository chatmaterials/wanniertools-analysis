#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from check_wanniertools_case import inspect


def render_markdown(path: Path) -> str:
    check = inspect(path)
    warnings = list(check.get("warnings") or [])
    lines = ["# Input Suggestions", "", f"Source: `{path}`", ""]

    if any("HR file" in warning for warning in warnings):
        lines.extend(
            [
                "No direct wt.in patch is enough here.",
                "",
                "```text",
                "# Restore or regenerate wannier90_hr.dat before rerunning.",
                "```",
                "",
            ]
        )

    if any("Bulk-band path" in warning for warning in warnings):
        lines.extend(
            [
                "Bulk-band path scaffold:",
                "",
                "```text",
                "KPATH_BULK = kx1 ky1 kz1   kx2 ky2 kz2",
                "```",
                "",
            ]
        )

    if any("Surface-state path" in warning for warning in warnings):
        lines.extend(
            [
                "Surface-state path scaffold:",
                "",
                "```text",
                "KPATH_SLAB = kx1 ky1   kx2 ky2",
                "```",
                "",
            ]
        )

    if any("Fermi-arc plane" in warning for warning in warnings):
        lines.extend(
            [
                "Fermi-arc plane scaffold:",
                "",
                "```text",
                "KPLANE_SLAB = kx0 ky0   vx1 vy1   vx2 vy2",
                "```",
                "",
            ]
        )

    if any("Wilson-loop plane" in warning for warning in warnings):
        lines.extend(
            [
                "Wilson-loop plane scaffold:",
                "",
                "```text",
                "KPLANE_BULK = kx0 ky0 kz0   vx1 vy1 vz1   vx2 vy2 vz2",
                "```",
                "",
            ]
        )

    if len(lines) == 3:
        lines.extend(["No conservative input snippet was required for this path.", ""])

    return "\n".join(lines).rstrip() + "\n"


def default_output(source: Path) -> Path:
    if source.is_file():
        return source.parent / f"{source.stem}.INPUT_SUGGESTIONS.md"
    return source / "INPUT_SUGGESTIONS.md"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export conservative WannierTools input suggestion snippets.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--output")
    args = parser.parse_args()

    source = Path(args.path).expanduser().resolve()
    output = Path(args.output).expanduser().resolve() if args.output else default_output(source)
    output.write_text(render_markdown(source))
    print(output)


if __name__ == "__main__":
    main()
