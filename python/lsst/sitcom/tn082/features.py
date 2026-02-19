# python/lsst/sitcom/tn082/features.py

"""
Extraction of physical properties from M1M3 hardpoint test data.

For each test group identified by scan_status, it downloads force, displacement, 
and EFD states, segments by test state 
(MOVINGNEGATIVE, TESTINGPOSITIVE, TESTINGNEGATIVE) and extracts:
  - Basic statistics of force and displacement.
  - Stiffness (N/µm) via linear fit forced through the origin.
  - Breakaway force and displacement (point of detachment).
  - Elevation and azimuth angles of the mount during the test.
  - Classification of breakaway force within acceptance bands.  
"""

import os
import numpy as np
import pandas as pd
from astropy.time import Time

from lsst.summit.utils.efdUtils import makeEfdClient
from lsst.ts.xml.enums.MTM1M3 import HardpointTest

from .utils import ensure_utc_index, ensure_dir


# Constants
BASE_TOPIC = "lsst.sal.MTM1M3"
N_HP = 6           # Amount of hardpoints
M_TO_UM = 1e6      # Convertion factor: meters → micrometers

# Adjustment parameters
BREAKAWAY_DISP_UM = 1.0        # Displacement gaps (µm) to detect breakaway.
BREAKAWAY_MIN_CONSEC = 3       # Consecutive samples above threshold to confirm breakaway.
DISP_FIT_UM = 100              # Displacement window maximum (µm) for stiffness fit.
FIT_POINTS_AROUND_ZERO = 10    # Points around zero for linear fit.

# Stiffness quality filters
STIFFNESS_NEG_CLAMP_EPS = -0.5  # Small negatives [-eps, 0) rounded to 0.0.
STIFFNESS_MAX_ABS = 100.0       # Stiffness with |k| > max discard like outlier (→ NaN).

# Breakaway force bands limits in Newtons
COMP_BAND_N = (2981.0, 3959.0)   # Compression band
TENS_BAND_N = (-4420.0, -3456.0) # Tension band

# Valid states for stiffness calculation
STIFF_OK_STATES: frozenset = frozenset({
    "TESTINGPOSITIVE",
    "TESTINGNEGATIVE",
    "MOVINGNEGATIVE",
})


# EFD download functions.
async def fetch_status_window(efd_client, t0, t1) -> pd.DataFrame:
    """
    Downloads the test states of each hardpoint in the window [t0, t1].

    Consult the 'logevent_hardpointTestStatus' topic of the EFD. The states correspond
    to the values of the HardpointTest enum (MOVINGNEGATIVE, TESTINGPOSITIVE, etc.).

    Args:
        efd_client: EFD client.
        t0: Start timestamp (UTC).
        t1: End timestamp (UTC).

    Returns:
        DataFrame with columns 'testState0'..'testState5' and UTC index,
         or empty DataFrame if no data is available.
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


async def fetch_force_disp_all(efd_client, t0, t1) -> pd.DataFrame:
    """
    Downloads measured force and displacement of all hardpoints in [t0, t1].

    Displacement is converted from meters to micrometers (factor M_TO_UM). 
    The resulting columns are 'measuredForce{i}' and 'displacement{i}'.

    Args:
        efd_client: EFD client.
        t0: Start timestamp (UTC).
        t1: End timestamp (UTC).

    Returns:
        DataFrame with columns of force and displacement for the N_HP hardpoints,
        with UTC index. Displacement expressed in µm.
    """
    fields = []
    for i in range(N_HP):
        fields += [f"measuredForce{i}", f"displacement{i}"]
    df = await efd_client.select_time_series(
        f"{BASE_TOPIC}.hardpointActuatorData",
        fields,
        Time(t0.to_pydatetime(), scale="utc"),
        Time(t1.to_pydatetime(), scale="utc"),
    )
    if df is None or df.empty:
        return pd.DataFrame()
    df = ensure_utc_index(df)
    for i in range(N_HP):
        fcol = f"measuredForce{i}"
        dcol = f"displacement{i}"
        if fcol in df.columns:
            df[fcol] = pd.to_numeric(df[fcol], errors="coerce")
        if dcol in df.columns:
            df[dcol] = pd.to_numeric(df[dcol], errors="coerce") * M_TO_UM
    return df


async def fetch_el_az_window(efd_client, t0, t1) -> tuple[float, float]:
    """
    Downloads the median elevation and azimuth of the mount in [t0, t1].

    The median is used to mitigate the effect of outliers during the window. 
    Returns (NaN, NaN) if no data is available or if any query error occurs.

    Args:
        efd_client: EFD client.
        t0: Start timestamp (UTC).
        t1: End timestamp (UTC).

    Returns:
        Tuple (elevation_deg, azimuth_deg) in decimal degrees.
    """
    try:
        el = await efd_client.select_time_series(
            "lsst.sal.MTMount.elevation", ["actualPosition"],
            Time(t0.to_pydatetime(), scale="utc"),
            Time(t1.to_pydatetime(), scale="utc"),
        )
        az = await efd_client.select_time_series(
            "lsst.sal.MTMount.azimuth", ["actualPosition"],
            Time(t0.to_pydatetime(), scale="utc"),
            Time(t1.to_pydatetime(), scale="utc"),
        )
    except Exception:
        return (np.nan, np.nan)

    el = ensure_utc_index(el) if (el is not None and not el.empty) else pd.DataFrame()
    az = ensure_utc_index(az) if (az is not None and not az.empty) else pd.DataFrame()

    el_deg = float(pd.to_numeric(el["actualPosition"], errors="coerce").median()) if "actualPosition" in el else np.nan
    az_deg = float(pd.to_numeric(az["actualPosition"], errors="coerce").median()) if "actualPosition" in az else np.nan
    return (el_deg, az_deg)


# State segmentation and slicing functions.

def build_state_segments(
    status_series: pd.Series, t0, t1
) -> list[tuple]:
    """
    Builds contiguous state segments from a series of temporal states.

    The output segment is a tuple list of (t_inicio, t_fin, estado_entero) covering the window [t0, t1].
    Changes in state are detected by comparing each value with the previous one. 
    The endpoints are extended to t0 and t1 to cover the entire window of interest.

    Args:
        status_series: Series with datetimeIndex and integer state values.
        t0: Start of the window of interest.
        t1: End of the window of interest.

    Returns:
        List of tuples (t_inicio, t_fin, estado), ordered chronologically.
        If the input series is empty or contains only NaNs, returns an empty list.
    """
    if status_series is None or status_series.empty:
        return []
    s = status_series.dropna()
    if s.empty:
        return []
    s = ensure_utc_index(s.to_frame("st"))["st"].astype(int)
    s = s[(s.index >= t0) & (s.index <= t1)]
    if s.empty:
        return []

    # Extend to the window edges to not lose the first/last state.
    if s.index[0] > t0:
        s.loc[t0] = s.iloc[0]
    if s.index[-1] < t1:
        s.loc[t1] = s.iloc[-1]
    s = s.sort_index()

    change = s.ne(s.shift()).to_numpy()
    idx = [i for i, c in enumerate(change) if c]
    segs = []
    for k in range(len(idx)):
        a = s.index[idx[k]]
        b = s.index[idx[k + 1]] if (k + 1) < len(idx) else t1
        segs.append((a, b, int(s.iloc[idx[k]])))
    return segs


def pick_longest_segment(
    segs: list[tuple], target_state: int
) -> tuple | None:
    """
    Selection of the longest segment corresponding to 'target_state'.

    Use for choosing the most representative phase of each test state 
    when there are multiple transitions in a window.

    Args:
        segs: Tuple list (t_start, t_end, state) generated by build_state_segments. 
        target_state: Integer searched state values (value of the enum HardpointTest).

    Returns:
        Tuple (t_start, t_end) of longest segment or None if no candidates.
    """
    cands = [(a, b) for (a, b, st) in segs if st == target_state and b > a]
    return max(cands, key=lambda ab: (ab[1] - ab[0])) if cands else None


def slice_by_segment(
    df: pd.DataFrame, seg: tuple | None, pad_s: float = 1.0
) -> pd.DataFrame:
    """
    Cut the DataFrame to the interval defined by 'seg', with a margin 'pad_s'.

    Margin 'pad_s' in seconds is added to both ends of the segment to avoid losing samples 
    at the edge of the segment due to resolution differences between EFD topics.

    Args:
        df: Dataframe with UTC DatetimeIndex.
        seg: Tuple (t_start, t_end) or None.
        pad_s: Margin in seconds to add to each end of the segment.

    Returns:
        Subset of the DataFrame within the expanded segment, or empty DataFrame.
    """
    if seg is None or df is None or df.empty:
        return pd.DataFrame()
    a, b = seg
    a = a - pd.Timedelta(seconds=pad_s)
    b = b + pd.Timedelta(seconds=pad_s)
    return df[(df.index >= a) & (df.index <= b)].copy()


# Stiffness fit functions.

def slope_through_origin(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calculates the slope of the least squares line forced to pass through the origin.

    Minimizes sum((y - k*x)^2) with analytical solution: k = dot(x,y) / dot(x,x).

    Args:
        x: Array with displacement values (µm).
        y: Array with force values (N).

    Returns:
        Slope in N/µm, or NaN if denominator is zero or not finite.
    """
    denom = float(np.dot(x, x))
    if denom == 0 or not np.isfinite(denom):
        return np.nan
    return float(np.dot(x, y) / denom)


def center_to_origin(df: pd.DataFrame) -> pd.DataFrame:
    """
    Traslates force and displacement data so that the point of minimum 
    absolute force is at the origin (0, 0).

    This eliminates the static offset before stiffness fitting, allowing 
    the regression forced through the origin to be applied correctly.  

    Args:
        df: Dataframe with 'force' and 'displacement' columns, temporal index.

    Returns:
        Dataframe copy with force and displacement centered. If the input is empty, returns an empty DataFrame.
    """
    df = df.sort_index().copy()
    if df.empty:
        return df
    i0 = df["force"].abs().idxmin()
    x0 = float(df.loc[i0, "displacement"])
    y0 = float(df.loc[i0, "force"])
    df["displacement"] -= x0
    df["force"] -= y0
    return df


def stiffness_from_df(df_fd: pd.DataFrame) -> float:
    """
    Calculates the stiffness (N/µm) of a hardpoint from force-displacement data.

    Pipeline of three steps:
      1. Centers the data at the point of minimum absolute force (see center_to_origin).
      2. Filters points within ±DISP_FIT_UM µm to exclude the non-linear regime.
      3. Fits the line forced through the origin using ±FIT_POINTS_AROUND_ZERO 
      samples around zero (most linear zone).

    Requires at least 20 total samples in the input DataFrame and at least 5 points 
    in the fitting window to return a valid stiffness.

    Args:
        df_fd: DataFrame with 'force' (N) and 'displacement' (µm) columns.

    Returns:
        Stiffness in N/µm, or NaN if insufficient data or fitting fails.
    """
    if df_fd is None or df_fd.empty or len(df_fd) < 20:
        return np.nan
    dfc = center_to_origin(df_fd)
    dfc = dfc[dfc["displacement"].abs() <= DISP_FIT_UM].copy()
    if dfc.empty:
        return np.nan
    x = dfc["displacement"].to_numpy(float)
    j0 = int(np.argmin(np.abs(x)))
    lo = max(0, j0 - FIT_POINTS_AROUND_ZERO)
    hi = min(len(dfc), j0 + FIT_POINTS_AROUND_ZERO + 1)
    df_fit = dfc.iloc[lo:hi]
    if len(df_fit) < 5:
        return np.nan
    return slope_through_origin(
        df_fit["displacement"].to_numpy(float),
        df_fit["force"].to_numpy(float),
    )


# Breakaway detection function.

def find_breakaway_index(displacement_um: pd.Series) -> int | None:
    """
    Detects the index of the breakaway point in the displacement series.

    Breakaway is defined as the first instant where at least BREAKAWAY_MIN_CONSEC consecutive samples
    have a displacement increment greater than BREAKAWAY_DISP_UM µm.

    Args:
        Displacement (µm) series with temporal index.
)
    Returns:
        Integer index (position) of the first breakaway point,
        or None if no breakaway is detected.
    """
    if displacement_um is None or displacement_um.empty:
        return None
    disp_diff = displacement_um.diff().abs()
    above = disp_diff > BREAKAWAY_DISP_UM
    if not above.any():
        return None

    count = 0
    first = None
    for i, ok in enumerate(above.to_numpy()):
        if ok:
            count += 1
            if first is None:
                first = i
            if count >= BREAKAWAY_MIN_CONSEC:
                return first
        else:
            count = 0
            first = None
    return None


# Statistics calculation function. 

def force_disp_stats(df_fd: pd.DataFrame) -> dict:
    """
    Calculates basic statistics of force and displacement.

    Args:
        df_fd: DataFrame with 'force' (N) and 'displacement' (µm) columns.

    Returns:
        Dictionary with n, force_max, force_min, force_mean,
        disp_ptp (peak-to-peak), disp_max y disp_min.
        If the DataFrame is invalid or missing columns, returns n=0 and NaN for the rest.
    """
    empty = dict(
        n=0,
        force_max=np.nan, force_min=np.nan, force_mean=np.nan,
        disp_ptp=np.nan, disp_max=np.nan, disp_min=np.nan,
    )
    if df_fd is None or df_fd.empty:
        return empty
    # Validate that expected columns exist before accessing.
    if not {"force", "displacement"}.issubset(df_fd.columns):
        return empty

    f = df_fd["force"]
    d = df_fd["displacement"]
    return dict(
        n=int(len(df_fd)),
        force_max=float(f.max()),
        force_min=float(f.min()),
        force_mean=float(f.mean()),
        disp_ptp=float(d.max() - d.min()),
        disp_max=float(d.max()),
        disp_min=float(d.min()),
    )


# Principal pipeline function. 

async def extract_features_for_groups(
    df_groups: pd.DataFrame,
    *,
    outdir: str = os.path.expanduser("~/breakaway_features"),
    csv_name: str = "breakaway_features.csv",
    debug: bool = False,
    efd_name: str = "usdf_efd",
    include_mount_angles: bool = True,
    overwrite: bool = False,
) -> pd.DataFrame:
    """
    Extracts physical features for each M1M3 hardpoint test group.

    For each group in 'df_groups' (defined by start/end timestamps and group_id), it performs the following steps:
      - Downloads the test states, force, displacement, and optionally the mount angles from the EFD.
      - Segments the data by test state (MOVINGNEGATIVE, TESTINGPOSITIVE, TESTINGNEGATIVE).
      - For each hardpoint and state, calculates stiffness, basic statistics, and breakaway point.
      - Classifies the breakaway force within acceptance bands.

    If the output CSV already exists and 'overwrite' is False, it loads 
    the features directly from the CSV instead of recomputing.

    Args:
        df_groups: DataFrame with columns 't_start_utc', 't_end_utc', 'group_id'
                   and optionally 'date'. Generated by scan_days_with_tests_real_status.
        outdir: Output directory for the features CSV.
        csv_name: Output CSV file name.
        debug: If True, prints progress to console.
        efd_name: Name of the EFD to connect for data download.
        include_mount_angles: If True, downloads elevation and azimuth of the mount. 
                              If False, these features will be set to NaN.
        overwrite: If True, forces recomputation even if the output CSV already exists. 
                   If False, loads from CSV if available.

    Returns:
        Dataframe with extracted features, one row per (group, hardpoint, state), including
         stiffness, statistics, breakaway, angles, and 'in_band' flag.
    """
    outdir = os.path.expanduser(outdir)
    ensure_dir(outdir)
    outpath = os.path.join(outdir, csv_name)

    if (not overwrite) and os.path.exists(outpath):
        if debug:
            print(f"Loading existing features CSV: {outpath}")
        return pd.read_csv(outpath)

    efd_client = makeEfdClient(efd_name)

    rows = []
    g = df_groups.copy()
    g["t_start_utc"] = pd.to_datetime(g["t_start_utc"], utc=True)
    g["t_end_utc"] = pd.to_datetime(g["t_end_utc"], utc=True)

    state_map = {
        "MOVINGNEGATIVE":   int(HardpointTest.MOVINGNEGATIVE),
        "TESTINGPOSITIVE":  int(HardpointTest.TESTINGPOSITIVE),
        "TESTINGNEGATIVE":  int(HardpointTest.TESTINGNEGATIVE),
    }

    for idx, gr in enumerate(g.itertuples(index=False)):
        t0 = pd.Timestamp(getattr(gr, "t_start_utc"))
        t1 = pd.Timestamp(getattr(gr, "t_end_utc"))
        date_str = getattr(gr, "date", None) or t0.strftime("%Y-%m-%d")
        group_id = int(getattr(gr, "group_id", idx))

        if include_mount_angles:
            el_deg, az_deg = await fetch_el_az_window(efd_client, t0, t1)
        else:
            el_deg, az_deg = (np.nan, np.nan)

        if debug and idx % 20 == 0:
            print(f"[{idx + 1}/{len(g)}] grupo {group_id} {t0} -> {t1}")

        sts = await fetch_status_window(efd_client, t0, t1)
        if sts.empty:
            continue

        act_all = await fetch_force_disp_all(efd_client, t0, t1)
        if act_all.empty:
            continue

        for hp in range(1, N_HP + 1):
            i = hp - 1
            fcol = f"measuredForce{i}"
            dcol = f"displacement{i}"
            scol = f"testState{i}"
            if fcol not in act_all.columns or dcol not in act_all.columns or scol not in sts.columns:
                continue

            hp_fd_all = (
                act_all[[fcol, dcol]]
                .rename(columns={fcol: "force", dcol: "displacement"})
                .dropna()
            )
            if hp_fd_all.empty:
                continue

            segs = build_state_segments(sts[scol], t0, t1)
            seg_by_state = {sv: pick_longest_segment(segs, sv) for sv in state_map.values()}

            for state_name, state_val in state_map.items():
                seg = seg_by_state.get(state_val)
                df_state = slice_by_segment(hp_fd_all, seg, pad_s=1.0)
                if df_state.empty:
                    continue

                stats = force_disp_stats(df_state)

                k_raw = stiffness_from_df(df_state)
                k_use = k_raw

                # Campling of small negative stiffness values due to numerical noise → 0.0
                if np.isfinite(k_use) and (STIFFNESS_NEG_CLAMP_EPS <= k_use < 0.0):
                    k_use = 0.0
                # Discard significant negative or positive stiffness values (inconsistent data)
                elif np.isfinite(k_use) and ((k_use < STIFFNESS_NEG_CLAMP_EPS) or (k_use > STIFFNESS_MAX_ABS)):
                    k_use = np.nan

                ba_idx = find_breakaway_index(df_state["displacement"])
                ba_disp  = float(df_state["displacement"].iloc[ba_idx]) if ba_idx is not None else np.nan
                ba_force = float(df_state["force"].iloc[ba_idx])        if ba_idx is not None else np.nan
                ba_time  = df_state.index[ba_idx]                       if ba_idx is not None else pd.NaT

                dur_s = (seg[1] - seg[0]).total_seconds() if seg is not None else np.nan

                rows.append({
                    "date":                  date_str,
                    "month":                 date_str[:7],
                    "group_id":              group_id,
                    "hp":                    hp,
                    "state":                 state_name,
                    "t_start_utc":           t0,
                    "t_end_utc":             t1,
                    "state_duration_s":      dur_s,
                    "stiffness_raw_N_per_um": k_raw,
                    "stiffness_N_per_um":    k_use,
                    # stiff_ok: valid stiffness in relevant states and within expected range.
                    "stiff_ok": bool(
                        (state_name in STIFF_OK_STATES)
                        and np.isfinite(k_use)
                        and (0.0 <= k_use <= STIFFNESS_MAX_ABS)
                    ),
                    **stats,
                    "breakaway_time_utc":    ba_time,
                    "breakaway_force_N":     ba_force,
                    "breakaway_disp_um":     ba_disp,
                    "elevation_deg":         el_deg,
                    "azimuth_deg":           az_deg,
                })

    df_feat = pd.DataFrame(rows)

    # Acceptance band classification based on breakaway force.
    # in_band: True if breakaway force falls within expected compression or tension band. 
    # NaN values are treated as False.
    if "breakaway_force_N" in df_feat.columns:
        f = pd.to_numeric(df_feat["breakaway_force_N"], errors="coerce")
    else:
        f = pd.Series(np.nan, index=df_feat.index)

    in_comp = (f >= COMP_BAND_N[0]) & (f <= COMP_BAND_N[1])
    in_tens = (f >= TENS_BAND_N[0]) & (f <= TENS_BAND_N[1])
    df_feat["in_band"] = (in_comp | in_tens).fillna(False).astype(bool)

    df_feat.to_csv(outpath, index=False)
    if debug:
        print(f"Saved CSV: {outpath} | filas={len(df_feat)}")
    return df_feat
