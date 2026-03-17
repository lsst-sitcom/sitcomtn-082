# python/lsst/sitcom/tn082/plot_bokeh_gauss.py

from __future__ import annotations

import numpy as np
import pandas as pd

from bokeh.models import ColumnDataSource, Select, CustomJS, HoverTool, Div
from bokeh.plotting import figure
from bokeh.layouts import column, row


# Define a robust normal PDF
def normal_pdf(x: np.ndarray, mu: float, sigma: float) -> np.ndarray:
    if (not np.isfinite(mu)) or (not np.isfinite(sigma)) or sigma <= 0:
        return np.full_like(x, np.nan, dtype=float)
    return (1.0 / (sigma * np.sqrt(2.0 * np.pi))) * np.exp(
        -0.5 * ((x - mu) / sigma) ** 2
    )


# Prepare DataFrame: clean, filter, bin elevation
def prep_df_for_gauss(
    df_feat: pd.DataFrame,
    *,
    states: list[str] | None = None,
) -> pd.DataFrame:
    dfp = df_feat.copy()

    required = ["hp", "state", "stiffness_N_per_um", "elevation_deg"]
    missing = [c for c in required if c not in dfp.columns]
    if missing:
        raise ValueError(f"Missing required columns in df_feat: {missing}")

    dfp["hp"] = pd.to_numeric(dfp["hp"], errors="coerce")
    dfp["state"] = dfp["state"].astype(str)
    dfp["stiffness_N_per_um"] = pd.to_numeric(
        dfp["stiffness_N_per_um"], errors="coerce"
    )
    dfp["elevation_deg"] = pd.to_numeric(dfp["elevation_deg"], errors="coerce")

    dfp = dfp.replace([np.inf, -np.inf], np.nan)
    dfp = dfp.dropna(
        subset=["hp", "state", "stiffness_N_per_um", "elevation_deg"]
    ).copy()

    if states is not None:
        dfp = dfp[dfp["state"].isin(states)].copy()

    # HP as string (for easy JS matching later)
    dfp["hp"] = dfp["hp"].astype(int).astype(str)
    dfp["state"] = dfp["state"].astype(str)

    return dfp


def bokeh_stiffness_gaussian_by_elevation(
    df_feat: pd.DataFrame,
    *,
    el_bin_w: int = 5,
    hist_bins: int = 40,
    clip_percentiles: tuple[float, float] = (1, 99),
    min_n_fit: int = 10,
    states: list[str] | None = None,
    title: str = "Stiffness distribution with normal fit",
):
    """
    Create a Bokeh layout (standalone) with:
      - stiffness histogram (density)
      - Normal fit curve (mu, sigma) for the selected subset
      - selectors: HP, State, Elevation-bin
    """
    dfp = prep_df_for_gauss(df_feat, states=states)

    # Bin elevation into discrete bins of width el_bin_w (e.g., 0-5, 5-10, etc.)
    w = int(el_bin_w)
    dfp["el_bin_lo"] = np.floor(dfp["elevation_deg"].to_numpy(float) / w) * w
    dfp["el_bin_lo"] = (
        pd.Series(dfp["el_bin_lo"], index=dfp.index).round().astype("Int64")
    )
    dfp["el_bin_hi"] = (dfp["el_bin_lo"] + w).astype("Int64")
    dfp["el_bin_label"] = (
        dfp["el_bin_lo"].astype(str) + "-" + dfp["el_bin_hi"].astype(str)
    )
    dfp = dfp[dfp["el_bin_label"] != "<NA>-<NA>"].copy()

    hp_list = sorted(dfp["hp"].unique().tolist())
    state_list = sorted(dfp["state"].unique().tolist())
    bins_available = sorted(dfp["el_bin_label"].unique().tolist())

    if not hp_list or not state_list or not bins_available:
        raise ValueError("No data left after cleaning/bins. Check inputs and filters.")

    # Stiffness range for histogram and PDF: clip by global percentiles to avoid extreme outliers dominating the plot
    x_all = dfp["stiffness_N_per_um"].to_numpy(float)
    p_lo, p_hi = clip_percentiles
    x_min, x_max = np.nanpercentile(x_all, [p_lo, p_hi]).astype(float)
    if not np.isfinite(x_min) or not np.isfinite(x_max) or x_max <= x_min:
        raise ValueError("Invalid stiffness range after percentile clipping.")

    hist_edges = np.linspace(x_min, x_max, int(hist_bins) + 1)
    hist_left = hist_edges[:-1]
    hist_right = hist_edges[1:]
    pdf_x = np.linspace(x_min, x_max, 250)

    # Precompute ALL histograms and normal fits for every (hp, elevation_bin, state) combination to enable fast JS filtering later.
    # This is a bit more memory intensive but makes the interactive experience smooth without Python callbacks.
    hist_rows = {
        "hp": [],
        "el_bin_label": [],
        "state": [],
        "left": [],
        "right": [],
        "top": [],
    }
    pdf_rows = {"hp": [], "el_bin_label": [], "state": [], "x": [], "y": []}
    stat_rows = {
        "hp": [],
        "el_bin_label": [],
        "state": [],
        "n": [],
        "mu": [],
        "sigma": [],
    }

    for (hp, lab, st), sub in dfp.groupby(["hp", "el_bin_label", "state"], sort=False):
        # convert to str for JS matching (also handles Int64 and categorical)
        hp = str(hp)
        lab = str(lab)
        st = str(st)

        x = sub["stiffness_N_per_um"].to_numpy(float)
        x = x[np.isfinite(x)]
        x = x[(x >= x_min) & (x <= x_max)]
        n = int(len(x))

        if n < 1:
            continue

        mu = float(np.mean(x)) if n >= 1 else np.nan
        sigma = float(np.std(x, ddof=1)) if n >= 2 else np.nan

        # Histogram (density) - only if enough points to be meaningful
        if n >= max(3, min_n_fit):
            h, _ = np.histogram(x, bins=hist_edges, density=True)
            for L, R, T in zip(hist_left, hist_right, h):
                hist_rows["hp"].append(hp)
                hist_rows["el_bin_label"].append(lab)
                hist_rows["state"].append(st)
                hist_rows["left"].append(float(L))
                hist_rows["right"].append(float(R))
                hist_rows["top"].append(float(T))

        # Normally distributed PDF curve (even if n is small, but sigma must be > 0)
        ypdf = normal_pdf(pdf_x, mu, sigma)
        for xx, yy in zip(pdf_x, ypdf):
            pdf_rows["hp"].append(hp)
            pdf_rows["el_bin_label"].append(lab)
            pdf_rows["state"].append(st)
            pdf_rows["x"].append(float(xx))
            pdf_rows["y"].append(float(yy))

        stat_rows["hp"].append(hp)
        stat_rows["el_bin_label"].append(lab)
        stat_rows["state"].append(st)
        stat_rows["n"].append(n)
        stat_rows["mu"].append(mu)
        stat_rows["sigma"].append(sigma)

    src_hist_all = ColumnDataSource(hist_rows)
    src_pdf_all = ColumnDataSource(pdf_rows)
    src_stat_all = ColumnDataSource(stat_rows)

    # DataSources for the currently selected subset (initially empty, will be filled by init_current)
    src_hist = ColumnDataSource({"left": [], "right": [], "top": []})
    src_pdf = ColumnDataSource({"x": [], "y": []})
    info = Div(text="", sizing_mode="stretch_width")

    # Selectors
    hp0 = hp_list[0]
    st0 = state_list[0]
    bin0 = bins_available[0]

    hp_sel = Select(title="HP", value=hp0, options=hp_list)
    st_sel = Select(title="State", value=st0, options=state_list)
    el_sel = Select(
        title=f"Elevation bin (deg, width={w})", value=bin0, options=bins_available
    )

    # init_current (Python)
    def init_current(hp_val: str, bin_val: str, st_val: str):
        hA = src_hist_all.data
        pA = src_pdf_all.data
        sA = src_stat_all.data

        left, right, top = [], [], []
        for i in range(len(hA.get("left", []))):
            if (
                hA["hp"][i] == hp_val
                and hA["el_bin_label"][i] == bin_val
                and hA["state"][i] == st_val
            ):
                left.append(hA["left"][i])
                right.append(hA["right"][i])
                top.append(hA["top"][i])
        src_hist.data = {"left": left, "right": right, "top": top}

        xx, yy = [], []
        for i in range(len(pA.get("x", []))):
            if (
                pA["hp"][i] == hp_val
                and pA["el_bin_label"][i] == bin_val
                and pA["state"][i] == st_val
            ):
                xx.append(pA["x"][i])
                yy.append(pA["y"][i])
        src_pdf.data = {"x": xx, "y": yy}

        n = 0
        mu = np.nan
        sigma = np.nan
        for i in range(len(sA.get("hp", []))):
            if (
                sA["hp"][i] == hp_val
                and sA["el_bin_label"][i] == bin_val
                and sA["state"][i] == st_val
            ):
                n = sA["n"][i]
                mu = sA["mu"][i]
                sigma = sA["sigma"][i]
                break

        if np.isfinite(mu) and np.isfinite(sigma):
            info.text = (
                f"<b>HP={hp_val}</b> | Elev bin <b>{bin_val}°</b> | <b>{st_val}</b>"
                f" — n={n}, μ={mu:.2f}, σ={sigma:.2f}"
            )
        else:
            info.text = (
                f"<b>HP={hp_val}</b> | Elev bin <b>{bin_val}°</b> | <b>{st_val}</b>"
                f" — n={n} (σ insuffient / invalid)"
            )

    init_current(hp0, bin0, st0)

    # plot
    p = figure(
        height=430,
        sizing_mode="stretch_width",
        title=title,
        tools="pan,wheel_zoom,box_zoom,reset,save",
    )
    p.xaxis.axis_label = "stiffness (N/µm)"
    p.yaxis.axis_label = "density"
    p.grid.grid_line_alpha = 0.3

    r_bar = p.quad(
        left="left",
        right="right",
        bottom=0,
        top="top",
        source=src_hist,
        line_alpha=0.2,
        fill_alpha=0.35,
        legend_label="Histogram (density)",
    )
    r_pdf = p.line("x", "y", source=src_pdf, line_width=3, legend_label="Normal fit")

    p.add_tools(
        HoverTool(
            renderers=[r_bar],
            tooltips=[
                ("bin", "@left{0.00} – @right{0.00}"),
                ("density", "@top{0.000}"),
            ],
        )
    )
    p.legend.location = "top_right"

    # callback JS: when any selector changes, update the histogram, PDF, and stats info by filtering the precomputed data
    cb = CustomJS(
        args=dict(
            h_all=src_hist_all,
            p_all=src_pdf_all,
            s_all=src_stat_all,
            h=src_hist,
            p=src_pdf,
            hp_sel=hp_sel,
            el_sel=el_sel,
            st_sel=st_sel,
            info=info,
        ),
        code="""
        const hp = hp_sel.value;
        const lab = el_sel.value;
        const st = st_sel.value;

        // HIST
        const hA = h_all.data;
        const left = [], right = [], top = [];
        for (let i = 0; i < hA['left'].length; i++) {
          if (hA['hp'][i] === hp && hA['el_bin_label'][i] === lab && hA['state'][i] === st) {
            left.push(hA['left'][i]);
            right.push(hA['right'][i]);
            top.push(hA['top'][i]);
          }
        }
        h.data = {left:left, right:right, top:top};
        h.change.emit();

        // PDF
        const pA = p_all.data;
        const xx = [], yy = [];
        for (let i = 0; i < pA['x'].length; i++) {
          if (pA['hp'][i] === hp && pA['el_bin_label'][i] === lab && pA['state'][i] === st) {
            xx.push(pA['x'][i]);
            yy.push(pA['y'][i]);
          }
        }
        p.data = {x:xx, y:yy};
        p.change.emit();

        // STATS
        const sA = s_all.data;
        let n = 0, mu = NaN, sigma = NaN;
        for (let i = 0; i < sA['hp'].length; i++) {
          if (sA['hp'][i] === hp && sA['el_bin_label'][i] === lab && sA['state'][i] === st) {
            n = sA['n'][i];
            mu = sA['mu'][i];
            sigma = sA['sigma'][i];
            break;
          }
        }

        if (Number.isFinite(mu) && Number.isFinite(sigma) && sigma > 0) {
          info.text = `<b>HP=${hp}</b> | Elev bin <b>${lab}°</b> | <b>${st}</b> — n=${n}, μ=${mu.toFixed(2)}, σ=${sigma.toFixed(2)}`;
        } else {
          info.text = `<b>HP=${hp}</b> | Elev bin <b>${lab}°</b> | <b>${st}</b> — n=${n} (σ inválida / insuficiente)`;
        }
        """,
    )

    hp_sel.js_on_change("value", cb)
    st_sel.js_on_change("value", cb)
    el_sel.js_on_change("value", cb)

    return column(row(hp_sel, st_sel, el_sel), info, p, sizing_mode="stretch_width")
