# Filling sensitivity of the sampled `W/W_N` families

## Result at a glance

**Filling matters in these calculations.** At matched sampled `(U,V_SO)` points, changing `n` changes the computed ratios, and the change is not a uniform vertical rescaling: its size and even its sign depend on temperature and parameter point. Changing `n` also changes which roots and finite-temperature points pass the strict band-admissibility rule.

This is a coarse sensitivity study, not a replacement for the dense production family plots or a thermodynamic stability comparison.

## What was run

The scan independently re-solved the stage-one superconducting state at each filling and parameter point using both policies, then recalculated the scattering numerator and normal reference with the **same filling**. Parameters held fixed were `Delta_t=4.5t`, `hbar*omega=0.7t`, the production signed Case-I coherence factor, and the existing master gap-versus-temperature form.

- Fillings: `n = 1.4, 1.5, 1.7, 1.885` (`1.885` is the existing ultrasonic default; this is not the HHM benchmark `n=1.875`).
- `W/W_N` sampled at `T/Tc = 0.3, 0.5, 0.7, 0.9, 0.999`.
- `U` families: `U/t = 15, 25, ..., 145, 150`, at `V_SO/t = 0, 0.4, 0.8`.
- `V_SO` families: `V_SO/t = 0, 0.1, ..., 0.9`, at `U/t = 30, 75, 115`.
- The two grids overlap at six coordinates, giving **69 unique `(U,V_SO)` points per filling**, 276 unique states overall, and both-policy runs at each state.
- Resolutions: stage-one `Nk=80`, number-equation `Nk=200`, DOS `Nk=1200`, energy quadrature `NELL=20000`.

The selected grids are deliberately coarser than the full original family plots. Plot markers show the actual samples; no interpolation or smoothing was applied. Empty/gapped samples are not zeros.

## Strict versus relaxed interpretation

- **Strict is primary:** only in-band stage-one roots and finite-temperature SC chemical potentials inside the analytic bare-band interval are retained. Rejected samples appear as gaps.
- **Relaxed is diagnostic:** residual-verified out-of-band roots and their finite-temperature ratios are retained and explicitly flagged in the CSV. They are not strict-policy acceptance and are not asserted to be physical or thermodynamically stable.
- Neither policy compares the free energies of competing roots. The calculations remain conditional on the model's assumed constant acoustic vertex.

## Observed admissibility counts

Counts below are out of 69 sampled `(U,V_SO)` coordinates per filling. “Finite-T out-of-band” counts the relaxed candidate's five temperatures at each superconducting coordinate; strict values at rejected samples are omitted.

| `n` | Strict SC roots / accepted coordinate-temperature samples | Relaxed SC roots | Relaxed out-of-band `T=0` roots | Relaxed out-of-band finite-`T` samples |
|---:|---:|---:|---:|---:|
| 1.4 | 47 / 235 | 47 | 0 | 0 |
| 1.5 | 52 / 260 | 52 | 0 | 1 |
| 1.7 | 63 / 315 | 64 | 1 | 35 |
| 1.885 | 42 / 210 | 69 | 27 | 136 |

This illustrates why the relaxed panels can have more coverage—especially at `n=1.885`—but that additional coverage is a change in candidate/admissibility domain, not a strict-policy enhancement of absorption.

## Size and character of the filling effect

For each filling below, the table gives the **median absolute difference** in `W/W_N` relative to `n=1.885`, among points where both fillings have a retained value at the same `(U,V_SO,T/Tc)`. It is descriptive of this coarse grid, not an uncertainty estimate. The matched-point counts are in `filling_sensitivity_vs_1p885.csv`.

| Policy | `n` | `T/Tc=0.3` | 0.5 | 0.7 | 0.9 | 0.999 |
|:--|--:|--:|--:|--:|--:|--:|
| Strict | 1.4 | 0.076 | 0.179 | 0.187 | 0.163 | 0.129 |
| Strict | 1.5 | 0.054 | 0.165 | 0.198 | 0.164 | 0.049 |
| Strict | 1.7 | 0.008 | 0.043 | 0.073 | 0.079 | 0.084 |
| Relaxed | 1.4 | 0.146 | 0.206 | 0.124 | 0.077 | 0.096 |
| Relaxed | 1.5 | 0.110 | 0.197 | 0.140 | 0.121 | 0.090 |
| Relaxed | 1.7 | 0.026 | 0.110 | 0.140 | 0.074 | 0.053 |

There is no universal monotonic trend with filling across all parameter points. For example, at `n=1.7` under the strict policy, the median signed difference from `n=1.885` is positive at all five displayed temperatures, but individual paired points include negative shifts; near `T/Tc=0.999` the median signed difference is only about `+0.007` while the median absolute difference is about `0.084`. For `n=1.4` and `1.5`, the paired strict median signed shift changes sign near `T/Tc=0.999`. Therefore, do not summarize the effect as a simple monotonic increase or decrease in absorption.

A small number of retained samples slightly exceed unity: the strict scan's maximum is `1.0159` at `(n,U/t,V_SO/t,T/Tc)=(1.5,15,0.8,0.9)`. The relaxed scan also has `1.0413` at the same filling/parameters and `1.0119` at the out-of-band diagnostic point `(1.7,15,0.8,0.9)`. These are recorded rather than clipped. The strict in-band exceedance was checked against stage-one `Nk=80,160,320`, energy quadrature `NELL=10,000`–`80,000`, and DOS-grid `Nk=1200,2400`; it remained `1.01589` to the shown precision. It is therefore not a quadrature-resolution artifact in those checks. Its physical interpretation still needs a separate audit before extending any blanket `W/W_N < 1` statement to other fillings; the existing `n=1.885` dataset is unchanged.

## Files

- `strict_U_filling_comparison.png`, `strict_VSO_filling_comparison.png`: primary in-band comparisons; gaps are omitted strict samples.
- `relaxed_U_filling_comparison.png`, `relaxed_VSO_filling_comparison.png`: diagnostic companions; out-of-band candidates remain included.
- `filling_sensitivity_data.json`: complete data and provenance, organized separately by policy.
- `filling_sensitivity_samples.csv`: long-form rows, one per `(n, policy, family, U, V_SO, T/Tc)`.
- `filling_sensitivity_vs_1p885.csv`: paired filling differences and coverage counts.
- `run_filling_sensitivity.py`: reproducible scan and figure generator.

To rerun from the repository root, install `requirements.txt`, then run:

```bash
.venv/bin/python project/ultrasonic/analysis/filling_sensitivity_wwn/run_filling_sensitivity.py
```

Existing production data, figures, archived PDFs, and manuscript sources were not changed by this scan.
