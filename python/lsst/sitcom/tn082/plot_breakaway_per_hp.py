# sitcomtn-082/python/lsst/sitcom/tn082/plot_breakaway_per_hp.py

"""
Breakaway force vs displacement scatter plots per hardpoint for M1M3 analysis.

Generates one figure per hardpoint showing breakaway force (N) against
displacement (µm), distinguishing test states by color and in-band vs
out-of-band points by marker style. Acceptance bands are drawn as shaded
regions with dashed boundary lines.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


# Constants

# Acceptance bands for breakaway force (N).
COMP_LIMITS = (2981, 3959)  # Compression band
TENS_LIMITS = (-4420, -3456)  # Tension band

# Default test states to include
DEFAULT_STATES = ("TESTINGPOSITIVE", "TESTINGNEGATIVE")

# Visual parameters
BAND_ALPHA = 0.12  # Shaded band transparency
BAND_LINE_LW = 1.0  # Dashed boundary line width
SCATTER_SIZE_IN = 18  # Marker size for in-band points (circles)
SCATTER_SIZE_OUT = 22  # Marker size for outliers points (crosses)
SCATTER_ALPHA_IN = 0.8
SCATTER_ALPHA_OUT = 0.9
FIG_SIZE = (6.8, 5.2)
DPI_DEFAULT = 150


# Helper functions


def filter_and_clean(
    df: pd.DataFrame,
    *,
    state_col: str,
    states: tuple[str, ...],
    stiff_ok_col: str,
    only_stiff_ok: bool,
    force_col: str,
    disp_col: str,
    in_band_col: str,
) -> pd.DataFrame:
    """
    Apply state and quality filters, convert columns to numeric, and drop invalid rows.

    Args:
        df: Raw features DataFrame.
        state_col: Column name for test state.
        states: Tuple of state names to include.
        stiff_ok_col: Column name for the stiffness quality flag.
        only_stiff_ok: If True, discard rows with stiff_ok=False or NaN.
        force_col: Column name for breakaway force (N).
        disp_col: Column name for breakaway displacement (µm).
        in_band_col: Column name for the in-band boolean flag.

    Returns:
        Cleaned copy of the DataFrame ready for plotting.

    """
    d = df.copy()
    d = d[d[state_col].isin(set(states))]

    if only_stiff_ok:
        d = d[d[stiff_ok_col].fillna(False).astype(bool)]

    d[force_col] = pd.to_numeric(d[force_col], errors="coerce")
    d[disp_col] = pd.to_numeric(d[disp_col], errors="coerce")
    d = d[np.isfinite(d[force_col]) & np.isfinite(d[disp_col])]

    # Treat NaN in_band as False to avoid dropping valid rows
    d[in_band_col] = d[in_band_col].fillna(False).astype(bool)

    if d.empty:
        raise ValueError(
            "No data remaining after filtering and cleaning. "
            "Check state selection, stiff_ok flag, and force/displacement columns."
        )
    return d


def draw_acceptance_bands(ax: plt.Axes) -> None:
    """
    Draw shaded acceptance bands and dashed boundary lines on the given axes.

    Compression band (COMP_LIMITS) and tension band (TENS_LIMITS) are drawn
    as semi-transparent horizontal spans with dashed boundary lines at each limit.

    """
    for lo, hi in (COMP_LIMITS, TENS_LIMITS):
        ax.axhspan(lo, hi, alpha=BAND_ALPHA, color="tab:blue")
        for y in (lo, hi):
            ax.axhline(
                y, linestyle="--", linewidth=BAND_LINE_LW, color="tab:blue", alpha=0.5
            )


def scatter_state(
    ax: plt.Axes,
    sub_state: pd.DataFrame,
    *,
    state: str,
    color: str,
    force_col: str,
    disp_col: str,
    in_band_col: str,
) -> None:
    """
    Plot in-band (circles) and out-of-band (crosses) points for a single state.

    In-band points use marker='o' to indicate nominal behavior.
    Out-of-band points use marker='x' to flag potential outliers.

    Args:
        force_col: Breakaway force column name.
        disp_col: Breakaway displacement column name.
    """
    inb = sub_state[sub_state[in_band_col]]
    if not inb.empty:
        ax.scatter(
            inb[disp_col],
            inb[force_col],
            marker="o",
            s=SCATTER_SIZE_IN,
            label=state,
            color=color,
            alpha=SCATTER_ALPHA_IN,
        )

    outb = sub_state[~sub_state[in_band_col]]
    if not outb.empty:
        ax.scatter(
            outb[disp_col],
            outb[force_col],
            marker="x",
            s=SCATTER_SIZE_OUT,
            label=f"{state} - outliers",
            color=color,
            alpha=SCATTER_ALPHA_OUT,
        )


# Main function


def plot_breakaway_per_hp(
    df: pd.DataFrame,
    *,
    hp_col: str = "hp",
    state_col: str = "state",
    in_band_col: str = "in_band",
    force_col: str = "breakaway_force_N",
    disp_col: str = "breakaway_disp_um",
    states: tuple[str, ...] = DEFAULT_STATES,
    only_stiff_ok: bool = True,
    stiff_ok_col: str = "stiff_ok",
    show: bool = True,
    save_png: bool = False,
    output_dir: str = "outputs",
    dpi: int = DPI_DEFAULT,
) -> dict[int, str | Figure]:
    """
    Generate one breakaway force vs displacement scatter plot per hardpoint.

    For each HP, the figure shows:
      - Shaded acceptance bands for compression (COMP_LIMITS) and
        tension (TENS_LIMITS) with dashed boundary lines.
      - In-band points (in_band=True) as filled circles ('o').
      - Out-of-band points (in_band=False) as crosses ('x').

    """
    d = filter_and_clean(
        df,
        state_col=state_col,
        states=states,
        stiff_ok_col=stiff_ok_col,
        only_stiff_ok=only_stiff_ok,
        force_col=force_col,
        disp_col=disp_col,
        in_band_col=in_band_col,
    )

    if save_png:
        os.makedirs(output_dir, exist_ok=True)

    color_map = {st: f"C{i}" for i, st in enumerate(states)}

    outputs: dict[int, str | Figure] = {}

    for hp, sub_hp in d.groupby(hp_col):
        fig, ax = plt.subplots(figsize=FIG_SIZE, constrained_layout=True)

        # Draw acceptance bands before data points so bands appear behind markers
        draw_acceptance_bands(ax)

        for st in states:
            sub_state = sub_hp[sub_hp[state_col] == st]
            if sub_state.empty:
                continue
            scatter_state(
                ax,
                sub_state,
                state=st,
                color=color_map[st],
                force_col=force_col,
                disp_col=disp_col,
                in_band_col=in_band_col,
            )

        ax.set_title(f"HP{int(hp)}: Breakaway force vs displacement")
        ax.set_xlabel("Displacement (µm)")
        ax.set_ylabel("Force (N)")
        ax.grid(True, alpha=0.25)
        ax.legend(fontsize=9, ncol=1)

        if save_png:
            state_tag = "_".join(states)
            fname = f"HP{int(hp)}_breakaway_{state_tag}.png"
            path = os.path.join(output_dir, fname)
            fig.savefig(path, dpi=dpi, bbox_inches="tight")
            plt.close(fig)
            outputs[int(hp)] = path
        else:
            outputs[int(hp)] = fig
            if show:
                plt.show()
            else:
                plt.close(fig)

    return outputs
