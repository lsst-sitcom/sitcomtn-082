# python/lsst/sitcom/tn082/scan_status.py

"""
Scan M1M3's Harpoints test.

Identify time intervals when tests were executed, 
aligning EFD commands with actual system states to define 
precise start and end windows per activity group.
"""

import os
import numpy as np
import pandas as pd
from astropy.time import Time

from lsst.sitcom.tn082.utils import (
    ensure_utc_index,
    today_utc_str,
    chunk_ranges_utc,
    group_by_gaps,
    ensure_dir,
)
from lsst.summit.utils.efdUtils import makeEfdClient
from lsst.ts.xml.enums.MTM1M3 import HardpointTest


BASE_TOPIC = "lsst.sal.MTM1M3"
N_HP = 6

# Define active states of the HardpointTest enum as a frozenset for efficient membership testing.
ACTIVE_STATES_DEFAULT: frozenset = frozenset({
    int(HardpointTest.MOVINGNEGATIVE),
    int(HardpointTest.TESTINGPOSITIVE),
    int(HardpointTest.TESTINGNEGATIVE),
})


async def fetch_test_commands_range(
    efd_client, t0: pd.Timestamp, t1: pd.Timestamp
) -> pd.DataFrame:
    """
    Download hardpoint test command starts in the range [t0, t1].

    Consult the 'command_testHardpoint' topic of the EFD and return the actuator involved in each command. 
    Returns an empty DataFrame if there are no data.

    Args:
        efd_client: EFD client instance.
        t0: Window start timestamp (UTC).
        t1: Window end timestamp (UTC).

    Returns:
        DataFrame with column 'hardpointActuator' and UTC index.
    """
    df = await efd_client.select_time_series(
        topic_name=f"{BASE_TOPIC}.command_testHardpoint",
        fields=["hardpointActuator"],
        start=Time(t0.to_pydatetime(), scale="utc"),
        end=Time(t1.to_pydatetime(), scale="utc"),
    )
    if df is None or df.empty:
        return pd.DataFrame()
    return ensure_utc_index(df)


async def fetch_test_status_range(
    efd_client, t0: pd.Timestamp, t1: pd.Timestamp
) -> pd.DataFrame:
    """
    Download the test status of each hardpoint in the range [t0, t1].

    Consult the 'logevent_hardpointTestStatus' topic of the EFD. The states
    correspond to the values of the HardpointTest enum (e.g. MOVINGNEGATIVE).

    Args:
        efd_client: EFD client instance.
        t0: Window start timestamp (UTC).
        t1: Window end timestamp (UTC).

    Returns:
        DataFrame with columns 'testState0'..'testState5' and UTC index.
    """
    df = await efd_client.select_time_series(
        topic_name=f"{BASE_TOPIC}.logevent_hardpointTestStatus",
        fields=[f"testState{i}" for i in range(N_HP)],
        start=Time(t0.to_pydatetime(), scale="utc"),
        end=Time(t1.to_pydatetime(), scale="utc"),
    )
    if df is None or df.empty:
        return pd.DataFrame()
    return ensure_utc_index(df)


def align_to_status_index(
    sts: pd.DataFrame, t_ref: pd.Timestamp
) -> pd.Timestamp | None:
    """
    Find the first timestamp in the status DataFrame index that is >= t_ref.

    Use this to align the reference time of a command with the actual index of the 
    status DataFrame, which may have a different resolution.

    Args:
        sts: States dataframe with UTC DatetimeIndex.
        t_ref: Reference time to align (UTC).

    Returns:
        First timestamp in the index of 'sts' that is >= t_ref, or None if it doesn't exist.
    """
    if sts is None or sts.empty:
        return None
    t_ref = pd.Timestamp(t_ref)
    if t_ref.tzinfo is None:
        t_ref = t_ref.tz_localize("UTC")
    else:
        t_ref = t_ref.tz_convert("UTC")

    pos = sts.index.searchsorted(t_ref, side="left")
    if pos >= len(sts.index):
        return None
    return sts.index[pos]


def compute_end_time_from_status(
    sts: pd.DataFrame,
    start_time: pd.Timestamp,
    hp_indices: list[int],
    *,
    active_states=None,
    max_duration: str = "35min",
    sample: str = "1s",
    end_buffer: str = "10s",
) -> pd.Timestamp | None:
    """
    Determine the end time of a test based on the actual states from the EFD.

    Resample the states at the 'sample' interval, identify the last instant when any hardpoint 
    was active, and add 'end_buffer' as a margin at the end. The search is limited to 'max_duration' 
    from 'start_time' to avoid excessively long windows.

    Detection of active states is vectorized with 'isin()' for efficiency.

    Args:
        sts: States dataframe with UTC index.
        start_time: Test beginning.
        hp_indices: Hardpoints index to monitor (0-based). 
        active_states: Set of int values corresponding to active states in the HardpointTest enum.
                       Use ACTIVE_STATES_DEFAULT for default.
        max_duration: Maxime duration to search forward from start_time.
        sample: Resolution of the resampling to detect the end.
        end_buffer: Extra margen added to the last active instant.

    Returns:
        Estimate end time of the test, or None if no activity was detected.
    """
    if sts is None or sts.empty:
        return None

    active_states = ACTIVE_STATES_DEFAULT if active_states is None else frozenset(int(x) for x in active_states)
    cols = [f"testState{i}" for i in hp_indices if f"testState{i}" in sts.columns]
    if not cols:
        return None

    start_time = pd.Timestamp(start_time)
    start_time = (
        start_time.tz_localize("UTC") if start_time.tzinfo is None
        else start_time.tz_convert("UTC")
    )

    t_end_search = start_time + pd.Timedelta(max_duration)
    df = sts.loc[
        (sts.index >= (start_time - pd.Timedelta("5s"))) & (sts.index <= t_end_search),
        cols,
    ].copy()
    if df.empty:
        return None

    # Convert to numeric, coercing errors to NaN, and resample to ensure a uniform time grid for detection.
    df = df.apply(pd.to_numeric, errors="coerce")
    df_rs = df.resample(sample).ffill()
    df_rs = df_rs.loc[df_rs.index >= start_time]
    if df_rs.empty:
        return None

    # Detection vectorized: True if any column contains an active state.
    # isin() ignore NaN automatically and is O(n) instead of O(n * m) with apply.
    is_active = df_rs.isin(active_states).any(axis=1)

    if not is_active.any():
        return None

    last_active = is_active[is_active].index.max()
    return last_active + pd.Timedelta(end_buffer)


async def scan_days_with_tests_real_status(
    start_date: str = "2023-01-01",
    end_date: str | None = None,
    *,
    chunk_days: int = 31,
    overlap_hours: int = 2,
    group_gap: str = "3min",
    max_duration: str = "35min",
    sample: str = "1s",
    end_buffer: str = "10s",
    outdir: str = os.path.expanduser("~/breakaway_scan_real"),
    save_csv: bool = True,
    overwrite: bool = False,
    debug: bool = False,
    efd_name: str = "usdf_efd",
):
    """
    EFD scan for hardpoint tests, generating summary tables by groups and days.

    For each temporal chunk:
      1. Download test commands and actual EFD states.
      2. Group commands by time gaps ('group_gap').
      3. Align each group with the status index and determine the real test window.
      4. Deduplicate already processed windows with 'seen'. 

    If the output CSVs already exist and 'overwrite=False', it loads them directly.

    Args:
        start_date: Start date of the scan (format 'YYYY-MM-DD').
        end_date: End date of the scan (default: today UTC).
        chunk_days: Size of each query chunk in days.
        overlap_hours: Overlap between chunks to avoid missing events at borders.
        group_gap: Minimum gap between commands to start a new group.
        max_duration: Maximum estimated duration of a test (search window).
        sample: Resolution for resampling to detect test end.
        end_buffer: Extra margen added to the last active instant.
        outdir: Directory where the output CSVs will be saved.
        save_csv: If True, saves the results to disk. If False, only returns the DataFrames.
        overwrite: If True, recompute even if CSVs already exist.
        debug: If True prints progress to console.
        efd_name: EFD client name to instantiate.

    Returns:
        Tuple (df_days, df_groups) with summaries by day and by test group.
    """
    if end_date is None:
        end_date = today_utc_str()

    ensure_dir(outdir)
    p_days = os.path.join(outdir, f"days_with_tests_status_{start_date}_to_{end_date}.csv")
    p_groups = os.path.join(outdir, f"groups_with_tests_status_{start_date}_to_{end_date}.csv")

    if save_csv and (not overwrite) and os.path.exists(p_days) and os.path.exists(p_groups):
        if debug:
            print("Loading CSVs existing:")
            print(" -", p_days)
            print(" -", p_groups)
        return pd.read_csv(p_days), pd.read_csv(p_groups)

    efd_client = makeEfdClient(efd_name)

    start = pd.Timestamp(f"{start_date} 00:00:00", tz="UTC")
    end   = pd.Timestamp(f"{end_date} 23:59:59", tz="UTC")

    if debug:
        print(f"Scan with status: {start} -> {end}")

    group_rows = []
    seen = set()  # Avoid duplicates across chunks (t0, t1, hp_indices). 

    for chunk_start, chunk_end in chunk_ranges_utc(start, end, days=chunk_days, overlap_hours=overlap_hours):
        if debug:
            print(f"\nChunk: {chunk_start} -> {chunk_end}")

        cmd = await fetch_test_commands_range(efd_client, chunk_start, chunk_end)
        if cmd.empty:
            continue

        sts = await fetch_test_status_range(efd_client, chunk_start, chunk_end)
        if sts.empty:
            if debug:
                print(" Empty status data for this chunk, skipping.")
            continue

        cmd = group_by_gaps(cmd, group_gap)

        #Sumarize commands by group_id: reference time, number of commands and unique HPs.
        gsum = (
            cmd.reset_index()
               .groupby("group_id")
               .agg(
                   reference_time=("index", "min"),
                   n_cmds=("group_id", "size"),
                   #Optimized: sorted unique values directly from the Series without creating a new one in the lambda.
                   uniq_hp=("hardpointActuator", lambda s: sorted(s.dropna().unique())),
               )
               .reset_index()
        )

        for _, r in gsum.iterrows():
            g_id = int(r["group_id"])
            t_ref = pd.Timestamp(r["reference_time"])
            t_ref = t_ref.tz_localize("UTC") if t_ref.tzinfo is None else t_ref.tz_convert("UTC")

            uniq_hp = r["uniq_hp"] if isinstance(r["uniq_hp"], list) else []
            hp_indices = (
                [int(hp) - 1 for hp in uniq_hp if 1 <= int(hp) <= N_HP]
                or list(range(N_HP))
            )

            # Aling the command reference time with the status index to find the actual start time of the test.
            t0 = align_to_status_index(sts, t_ref)
            if t0 is None:
                continue

            t1 = compute_end_time_from_status(
                sts=sts, start_time=t0, hp_indices=hp_indices,
                max_duration=max_duration, sample=sample, end_buffer=end_buffer,
            )
            if t1 is None or t1 <= t0:
                continue

            key = (t0, t1, tuple(hp_indices))
            if key in seen:
                continue
            seen.add(key)

            group_rows.append({
                "date": t0.strftime("%Y-%m-%d"),
                "group_id": g_id,
                "t_start_utc": t0,
                "t_end_utc": t1,
                "duration_s": (t1 - t0).total_seconds(),
                "n_cmds": int(r["n_cmds"]),
                "uniq_hp": ",".join(map(str, uniq_hp)) if isinstance(uniq_hp, list) else str(uniq_hp),
                "hp_indices": ",".join(str(i) for i in hp_indices),
            })

    if not group_rows:
        return pd.DataFrame(), pd.DataFrame()

    df_groups = (
        pd.DataFrame(group_rows)
        .sort_values(["date", "t_start_utc"])
        .reset_index(drop=True)
    )

    df_days = (
        df_groups.groupby("date")
        .agg(
            n_groups=("group_id", "nunique"),
            total_duration_s=("duration_s", "sum"),
            mean_duration_s=("duration_s", "mean"),
            first_test_utc=("t_start_utc", "min"),
            last_test_utc=("t_end_utc", "max"),
            n_cmds=("n_cmds", "sum"),
        )
        .reset_index()
        .sort_values("date")
        .reset_index(drop=True)
    )
    df_days["month"] = df_days["date"].str.slice(0, 7)
    df_days["total_duration_h"] = df_days["total_duration_s"] / 3600.0

    if save_csv:
        df_days.to_csv(p_days, index=False)
        df_groups.to_csv(p_groups, index=False)
        if debug:
            print("Saved CSV:")
            print(" -", p_days)
            print(" -", p_groups)

    return df_days, df_groups
