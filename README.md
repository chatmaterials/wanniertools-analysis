# wanniertools-analysis

[![CI](https://img.shields.io/github/actions/workflow/status/chatmaterials/wanniertools-analysis/ci.yml?branch=main&label=CI)](https://github.com/chatmaterials/wanniertools-analysis/actions/workflows/ci.yml) [![Release](https://img.shields.io/github/v/release/chatmaterials/wanniertools-analysis?display_name=tag)](https://github.com/chatmaterials/wanniertools-analysis/releases)

Standalone skill for WannierTools post-processing, model handoff checks, and topological analysis setup.

## What This Skill Covers

- `wt.in` template generation for bulk-band, surface-state, Fermi-arc, and Wilson-loop tasks
- checks for missing `wannier90_hr.dat` references and unedited placeholders
- quick summaries from `WT.out` and generated post-processing outputs
- recovery recommendations for missing models or placeholder analysis setups

## What It Does Not Do

- it does not pretend a bad Wannier model becomes trustworthy after post-processing
- it does not invent surface orientations or occupied-band counts without explicit context
- it does not guess physically meaningful k-planes for the user

## Install

```bash
npx skills add chatmaterials/wanniertools-analysis -g -y
```

## Local Validation

```bash
python3 -m py_compile scripts/*.py
npx skills add . --list
python3 scripts/make_wanniertools_input.py /tmp/wt-test --task bulk-band --num-occupied 16
python3 scripts/check_wanniertools_case.py /tmp/wt-test
python3 scripts/recommend_wanniertools_recovery.py fixtures/missing-hr
python3 scripts/export_recovery_plan.py fixtures/missing-hr
python3 scripts/export_status_report.py fixtures/missing-hr
python3 scripts/export_input_suggestions.py fixtures/missing-hr
python3 scripts/run_regression.py
```

## First Release Checklist

1. Initialize a fresh repository from this directory.
2. Run the local validation commands from this directory.
3. Commit the repo root as the first release candidate.
4. Tag the first release, for example `v0.1.0`.

## Suggested First Commit

```bash
git init
git add .
git commit -m "Initial release of wanniertools-analysis"
git tag v0.1.0
```
