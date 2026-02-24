#!/usr/bin/env python3
"""
Post-process NGAWest2 MPI outputs (H1/H2 + optional RotD).

What it does
------------
1) Merge H1/H2 metrics into a single table (wide columns).
2) Merge optional RotD metrics (pivoted wide).
3) Write:
   - <prefix>_metrics_combined.csv
   - <prefix>_summary_plots.pdf

PDF layout
----------
- Page 1: histograms (predictors + key outputs)
- For each requested output metric y:
  - Page: regressions y vs predictors (train/test + train-fit + 16/84% bands)
  - Page: residual diagnostics (residuals vs predictors + binned 16/84% bands)

Key updates
-----------
- Supports dict-based flatfile variables written as CSV columns: flat__MW, flat__VS30, ...
- Treats sentinel missing values (default -999) PER-COLUMN (does not drop whole record).
- --ml-missing {drop,impute} controls missing predictor handling in fits.
- Train/test split for visualization with counts in legends.
- Plot RAW values; if logx/logy is requested, sets axis scale to log (no ln(x) plotting).
- Ensures log axes have major+minor ticks; labels show plain numbers (e.g., 600 not 6×10^2).

Author: Silvia Mazzoni (silviamazzoni@yahoo.com)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

FLAT_KEYS = ["MW", "VS30", "EpiD", "Rjb", "HypD", "ClstD", "PGA", "PGV", "Tp"]

FLAT_LABEL = {
    "MW": "Mw",
    "VS30": "Vs30 (m/s)",
    "EpiD": "EpiD (km)",
    "Rjb": "Rjb (km)",
    "HypD": "HypD (km)",
    "ClstD": "ClstD (km)",
    "PGA": "PGA (g)",
    "PGV": "PGV (cm/s)",
    "Tp": "Tp (s)",
}

LOG_X_DEFAULT = {"VS30", "EpiD", "Rjb", "HypD", "ClstD", "Tp", "PGV", "PGA"}
LOG_HIST_DEFAULT = LOG_X_DEFAULT | {"amp_range_H1", "amp_range_H2", "amp_range_geom_mean"}

# -----------------------------------------------------------------------------
# Optional ML outputs (from nga_mpi_ml_example.py)
# -----------------------------------------------------------------------------
# Expected optional files per component (H1/H2) in --workdir:
#   <prefix>_ml_report_<comp>.txt
#   <prefix>_ml_preds_<comp>.csv           (only if ML run used --write-preds)
#   <prefix>_model_<comp>.json/.joblib     (if ML run saved a model artifact)
#
# This post-processor:
#   - merges per-record preds/residuals into the combined table (when present)
#   - adds a few ML diagnostic pages to the PDF (when preds are present)


# -----------------------------------------------------------------------------
# Plot styling / ticks
# -----------------------------------------------------------------------------

def set_plot_style(*, base=7, label=7, title=8, legend=6, ticks=6) -> None:
    plt.rcParams.update(
        {
            "font.size": base,
            "axes.labelsize": label,
            "axes.titlesize": title,
            "legend.fontsize": legend,
            "xtick.labelsize": ticks,
            "ytick.labelsize": ticks,
        }
    )

    # Make minor ticks visible and distinct
    mpl.rcParams.update(
        {
            "xtick.minor.visible": True,
            "ytick.minor.visible": True,
            "xtick.major.size": 4,
            "xtick.minor.size": 2,
            "ytick.major.size": 4,
            "ytick.minor.size": 2,
            "xtick.major.width": 0.8,
            "xtick.minor.width": 0.6,
            "ytick.major.width": 0.8,
            "ytick.minor.width": 0.6,
            "xtick.direction": "in",
            "ytick.direction": "in",
        }
    )


def _apply_log_locators(ax: plt.Axes, which: str) -> None:
    """Ensure major+minor ticks exist on a log axis; minor labels hidden."""
    axis = ax.xaxis if which == "x" else ax.yaxis
    axis.set_major_locator(LogLocator(base=10.0, numticks=12))
    axis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=100))
    axis.set_minor_formatter(NullFormatter())


def _plain_log_labels(ax: plt.Axes, which: str, *, base: float = 10.0) -> None:
    """
    Replace default scientific tick labels on log axes with plain numbers.
    Also place major ticks at 1..9 * 10^k (so "600" can be labeled).
    """
    def fmt(v, pos=None):
        if not np.isfinite(v) or v <= 0:
            return ""
        if abs(v - round(v)) / max(1.0, abs(v)) < 1e-10:
            return f"{int(round(v))}"
        return f"{v:g}"

    locator = LogLocator(base=base, subs=np.arange(1, 10))
    formatter = FuncFormatter(fmt)

    if which in ("x", "both"):
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
    if which in ("y", "both"):
        ax.yaxis.set_major_locator(locator)
        ax.yaxis.set_major_formatter(formatter)


def _set_log_axis(ax: plt.Axes, which: str) -> None:
    """Apply log scaling + good tick behavior."""
    if which == "x":
        ax.set_xscale("log")
        _plain_log_labels(ax, "x")
        _apply_log_locators(ax, "x")
    elif which == "y":
        ax.set_yscale("log")
        _plain_log_labels(ax, "y")
        _apply_log_locators(ax, "y")
    else:
        raise ValueError(which)
    ax.minorticks_on()


def _figsize_for(nplots: int, ncols: int, subplot_w: float, subplot_h: float) -> Tuple[float, float, int]:
    ncols = max(1, int(ncols))
    nrows = int(np.ceil(nplots / ncols)) if nplots > 0 else 1
    return subplot_w * ncols, subplot_h * nrows, nrows


# -----------------------------------------------------------------------------
# Data helpers
# -----------------------------------------------------------------------------

def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing: {path}")
    return pd.read_csv(path)


def _parse_kv_report(path: Path) -> Dict[str, object]:
    """Parse a simple key:value report (like the ML report txt)."""
    out: Dict[str, object] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            continue
        try:
            out[k] = float(v)
        except Exception:
            out[k] = v
    return out


def _read_ml_preds(path: Path) -> pd.DataFrame:
    """Read per-record ML predictions CSV (if present) and normalize RSN as string."""
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "rec_id" in df.columns and "RSN" not in df.columns:
        df = df.rename(columns={"rec_id": "RSN"})
    df = _ensure_str_rsn(df, "RSN")
    keep = [c for c in ["RSN", "component", "split", "y", "yhat", "resid"] if c in df.columns]
    return df[keep].copy()


def load_ml_outputs(prefix: str, workdir: Path) -> Tuple[pd.DataFrame, Dict[str, Dict[str, object]]]:
    """Load optional ML outputs for H1/H2. Returns (preds_wide, reports)."""
    reports: Dict[str, Dict[str, object]] = {}
    preds_long: List[pd.DataFrame] = []

    for comp in ("H1", "H2"):
        rep = _parse_kv_report(workdir / f"{prefix}_ml_report_{comp}.txt")
        if rep:
            reports[comp] = rep

        p = workdir / f"{prefix}_ml_preds_{comp}.csv"
        dfl = _read_ml_preds(p)
        if not dfl.empty:
            if "component" not in dfl.columns:
                dfl["component"] = comp
            preds_long.append(dfl)

    if not preds_long:
        return pd.DataFrame(), reports

    pl = pd.concat(preds_long, ignore_index=True)
    value_cols = [c for c in ["split", "y", "yhat", "resid"] if c in pl.columns]
    piv = pl.pivot_table(index="RSN", columns="component", values=value_cols, aggfunc="first")
    piv.columns = [f"{v}_{k}" for (v, k) in piv.columns]
    piv = piv.reset_index()
    piv = _ensure_str_rsn(piv, "RSN")
    return piv, reports


def _ensure_str_rsn(df: pd.DataFrame, col: str = "RSN") -> pd.DataFrame:
    """Force RSN to string consistently (avoids pandas merge dtype error)."""
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=[col]).copy()
        df[col] = df[col].astype("Int64").astype(str)


    return df


def _sanitize_prefix(prefix: str) -> str:
    """Avoid prefix with '/' creating nested output paths."""
    return prefix.replace("/", "_").replace("\\", "_").strip("_")


def _replace_sentinels(series: pd.Series, sentinels: List[float]) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    for v in sentinels:
        s = s.mask(np.isclose(s.astype(float), float(v), equal_nan=False))
    return s


def _train_test_mask(n: int, test_frac: float, seed: int) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(int(seed))
    idx = np.arange(n)
    rng.shuffle(idx)
    ntest = int(np.floor(test_frac * n))
    test = np.zeros(n, dtype=bool)
    test[idx[:ntest]] = True
    return ~test, test


def _to_model(x: np.ndarray, *, use_log: bool) -> np.ndarray:
    """
    Map raw x to model-space.
    If use_log, returns ln(x) for x>0 else NaN.
    """
    x = np.asarray(x, dtype=float)
    if not use_log:
        return x
    out = np.full_like(x, np.nan, dtype=float)
    m = np.isfinite(x) & (x > 0)
    out[m] = np.log(x[m])
    return out


def _prep_xy(
    df: pd.DataFrame,
    xcol: str,
    ycol: str,
    *,
    logx: bool,
    logy: bool,
    sentinels: List[float],
    missing_mode: str,  # drop|impute (impute affects x in model space)
    train_mask: np.ndarray,
    test_mask: np.ndarray,
) -> Dict[str, np.ndarray]:
    """
    Returns raw arrays for plotting + model-space arrays for fitting.

    Keys:
      x_train_raw, y_train_raw, x_test_raw, y_test_raw
      x_train_mod, y_train_mod, x_test_mod, y_test_mod
    """
    x0 = _replace_sentinels(df.get(xcol, np.nan), sentinels).to_numpy(dtype=float, copy=False)
    y0 = _replace_sentinels(df.get(ycol, np.nan), sentinels).to_numpy(dtype=float, copy=False)

    xtr_raw = x0[train_mask].astype(float, copy=True)
    ytr_raw = y0[train_mask].astype(float, copy=True)
    xte_raw = x0[test_mask].astype(float, copy=True)
    yte_raw = y0[test_mask].astype(float, copy=True)

    xtr_mod = _to_model(xtr_raw, use_log=logx)
    ytr_mod = _to_model(ytr_raw, use_log=logy)
    xte_mod = _to_model(xte_raw, use_log=logx)
    yte_mod = _to_model(yte_raw, use_log=logy)

    # y must be finite in model space
    mtr_y = np.isfinite(ytr_mod)
    mte_y = np.isfinite(yte_mod)
    xtr_raw, ytr_raw, xtr_mod, ytr_mod = xtr_raw[mtr_y], ytr_raw[mtr_y], xtr_mod[mtr_y], ytr_mod[mtr_y]
    xte_raw, yte_raw, xte_mod, yte_mod = xte_raw[mte_y], yte_raw[mte_y], xte_mod[mte_y], yte_mod[mte_y]

    if missing_mode == "drop":
        mtr = np.isfinite(xtr_mod) & np.isfinite(ytr_mod)
        mte = np.isfinite(xte_mod) & np.isfinite(yte_mod)
        return {
            "x_train_raw": xtr_raw[mtr],
            "y_train_raw": ytr_raw[mtr],
            "x_test_raw": xte_raw[mte],
            "y_test_raw": yte_raw[mte],
            "x_train_mod": xtr_mod[mtr],
            "y_train_mod": ytr_mod[mtr],
            "x_test_mod": xte_mod[mte],
            "y_test_mod": yte_mod[mte],
        }

    if missing_mode == "impute":
        def _imp(xx: np.ndarray) -> np.ndarray:
            out = xx.copy()
            m = np.isfinite(out)
            med = float(np.nanmedian(out[m])) if np.any(m) else 0.0
            out[~m] = med
            return out

        return {
            "x_train_raw": xtr_raw,
            "y_train_raw": ytr_raw,
            "x_test_raw": xte_raw,
            "y_test_raw": yte_raw,
            "x_train_mod": _imp(xtr_mod),
            "y_train_mod": ytr_mod,
            "x_test_mod": _imp(xte_mod),
            "y_test_mod": yte_mod,
        }

    raise ValueError(f"Unknown missing_mode: {missing_mode}")


def r2_score(y: np.ndarray, yhat: np.ndarray) -> float:
    y = np.asarray(y, dtype=float)
    yhat = np.asarray(yhat, dtype=float)
    m = np.isfinite(y) & np.isfinite(yhat)
    if int(np.sum(m)) < 3:
        return np.nan
    y = y[m]; yhat = yhat[m]
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan


def _fit_line_r2_sigma(x: np.ndarray, y: np.ndarray) -> Optional[Tuple[float, float, float, float, int]]:
    """Fit y=a*x+b in model space. Return (a,b,r2,sigma,n) or None."""
    m = np.isfinite(x) & np.isfinite(y)
    x = x[m]
    y = y[m]
    n = int(x.size)
    if n < 8:
        return None

    A = np.vstack([x, np.ones_like(x)]).T
    a, b = np.linalg.lstsq(A, y, rcond=None)[0]
    yhat = a * x + b
    resid = y - yhat

    ss_res = float(np.sum(resid**2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan
    sigma = float(np.nanstd(resid, ddof=2)) if n > 2 else np.nan
    return float(a), float(b), float(r2), float(sigma), n


def _binned_percentiles(
    x: np.ndarray,
    y: np.ndarray,
    nbins: int = 20,
    p_lo: float = 0.16,
    p_hi: float = 0.84,
) -> Optional[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    """Bin by x and compute median + 16/84% bands."""
    m = np.isfinite(x) & np.isfinite(y)
    x = x[m]
    y = y[m]
    if x.size < 10:
        return None

    xmin = float(np.nanmin(x))
    xmax = float(np.nanmax(x))
    if not np.isfinite(xmin) or not np.isfinite(xmax) or xmin == xmax:
        return None

    edges = np.linspace(xmin, xmax, nbins + 1)
    idx = np.digitize(x, edges) - 1

    xc, y50, ylo, yhi, nn = [], [], [], [], []
    for b in range(nbins):
        mb = idx == b
        if np.sum(mb) < 3:
            continue
        yb = y[mb]
        xc.append(0.5 * (edges[b] + edges[b + 1]))
        y50.append(np.nanmedian(yb))
        ylo.append(np.nanquantile(yb, p_lo))
        yhi.append(np.nanquantile(yb, p_hi))
        nn.append(np.sum(mb))

    if len(xc) < 3:
        return None
    return np.asarray(xc), np.asarray(y50), np.asarray(ylo), np.asarray(yhi), np.asarray(nn)


# -----------------------------------------------------------------------------
# Merge
# -----------------------------------------------------------------------------

def load_and_merge(prefix: str, workdir: Path) -> pd.DataFrame:
    h1_path = workdir / f"{prefix}_metrics_H1.csv"
    h2_path = workdir / f"{prefix}_metrics_H2.csv"
    rotd_path = workdir / f"{prefix}_metrics_RotD.csv"

    h1 = _read_csv(h1_path)
    h2 = _read_csv(h2_path)

    if "rec_id" not in h1.columns or "rec_id" not in h2.columns:
        raise ValueError("Expected 'rec_id' column in metrics files.")

    h1 = h1.rename(columns={"rec_id": "RSN"})
    h2 = h2.rename(columns={"rec_id": "RSN"})

    if "component" in h1.columns:
        h1 = h1.drop(columns=["component"])
    if "component" in h2.columns:
        h2 = h2.drop(columns=["component"])

    h1 = _ensure_str_rsn(h1, "RSN")
    h2 = _ensure_str_rsn(h2, "RSN")

    h1 = h1.set_index("RSN")
    h2 = h2.set_index("RSN")
    h1.columns = [f"{c}_H1" for c in h1.columns]
    h2.columns = [f"{c}_H2" for c in h2.columns]

    df = h1.join(h2, how="inner").reset_index()

    # Geometric mean of amp_range
    if "amp_range_H1" in df.columns and "amp_range_H2" in df.columns:
        a1 = pd.to_numeric(df["amp_range_H1"], errors="coerce").to_numpy()
        a2 = pd.to_numeric(df["amp_range_H2"], errors="coerce").to_numpy()
        df["amp_range_geom_mean"] = np.sqrt(a1 * a2)
    else:
        df["amp_range_geom_mean"] = np.nan

    # Optional RotD merge (pivot wide)
    if rotd_path.exists():
        rotd = pd.read_csv(rotd_path)
        if {"rsn", "rotd"}.issubset(set(rotd.columns)):
            rotd = rotd.copy()
            rotd["rsn"] = pd.to_numeric(rotd["rsn"], errors="coerce")
            rotd = rotd.dropna(subset=["rsn"])
            rotd["RSN"] = rotd["rsn"].astype("Int64").astype(str)

            value_cols = [c for c in ["pga", "amp_range", "dt_peaks", "dt_peaks_norm", "duration", "angle_deg"] if c in rotd.columns]
            piv = rotd.pivot_table(index="RSN", columns="rotd", values=value_cols, aggfunc="first")
            piv.columns = [f"{v}_{k}" for (v, k) in piv.columns]
            piv = piv.reset_index()

            piv = _ensure_str_rsn(piv, "RSN")
            df = _ensure_str_rsn(df, "RSN")
            df = df.merge(piv, on="RSN", how="left")

    # Optional ML merge (per-record preds/residuals)
    preds_ml, _reports = load_ml_outputs(prefix, workdir)
    if not preds_ml.empty:
        preds_ml = _ensure_str_rsn(preds_ml, "RSN")
        df = _ensure_str_rsn(df, "RSN")
        df = df.merge(preds_ml, on="RSN", how="left")    

    return df


# -----------------------------------------------------------------------------
# Plotting
# -----------------------------------------------------------------------------

def plot_histograms_page(
    df: pd.DataFrame,
    pdf: PdfPages,
    cols: List[Tuple[str, str]],
    *,
    sentinels: List[float],
    ncols: int,
    subplot_w: float,
    subplot_h: float,
    page_title: str,
    show: bool = False,
    no_pdf: bool = False,
) -> None:
    n = len(cols)
    fig_w, fig_h, nrows = _figsize_for(n, ncols, subplot_w, subplot_h)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_w, fig_h))
    fig.set_facecolor("#fcf3fc")
    axes = np.asarray(axes).reshape(-1)



    for ax, (col, label) in zip(axes, cols):
        if col not in df.columns:
            ax.set_title(f"{label} (missing)")
            ax.axis("off")
            continue

        x = _replace_sentinels(df[col], sentinels).to_numpy(dtype=float, copy=False)
        x = x[np.isfinite(x)]
        if x.size == 0:
            ax.set_title(f"{label} (no data)")
            ax.axis("off")
            continue

        use_log = (col in LOG_HIST_DEFAULT) or col.startswith("amp_range")
        if use_log:
            x = x[x > 0]
            if x.size == 0:
                ax.set_title(f"{label} (no positive data)")
                ax.axis("off")
                continue
            bins = np.logspace(np.log10(np.min(x)), np.log10(np.max(x)), 40)
            ax.hist(x, bins=bins)
            _set_log_axis(ax, "x")
        else:
            ax.hist(x, bins=40)

        ax.set_xlabel(label)
        ax.set_ylabel("count")
        ax.grid(True, alpha=0.2)

    for ax in axes[len(cols):]:
        ax.axis("off")

    fig.suptitle(page_title, fontsize=plt.rcParams.get("axes.titlesize", 8) + 2)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _emit_figure(fig, pdf, show=show, no_pdf=no_pdf)



def plot_regressions_page(
    df: pd.DataFrame,
    pdf: PdfPages,
    pairs: List[Tuple[str, str, str, bool, bool]],
    *,
    sentinels: List[float],
    missing_mode: str,
    train_mask: np.ndarray,
    test_mask: np.ndarray,
    ncols: int,
    subplot_w: float,
    subplot_h: float,
    page_title: str,
    show: bool = False,
    no_pdf: bool = False,
) -> None:
    n = len(pairs)
    fig_w, fig_h, nrows = _figsize_for(n, ncols, subplot_w, subplot_h)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_w, fig_h))
    fig.set_facecolor("#f3fcf8")
    axes = np.asarray(axes).reshape(-1)

    for ax, (xcol, ycol, title, logx, logy) in zip(axes, pairs):
        out = _prep_xy(
            df, xcol, ycol,
            logx=logx, logy=logy,
            sentinels=sentinels,
            missing_mode=missing_mode,
            train_mask=train_mask,
            test_mask=test_mask,
        )

        xtr_raw, ytr_raw = out["x_train_raw"], out["y_train_raw"]
        xte_raw, yte_raw = out["x_test_raw"], out["y_test_raw"]
        xtr_mod, ytr_mod = out["x_train_mod"], out["y_train_mod"]

        if xtr_raw.size + xte_raw.size == 0:
            ax.set_title(f"{title} (no data)")
            ax.axis("off")
            continue

        if xtr_raw.size:
            ax.scatter(xtr_raw, ytr_raw, s=8, alpha=0.50, color='blue', label=f"train (n={xtr_raw.size})")
        if xte_raw.size:
            ax.scatter(xte_raw, yte_raw, s=12, alpha=0.70, color='red', label=f"test (n={xte_raw.size})")

        if logx:
            _set_log_axis(ax, "x")
        if logy:
            _set_log_axis(ax, "y")

        # Fit in model space (train only) and map back to raw for plotting
        fit = _fit_line_r2_sigma(xtr_mod, ytr_mod)
        if fit is not None:
            a, b, r2, sig, nfit = fit

            x_all = np.r_[xtr_raw, xte_raw]
            x_all = x_all[np.isfinite(x_all)]
            if logx:
                x_all = x_all[x_all > 0]
                xs_raw = np.logspace(np.log10(np.min(x_all)), np.log10(np.max(x_all)), 160)
                xs_mod = np.log(xs_raw)
            else:
                xs_raw = np.linspace(np.min(x_all), np.max(x_all), 160)
                xs_mod = xs_raw

            ys_mod = a * xs_mod + b
            if logy:
                ys_raw = np.exp(ys_mod)
                ax.plot(xs_raw, ys_raw, color='blue', linewidth=1.5)
                if np.isfinite(sig) and sig > 0:
                    ax.fill_between(xs_raw, np.exp(ys_mod - sig), np.exp(ys_mod + sig), color='blue', alpha=0.2)
            else:
                ys_raw = ys_mod
                ax.plot(xs_raw, ys_raw, color='blue', linewidth=1.5)
                if np.isfinite(sig) and sig > 0:
                    ax.fill_between(xs_raw, ys_raw - sig, ys_raw + sig, color='blue', alpha=0.2)

            ax.text(
                0.02, 0.96,
                f"fit(train): n={nfit}\nR²={r2:.3g}\nσ={sig:.3g}",
                transform=ax.transAxes,
                va="top",
                fontsize=plt.rcParams.get("xtick.labelsize", 6),
            )

        ax.set_xlabel(FLAT_LABEL.get(xcol, xcol))
        ax.set_ylabel(FLAT_LABEL.get(ycol, ycol))
        ax.set_title(title)
        ax.grid(True, alpha=0.2)
        ax.legend(loc="best", frameon=True)

    for ax in axes[len(pairs):]:
        ax.axis("off")

    fig.suptitle(page_title, fontsize=plt.rcParams.get("axes.titlesize", 8) + 2)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _emit_figure(fig, pdf, show=show, no_pdf=no_pdf)
    



def plot_residuals_page(
    df: pd.DataFrame,
    pdf: PdfPages,
    pairs: List[Tuple[str, str, str, bool, bool]],
    *,
    sentinels: List[float],
    missing_mode: str,
    train_mask: np.ndarray,
    test_mask: np.ndarray,
    nbins: int,
    ncols: int,
    subplot_w: float,
    subplot_h: float,
    page_title: str,
    show: bool = False,
    no_pdf: bool = False,    
) -> None:
    """
    Residuals are computed relative to the TRAIN fit, in MODEL space.
    Residual axis is linear (model-space residuals).
    """
    n = len(pairs)
    fig_w, fig_h, nrows = _figsize_for(n, ncols, subplot_w, subplot_h)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_w, fig_h))
    fig.set_facecolor("#f0ebfd")
    axes = np.asarray(axes).reshape(-1)

    for ax, (xcol, ycol, title, logx, logy) in zip(axes, pairs):
        out = _prep_xy(
            df, xcol, ycol,
            logx=logx, logy=logy,
            sentinels=sentinels,
            missing_mode=missing_mode,
            train_mask=train_mask,
            test_mask=test_mask,
        )

        xtr_raw, xte_raw = out["x_train_raw"], out["x_test_raw"]
        xtr_mod, ytr_mod = out["x_train_mod"], out["y_train_mod"]
        xte_mod, yte_mod = out["x_test_mod"], out["y_test_mod"]

        fit = _fit_line_r2_sigma(xtr_mod, ytr_mod)
        if fit is None or xtr_mod.size < 8:
            ax.set_title(f"Residuals: {title} (no fit)")
            ax.axis("off")
            continue

        a, b, _, _, _ = fit
        rtr = ytr_mod - (a * xtr_mod + b)
        rte = yte_mod - (a * xte_mod + b) if xte_mod.size else np.array([], dtype=float)

        if rtr.size:
            ax.scatter(xtr_raw, rtr, s=8, alpha=0.50, color='blue', label=f"train (n={rtr.size})")
        if rte.size:
            ax.scatter(xte_raw, rte, s=12, alpha=0.70, color='red', label=f"test (n={rte.size})")

        if logx:
            _set_log_axis(ax, "x")

        # Bin in model-x if logx, but plot against raw-x
        xb = xtr_mod if logx else xtr_raw
        bp = _binned_percentiles(xb, rtr, nbins=nbins, p_lo=0.16, p_hi=0.84)
        if bp is not None:
            xc, r50, rlo, rhi, _nn = bp
            xc_plot = np.exp(xc) if logx else xc
            ax.plot(xc_plot, r50, color='blue', linewidth=1.5)
            ax.fill_between(xc_plot, rlo, rhi, color='blue', alpha=0.2)

        ax.axhline(0.0, linewidth=1.0, alpha=0.6)
        ax.set_xlabel(FLAT_LABEL.get(xcol, xcol))
        ax.set_ylabel("residual (model space)")
        ax.set_title(f"Residuals: {title}")
        ax.grid(True, alpha=0.2)
        ax.legend(loc="best", frameon=True)

    for ax in axes[len(pairs):]:
        ax.axis("off")

    fig.suptitle(page_title, fontsize=plt.rcParams.get("axes.titlesize", 8) + 2)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    pdf.savefig(fig)
    plt.close(fig)


def plot_ml_pages(
    df: pd.DataFrame,
    pdf: PdfPages,
    *,
    sentinels: List[float],
    ncols: int,
    subplot_w: float,
    subplot_h: float,
    page_title_prefix: str = "ML diagnostics",
    show: bool = False,
    no_pdf: bool = False,
) -> None:
    """Add ML diagnostic pages if ML prediction columns exist."""
    comps = []
    for comp in ("H1", "H2"):
        if f"yhat_{comp}" in df.columns and f"y_{comp}" in df.columns:
            comps.append(comp)
    if not comps:
        return

    # Page 1: yhat vs y
    n = len(comps)
    fig_w, fig_h, nrows = _figsize_for(n, ncols, subplot_w, subplot_h)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_w, fig_h))
    fig.set_facecolor("#fff7e6")
    axes = np.asarray(axes).reshape(-1)

    for ax, comp in zip(axes, comps):
        y = _replace_sentinels(df[f"y_{comp}"], sentinels).to_numpy(dtype=float, copy=False)
        yh = _replace_sentinels(df[f"yhat_{comp}"], sentinels).to_numpy(dtype=float, copy=False)
        split = df.get(f"split_{comp}", pd.Series([""] * len(df))).astype(str).to_numpy()

        m = np.isfinite(y) & np.isfinite(yh)
        y = y[m]; yh = yh[m]; split = split[m]

        if y.size == 0:
            ax.set_title(f"{comp}: no ML preds")
            ax.axis("off")
            continue

        for lab, mask in [("train", split == "train"), ("test", split == "test")]:
            if np.any(mask):
                ax.scatter(y[mask], yh[mask], s=10, alpha=0.65, label=f"{lab} (n={int(np.sum(mask))})")

        lo = float(np.nanmin(np.r_[y, yh]))
        hi = float(np.nanmax(np.r_[y, yh]))
        if np.isfinite(lo) and np.isfinite(hi) and lo != hi:
            ax.plot([lo, hi], [lo, hi], linewidth=1.0, alpha=0.7)

        ax.text(
            0.02, 0.96,
            f"R²(all)={r2_score(y, yh):.3g}",
            transform=ax.transAxes,
            va="top",
            fontsize=plt.rcParams.get("xtick.labelsize", 6),
        )

        ax.set_title(f"{comp}: yhat vs y (amp_range)")
        ax.set_xlabel("y (true)")
        ax.set_ylabel("yhat (pred)")
        ax.grid(True, alpha=0.2)
        ax.legend(loc="best", frameon=True)

    for ax in axes[len(comps):]:
        ax.axis("off")

    fig.suptitle(f"{page_title_prefix}: Predictions", fontsize=plt.rcParams.get("axes.titlesize", 8) + 2)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _emit_figure(fig, pdf, show=show, no_pdf=no_pdf)


    # Page 2: residual histograms
    fig_w, fig_h, nrows = _figsize_for(n, ncols, subplot_w, subplot_h)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(fig_w, fig_h))
    fig.set_facecolor("#eef7ff")
    axes = np.asarray(axes).reshape(-1)

    for ax, comp in zip(axes, comps):
        r = _replace_sentinels(df.get(f"resid_{comp}", np.nan), sentinels).to_numpy(dtype=float, copy=False)
        split = df.get(f"split_{comp}", pd.Series([""] * len(df))).astype(str).to_numpy()
        m = np.isfinite(r)
        r = r[m]; split = split[m]

        if r.size == 0:
            ax.set_title(f"{comp}: no residuals")
            ax.axis("off")
            continue

        for lab, mask in [("train", split == "train"), ("test", split == "test")]:
            if np.any(mask):
                ax.hist(r[mask], bins=40, alpha=0.55, label=f"{lab} (n={int(np.sum(mask))})")

        ax.axvline(0.0, linewidth=1.0, alpha=0.7)
        ax.set_title(f"{comp}: residuals (y - yhat)")
        ax.set_xlabel("residual")
        ax.set_ylabel("count")
        ax.grid(True, alpha=0.2)
        ax.legend(loc="best", frameon=True)

    for ax in axes[len(comps):]:
        ax.axis("off")

    fig.suptitle(f"{page_title_prefix}: Residuals", fontsize=plt.rcParams.get("axes.titlesize", 8) + 2)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _emit_figure(fig, pdf, show=show, no_pdf=no_pdf)


def _emit_figure(fig, pdf, *, show: bool, no_pdf: bool):
    if not no_pdf and pdf is not None:
        pdf.savefig(fig)
    if show:
        plt.show()
    plt.close(fig)

# def emit(fig, pdf, show: bool):
#     if pdf is not None:
#         pdf.savefig(fig)
#     if show:
#         plt.show()
#     plt.close(fig)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", required=True, help="Prefix used by your MPI script (e.g., NGAWest2)")
    ap.add_argument("--workdir", default=".", help="Directory containing the output CSVs")
    ap.add_argument("--outdir", default="", help="Output directory (default: <workdir>/<prefix>_postproc)")
    ap.add_argument("--target", default="amp_range_geom_mean", help="Default output metric (y)")

    ap.add_argument(
        "--sentinel",
        type=float,
        action="append",
        default=[-999.0],
        help="Sentinel missing value(s) treated as NaN (repeatable). Default: -999.0",
    )

    ap.add_argument(
        "--ml-missing",
        choices=["drop", "impute"],
        default="drop",
        help="Missing predictor handling for fits: drop pairs with NaN or median-impute x (per split).",
    )

    ap.add_argument("--test-frac", type=float, default=0.20, help="Test fraction for train/test split")
    ap.add_argument("--seed", type=int, default=12345, help="RNG seed for train/test split")
    ap.add_argument("--nbins", type=int, default=20, help="Bins for residual percentile bands")

    ap.add_argument("--subplot-w", type=float, default=4.0, help="Width per subplot (inches)")
    ap.add_argument("--subplot-h", type=float, default=2.0, help="Height per subplot (inches)")
    ap.add_argument("--ncols", type=int, default=2, help="Subplot columns per page")

    ap.add_argument(
        "--outputs",
        default="",
        help="Comma-separated list of output metrics (y columns). "
             "If empty, uses --target + any RotD outputs present.",
    )

    ap.add_argument("--font-base", type=float, default=7)
    ap.add_argument("--font-label", type=float, default=7)
    ap.add_argument("--font-title", type=float, default=8)
    ap.add_argument("--font-legend", type=float, default=6)
    ap.add_argument("--font-tick", type=float, default=6)

    ap.add_argument("--show", action="store_true",
                help="Display figures interactively instead of writing only to PDF")
    ap.add_argument("--no-pdf", action="store_true",
                help="If set, do not write the PDF (useful with --show)")

    

    args = ap.parse_args(argv)

    set_plot_style(
        base=args.font_base,
        label=args.font_label,
        title=args.font_title,
        legend=args.font_legend,
        ticks=args.font_tick,
    )

    workdir = Path(args.workdir).expanduser().resolve()
    prefix_in = args.prefix
    prefix_safe = _sanitize_prefix(prefix_in)

    outdir = Path(args.outdir).expanduser().resolve() if args.outdir else (workdir / f"{prefix_safe}_postproc")
    outdir.mkdir(parents=True, exist_ok=True)

    df = load_and_merge(prefix_in, workdir)






    combined_csv = outdir / f"{prefix_safe}_metrics_combined.csv"
    df.to_csv(combined_csv, index=False)
    print(f"Wrote: {combined_csv}")

    # Optional: capture ML report summaries (if present)
    _preds_ml, ml_reports = load_ml_outputs(prefix_in, workdir)
    if ml_reports:
        ml_summary_path = outdir / f"{prefix_safe}_ml_summary.json"
        with open(ml_summary_path, "w", encoding="utf-8") as f:
            json.dump(ml_reports, f, indent=2)
        print(f"Wrote: {ml_summary_path}")
    
        # Pull flat vars from either H1 or H2 (they should match)
        for k in FLAT_KEYS:
            c1 = f"flat__{k}_H1"
            c2 = f"flat__{k}_H2"
            if c1 in df.columns:
                df[k] = pd.to_numeric(df[c1], errors="coerce")
            elif c2 in df.columns:
                df[k] = pd.to_numeric(df[c2], errors="coerce")
            else:
                df[k] = np.nan
            df[k] = _replace_sentinels(df[k], args.sentinel)
    
        if args.target not in df.columns:
            raise ValueError(f"--target '{args.target}' not found in merged table.")
    
        # Choose outputs (one regression+residual page per output)
        if args.outputs.strip():
            outputs = [s.strip() for s in args.outputs.split(",") if s.strip()]
        else:
            outputs = [args.target]
            for y in [
                "pga_RotD50", "amp_range_RotD50",
                "pga_RotD0", "pga_RotD100",
                "amp_range_RotD0", "amp_range_RotD100",
            ]:
                if y in df.columns and y not in outputs:
                    outputs.append(y)
    
        outputs = [y for y in outputs if y in df.columns]
        if not outputs:
            raise ValueError("No valid outputs found. Check --target/--outputs.")
    
        train_mask, test_mask = _train_test_mask(len(df), test_frac=float(args.test_frac), seed=int(args.seed))

    # Histogram columns (one page total)
    hist_cols: List[Tuple[str, str]] = [(k, FLAT_LABEL.get(k, k)) for k in FLAT_KEYS]
    for c, lab in [
        ("dt_H1", "dt (s) [H1]"),
        ("dt_H2", "dt (s) [H2]"),
        ("amp_range_H1", "Range (H1)"),
        ("amp_range_H2", "Range (H2)"),
        ("amp_range_geom_mean", "Range (GM)"),
        ("duration_H1", "Duration (H1) (s)"),
        ("duration_H2", "Duration (H2) (s)"),
        ("dt_peaks_norm_H1", "Δt_peaks/Dur (H1)"),
        ("dt_peaks_norm_H2", "Δt_peaks/Dur (H2)"),
    ]:
        if c in df.columns:
            hist_cols.append((c, lab))

    report_pdf = outdir / f"{prefix_safe}_summary_plots.pdf"

    pdf = None
    if not args.no_pdf:
        pdf = PdfPages(report_pdf)

    try:
        with PdfPages(report_pdf) as pdf:
            plot_histograms_page(
                df,
                pdf,
                hist_cols,
                sentinels=args.sentinel,
                ncols=args.ncols,
                subplot_w=args.subplot_w,
                subplot_h=args.subplot_h,
                page_title=f"Histograms (n={len(df)})",
                show=args.show,
                no_pdf=args.no_pdf,
            )
            # Optional ML pages (if ML preds CSVs exist)
            plot_ml_pages(
                df,
                pdf,
                sentinels=args.sentinel,
                ncols=args.ncols,
                subplot_w=args.subplot_w,
                subplot_h=args.subplot_h,
                page_title_prefix="ML diagnostics",
                show=args.show,
                no_pdf=args.no_pdf,
            )
    
            for ycol in outputs:
                pairs: List[Tuple[str, str, str, bool, bool]] = []
                for xcol in FLAT_KEYS:
                    logx = xcol in LOG_X_DEFAULT
                    logy = True  # keep your current choice
                    title = f"{ycol} vs {FLAT_LABEL.get(xcol, xcol)}"
                    pairs.append((xcol, ycol, title, logx, logy))
    
                # Optional extra relationship only for the GM case
                if ycol == "amp_range_geom_mean" and "amp_range_H1" in df.columns and "amp_range_H2" in df.columns:
                    pairs.append(("amp_range_H1", "amp_range_H2", "amp_range_H1 vs amp_range_H2", True, True))
    
                plot_regressions_page(
                    df,
                    pdf,
                    pairs,
                    sentinels=args.sentinel,
                    missing_mode=args.ml_missing,
                    train_mask=train_mask,
                    test_mask=test_mask,
                    ncols=args.ncols,
                    subplot_w=args.subplot_w,
                    subplot_h=args.subplot_h,
                    page_title=f"Regressions for {ycol} (missing={args.ml_missing})",
                    show=args.show,
                    no_pdf=args.no_pdf,
                )
    
                plot_residuals_page(
                    df,
                    pdf,
                    pairs,
                    sentinels=args.sentinel,
                    missing_mode=args.ml_missing,
                    train_mask=train_mask,
                    test_mask=test_mask,
                    nbins=int(args.nbins),
                    ncols=args.ncols,
                    subplot_w=args.subplot_w,
                    subplot_h=args.subplot_h,
                    page_title=f"Residual diagnostics for {ycol} (missing={args.ml_missing})",
                    show=args.show,
                    no_pdf=args.no_pdf,
                )
        pass
    finally:
        if pdf is not None:
            pdf.close()
    
    if not args.no_pdf:
        print(f"Wrote: {report_pdf}")        

    # print(f"Wrote: {report_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Examples:
# python3 postprocess_nga_metrics_extended_ml.py --prefix NGAWest2 --workdir out_process --target amp_range_geom_mean
# python3 postprocess_nga_metrics_extended_ml.py --prefix NGAWest2 --workdir out_process --ml-missing impute --sentinel -999 --sentinel -999.0
