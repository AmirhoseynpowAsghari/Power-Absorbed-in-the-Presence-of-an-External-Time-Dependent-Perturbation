# Editable Physical Review-style manuscript draft

## Files

- `draft_prb.tex` — APS REVTeX 4.2 manuscript source using the `prb,reprint` two-column journal layout; this is the authoritative editable version.
- `draft_references.bib` — bibliography entries used in the source.
- `draft_prb.pdf` — generated reading proof; the REVTeX source remains authoritative and editable.

The archived corrected paper at `../../../archive/pre_f02_baseline/paper_correction_results/arXiv_2607.02812_corrected.pdf` is retained as a read-only reference; this draft is a separate manuscript and does not overwrite it.

The author names and affiliation follow the original manuscript in `../vendor/arXiv_2607.02812_original.pdf`; please confirm the author list, corresponding-author details, acknowledgments, and funding before submission.

## Scientific scope of this draft

This is a corrected **model-paper draft**, not a claim that the project has completed a microscopic finite-wave-vector ultrasonic calculation. It deliberately calls the computed observable a constant-vertex quasiparticle-scattering ratio and states that the acoustic vertex is unspecified by the HHM electronic Hamiltonian. Its SOC trends are conditional on the assumed vertex and supplied gap inputs.

The manuscript corrects or qualifies these original claims/formulas:

- Uses the signed Case-I factor derived from the stated Bogoliubov matrix element, with energy conservation imposed on quasiparticle energies.
- Keeps the two energy-inversion roots and the Jacobian in the branch-resolved quasiparticle DOS; derives the final $\ell$-quadrature explicitly, retaining the final-state $E'/\ell'$ DOS factor and exact branch-pair band support.
- Distinguishes the helicity label from the energy-branch label.
- Uses the signed $\xi_\sigma\xi_{\sigma'}$ Case-I factor; absolute-value and earlier-paper variants appear only in the comparison diagnostic.
- Identifies the actual pair-channel threshold in this model as `hbar*omega = 2 E_min`, not `2 Delta_eff` in general.
- Does not call `W/W_N` a superfluid weight or a material-specific attenuation coefficient.
- Does not equate strain-modulated hopping with a scalar density vertex without a microscopic derivation.
- Does not claim the constant-vertex, unrestricted momentum sum is a clean finite-q acoustic response.
- Identifies the stage-one nonlinear gap-threshold `Tc` proxy separately from the HHM linearized-determinant criterion, and treats the rigid fitted gap shape as a modeling choice.

The full earlier finite-q audit is in `../ultrasonic/FINITE_Q_ACOUSTIC_COUPLING_ASSESSMENT.md`.

## Figures included by reference

No figure data or image files were copied, overwritten, or regenerated for the manuscript. The `.tex` points directly to these existing repository assets:

1. `ultrasonic/figures/strict_policy/WWN_vs_TTc_and_Delta_VSOfamilies.png` — strict-window temperature/gap families.
2. `ultrasonic/figures/strict_policy/WWN_vs_U_families_VSO.png` — strict-window $U$ families across SOC.
3. `ultrasonic/figures/strict_policy/WWN_vs_VSO_families_U.png` — strict-window SOC families across $U$.
4. `ultrasonic/figures/W_WN_groups_Dt_scan.png` — corrected first-paper Group C, retained as a relaxed-window comparison; the $\Delta_t=4.5t$ root is out of band and diagnostic.
5. `ultrasonic/figures/W_WN_groups_VSO_scan.png` — corrected first-paper Group D, retained as a relaxed-window comparison distinct from the strict scan.
6. `ultrasonic/analysis/wwn_temperature_maxima/temperature_envelope_max_vs_U.png` — pointwise envelope over the five sampled temperatures, with strict and relaxed policies separately styled.
7. `ultrasonic/analysis/wwn_temperature_maxima/temperature_peak_analysis_two_panel.png` — strict-only exact sampled maxima and their temperature dependence.
8. `ultrasonic/figures/W_WN_coherence_variants.png` — signed, absolute-value, earlier-paper, and textbook coherence prescriptions; only the signed form is used in the primary results.
9. `ultrasonic/figures/branch_decomposition.png` — energy-root branches and the model-specific spectral threshold.
10. `ultrasonic/figures/dual_space_k_vs_energy.png` — numerical cross-check within the unrestricted model.
11. `ultrasonic/figures/soc_explicit_vertex.png` — helicity-vertex sensitivity diagnostic, explicitly not a finite-$q$ calculation.
12. `ultrasonic/figures/branch_structure_sigma_vs_s.png` — explains the distinct energy-root (`sigma`) and Rashba-helicity (`s`) indices.
13. `ultrasonic/figures/coherence_factors_per_branch.png` — branch-pair Case-I coherence diagnostic illustrating why signed root variables enter the transition weight.
14. `ultrasonic/figures/strict_policy/soc_scans_by_U.png` — existing strict-policy SOC scans at fixed `U`; absent/rejected samples remain gaps.
15. `ultrasonic/figures/strict_policy/extrema_by_U.png` — strict-policy sampled maxima/minima versus `U` for the shown SOC and temperature panels.
16. `ultrasonic/figures/strict_policy/extrema_tracks_by_soc.png` — sampled extrema over the stored `U` grid versus SOC; open markers identify `U`-boundary extrema.

Strict-policy results remain primary; missing or rejected strict samples are gaps, not zeros. The corrected Group C/D composites are shown separately and explicitly identified as relaxed-window legacy comparisons, not replacements for the strict family figures. The maxima plots use only existing sampled data; no interpolation, smoothing, jitter, or response recalculation was applied.

## Build

The editable source now requests the APS Physical Review B `reprint` layout (two columns), rather than `preprint`. Compile it from this directory with REVTeX 4.2 and a working LaTeX/BibTeX installation:

```sh
latexmk -pdf -interaction=nonstopmode draft_prb.tex
```

The checked-in `draft_prb.pdf` is still the earlier 16-page Pandoc-to-Typst reading proof. It is not a native REVTeX rendering and it predates the five additional figure insertions and the `reprint` layout update. A native PDF could not be produced in this sandbox because no TeX/REVTeX engine is installed. This explains why the earlier PDF did not look like a typeset Physical Review paper: the source was APS-formatted, but its rendered proof was a Typst conversion, not an APS class build. The `.tex` and `.bib` are authoritative; compile them with REVTeX to obtain the genuine journal-style layout before submission. Figure paths are relative and assume compilation from this directory.

## Open items for author review

1. Confirm the author list, correspondence, acknowledgments, and funding.
2. Decide whether the paper should remain a clearly labeled phenomenological model study or wait for a specified electron--phonon vertex and finite-q calculation.
3. Verify references and any claims against the cited source papers before submission; the current draft cites only the HHM and Levy works represented in the repository.
4. Review all referenced strict-policy, extrema, branch/coherence, corrected legacy Group C/D, and validation figures in context. All are existing repository outputs; the manuscript only references them and does not regenerate or modify them. Boundary extrema and rejected samples are described explicitly; no extrema are interpolated, and none is a free-energy stability test.
