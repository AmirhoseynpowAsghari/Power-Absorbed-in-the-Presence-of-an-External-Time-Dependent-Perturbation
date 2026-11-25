#!/usr/bin/env python3
"""Coarse, matched filling-sensitivity scan for W/W_N under strict and relaxed policies.

This is additive: outputs live under analysis/filling_sensitivity_wwn and existing
production results/figures are not touched.  It re-solves the superconducting state for each
(n, U, V_SO) and recomputes W and W_N at the same filling. The deliberately coarse shared
parameter grid is for sensitivity diagnosis, not exact reproduction of the dense family plots.
"""
from __future__ import annotations
import csv, datetime as dt, json, os, sys, time
from multiprocessing import Pool
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ULTRA = os.path.abspath(os.path.join(HERE, "../.."))
SCP = os.path.abspath(os.path.join(ULTRA, "../sc_params"))
sys.path[:0] = [ULTRA, SCP]
os.chdir(ULTRA)

import solvers
from absorption import S_normal, S_scattering
from dos_ua import NormalDOS
from parameters_ua import OMEGA, NBINS, SMOOTH
from physics_ua import SCState

OUT = HERE
FILLINGS = (1.4, 1.5, 1.7, 1.885)
DELTA_T = 4.5
FRACS = (0.3, 0.5, 0.7, 0.9, 0.999)
# Matched but intentionally coarser than the full publication-family grids.
U_SWEEP = tuple(float(x) for x in (*range(15, 146, 10), 150))
U_SWEEP_VSO = (0.0, 0.4, 0.8)
VSO_SWEEP = tuple(round(float(x), 2) for x in np.arange(0.0, 0.9001, 0.1))
VSO_SWEEP_U = (30.0, 75.0, 115.0)
NK_STAGE1, NK_MU, NK_DOS, NELL = 80, 200, 1200, 20000
BAND_TOL = solvers.BAND_EDGE_TOL
_DOS = {}
_DOS_ORDER = []


def get_dos(vso):
    key = round(float(vso), 6)
    if key not in _DOS:
        if len(_DOS_ORDER) >= 3:
            del _DOS[_DOS_ORDER.pop(0)]
        _DOS[key] = NormalDOS(key, Nk=NK_DOS, nbins=NBINS, smooth=SMOOTH)
        _DOS_ORDER.append(key)
    return _DOS[key]


def inside_band(mu, vso):
    lo, hi = solvers.bare_band_window(np.empty(0), float(vso))
    return bool(lo - BAND_TOL <= float(mu) <= hi + BAND_TOL)


def calc_curve(state1, nfill, vso, policy, reuse=None):
    """Calculate/retain ratios and always record finite-T band admissibility."""
    if float(state1.get("Tc") or 0.0) <= 0.0:
        return [None] * len(FRACS), [], []
    sc = SCState(params=dict(VSO=float(vso), Tc=float(state1["Tc"]),
                             D0_0=float(state1["D0_0"]), DS_0=float(state1["DS_0"]),
                             Deff_0=float(state1["Deff_0"])),
                 Nk_mu=NK_MU, n_tgt=float(nfill))
    ratios, mus, accepted = [], [], []
    dos = None
    for i, frac in enumerate(FRACS):
        st = sc.at(float(frac))
        ok = inside_band(st["mu"], vso)
        mus.append(float(st["mu"]))
        accepted.append(ok)
        if policy == "strict" and not ok:
            ratios.append(None)
            continue
        if reuse is not None and i < len(reuse) and reuse[i] is not None:
            ratios.append(float(reuse[i]))
            continue
        if dos is None:
            dos = get_dos(vso)
        sn = S_normal(dos, st["T"], OMEGA, st["mu_N"])
        ss, _ = S_scattering(dos, st["T"], OMEGA, st["D0"], st["DS"],
                             st["mu"], "a_signed", nell=NELL)
        ratio = float(ss / sn) if np.isfinite(sn) and sn != 0 and np.isfinite(ss) else None
        ratios.append(ratio)
    return ratios, mus, accepted


def roots_match(a, b):
    if not a or not b or float(a.get("Tc") or 0) <= 0 or float(b.get("Tc") or 0) <= 0:
        return False
    for k in ("Tc", "D0_0", "DS_0", "Deff_0", "mu_0"):
        x, y = a.get(k), b.get(k)
        if x is None or y is None or abs(float(x)-float(y)) > 2e-7*max(1.,abs(float(x)),abs(float(y))):
            return False
    return True


def evaluate(task):
    nfill, U, vso = task
    rows = {}
    stage = {}
    for policy in ("relaxed", "strict"):
        solvers.MU_WINDOW_POLICY = policy
        try:
            s = solvers.solve_set_core(float(U), DELTA_T, float(nfill), float(vso), Nk=NK_STAGE1)
            stage[policy] = s
        except Exception as exc:
            stage[policy] = dict(U=float(U), V_SO=float(vso), n=float(nfill), Tc=0.0,
                                 error=f"{type(exc).__name__}: {exc}", policy=policy)
    rrel = stage["relaxed"]
    relaxed_ratio, relaxed_mu, relaxed_inside = calc_curve(rrel, nfill, vso, "relaxed")
    rstrict = stage["strict"]
    reuse = relaxed_ratio if roots_match(rstrict, rrel) else None
    strict_ratio, strict_mu, strict_inside = calc_curve(rstrict, nfill, vso, "strict", reuse=reuse)
    for policy, s, ratios, mus, accepted, reused in (
        ("relaxed", rrel, relaxed_ratio, relaxed_mu, relaxed_inside, False),
        ("strict", rstrict, strict_ratio, strict_mu, strict_inside, reuse is not None)):
        rows[policy] = dict(n=float(nfill), U=float(U), VSO=float(vso), policy=policy,
            Tc=float(s.get("Tc") or 0.0), Tc_bracketed=s.get("Tc_bracketed"),
            D0_0=s.get("D0_0"), DS_0=s.get("DS_0"), Deff_0=s.get("Deff_0"), mu_0=s.get("mu_0"),
            mu0_inside=(s.get("mu_window") or {}).get("inside"),
            stage1_no_inband_root=s.get("no_inband_root"), stage1_error=s.get("error"),
            stage2_mu=mus, stage2_inside=accepted, ratio=ratios,
            reused_matching_relaxed_curve=bool(reused))
    return rows["relaxed"], rows["strict"]


def all_tasks():
    points = set()
    for v in U_SWEEP_VSO:
        for u in U_SWEEP:
            points.add((u, v, "U"))
    for u in VSO_SWEEP_U:
        for v in VSO_SWEEP:
            points.add((u, v, "VSO"))
    return [(n, u, v, family) for n in FILLINGS for u, v, family in sorted(points, key=lambda z:(z[2],z[0]))]


def worker(task):
    n, u, v, family = task
    rel, strict = evaluate((n, u, v))
    rel["families"] = [family]
    strict["families"] = [family]
    return rel, strict


def make_csv(rows, path):
    fields = ["n", "policy", "family", "U", "VSO", "Tc", "Tc_bracketed", "D0_0", "DS_0",
              "Deff_0", "mu_0", "mu0_inside", "stage1_no_inband_root", "stage1_error",
              "T_over_Tc", "stage2_mu", "stage2_inside", "W_over_WN", "reused_matching_relaxed_curve"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader()
        for r in rows:
            for i, frac in enumerate(FRACS):
                w.writerow(dict(n=r["n"], policy=r["policy"], family=";".join(r["families"]),
                    U=r["U"], VSO=r["VSO"], Tc=r.get("Tc"), Tc_bracketed=r.get("Tc_bracketed"),
                    D0_0=r.get("D0_0"), DS_0=r.get("DS_0"), Deff_0=r.get("Deff_0"), mu_0=r.get("mu_0"),
                    mu0_inside=r.get("mu0_inside"), stage1_no_inband_root=r.get("stage1_no_inband_root"),
                    stage1_error=r.get("stage1_error"), T_over_Tc=frac,
                    stage2_mu=(r.get("stage2_mu") or [None]*len(FRACS))[i],
                    stage2_inside=(r.get("stage2_inside") or [None]*len(FRACS))[i],
                    W_over_WN=(r.get("ratio") or [None]*len(FRACS))[i],
                    reused_matching_relaxed_curve=r.get("reused_matching_relaxed_curve")))


def plot_family(rows, family, policy, path):
    # Three panels, each a selected fixed-coordinate slice; curves are the standard T/Tc values.
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.4), sharey=True)
    cmap = plt.get_cmap("viridis")
    if family == "U":
        panels, xkey, pkey = U_SWEEP_VSO, "U", "VSO"
        subtitle = r"$W/W_N$ versus $U/t$ at fixed $V_{SO}/t$"
    else:
        panels, xkey, pkey = VSO_SWEEP_U, "VSO", "U"
        subtitle = r"$W/W_N$ versus $V_{SO}/t$ at fixed $U/t$"
    for ax, panel in zip(axes, panels):
        for j, frac in enumerate(FRACS):
            col = cmap(0.05 + 0.9*j/(len(FRACS)-1))
            for n in FILLINGS:
                group = [r for r in rows if r["policy"] == policy and r["n"] == n
                         and r["families"] == [family] and abs(r[pkey]-panel)<1e-9]
                group.sort(key=lambda r:r[xkey])
                xx, yy = [], []
                for r in group:
                    vals = r.get("ratio") or []
                    value = vals[j] if len(vals)>j else None
                    if value is not None and np.isfinite(float(value)):
                        xx.append(r[xkey]); yy.append(float(value))
                if xx:
                    ax.plot(xx, yy, marker="o", ms=2.3, lw=1.0, color=col,
                            ls={1.4:"-",1.5:"--",1.7:":",1.885:"-."}[n],
                            label=f"n={n:g}, T/Tc={frac:g}")
        ax.set_title((r"$V_{SO}/t=$" if family=="U" else r"$U/t=$") + f"{panel:g}")
        ax.set_xlabel(r"$U/t$" if family=="U" else r"$V_{SO}/t$")
        ax.grid(alpha=.25)
    axes[0].set_ylabel(r"$W/W_N$")
    # Two-key legend: line style marks filling, color marks temperature.
    fill_handles = [plt.Line2D([],[],color="0.2",ls=ls,label=f"n={n:g}")
                    for n,ls in [(1.4,"-"),(1.5,"--"),(1.7,":"),(1.885,"-.")]]
    temp_handles = [plt.Line2D([],[],color=cmap(0.05+0.9*j/(len(FRACS)-1)),lw=2,label=f"T/Tc={f:g}")
                    for j,f in enumerate(FRACS)]
    fig.legend(handles=fill_handles+temp_handles, loc="lower center", ncol=5,
               bbox_to_anchor=(.5,-.06), fontsize=8)
    admiss = ("strict: only roots and finite-T points inside the analytic bare-band window; gaps are rejected samples"
              if policy=="strict" else
              "relaxed: residual-verified roots retained even outside the band; diagnostic, not strict acceptance")
    fig.suptitle(f"{subtitle}; Δt=4.5t, ħω=0.7t\n{policy.capitalize()} policy — {admiss}", fontsize=10)
    fig.tight_layout(rect=(0,.12,1,.88))
    fig.savefig(path,dpi=160,bbox_inches="tight"); plt.close(fig)


def make_summary(relaxed, strict, path):
    base={(r["n"],r["policy"],r["U"],r["VSO"]):r for r in relaxed+strict}
    fields=["policy","n","T_over_Tc","matched_valid","baseline_valid","valid_at_n","coverage_change",
            "median_signed_delta_vs_n1p885","median_abs_delta_vs_n1p885","max_abs_delta_vs_n1p885"]
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n"); w.writeheader()
        for policy in ("strict","relaxed"):
            for n in FILLINGS:
                for i,frac in enumerate(FRACS):
                    ds=[]; signed=[]; nvalid=basevalid=matched=0
                    for key,r in base.items():
                        nn,pp,u,v=key
                        if pp!=policy or nn!=n: continue
                        rb=base.get((1.885,policy,u,v))
                        y=r["ratio"][i] if r.get("ratio") and len(r["ratio"])>i else None
                        yb=rb["ratio"][i] if rb and rb.get("ratio") and len(rb["ratio"])>i else None
                        nvalid += y is not None
                        basevalid += yb is not None
                        if y is not None and yb is not None:
                            matched+=1; delta=float(y)-float(yb); signed.append(delta); ds.append(abs(delta))
                    w.writerow(dict(policy=policy,n=n,T_over_Tc=frac,matched_valid=matched,
                        baseline_valid=basevalid,valid_at_n=nvalid,coverage_change=nvalid-basevalid,
                        median_signed_delta_vs_n1p885=(float(np.median(signed)) if signed else ""),
                        median_abs_delta_vs_n1p885=(float(np.median(ds)) if ds else ""),
                        max_abs_delta_vs_n1p885=(float(max(ds)) if ds else "")))


def main():
    t0=time.time(); tasks=all_tasks(); print(f"Matched filling scan: {len(tasks)} (n,U,VSO,family) tasks",flush=True)
    # Collapse duplicate U/VSO coordinates across families before computing, restore family labels after.
    coord_families={}
    for n,u,v,fam in tasks: coord_families.setdefault((n,u,v),set()).add(fam)
    unique=[(n,u,v,tuple(sorted(fs))) for (n,u,v),fs in sorted(coord_families.items())]
    print(f"Unique states: {len(unique)}; n={FILLINGS}; standard fractions={FRACS}",flush=True)
    packed=[]
    # Evaluate once per (n,U,VSO), then attach the scan-family membership to each row.
    with Pool(2) as pool:
        for k,(rel,strict) in enumerate(pool.imap(worker, [(n,u,v,"U" if "U" in fs else "VSO")
                                                            for n,u,v,fs in unique], chunksize=1),1):
            # Correctly attach all family memberships, including coordinates shared by both scans.
            fs=coord_families[(rel["n"],rel["U"],rel["VSO"])]
            rel["families"]=sorted(fs); strict["families"]=sorted(fs)
            packed.append((rel,strict))
            if k%10==0 or k==len(unique):
                print(f"  {k}/{len(unique)} states; elapsed {time.time()-t0:.0f}s",flush=True)
    relaxed=[p[0] for p in packed]; strict=[p[1] for p in packed]
    os.makedirs(OUT,exist_ok=True)
    with open(os.path.join(OUT,"filling_sensitivity_data.json"),"w",encoding="utf-8") as f:
        json.dump(dict(provenance=dict(stage="matched filling sensitivity; coarse grid",fillings=FILLINGS,
            Delta_t=DELTA_T,hbar_omega=OMEGA,temperature_fractions=FRACS,U_sweep=U_SWEEP,
            U_sweep_VSO=U_SWEEP_VSO,VSO_sweep=VSO_SWEEP,VSO_sweep_U=VSO_SWEEP_U,
            NK_stage1=NK_STAGE1,NK_mu=NK_MU,NK_DOS=NK_DOS,NELL=NELL,strict_band_tolerance=BAND_TOL,
            methods="Both policies re-solved independently at each filling; strict stage-two points outside the analytic band omitted; relaxed out-of-band ratios retained and flagged. W and W_N use same-filling normal chemical potential.",
            caveat="Coarse sampled sensitivity study, not a dense-curve reproduction or free-energy stability analysis.",
            utc=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")),
            relaxed=relaxed,strict=strict),f,indent=2,allow_nan=False)
    make_csv(relaxed+strict,os.path.join(OUT,"filling_sensitivity_samples.csv"))
    make_summary(relaxed,strict,os.path.join(OUT,"filling_sensitivity_vs_1p885.csv"))
    for pol,rows in (("strict",strict),("relaxed",relaxed)):
        for fam in ("U","VSO"):
            plot_family(rows,fam,pol,os.path.join(OUT,f"{pol}_{fam}_filling_comparison.png"))
    print(f"Finished in {time.time()-t0:.1f}s; outputs in {OUT}",flush=True)

if __name__=="__main__": main()
