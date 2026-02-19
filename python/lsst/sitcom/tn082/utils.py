# python/lsst/sitcom/tn082/utils.py

"""
Functions for general use. 
Includes handling of UTC indices, generating time ranges by chunks, 
grouping by time gaps, and creating directories.
"""

import os
import pandas as pd
from datetime import datetime, timezone


def ensure_utc_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assure that the DataFrame index is a sorted UTC DatetimeIndex.

    If the index has no timezone, it is localized as UTC.
    If it already has a timezone, it is converted to UTC.

    Args:
        df: Input dataFrame. 

    Returns:
        DataFrame with UTC DatetimeIndex sorted, or the same df if it is empty.
    """
    if df is None or df.empty:
        return df
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    else:
        df.index = df.index.tz_convert("UTC")
    return df.sort_index()


def today_utc_str() -> str:
    """
    Returns the current date in UTC as a string in 'YYYY-MM-DD' format.
    end_date=None when calling get_data() will use this value as default, so it represents "today" in UTC.
    """
    return datetime.now(timezone.utc).date().strftime("%Y-%m-%d")


def chunk_ranges_utc(
    start: pd.Timestamp,
    end: pd.Timestamp,
    days: int = 31,
    overlap_hours: int = 2,
):
    """
    Range generator for overlapping time chunks between start and end timestamps.

    Overlapping avoids losing events at the boundaries between chunks. 
    If the overlap is greater than or equal to the chunk size, it is reduced to zero 
    to prevent infinite loops, without raising an exception.

    Args:
        start: Star timestamp (UTC).
        end: End timestamp (UTC).
        days: Size for each chunk in days. 
        overlap_hours: Hours of overlap between consecutive chunks.

    Yields:
        Tuples (chunk_start, chunk_end) like pd.Timestamps UTC.
    """
    delta = pd.Timedelta(days=days)
    overlap = pd.Timedelta(hours=overlap_hours)

    # If overlap is greater than or equal to the chunk size, set it to zero to avoid infinite loops.
    if overlap >= delta:
        overlap = pd.Timedelta(0)

    chunk_start = start
    while chunk_start < end:
        chunk_end = min(chunk_start + delta, end)
        yield chunk_start, chunk_end
        if chunk_end >= end:
            break
        chunk_start = chunk_end - overlap


def group_by_gaps(df: pd.DataFrame, gap: str) -> pd.DataFrame:
    """
    Asign group identifiers to consecutive rows based on time gaps.

    A new group starts whenever the time difference between two consecutive rows 
    exceeds the 'gap' threshold. This allows identifying bursts of activity separated in time.
   
    Args:
        df: Dataframe with sorted DatetimeIndex.
        gap: Gap threshold as a Timedelta string (e.g. '3min', '30s').

    Returns:
        Original dataframe with an additional 'group_id' column. 
        If the input df is empty, it is returned unchanged.
    """
    if df is None or df.empty:
        return df
    gid = df.index.to_series().diff().gt(pd.Timedelta(gap)).cumsum()
    return df.assign(group_id=gid)


def ensure_dir(path: str) -> None:
    """
    Create the directory at 'path' if it does not exist.

    Args:
        path: Path to the directory to be created.
    """
    os.makedirs(path, exist_ok=True)
