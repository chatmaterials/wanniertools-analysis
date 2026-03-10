# WannierTools Failure Modes

Load this file when a WannierTools run fails or produces suspicious output.

## Common patterns

### Missing `wannier90_hr.dat`

- this is a model-handoff problem, not a post-processing problem

### Placeholder `wt.in`

- if the input still contains placeholder surface or k-space definitions, the run is not ready

### Ambiguous occupied-band count

- topological outputs are not trustworthy until the occupied subspace is correctly defined
