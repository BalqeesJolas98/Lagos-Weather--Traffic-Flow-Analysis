"""Data loading and standardization for the Lagos weather-traffic study."""
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


def _clean_columns(df):
    df = df.copy()
    df.columns = [str(c).replace("\xa0", " ").strip() for c in df.columns]
    return df


def _find_col(df, candidates, required=True):
    normalized = {
        str(c).lower().replace(" ", "").replace("_", "").replace("(", "").replace(")", ""): c
        for c in df.columns
    }
    for candidate in candidates:
        key = candidate.lower().replace(" ", "").replace("_", "").replace("(", "").replace(")", "")
        if key in normalized:
            return normalized[key]
    if required:
        raise KeyError(f"Could not find any of {candidates}. Columns: {list(df.columns)}")
    return None


def standardize_sheet(df, road, season):
    """Standardize source naming while preserving the paper's study variables."""
    df = _clean_columns(df)
    date_col = _find_col(
        df, ["DATE/TIME", "DATE_TIME", "Date Time", "Datetime", "Date/Time"], required=False
    )
    condition_col = _find_col(df, ["Condition"], required=False)

    colmap = {
        "Temperature": _find_col(df, ["Temp (°C)", "Temp_(°C)", "Temp"]),
        "Dew_Point": _find_col(df, ["Dew Point (°C)", "Dew_Point_(°C)", "Dew Point"]),
        "Precipitation": _find_col(
            df, ["Precipitation(mm)", "Precipitation (mm)", "Precipitation"]
        ),
        "Traffic_Volume": _find_col(df, ["Total"]),
        "Traffic_Density": _find_col(df, ["Traffic Density", "Traffic_Density"]),
        "Private_Vehicle": _find_col(df, ["Private Vehicle", "Private_Vehicle"], required=False),
        "Commercial_Bus": _find_col(df, ["Commercial Bus", "Commercial_Bus"], required=False),
        "Truck": _find_col(df, ["Truck"], required=False),
    }

    return pd.DataFrame(
        {
            "Road": road,
            "Season": season,
            "Date_Time": pd.to_datetime(df[date_col], errors="coerce") if date_col else pd.NaT,
            "Temperature": pd.to_numeric(df[colmap["Temperature"]], errors="coerce"),
            "Dew_Point": pd.to_numeric(df[colmap["Dew_Point"]], errors="coerce"),
            "Precipitation": pd.to_numeric(df[colmap["Precipitation"]], errors="coerce"),
            "Traffic_Volume": pd.to_numeric(df[colmap["Traffic_Volume"]], errors="coerce"),
            "Traffic_Density": pd.to_numeric(df[colmap["Traffic_Density"]], errors="coerce"),
            "Private_Vehicle": pd.to_numeric(df[colmap["Private_Vehicle"]], errors="coerce") if colmap["Private_Vehicle"] else pd.Series(pd.NA, index=df.index, dtype="Float64"),
            "Commercial_Bus": pd.to_numeric(df[colmap["Commercial_Bus"]], errors="coerce") if colmap["Commercial_Bus"] else pd.Series(pd.NA, index=df.index, dtype="Float64"),
            "Truck": pd.to_numeric(df[colmap["Truck"]], errors="coerce") if colmap["Truck"] else pd.Series(pd.NA, index=df.index, dtype="Float64"),
            "Condition": (
                df[condition_col].astype("string").str.strip()
                if condition_col
                else pd.Series(pd.NA, index=df.index, dtype="string")
            ),
        }
    )


def _resolve_workbook(canonical_name, original_name):
    canonical = DATA_DIR / canonical_name
    original = DATA_DIR / original_name
    if canonical.exists():
        return canonical
    if original.exists():
        return original
    raise FileNotFoundError(
        f"Required workbook not found. Expected '{canonical_name}' or '{original_name}' in {DATA_DIR}."
    )


def load_data():
    """Load the four traffic sheets used by the paper."""
    dry_file = _resolve_workbook(
        "DRY_SEASON_DATASET.xlsx", "DRY_SEASON_DATASET DEC- JAN.xlsx"
    )
    wet_file = _resolve_workbook(
        "WET_SEASON_DATASET.xlsx", "WET_SEASON_DATASET APR- MAY.xlsx"
    )
    frames = []
    for road in ["Marina Road", "Broad Street"]:
        frames.append(standardize_sheet(pd.read_excel(dry_file, sheet_name=road), road, "Dry"))
    for road in ["Marina Road", "Broad Street"]:
        frames.append(standardize_sheet(pd.read_excel(wet_file, sheet_name=road), road, "Wet"))
    return pd.concat(frames, ignore_index=True)


def model_subset(data, season, road, outcome):
    """Return model-ready complete cases while retaining Date_Time for validation."""
    required = ["Date_Time", "Temperature", "Dew_Point", "Precipitation", outcome]
    subset = data[(data["Season"] == season) & (data["Road"] == road)].copy()
    return subset[required].dropna(
        subset=["Temperature", "Dew_Point", "Precipitation", outcome]
    )
