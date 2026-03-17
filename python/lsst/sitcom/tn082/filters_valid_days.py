# python/lsst/sitcom/tn082/filters_valid_days.py

""""
Complete pipeline to filter valid days based on physical criteria and state combinations.
""""

from __future__ import annotations

import pandas as pd


VALID_STATES = ("TESTINGPOSITIVE", "TESTINGNEGATIVE")


def to_datetime(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """
    To convert specified columns to datetime.
    """
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = pd.to_datetime(out[c], errors="coerce")
    return out


def ensure_date_column(
    df: pd.DataFrame,
    date_col: str = "date",
    t_start_col: str = "t_start_utc",
) -> pd.DataFrame:
    """
    To ensure a 'date' column of type datetime-normalized exists.
    If not, it creates it from 't_start_utc'.
    """
    out = df.copy()

    if date_col in out.columns:
        out[date_col] = pd.to_datetime(out[date_col], errors="coerce").dt.normalize()
    elif t_start_col in out.columns:
        out[date_col] = pd.to_datetime(out[t_start_col], errors="coerce").dt.normalize()
    else:
        raise ValueError(
            f"No exist '{date_col}' or '{t_start_col}' for to create the date column."
        )

    return out


def basic_physical_filter(
    df: pd.DataFrame,
    *,
    elevation_min: float = 20.0,
    stiffness_min: float = 1.0,
    elevation_col: str = "elevation_deg",
    stiffness_col: str = "stiffness_N_per_um",
    stiff_ok_col: str = "stiff_ok",
) -> pd.DataFrame:
    """
    Basic filter:
    - elevation > elevation_min
    - stiffness > stiffness_min
    - stiff_ok == True
    """
    out = df.copy()

    # Assure numeric types for filtering
    out[elevation_col] = pd.to_numeric(out[elevation_col], errors="coerce")
    out[stiffness_col] = pd.to_numeric(out[stiffness_col], errors="coerce")

    if stiff_ok_col in out.columns:
        stiff_mask = out[stiff_ok_col].fillna(False).astype(bool)
    else:
        stiff_mask = True

    mask = (
        out[elevation_col].gt(elevation_min)
        & out[stiffness_col].gt(stiffness_min)
        & stiff_mask
    )

    return out.loc[mask].copy()


def keep_only_testing_states(
    df: pd.DataFrame,
    *,
    state_col: str = "state",
    valid_states: tuple[str, str] = VALID_STATES,
) -> pd.DataFrame:
    """
    Let's keep only rows where 'state' is in valid_states.
    """
    out = df.copy()
    return out.loc[out[state_col].isin(valid_states)].copy()


def find_valid_days_all_6hp_both_states(
    df: pd.DataFrame,
    *,
    date_col: str = "date",
    hp_col: str = "hp",
    state_col: str = "state",
    valid_states: tuple[str, str] = VALID_STATES,
    required_hps: tuple[int, ...] = (1, 2, 3, 4, 5, 6),
) -> pd.DataFrame:
    """
    Found valid days where, after physical filtering:
    - all 6 HPs are present
    - each HP has both states: TESTINGPOSITIVE and TESTINGNEGATIVE

    Returns a DataFrame summary by day with:
    - date
    - n_pairs_ok
    - is_valid_day
    """
    out = df.copy()

    # Blend of groupby and drop_duplicates to find unique date-hp-state combinations
    pairs = out[[date_col, hp_col, state_col]].dropna().drop_duplicates()

    # Count unique states per date-hp pair
    states_per_hp = (
        pairs.groupby([date_col, hp_col])[state_col]
        .nunique()
        .reset_index(name="n_states")
    )

    states_per_hp["hp_ok"] = states_per_hp["n_states"].eq(len(valid_states))

    # Kept only date-hp pairs that have both states
    states_per_hp = states_per_hp[states_per_hp[hp_col].isin(required_hps)].copy()

    # For day summary, we need to know:
    day_summary = (
        states_per_hp.groupby(date_col)
        .agg(
            n_hps_present=(hp_col, "nunique"),
            n_pairs_ok=("hp_ok", "sum"),
        )
        .reset_index()
    )

    day_summary["is_valid_day"] = day_summary["n_hps_present"].eq(
        len(required_hps)
    ) & day_summary["n_pairs_ok"].eq(len(required_hps))

    return day_summary.sort_values(date_col).reset_index(drop=True)


def filter_valid_days_all_6hp_both_states(
    df: pd.DataFrame,
    *,
    elevation_min: float = 20.0,
    stiffness_min: float = 1.0,
    date_col: str = "date",
    t_start_col: str = "t_start_utc",
    hp_col: str = "hp",
    state_col: str = "state",
    elevation_col: str = "elevation_deg",
    stiffness_col: str = "stiffness_N_per_um",
    stiff_ok_col: str = "stiff_ok",
    valid_states: tuple[str, str] = VALID_STATES,
    required_hps: tuple[int, ...] = (1, 2, 3, 4, 5, 6),
    return_day_summary: bool = False,
) -> pd.DataFrame | tuple[pd.DataFrame, pd.DataFrame]:
    """
    Complete pipeline:
    1. Assure date column exists
    2. Keep only rows with state in valid_states
    3. Elevation filter > 20
    4. Stiffness filter > 1
    5. Stiff_ok filter == True
    6. Keep only days that have:
       - 6 HP
       - HP with both states

    Returns:
    - df_filter
    or
    - (df_filter, day_summary) if return_day_summary=True
    """
    out = df.copy()

    out = to_datetime(out, [t_start_col, "t_end_utc", "breakaway_time_utc"])
    out = ensure_date_column(out, date_col=date_col, t_start_col=t_start_col)
    out = keep_only_testing_states(out, state_col=state_col, valid_states=valid_states)
    out = basic_physical_filter(
        out,
        elevation_min=elevation_min,
        stiffness_min=stiffness_min,
        elevation_col=elevation_col,
        stiffness_col=stiffness_col,
        stiff_ok_col=stiff_ok_col,
    )

    day_summary = find_valid_days_all_6hp_both_states(
        out,
        date_col=date_col,
        hp_col=hp_col,
        state_col=state_col,
        valid_states=valid_states,
        required_hps=required_hps,
    )

    valid_days = set(day_summary.loc[day_summary["is_valid_day"], date_col])

    out_valid = out.loc[out[date_col].isin(valid_days)].copy()
    out_valid = out_valid.sort_values([date_col, hp_col, state_col, t_start_col])

    if return_day_summary:
        return out_valid, day_summary

    return out_valid


def summarize_valid_days(
    df_valid: pd.DataFrame,
    *,
    date_col: str = "date",
    hp_col: str = "hp",
    state_col: str = "state",
) -> pd.DataFrame:
    """
    Return a summary of the valid days DataFrame, counting rows per date-hp-state combination.
    """
    summary = (
        df_valid.groupby([date_col, hp_col, state_col])
        .size()
        .reset_index(name="n_rows")
        .sort_values([date_col, hp_col, state_col])
        .reset_index(drop=True)
    )
    return summary
