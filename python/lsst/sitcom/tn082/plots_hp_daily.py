# python/lsst/sitcom/tn082/filters_valiplots_hp_daily.py

"""
Script to generate daily aggregated stiffness and breakaway force plots for each hardpoint,
split by test state, with optional tolerance bands and shared y-axis limits.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Iterable, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Default test states shown in both plots
DEFAULT_STATES = ("TESTINGPOSITIVE", "TESTINGNEGATIVE")

# Tolerance bands for breakaway force [N]
COMP_BAND = (2981.0, 3959.0)  # Compression tolerance band
TENS_BAND = (-4420.0, -3456.0)  # Tension tolerance band


# Status color palette — aligned with HardpointTest enum values used across
# the codebase so that state colors are consistent in every plot.

STATUS_COLORS = {
    "NOTTESTED": "lightgrey",
    "MOVINGNEGATIVE": "lightsteelblue",
    "TESTINGPOSITIVE": "forestgreen",
    "TESTINGNEGATIVE": "royalblue",
    "MOVINGREFERENCE": "darkseagreen",
    "PASSED": "dimgrey",
    "FAILED": "red",
}


def dt_utc(s: pd.Series) -> pd.Series:
    """Parse a Series to timezone-aware UTC datetime, coercing invalid values to NaT."""
    return pd.to_datetime(s, errors="coerce", utc=True)


def ensure_outdir(outdir: Optional[str]) -> Optional[Path]:
    """Resolve and create the output directory if a path was provided."""
    if outdir is None:
        return None
    p = Path(os.path.expanduser(outdir))
    p.mkdir(parents=True, exist_ok=True)
    return p


def state_color(state: str) -> str:
    """
    Return the canonical color for a given hardpoint state string.
    Falls back to a neutral grey if the state is not in STATUS_COLORS.
    """
    return STATUS_COLORS.get(state, "grey")


def plot_daily_stiffness_each_hp(
    df: pd.DataFrame,
    *,
    time_col: str = "t_start_utc",  # or "date"
    value_col: str = "stiffness_N_per_um",
    hp_col: str = "hp",
    state_col: str = "state",
    states: Sequence[str] = DEFAULT_STATES,
    since: str = "2025-01-01",
    require_stiff_ok: bool = True,
    only_valid_days=True,
    agg: str = "mean",  # "mean" or "median"
    show_std_band: bool = True,  # daily ± std shaded band
    share_ylim: bool = True,
    pad_frac: float = 0.05,
    hp_list: Optional[Iterable[int]] = None,
    show: bool = True,
    outdir: Optional[str] = None,
    fname_prefix: str = "daily_stiffness",
    dpi: int = 160,
) -> Dict[int, plt.Figure]:
    """
    One figure per HP: daily aggregated stiffness vs time, split by state.

    Each state is drawn with its canonical color from STATUS_COLORS. An optional
    shaded band shows ± one standard deviation around the daily aggregate.

    Args:
        df:              Input DataFrame.
        time_col:        Column with timestamps (UTC).
        value_col:       Column with stiffness values [N/µm].
        hp_col:          Column identifying the hardpoint number.
        state_col:       Column with the HardpointTest state string.
        states:          States to include in the plot.
        since:           Earliest date to include (ISO format).
        require_stiff_ok: If True, rows where stiff_ok is False are dropped.
        only_valid_days:  If True, rows where valid_days is False are dropped.
        agg:             Daily aggregation method: "mean" or "median".
        show_std_band:   If True, draw a ± std shaded band around the aggregate line.
        share_ylim:      If True, all HP figures share the same y-axis limits.
        pad_frac:        Fractional padding added to the shared y-axis limits.
        hp_list:         Subset of hardpoints to plot (None → all available).
        show:            If True, call plt.show() after each figure.
        outdir:          Directory to save PNG files (None → do not save).
        fname_prefix:    Filename prefix for saved PNGs.
        dpi:             Resolution for saved PNGs.

    Returns:
        Dictionary mapping hardpoint number → matplotlib Figure.

    Raises:
        KeyError:  If a required column is missing from the DataFrame.
        ValueError: If no data remains after filtering, or if agg is invalid.
    """
    d = df.copy()

    # Parse timestamps and apply date filter (UTC-aware)
    if time_col not in d.columns:
        raise KeyError(f"Missing column: {time_col}")
    d["_t"] = dt_utc(d[time_col])
    d = d[d["_t"].notna()].copy()
    d = d[d["_t"] >= pd.Timestamp(since, tz="UTC")].copy()
    # Floor to day resolution for daily grouping
    d["day"] = d["_t"].dt.floor("D")

    # Optional quality filter based on stiff_ok column
    if require_stiff_ok:
        if "stiff_ok" not in d.columns:
            raise KeyError("Missing column: stiff_ok")
        d = d[d["stiff_ok"].fillna(False).astype(bool)].copy()

    # Valid-day filter
    if only_valid_days:
        if "valid_day" not in d.columns:
            raise KeyError("Column 'valid_day' not found. Run filter_valid_days first.")
        d = d[d["valid_day"].fillna(False).astype(bool)]

    d = d[d["stiffness_N_per_um"] > 1].copy()

    # Validate required columns and coerce types for filtering and plotting
    for c in (hp_col, state_col, value_col):
        if c not in d.columns:
            raise KeyError(f"Missing column: '{c}'")

    d[hp_col] = pd.to_numeric(d[hp_col], errors="coerce").astype("Int64")
    d[value_col] = pd.to_numeric(d[value_col], errors="coerce")
    d = d[d[hp_col].notna() & d[value_col].notna()].copy()
    d = d[d[state_col].isin(states)].copy()

    if d.empty:
        raise ValueError("No data remaining after filters for stiffness.")

    # Determine which hardpoints to plot
    hps_all = sorted(d[hp_col].unique().astype(int).tolist())
    if hp_list is None:
        hp_use = hps_all
    else:
        hp_set = set(hps_all)
        hp_use = [int(h) for h in hp_list if int(h) in hp_set]
    if not hp_use:
        raise ValueError("hp_list does not intersect with available hardpoints.")

    # Daily aggregation grouped by (day, hp, state)
    if agg == "mean":
        daily = d.groupby(["day", hp_col, state_col], as_index=False).agg(
            y=(value_col, "mean"), y_std=(value_col, "std"), n=(value_col, "size")
        )
    elif agg == "median":
        daily = d.groupby(["day", hp_col, state_col], as_index=False).agg(
            y=(value_col, "median"), y_std=(value_col, "std"), n=(value_col, "size")
        )
    else:
        raise ValueError("agg must be 'mean' or 'median'")

    # Compute shared y-axis limits across all HPs if requested, including std band extents if shown
    ylims = None
    if share_ylim:
        y = daily["y"].to_numpy(float)
        y_min = float(np.nanmin(y))
        y_max = float(np.nanmax(y))
        if show_std_band:
            # Extend limits to include the std band extents
            lo = (daily["y"] - daily["y_std"]).to_numpy(float)
            hi = (daily["y"] + daily["y_std"]).to_numpy(float)
            y_min = min(y_min, float(np.nanmin(lo)))
            y_max = max(y_max, float(np.nanmax(hi)))
        span = y_max - y_min
        pad = pad_frac * span if np.isfinite(span) and span > 0 else 1.0
        ylims = (y_min - pad, y_max + pad)

    outpath = ensure_outdir(outdir)
    figs: Dict[int, plt.Figure] = {}

    # One figure per hardpoint
    for hp in hp_use:
        sub = daily[daily[hp_col].astype(int) == hp]
        fig, ax = plt.subplots(figsize=(10, 4.8), constrained_layout=True)

        for st in states:
            ssub = sub[sub[state_col] == st].sort_values("day")
            if ssub.empty:
                continue
            # Use canonical status color from STATUS_COLORS
            color = state_color(st)
            ax.plot(
                ssub["day"],
                ssub["y"],
                marker="o",
                alpha=0.85,
                color=color,
                label=f"{st} ({agg})",
            )
            if show_std_band:
                # Shaded ± std band with reduced opacity
                ax.fill_between(
                    ssub["day"],
                    (ssub["y"] - ssub["y_std"]).to_numpy(float),
                    (ssub["y"] + ssub["y_std"]).to_numpy(float),
                    alpha=0.15,
                    color=color,
                )

        ax.set_title(
            f"HP{hp} — Daily stiffness ({agg}) since {pd.Timestamp(since).date()}"
        )
        ax.set_xlabel("Day (UTC)")
        ax.set_ylabel("Stiffness [N/µm]")
        ax.grid(True, alpha=0.25)
        if ylims is not None:
            ax.set_ylim(*ylims)
        ax.legend(loc="best", fontsize=9, frameon=True)

        figs[hp] = fig
        if outpath is not None:
            fig.savefig(outpath / f"{fname_prefix}_HP{hp}.png", dpi=dpi)

        if show:
            plt.show()
        else:
            plt.close(fig)

    return figs


def plot_breakaway_each_hp(
    df: pd.DataFrame,
    *,
    time_col: str = "t_start_utc",
    y_col: str = "breakaway_force_N",
    hp_col: str = "hp",
    state_col: str = "state",
    states: Sequence[str] = DEFAULT_STATES,
    since: str = "2025-01-01",
    require_stiff_ok: bool = True,
    only_valid_days=True,
    share_ylim: bool = True,
    pad_frac: float = 0.05,
    hp_list: Optional[Iterable[int]] = None,
    comp_band: Tuple[float, float] = COMP_BAND,
    tens_band: Tuple[float, float] = TENS_BAND,
    include_bands_in_ylim: bool = True,
    show_inband_markers: bool = False,
    show: bool = True,
    outdir: Optional[str] = None,
    fname_prefix: str = "breakaway_time",
    dpi: int = 160,
) -> Dict[int, plt.Figure]:

    d = df.copy()

    if time_col not in d.columns:
        raise KeyError(f"Missing column: {time_col}")
    d["_t"] = dt_utc(d[time_col])
    d = d[d["_t"].notna()].copy()
    d = d[d["_t"] >= pd.Timestamp(since, tz="UTC")].copy()

    for c in (hp_col, state_col, y_col):
        if c not in d.columns:
            raise KeyError(f"Missing column: '{c}'")

    d[hp_col] = pd.to_numeric(d[hp_col], errors="coerce").astype("Int64")
    d[y_col] = pd.to_numeric(d[y_col], errors="coerce")
    d = d[d[hp_col].notna() & d[y_col].notna()].copy()
    d = d[d[state_col].isin(states)].copy()

    # Valid-day filter
    if only_valid_days:
        if "valid_day" not in d.columns:
            raise KeyError("Column 'valid_day' not found. Run filter_valid_days first.")
        d = d[d["valid_day"].fillna(False).astype(bool)]

    if require_stiff_ok:
        if "stiff_ok" not in d.columns:
            raise KeyError("Missing column: stiff_ok")
        d = d[d["stiff_ok"].fillna(False).astype(bool)].copy()

    has_in_band = "in_band" in d.columns
    if has_in_band:
        d["in_band"] = d["in_band"].fillna(False).astype(bool)

    if d.empty:
        raise ValueError("No data remaining after filters for breakaway.")

    hps_all = sorted(d[hp_col].unique().astype(int).tolist())
    if hp_list is None:
        hp_use = hps_all
    else:
        hp_set = set(hps_all)
        hp_use = [int(h) for h in hp_list if int(h) in hp_set]
    if not hp_use:
        raise ValueError("hp_list does not intersect with available hardpoints.")

    ylims = None
    if share_ylim:
        y = d[y_col].to_numpy(float)
        y_min = float(np.nanmin(y))
        y_max = float(np.nanmax(y))
        if include_bands_in_ylim:
            y_min = min(y_min, comp_band[0], comp_band[1], tens_band[0], tens_band[1])
            y_max = max(y_max, comp_band[0], comp_band[1], tens_band[0], tens_band[1])
        span = y_max - y_min
        pad = pad_frac * span if np.isfinite(span) and span > 0 else 1.0
        ylims = (y_min - pad, y_max + pad)

    outpath = ensure_outdir(outdir)
    figs: Dict[int, plt.Figure] = {}

    for hp in hp_use:
        sub = d[d[hp_col].astype(int) == hp].sort_values("_t")
        fig, ax = plt.subplots(figsize=(10, 4.8), constrained_layout=True)

        ax.axhspan(comp_band[0], comp_band[1], alpha=0.15, label="Compression band")
        ax.axhspan(tens_band[0], tens_band[1], alpha=0.15, label="Tension band")

        for st in states:
            ssub = sub[sub[state_col] == st]
            if ssub.empty:
                continue

            color = state_color(st)

            if show_inband_markers and has_in_band:
                inb = ssub[ssub["in_band"]]
                outb = ssub[~ssub["in_band"]]

                if not inb.empty:
                    ax.scatter(
                        inb["_t"],
                        inb[y_col],
                        s=22,
                        alpha=0.9,
                        marker="o",
                        color=color,
                        label=f"{st}",
                    )
                if not outb.empty:
                    ax.scatter(
                        outb["_t"],
                        outb[y_col],
                        s=32,
                        alpha=0.9,
                        marker="x",
                        color=color,
                        label=f"{st} outliers",
                    )
            else:
                ax.scatter(
                    ssub["_t"], ssub[y_col], s=22, alpha=0.9, color=color, label=f"{st}"
                )

        ax.set_title(
            f"HP{hp} — Breakaway force vs time since {pd.Timestamp(since).date()}"
        )
        ax.set_xlabel("Time (UTC)")
        ax.set_ylabel("Breakaway force [N]")
        ax.grid(True, alpha=0.25)
        ax.axhline(0.0, linewidth=1, alpha=0.4)
        if ylims is not None:
            ax.set_ylim(*ylims)

        ax.legend(loc="best", fontsize=9, frameon=True)

        figs[hp] = fig
        if outpath is not None:
            fig.savefig(outpath / f"{fname_prefix}_HP{hp}.png", dpi=dpi)

        if show:
            plt.show()
        else:
            plt.close(fig)

    return figs
