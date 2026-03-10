# WannierTools Reference

Load this file for WannierTools-specific workflow expectations.

## Minimum working set

- required input: `wt.in`
- validated model file: usually `wannier90_hr.dat`
- runtime output: `WT.out` plus analysis-specific files such as bulk bands, surface spectra, or arc data

## Analysis modes

### Bulk band workflow

- requires a defensible k-path
- useful for checking the tight-binding interpolation against expectations before surface analysis

### Surface workflow

- requires an explicit surface orientation
- depends strongly on the model quality and occupied-band count

### Fermi-arc workflow

- requires a well-defined surface problem and energy reference
- do not claim arc features are meaningful if the underlying bulk model is not trusted

### Wilson-loop workflow

- requires a clear occupied subspace definition
- can be invalidated by an inconsistent model or incorrect occupied-band count
