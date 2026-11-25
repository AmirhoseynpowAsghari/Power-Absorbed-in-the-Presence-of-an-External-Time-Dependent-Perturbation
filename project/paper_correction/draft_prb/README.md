# Editable Physical Review-style manuscript draft

## Files

- `draft_prb.tex` — APS REVTeX 4.2 manuscript source using the `prb,reprint` two-column journal layout; this is the authoritative editable version.
- `draft_references.bib` — bibliography entries used in the source.
- `overleaf_prb_source_policy_comparison.zip` — self-contained Overleaf package for the current source and strict/relaxed figure comparisons.
- `draft_prb_native.pdf` — prior APS/REVTeX two-column author-version proof; it predates the latest strict/relaxed figure edits and must be rebuilt before it can be treated as a proof of the current source. The older `draft_prb.pdf` is intentionally preserved unchanged.
- `draft_prb.pdf` — earlier Pandoc-to-Typst reading proof, retained unchanged for provenance; it does not represent the current REVTeX source.

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

No repository figure data or image files were overwritten or regenerated for this manuscript revision. The `.tex` points directly to existing repository assets; the updated Overleaf ZIP packages copies of the referenced images so it is self-contained. The strict-only family and extrema figures now have adjacent relaxed-policy companion figures; relaxed plots are explicitly diagnostic and are never substituted for missing strict values.

- `ultrasonic/figures/strict_policy/WWN_vs_U_families_VSO.png` and `ultrasonic/figures/WWN_vs_U_families_VSO.png` — strict/relaxed $U$ families across SOC.
- `ultrasonic/figures/strict_policy/WWN_vs_VSO_families_U.png` and `ultrasonic/figures/WWN_vs_VSO_families_U.png` — strict/relaxed SOC families across $U$.
- `ultrasonic/figures/strict_policy/soc_scans_by_U.png` and `ultrasonic/figures/soc_scans_by_U.png` — strict/relaxed fixed-$U$ SOC scans.
- `ultrasonic/figures/strict_policy/extrema_by_U.png` and `ultrasonic/figures/extrema_by_U.png` — strict/relaxed sampled extrema versus $U$.
- `ultrasonic/figures/strict_policy/extrema_tracks_by_soc.png` and `ultrasonic/figures/extrema_tracks_by_soc.png` — strict/relaxed extrema tracks versus SOC.
- `ultrasonic/analysis/wwn_temperature_maxima/temperature_peak_analysis_two_panel.png` and `temperature_peak_analysis_two_panel_relaxed.png` — strict/relaxed sampled peak locations and magnitudes.
- `ultrasonic/analysis/wwn_temperature_maxima/temperature_envelope_max_vs_U.png` — pointwise envelope over sampled temperatures, with strict and relaxed policies already styled separately.
- `ultrasonic/figures/W_WN_groups_Dt_scan.png` and `W_WN_groups_VSO_scan.png` — corrected legacy Group C/D relaxed-window composites, kept distinct from the regenerated strict-policy figures.
- `ultrasonic/figures/W_WN_coherence_variants.png`, `coherence_factors_per_branch.png`, and `branch_structure_sigma_vs_s.png` — coherence, energy-root, and helicity-label diagnostics.
- `ultrasonic/figures/dual_space_k_vs_energy.png` — numerical cross-check within the unrestricted model.

The strict temperature/gap family image, branch-decomposition/threshold image, and SOC vertex-sensitivity image were removed from the manuscript at the author's request. Strict-policy results remain primary; rejected or missing strict samples are gaps, not zeros. The policy-specific peak comparison uses existing sampled data only: no interpolation, smoothing, jitter, or response recalculation was applied. The strict maxima are inside their admissible $U$ intervals, while all 25 relaxed peak records have out-of-band zero-temperature roots and lie at or near the low-$U$ end of the sampled range. This explains their different visual prominence without implying that the strict policy itself increases absorption or that either set establishes free-energy stability.

## Build

The editable source requests the APS Physical Review B `reprint` layout: two-column text, APS section and equation numbering, front matter, and full-width figure floats. Compile it from this directory with REVTeX 4.2 and a working LaTeX/BibTeX installation:

```sh
latexmk -pdf -interaction=nonstopmode draft_prb.tex
```

`draft_prb_native.pdf` is the prior 16-page XeTeX/REVTeX 4.2 author-version proof; it has not been rebuilt after the latest figure changes, so it does not represent the current `.tex`. The source follows the Physical Review article typography and two-column composition illustrated by the attached Li (2008) paper; the `.tex` and `.bib` remain the editable source of record. The published-paper masthead, volume/page assignment, DOI, and received/published dates in the example are publisher metadata and have not been fabricated for this unpublished draft. The older `draft_prb.pdf` remains untouched: it is the earlier Pandoc-to-Typst proof and does not match the current source. Figure paths are relative and assume compilation from this directory.

## Open items for author review

1. Confirm the author list, correspondence, acknowledgments, and funding.
2. Decide whether the paper should remain a clearly labeled phenomenological model study or wait for a specified electron--phonon vertex and finite-q calculation.
3. Verify references and any claims against the cited source papers before submission; the current draft cites only the HHM and Levy works represented in the repository.
4. Review all referenced strict-policy, extrema, branch/coherence, corrected legacy Group C/D, and validation figures in context. All are existing repository outputs; the manuscript only references them and does not regenerate or modify them. Boundary extrema and rejected samples are described explicitly; no extrema are interpolated, and none is a free-energy stability test.
