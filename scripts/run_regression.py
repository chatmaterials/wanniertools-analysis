#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True, check=True)


def run_json(*args: str):
    return json.loads(run(*args).stdout)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    fixture = ROOT / "fixtures" / "completed"
    checked = run_json("scripts/check_wanniertools_case.py", str(fixture), "--json")
    ensure(checked["missing_files"] == [], "fixture should not miss required files")
    ensure(checked["warnings"] == [], "fixture should not emit warnings")

    summary = run_json("scripts/summarize_wanniertools_run.py", str(fixture), "--json")
    ensure(summary["completed"] is True, "fixture should be marked completed")
    ensure("bulkbands.dat" in summary["notable_outputs"], "fixture should report bulkbands.dat")

    failure = ROOT / "fixtures" / "missing-hr"
    checked_failure = run_json("scripts/check_wanniertools_case.py", str(failure), "--json")
    ensure(any("HR file" in warning for warning in checked_failure["warnings"]), "failure fixture should report missing HR model")
    summary_failure = run_json("scripts/summarize_wanniertools_run.py", str(failure), "--json")
    ensure(summary_failure["completed"] is False, "missing-HR fixture should not be marked completed")
    ensure(any("No WT.out-style" in warning for warning in summary_failure["warnings"]), "missing-HR fixture should report absent output")
    recovery = run_json("scripts/recommend_wanniertools_recovery.py", str(failure), "--json")
    ensure(recovery["severity"] == "error", "missing HR model should be an error-level recovery case")
    ensure(any("HR" in action or "model" in action.lower() for action in recovery["recommended_actions"]), "recovery advice should mention restoring the model")
    ensure(recovery["safe_to_reuse_existing_state"] is False, "missing HR model should not allow state reuse")

    temp_dir = Path(tempfile.mkdtemp(prefix="wanniertools-regression-"))
    arc_dir = Path(tempfile.mkdtemp(prefix="wanniertools-arc-regression-"))
    try:
        run("scripts/make_wanniertools_input.py", str(temp_dir), "--task", "bulk-band", "--num-occupied", "16")
        generated = run_json("scripts/check_wanniertools_case.py", str(temp_dir), "--json")
        ensure(any("placeholder" in warning.lower() for warning in generated["warnings"]), "generated template should emit placeholder warnings")
        ensure(any("template" in warning.lower() for warning in generated["warnings"]), "generated input should be marked as template")
        workflow_plan = (temp_dir / "WORKFLOW_PLAN.md").read_text()
        ensure("# Workflow Plan" in workflow_plan, "generated workflow should include WORKFLOW_PLAN.md")
        ensure("WannierTools Setup" in workflow_plan, "workflow plan should describe the setup stage")
        plan_path = Path(run("scripts/export_recovery_plan.py", str(failure), "--output", str(temp_dir / "RESTART_PLAN.md")).stdout.strip())
        plan_text = plan_path.read_text()
        ensure("# Recovery Plan" in plan_text, "exported plan should have a recovery-plan heading")
        ensure("model" in plan_text.lower() or "hr" in plan_text.lower(), "exported plan should mention the missing model")
        status_path = Path(run("scripts/export_status_report.py", str(failure), "--output", str(temp_dir / "STATUS_REPORT.md")).stdout.strip())
        status_text = status_path.read_text()
        ensure("# Status Report" in status_text, "exported status should have a status-report heading")
        ensure("Referenced HR file not found" in status_text, "status report should include the missing-model warning")
        suggest_path = Path(run("scripts/export_input_suggestions.py", str(failure), "--output", str(temp_dir / "INPUT_SUGGESTIONS.md")).stdout.strip())
        suggest_text = suggest_path.read_text()
        ensure("# Input Suggestions" in suggest_text, "exported suggestions should have an input-suggestions heading")
        ensure("wannier90_hr.dat" in suggest_text or "KPATH_BULK" in suggest_text, "WannierTools suggestions should include a model or path scaffold")
        run("scripts/make_wanniertools_input.py", str(arc_dir), "--task", "fermi-arc", "--num-occupied", "16")
        arc = run_json("scripts/check_wanniertools_case.py", str(arc_dir), "--json")
        ensure(any("fermi-arc plane" in warning.lower() for warning in arc["warnings"]), "fermi-arc mode should emit the plane placeholder warning")
    finally:
        shutil.rmtree(temp_dir)
        shutil.rmtree(arc_dir)

    print("wanniertools-analysis regression passed")


if __name__ == "__main__":
    main()
