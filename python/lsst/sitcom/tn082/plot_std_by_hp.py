# python/lsst/sitcom/tn082/plot_std_by_hp.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Status color palette — consistent with HardpointTest enum across the codebase
STATUS_COLORS = {
    "NOTTESTED": "lightgrey",
    "MOVINGNEGATIVE": "lightsteelblue",
    "TESTINGPOSITIVE": "forestgreen",
    "TESTINGNEGATIVE": "royalblue",
    "MOVINGREFERENCE": "darkseagreen",
    "PASSED": "dimgrey",
    "FAILED": "red",
}


def plot_std_by_hp_bar(
    df,
    *,
    value_col="stiffness_N_per_um",
    states=("TESTINGPOSITIVE", "TESTINGNEGATIVE"),
    only_in_band=None,
    only_stiff_ok=True,
    only_valid_days=True,  # Filter rows where valid_day == True
    since="2025-01-01",  # Earliest date to include (ISO format, inclusive)
    savepath=None,
    show=True,
):
    """
    Bar chart of stiffness std per hardpoint, split by state.

    Args:
        df:             Features DataFrame with columns 'hp', 'state',
                        'stiffness_N_per_um', 'stiff_ok', 'in_band',
                        'valid_day', and 'date'.
        value_col:      Column to compute std on.
        states:         States to include.
        only_in_band:   True → keep only in-band rows; False → out-of-band only;
                        None → no filter.
        only_stiff_ok:  If True, drop rows where stiff_ok is False/NaN.
        only_valid_days: If True, keep only rows where valid_day is True.
        since:          Drop rows whose date is earlier than this ISO string.
        savepath:       Path to save PNG (None → do not save).
        show:           If True, call plt.show().

    Returns:
        Tuple (fig, g) where g is the grouped std DataFrame (hp × state).
    """
    d = df.copy()

    # Date filter
    d["date"] = pd.to_datetime(d["date"], errors="coerce").dt.normalize()
    since_ts = pd.Timestamp(since).normalize()
    d = d[d["date"] >= since_ts]

    d = d[d["stiffness_N_per_um"] > 1].copy()

    # Valid-day filter
    if only_valid_days:
        if "valid_day" not in d.columns:
            raise KeyError("Column 'valid_day' not found. Run filter_valid_days first.")
        d = d[d["valid_day"].fillna(False).astype(bool)]

    # State filter
    d = d[d["state"].isin(states)]

    # Quality filters
    if only_stiff_ok:
        d = d[d["stiff_ok"].fillna(False).astype(bool)]

    if only_in_band is not None:
        band = d["in_band"].fillna(False).astype(bool)
        d = d[band] if only_in_band else d[~band]

    # Coerce value column
    d[value_col] = pd.to_numeric(d[value_col], errors="coerce")
    d = d[d[value_col].notna()]

    if d.empty:
        raise ValueError("No data remaining after filters.")

    #  Aggregate: std per (hp, state)
    g = d.groupby(["hp", "state"])[value_col].std().unstack("state").sort_index()

    # Plot
    fig, ax = plt.subplots(figsize=(8, 4), constrained_layout=True)
    x = np.arange(len(g.index))
    n_states = len(states)
    width = 0.8 / n_states
    offsets = np.linspace(-(n_states - 1) / 2, (n_states - 1) / 2, n_states) * width

    for offset, state in zip(offsets, states):
        if state not in g.columns:
            continue
        ax.bar(
            x + offset,
            g[state],
            width=width,
            label=state,
            color=STATUS_COLORS.get(state, "grey"),  # canonical status color
        )

    ax.set_xticks(x)
    ax.set_xticklabels([f"HP{int(h)}" for h in g.index])
    ax.set_xlabel("Hardpoint")
    ax.set_ylabel("Std (N/µm)")
    ax.set_title(f"Stiffness std by HP — valid days since {since}")
    ax.legend(fontsize=9, frameon=True)

    # Save
    if savepath is not None:
        os.makedirs(os.path.dirname(os.path.abspath(savepath)), exist_ok=True)
        fig.savefig(savepath, dpi=150)
        print(f"Saved figure to {savepath}")

    if show:
        plt.show()

    return fig, g
