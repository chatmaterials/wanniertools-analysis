---
name: "wanniertools-analysis"
description: "Use when the task involves WannierTools workflows, including wt.in design, handoff from wannier90_hr.dat or tight-binding models, surface-state, bulk-band, Fermi-arc, and Wilson-loop analyses, and diagnosis of WT.out or model-readiness issues."
---

# WannierTools Analysis

This skill is for WannierTools and similar topological post-processing from an already validated Wannier tight-binding model. Use it when the user needs help preparing `wt.in`, checking model handoff, or reviewing surface or topological analysis outputs.

## When to use

Use this skill when the request mentions or implies:

- `WannierTools`, `wt.in`, `WT.out`, `wannier90_hr.dat`
- bulk bands, surface states, surface Green's functions, Fermi arcs, nodal searches, Wilson loops
- topological invariants or surface-orientation setup from a Wannier model

## Operating stance

Prioritize missing information in this order:

1. whether the Wannier model is already physically validated
2. target analysis mode: bulk, surface, Fermi arc, Wilson loop, or node search
3. surface orientation, k-path, or k-plane definition
4. number of occupied bands and model conventions

Never silently invent:

- a surface orientation without user intent
- a k-path or k-plane that has no physical or literature basis
- whether the supplied `hr.dat` is actually trustworthy
- the number of occupied bands if the model origin is unclear

## Workflow

### 1. Classify the request

- **Setup**: create or edit `wt.in` and the directory layout.
- **Review**: inspect `wt.in`, `WT.out`, and model files and summarize readiness or issues.
- **Recovery**: explain why the analysis failed or why the model handoff is not yet defensible.

### 2. Gather the minimum viable context

Before recommending a `wt.in` edit, establish:

- which validated Wannier model is being used
- what analysis is desired
- the intended surface normal or reciprocal-space path
- how many occupied bands the post-processing should treat as filled

### 3. Use the bundled helpers

- `scripts/make_wanniertools_input.py`
  Create a conservative `wt.in.template` for bulk, surface, Fermi-arc, or Wilson-loop workflows.
- `scripts/check_wanniertools_case.py`
  Check for missing `wt.in` and `wannier90_hr.dat`-style dependencies.
- `scripts/summarize_wanniertools_run.py`
  Summarize a working directory or `WT.out` using auditable heuristics.
- `scripts/recommend_wanniertools_recovery.py`
  Turn incomplete or blocked WannierTools runs into concrete recovery guidance.
- `scripts/export_status_report.py`
  Export a shareable markdown status report from a WannierTools working directory.
- `scripts/export_input_suggestions.py`
  Export conservative WannierTools input suggestion snippets based on detected recovery patterns.

### 4. Load focused references only when needed

- workflow and file expectations: `references/wanniertools.md`
- model handoff and surface choices: `references/model-handoff.md`
- common failures: `references/failure-modes.md`

### 5. Deliver an auditable answer

Whenever you recommend a `wt.in` change, include:

- the target analysis mode
- the assumed model source and number of occupied bands
- unresolved geometry or topology choices the user must confirm
- what output files should appear if the next stage succeeds

## Guardrails

- Do not treat WannierTools as a substitute for a bad Wannier model.
- Surface-state and Fermi-arc analysis require a defensible surface orientation, not a random choice.
- If the user cannot justify the occupied-band count, say that the analysis setup is underdetermined.

## Quality bar

- Prefer explicit geometry and model assumptions over generic topological buzzwords.
- Distinguish model-readiness issues from post-processing issues.
- If the input still contains placeholders, say so directly.
