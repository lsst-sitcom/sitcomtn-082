# python/lsst/sitcom/tn082/plots_stats.py

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ----------------------------
# Config
# ----------------------------
@dataclass(frozen=True)
class BandConfig:
    # Used only for reference shading in plots (in_band is assumed to exist already)
    comp_band_n: tuple[float, float] = (2981.0, 3959.0)
    tens_band_n: tuple[float, float] = (-4420.0, -3456.0)


TESTING_STATES = ("TESTINGPOSITIVE", "TESTINGNEGATIVE")


# ----------------------------
# Small helpers
# ----------------------------
def ensure_dir(path: str) -> None:
    """Create directory if needed."""
    os.makedirs(os.path.expanduser(path), exist_ok=True)


def add_day_columns(df: pd.DataFrame, *, time_col: str = "breakaway_time_utc") -> pd.DataFrame:
    """
    Ensure time_col is datetime (UTC) and add:
      - day: UTC floored day
      - year: integer year
    """
    out = df.copy()
    t = pd.to_datetime(out.get(time_col), errors="coerce", utc=True)
    out[time_col] = t
    out["day"] = t.dt.floor("D")
    out["year"] = t.dt.year
    return out


def add_out_of_band_from_in_band_inplace(
    df: pd.DataFrame,
    *,
    in_band_col: str = "in_band",
    out_col: str = "out_of_band",
) -> None:
    """
    Add out_of_band = NOT in_band (in-place). NaN -> False.
    Requires in_band_col to exist.
    """
    if in_band_col not in df.columns:
        raise ValueError(f"Missing required column '{in_band_col}'")
    df[in_band_col] = df[in_band_col].fillna(False).astype(bool)
    df[out_col] = (~df[in_band_col]).astype(bool)


def _filter_testing(df: pd.DataFrame, *, state_col: str = "state") -> pd.DataFrame:
    if state_col not in df.columns:
        return df
    return df[df[state_col].isin(TESTING_STATES)].copy()


def _to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


# ----------------------------
# Tables / aggregates
# ----------------------------
def outside_points_by_hp(
    df: pd.DataFrame,
    *,
    hp_col: str = "hp",
    out_col: str = "out_of_band",
) -> pd.DataFrame:
    tab = (
        df.groupby(hp_col, dropna=False, as_index=False)
          .agg(
              n_total=(out_col, "size"),
              n_outside=(out_col, "sum"),
          )
    )
    tab["pct_outside"] = 100.0 * tab["n_outside"] / tab["n_total"]
    return tab.sort_values(hp_col).reset_index(drop=True)


def outside_days_by_year(
    df: pd.DataFrame,
    *,
    out_col: str = "out_of_band",
) -> pd.DataFrame:
    """
    A day is 'outside-day' if it has >=1 out_of_band point.
    Returns #days per year.
    """
    by_day = (
        df.dropna(subset=["day"])
          .groupby(["year", "day"], as_index=False)
          .agg(any_outside=(out_col, "any"))
    )
    summ = (
        by_day.groupby("year", as_index=False)
              .agg(
                  n_days_total=("day", "size"),
                  n_days_outside=("any_outside", "sum"),
              )
    )
    summ["pct_days_outside"] = 100.0 * summ["n_days_outside"] / summ["n_days_total"]
    return summ.sort_values("year").reset_index(drop=True)


def daily_stiffness_inside_outside(
    df: pd.DataFrame,
    *,
    stiffness_col: str = "stiffness_N_per_um",
    out_col: str = "out_of_band",
) -> pd.DataFrame:
    """
    Builds a daily table with stiffness statistics and a day_class:
      outside if >=1 outside point in day, else inside
    """
    d = df.copy()
    d[stiffness_col] = _to_num(d.get(stiffness_col))
    d = d[np.isfinite(d[stiffness_col])].copy()

    daily = (
        d.dropna(subset=["day"])
         .groupby("day", as_index=False)
         .agg(
             year=("year", "first"),
             n_points=(out_col, "size"),
             any_outside=(out_col, "any"),
             frac_outside=(out_col, "mean"),
             stiff_mean=(stiffness_col, "mean"),
             stiff_median=(stiffness_col, "median"),
             stiff_std=(stiffness_col, "std"),
         )
    )
    daily["day_class"] = np.where(daily["any_outside"], "outside", "inside")
    return daily.sort_values("day").reset_index(drop=True)


# ----------------------------
# Plots
# ----------------------------
def plot_hist_outside_points_by_hp(
    df: pd.DataFrame,
    *,
    hp_col: str = "hp",
    out_col: str = "out_of_band",
    title: str = "Outside-band points by hardpoint",
    savepath: str | None = None,
    show: bool = False,
):
    tab = outside_points_by_hp(df, hp_col=hp_col, out_col=out_col)

    plt.close("all")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(tab[hp_col].astype(int), tab["n_outside"].astype(int))

    ax.set_xlabel("Hardpoint (HP)")
    ax.set_ylabel("# outside-band points")
    ax.set_title(title)
    ax.grid(True, axis="y", alpha=0.25)

    for _, r in tab.iterrows():
        ax.text(
            int(r[hp_col]), int(r["n_outside"]),
            f'{r["pct_outside"]:.1f}%',
            ha="center", va="bottom", fontsize=9
        )

    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, dpi=200)
    if show:
        plt.show()
    return fig, ax, tab


def plot_hist_outside_days_by_year(
    df: pd.DataFrame,
    *,
    title: str = "Days with ≥1 outside-band point per year",
    savepath: str | None = None,
    show: bool = False,
):
    summ = outside_days_by_year(df)

    plt.close("all")
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(summ["year"].astype(int), summ["n_days_outside"].astype(int))

    ax.set_xlabel("Year")
    ax.set_ylabel("# outside-days")
    ax.set_title(title)
    ax.grid(True, axis="y", alpha=0.25)

    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, dpi=200)
    if show:
        plt.show()
    return fig, ax, summ


def plot_stiffness_inside_vs_outside_boxplot(
    df: pd.DataFrame,
    *,
    stiffness_col: str = "stiffness_N_per_um",
    out_col: str = "out_of_band",
    use: str = "mean",  # "mean" or "median"
    title: str = "Daily stiffness: inside-days vs outside-days",
    savepath: str | None = None,
    show: bool = False,
):
    daily = daily_stiffness_inside_outside(df, stiffness_col=stiffness_col, out_col=out_col)
    value_col = "stiff_mean" if use == "mean" else "stiff_median"

    inside = daily.loc[daily["day_class"] == "inside", value_col].dropna().to_numpy(float)
    outside = daily.loc[daily["day_class"] == "outside", value_col].dropna().to_numpy(float)
    if inside.size == 0 or outside.size == 0:
        raise ValueError("Not enough data in inside/outside groups for stiffness boxplot.")

    plt.close("all")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot([inside, outside], labels=["inside-days", "outside-days"], showfliers=True)
    ax.set_ylabel(value_col)
    ax.set_title(title)
    ax.grid(True, axis="y", alpha=0.25)

    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, dpi=200)
    if show:
        plt.show()
    return fig, ax, daily


def plot_breakaway_force_vs_disp_testing_expected_band(
    df: pd.DataFrame,
    *,
    hp_col: str = "hp",
    state_col: str = "state",
    force_col: str = "breakaway_force_N",
    disp_col: str = "breakaway_disp_um",
    bands: BandConfig = BandConfig(),
    hps: Iterable[int] = (1, 2, 3, 4, 5, 6),
    ncols: int = 3,
    title: str = "Breakaway force vs disp (testing, expected band)",
    savepath: str | None = None,
    show: bool = False,
):
    # Keep only points inside the expected band for each testing state:
    #  - TESTINGPOSITIVE -> tension band
    #  - TESTINGNEGATIVE -> compression band
    d = df.copy()
    d[force_col] = _to_num(d.get(force_col))
    d[disp_col] = _to_num(d.get(disp_col))
    d = d[np.isfinite(d[force_col]) & np.isfinite(d[disp_col])].copy()
    d = _filter_testing(d, state_col=state_col)

    in_comp = (d[force_col] >= bands.comp_band_n[0]) & (d[force_col] <= bands.comp_band_n[1])
    in_tens = (d[force_col] >= bands.tens_band_n[0]) & (d[force_col] <= bands.tens_band_n[1])
    keep = ((d[state_col] == "TESTINGPOSITIVE") & in_tens) | ((d[state_col] == "TESTINGNEGATIVE") & in_comp)
    d = d[keep].copy()

    hps = list(hps)
    nrows = int(np.ceil(len(hps) / ncols))

    plt.close("all")
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16, 8), sharex=True, sharey=True)
    axes = np.array(axes).reshape(-1)

    for i, hp in enumerate(hps):
        ax = axes[i]
        sub = d[d[hp_col] == hp] if hp_col in d.columns else d.iloc[0:0]

        # band shading (reference)
        ax.axhspan(bands.comp_band_n[0], bands.comp_band_n[1], alpha=0.15)
        ax.axhspan(bands.tens_band_n[0], bands.tens_band_n[1], alpha=0.15)
        ax.axhline(0, linewidth=1, alpha=0.35)

        for st in TESTING_STATES:
            ssub = sub[sub[state_col] == st]
            if not ssub.empty:
                ax.scatter(ssub[disp_col], ssub[force_col], s=12, alpha=0.85, label=st)

        ax.set_title(f"HP{hp} (n={len(sub)})")
        ax.grid(True, alpha=0.25)

        if i % ncols == 0:
            ax.set_ylabel(force_col)
        if i >= (nrows - 1) * ncols:
            ax.set_xlabel(disp_col)

    for j in range(len(hps), len(axes)):
        axes[j].axis("off")

    # global legend unique
    all_h, all_l = [], []
    for ax in axes[: len(hps)]:
        h, l = ax.get_legend_handles_labels()
        all_h += h
        all_l += l
    uniq = {}
    for h, l in zip(all_h, all_l):
        if l not in uniq:
            uniq[l] = h
    if uniq:
        fig.legend(uniq.values(), uniq.keys(), loc="upper right", frameon=True)

    fig.suptitle(title, y=0.98)
    fig.tight_layout(rect=[0, 0, 0.93, 0.95])

    if savepath:
        fig.savefig(savepath, dpi=200)
    if show:
        plt.show()
    return fig, axes[: len(hps)], d


def plot_breakaway_force_vs_disp_outside_points(
    df: pd.DataFrame,
    *,
    force_col: str = "breakaway_force_N",
    disp_col: str = "breakaway_disp_um",
    out_col: str = "out_of_band",
    bands: BandConfig = BandConfig(),
    title: str = "Breakaway force vs disp (outside-band points only)",
    savepath: str | None = None,
    show: bool = False,
):
    d = df.copy()
    d[force_col] = _to_num(d.get(force_col))
    d[disp_col] = _to_num(d.get(disp_col))
    d = d[np.isfinite(d[force_col]) & np.isfinite(d[disp_col])].copy()
    if out_col not in d.columns:
        raise ValueError(f"Missing column: {out_col}. Add it first.")

    d = d[d[out_col]].copy()
    if d.empty:
        raise ValueError("No outside-band points to plot.")

    plt.close("all")
    fig, ax = plt.subplots(figsize=(10, 6))

    # reference shading
    ax.axhspan(bands.comp_band_n[0], bands.comp_band_n[1], alpha=0.15)
    ax.axhspan(bands.tens_band_n[0], bands.tens_band_n[1], alpha=0.15)
    ax.axhline(0, linewidth=1, alpha=0.35)

    ax.scatter(d[disp_col], d[force_col], s=18, alpha=0.85)

    ax.set_xlabel(disp_col)
    ax.set_ylabel(force_col)
    ax.set_title(title)
    ax.grid(True, alpha=0.25)

    fig.tight_layout()
    if savepath:
        fig.savefig(savepath, dpi=200)
    if show:
        plt.show()
    return fig, ax, d


# ----------------------------
# Main driver: generate report
# ----------------------------
def generate_stats_report(
    df_feat: pd.DataFrame,
    *,
    outdir: str,
    bands: BandConfig = BandConfig(),
    time_col: str = "breakaway_time_utc",
    force_col: str = "breakaway_force_N",
    disp_col: str = "breakaway_disp_um",
    stiffness_col: str = "stiffness_N_per_um",
    hp_col: str = "hp",
    state_col: str = "state",
    in_band_col: str = "in_band",
    out_col: str = "out_of_band",
    save_images: bool = True,   # if False, only CSV tables are written
    show: bool = False,
) -> dict[str, str]:
    """
    Generate standard statistics tables and (optionally) figures into outdir.

    Assumptions:
      - df_feat already contains `in_band` boolean (True/False). NaN treated as False.
    """
    outdir = os.path.expanduser(outdir)
    ensure_dir(outdir)

    d = df_feat.copy()

    # Ensure in_band exists + boolean
    if in_band_col not in d.columns:
        raise ValueError(f"Missing required column '{in_band_col}' in df_feat")
    d[in_band_col] = d[in_band_col].fillna(False).astype(bool)

    # Derive out_of_band and add day/year
    add_out_of_band_from_in_band_inplace(d, in_band_col=in_band_col, out_col=out_col)
    d = add_day_columns(d, time_col=time_col)

    outputs: dict[str, str] = {}

    # ---- CSV tables (always) ----
    tab_hp = outside_points_by_hp(d, hp_col=hp_col, out_col=out_col)
    csvpath = os.path.join(outdir, "outside_points_by_hp.csv")
    tab_hp.to_csv(csvpath, index=False)
    outputs["outside_points_by_hp_csv"] = csvpath

    tab_year = outside_days_by_year(d, out_col=out_col)
    csvpath = os.path.join(outdir, "outside_days_by_year.csv")
    tab_year.to_csv(csvpath, index=False)
    outputs["outside_days_by_year_csv"] = csvpath

    daily = daily_stiffness_inside_outside(d, stiffness_col=stiffness_col, out_col=out_col)
    csvpath = os.path.join(outdir, "daily_stiffness_inside_outside.csv")
    daily.to_csv(csvpath, index=False)
    outputs["daily_stiffness_inside_outside_csv"] = csvpath

    # ---- Figures (optional) ----
    if save_images:
        figpath = os.path.join(outdir, "hist_outside_points_by_hp.png")
        plot_hist_outside_points_by_hp(d, hp_col=hp_col, out_col=out_col, savepath=figpath, show=show)
        outputs["hist_outside_points_by_hp_png"] = figpath

        figpath = os.path.join(outdir, "hist_outside_days_by_year.png")
        plot_hist_outside_days_by_year(d, savepath=figpath, show=show)
        outputs["hist_outside_days_by_year_png"] = figpath

        figpath = os.path.join(outdir, "box_stiffness_inside_vs_outside.png")
        plot_stiffness_inside_vs_outside_boxplot(
            d, stiffness_col=stiffness_col, out_col=out_col, use="mean", savepath=figpath, show=show
        )
        outputs["box_stiffness_inside_vs_outside_png"] = figpath

        figpath = os.path.join(outdir, "grid_force_vs_disp_testing_expected_band.png")
        plot_breakaway_force_vs_disp_testing_expected_band(
            d,
            hp_col=hp_col,
            state_col=state_col,
            force_col=force_col,
            disp_col=disp_col,
            bands=bands,
            savepath=figpath,
            show=show,
        )
        outputs["grid_force_vs_disp_testing_expected_band_png"] = figpath

        figpath = os.path.join(outdir, "scatter_force_vs_disp_outside_points.png")
        plot_breakaway_force_vs_disp_outside_points(
            d,
            force_col=force_col,
            disp_col=disp_col,
            out_col=out_col,
            bands=bands,
            savepath=figpath,
            show=show,
        )
        outputs["scatter_force_vs_disp_outside_points_png"] = figpath

    return outputs
