# python/lsst/sitcom/tn082/plots_bokeh.py

"""
Interactive Bokeh visualizations for M1M3 hardpoint analysis.

Dashboards that allow exploring stiffness and test counts by day, hardpoint, 
and state with interactive filters without needing a server.
"""

import numpy as np
import pandas as pd

from bokeh.models import ColumnDataSource, Select, MultiSelect, CustomJS, HoverTool
from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column, row
from bokeh.palettes import Category10
from bokeh.resources import CDN
from bokeh.embed import file_html


# Constants for visualization parameters
_MS_PER_DAY = 24 * 60 * 60 * 1000   # Miliseconds in a day (used for bar width).
_BAR_WIDTH_FRAC = 0.85               # Fraction of the day to use as bar width to avoid overlap.
_DEFAULT_ALPHA = 0.9                 # Opacity for visible elements (used in JS filter).
_HIDDEN_ALPHA = 0.0                  # Opacity for hidden elements in JS filter.
_SCATTER_SIZE = 7                    # Scatter size for stiffness plot.
_PALETTE = Category10[10]            # Palette for hardpoints.


def _prepare_daily_data(df_feat: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and aggregate feature data to daily level by (day, HP, state).

    Steps:
       - Convert and validate date, HP, state and stiffness columns.
       - Remove infinities and rows with NaN in key columns.
       - Group by (day, hp, state) calculating count, mean and std of stiffness.
       - Add 'day_ms' column (epoch in ms) for Bokeh datetime compatibility.
       - Initialize 'alpha' to _DEFAULT_ALPHA (used by JS filter).

    Args:
        df_feat: Features DataFrame with columns 'date', 'hp', 'state', 'stiffness_N_per_um' and 'group_id'.
    Returns:
        Daily DataFrame sorted by date with columns:
        day, hp, state, n_tests, stiff_mean, stiff_std, day_ms, alpha.

    Raises:
        ValueError: If the resulting daily DataFrame is empty after cleaning, 
        indicating issues with the input data.
    """
    dfp = df_feat.copy()
    dfp["date"] = pd.to_datetime(dfp["date"], errors="coerce")
    dfp["hp"] = dfp["hp"].astype(str)
    dfp["state"] = dfp["state"].astype(str)
    dfp["stiffness_N_per_um"] = pd.to_numeric(dfp["stiffness_N_per_um"], errors="coerce")
    dfp = dfp.replace([np.inf, -np.inf], np.nan)
    dfp = dfp.dropna(subset=["date", "hp", "state", "stiffness_N_per_um"])
    dfp["day"] = dfp["date"].dt.floor("D")

    # Select the appropriate column for counting tests: prefer 
    # 'group_id' if available, otherwise use 'stiffness_N_per_um'.
    count_col = "group_id" if "group_id" in dfp.columns else "stiffness_N_per_um"

    daily = (
        dfp.groupby(["day", "hp", "state"], as_index=False)
           .agg(
               n_tests=(count_col, "count"),
               stiff_mean=("stiffness_N_per_um", "mean"),
               stiff_std=("stiffness_N_per_um", "std"),
           )
    ).sort_values("day").reset_index(drop=True)

    if daily.empty:
        raise ValueError(
            "DataFrame was empty after cleaning. Please check that 'date', 'hp', 'state' and " \
            "'stiffness_N_per_um' have valid data."
        )

    # Epoch in milliseconds for Bokeh datetime axes compatibility
    daily["day_ms"] = (daily["day"].astype("int64") // 10**6).astype(np.int64)
    daily["alpha"] = _DEFAULT_ALPHA
    return daily


def _assign_colors(daily: pd.DataFrame, hp_list: list[str]) -> pd.DataFrame:
    """
    Asigns a Category10 color to each hardpoint.

    Args:
        daily: Daily DataFrame with 'hp' column.
        hp_list: Sort list for index-based color assignment.

    Returns:
        Daily DataFrame with added 'color' column.
    """
    hp_to_color = {hp: _PALETTE[i % len(_PALETTE)] for i, hp in enumerate(hp_list)}
    daily["color"] = daily["hp"].map(hp_to_color).fillna("grey")
    return daily


def _make_filter_widgets(
    hp_list: list[str], state_list: list[str]
) -> tuple[Select, MultiSelect]:
    """
    Creates interactive filter widgets for HP and State.

    HP widget is a simple Select with an "ALL" option to show all hardpoints.
    State widget is a MultiSelect that allows selecting multiple states.

    Args:
        hp_list: Sort list of available HPs.
        state_list: Sort list of available states.

    Returns:
        Tuple (hp_sel, st_sel) with Bokeh widgets.
    """
    hp_sel = Select(
        title="HP",
        value="ALL",
        options=["ALL"] + hp_list,
    )
    st_sel = MultiSelect(
        title="State(s)",
        value=state_list,
        options=state_list,
        size=min(6, max(3, len(state_list))),
    )
    return hp_sel, st_sel


def _make_filter_callback(
    src: ColumnDataSource, hp_sel: Select, st_sel: MultiSelect
) -> CustomJS:
    """
    Generates the JavaScript callback for filtering elements by HP and State.

    Visibility is controlled by modifying the 'alpha' column of the ColumnDataSource:
      - Elements that match the filters get alpha = 0.9 (visible).
      - The rest get alpha = 0.0 (invisible), without removing data from the source.

    This allows to maintain interactivity fluid.

    Args:
        src: ColumnDataSource shared by all renderers.
        hp_sel: HP widget Select.
        st_sel: State widget MultiSelect.

    Returns:
        CustomJS ready to connect with js_on_change.
    """
    return CustomJS(
        args=dict(src=src, hp_sel=hp_sel, st_sel=st_sel),
        code=f"""
          const d = src.data;
          const hp = hp_sel.value;
          const states = new Set(st_sel.value);
          const alpha_vis = {_DEFAULT_ALPHA};
          const alpha_hid = {_HIDDEN_ALPHA};

          for (let i = 0; i < d['alpha'].length; i++) {{
            const ok_hp = (hp === "ALL") || (d['hp'][i] === hp);
            const ok_st = states.has(d['state'][i]);
            d['alpha'][i] = (ok_hp && ok_st) ? alpha_vis : alpha_hid;
          }}
          src.change.emit();
        """,
    )


def _build_count_figure(
    src: ColumnDataSource, x_range=None
) -> tuple[figure, object]:
    """
    Constructs the daily test count bar chart.

    The width of each bar is _BAR_WIDTH_FRAC of the day to avoid overlap.
    The legend is interactive (click to hide/show by HP).

    Args:
        src: ColumnDataSource with daily data.
        x_range: Shared X range (to synchronize zoom with other plots).

    Returns:
        Tuple (figure, bar renderer).
    """
    kwargs = dict(x_range=x_range) if x_range is not None else {}
    p = figure(
        x_axis_type="datetime",
        height=240,
        sizing_mode="stretch_width",
        title="Count daily tests by HP and state",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        **kwargs,
    )

    r_bar = p.vbar(
        x="day",
        top="n_tests",
        width=int(_MS_PER_DAY * _BAR_WIDTH_FRAC),
        source=src,
        fill_color={"field": "color"},
        line_color={"field": "color"},
        fill_alpha={"field": "alpha"},
        line_alpha={"field": "alpha"},
        legend_field="hp",
    )

    p.legend.title = "HP"
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"

    p.add_tools(HoverTool(
        renderers=[r_bar],
        tooltips=[
            ("Día",     "@day{%F}"),
            ("HP",      "@hp"),
            ("Estado",  "@state"),
            ("N tests", "@n_tests"),
            ("Rigidez media", "@stiff_mean{0.00} N/µm"),
        ],
        formatters={"@day": "datetime"},
    ))

    return p, r_bar


def _build_stiffness_figure(
    src: ColumnDataSource, x_range
) -> figure:
    """
    Constructs the daily mean stiffness scatter plot.

    Shared X range with the count figure to synchronize temporal zooming.
    Legend is hidden to avoid duplicating information already visible in the upper count plot.

    Args:
        src: Shared ColumnDataSource.
        x_range: Shared X range (to synchronize zoom with count plot).

    Returns:
        Bokeh figure ready to be added to the layout.
    """
    p = figure(
        x_axis_type="datetime",
        height=360,
        sizing_mode="stretch_width",
        title="Daily mean stiffness (N/µm)",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        x_range=x_range,
    )
    p.yaxis.axis_label = "Stiffness(N/µm)"

    r_pts = p.scatter(
        "day", "stiff_mean",
        source=src,
        size=_SCATTER_SIZE,
        fill_color={"field": "color"},
        line_color={"field": "color"},
        fill_alpha={"field": "alpha"},
        line_alpha={"field": "alpha"},
        legend_field="hp",
    )

    p.legend.visible = False

    p.add_tools(HoverTool(
        renderers=[r_pts],
        tooltips=[
            ("Day",            "@day{%F}"),
            ("HP",             "@hp"),
            ("State",         "@state"),
            ("Stiffness mean",  "@stiff_mean{0.00} N/µm"),
            ("Stiffness std",    "@stiff_std{0.00} N/µm"),
            ("N tests",        "@n_tests"),
        ],
        formatters={"@day": "datetime"},
    ))

    return p

def save_dashboard_html(
    df_feat: pd.DataFrame,
    outpath: str = "~/sitcomtn-082/_static/dashboard_hardpoints.html",
) -> str:
    """
    Export dashboard as standalone HTML to embed in a technote.

    Args:
        df_feat: Features DataFrame.
        outpath: Output path for the HTML file.

    Returns:
        Path of the generated file.
    """
    layout = bokeh_daily_stiffness_dashboard(df_feat)
    html = file_html(layout, CDN, "Dashboard Hardpoints M1M3")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Dashboard saved to: {outpath}")
    return outpath

def bokeh_daily_stiffness_dashboard(df_feat: pd.DataFrame):
    """
    Stiffness and daily test count interactive dashboard with Bokeh.

    Generates a Bokeh layout with two synchronized plots and two filter widgets:
      - Upper plot: daily test count bars by HP and state.
      - Lower plot: daily mean stiffness scatter (N/µm).
      - HP filter: Simple Select with "ALL" option to show all hardpoints.
      - State filter: MultiSelect to choose one or more test states.    

    The filters operate through a CustomJS that modifies the 'alpha' column of the shared ColumnDataSource, 
    allowing to show/hide elements without needing a Python server (standalone HTML).

    Range selection (zoom) in the X axis is synchronized between both plots, 
    facilitating temporal analysis of counts and stiffness together.

    Args:
        df_feat: Features DataFrame with columns:
                 'date', 'hp', 'state', 'stiffness_N_per_um' and 'group_id'.

    Returns:
        Bokeh column layout ready for show() or save() as standalone HTML.

    Raises:
        ValueError: If the DataFrame is empty after data cleaning.
    """
    daily = _prepare_daily_data(df_feat)

    hp_list = sorted(daily["hp"].unique().tolist())
    state_list = sorted(daily["state"].unique().tolist())

    daily = _assign_colors(daily, hp_list)
    src = ColumnDataSource(daily)

    hp_sel, st_sel = _make_filter_widgets(hp_list, state_list)
    cb = _make_filter_callback(src, hp_sel, st_sel)
    hp_sel.js_on_change("value", cb)
    st_sel.js_on_change("value", cb)

    p_count, _ = _build_count_figure(src)
    p_stiff = _build_stiffness_figure(src, x_range=p_count.x_range)

    return column(
        row(hp_sel, st_sel),
        p_count,
        p_stiff,
        sizing_mode="stretch_width",
    )
