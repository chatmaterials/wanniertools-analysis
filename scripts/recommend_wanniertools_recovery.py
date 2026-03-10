#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from check_wanniertools_case import inspect
from summarize_wanniertools_run import summarize


def build_recommendation(path: Path) -> dict[str, object]:
    check = inspect(path)
    summary = summarize(path)
    warnings = list(check.get("warnings") or []) + list(summary.get("warnings") or [])
    missing_files = list(check.get("missing_files") or [])
    issues: list[str] = []
    actions: list[str] = []
    severity = "info"
    safe_restart = False
    restart_strategy = "No recovery action is needed yet."

    if missing_files:
        severity = "error"
        issues.append("The WannierTools directory is missing its main input.")
        actions.append("Create or restore wt.in before attempting a run or restart.")

    if any("HR file" in warning for warning in warnings):
        severity = "error"
        issues.append("The tight-binding model file is missing.")
        actions.append("Restore wannier90_hr.dat or regenerate the model from the Wannier90 workflow before running WannierTools.")
        restart_strategy = "Do not restart until the HR file is available."

    placeholder_warnings = [warning for warning in warnings if "placeholder" in warning.lower() or "template" in warning.lower()]
    if placeholder_warnings:
        severity = "error" if severity == "info" else severity
        issues.append("The WannierTools setup still contains placeholder geometry or k-space definitions.")
        actions.append("Replace the placeholder surface, path, or plane definitions with physically justified values.")
        restart_strategy = "Finalize wt.in first; restarting a placeholder setup is not useful."

    if summary.get("output_file") and not summary.get("completed"):
        severity = "warning" if severity == "info" else severity
        issues.append("WannierTools produced output but did not finish normally.")
        actions.append("Inspect WT.out before rerunning and verify that the model and occupied-band count are still valid.")
        restart_strategy = "If the model input is unchanged and the output stopped cleanly, rerun after correcting the specific WT.out issue."
        safe_restart = True

    if summary.get("output_file") is None and not issues:
        severity = "warning"
        issues.append("No WT.out-style output is present yet.")
        actions.append("Run WannierTools first or confirm whether output was written elsewhere.")
        restart_strategy = "No restart is possible yet because there is no output state to reuse."

    if not issues:
        issues.append("No critical recovery issues were detected.")
        actions.append("Proceed with the current WannierTools analysis output.")

    return {
        "path": str(path),
        "severity": severity,
        "issues": issues,
        "recommended_actions": actions,
        "restart_strategy": restart_strategy,
        "safe_to_reuse_existing_state": safe_restart,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Recommend WannierTools recovery or restart actions from a working directory.")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    record = build_recommendation(Path(args.path).expanduser().resolve())
    if args.json:
        print(json.dumps(record, indent=2))
        return
    print(f"[{Path(record['path']).name}] {record['severity']}")
    print("Issues: " + "; ".join(record["issues"]))
    for action in record["recommended_actions"]:
        print("- " + action)
    print("Restart strategy: " + record["restart_strategy"])


if __name__ == "__main__":
    main()
