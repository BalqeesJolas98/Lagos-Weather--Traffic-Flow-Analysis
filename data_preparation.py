"""Data loading and standardization for the Lagos weather-traffic study."""
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _clean_columns(df):
    df = df.copy()
    df.columns = [str(c).replace("\xa0", " ").strip() for c in df.columns]
    return df


def _find_col(df, candidates):
    normalized = {
        str(c).lower().replace(" ", "").replace("_", "").replace("(", "").replace(")", ""): c
        for c in df.columns
    }
    for cand in candidates:
        key = cand.lower().replace(" ", "").replace("_", "").replace("(", "").replace(")", "")
        if key in normalized:
            return normalized[key]
    raise KeyError(f"Could not find any of {candidates}. Columns: {list(df.columns)}")


def standardize_sheet(df, road, season):
    """Map workbook-specific column names to a common analysis schema."""
    df = _clean_columns(df)

    colmap = {
        "Temperature": _find_col(df, ["Temp (°C)", "Temp_(°C)", "Temp"]),
        "Dew_Point": _find_col(df, ["Dew Point (°C)", "Dew_Point_(°C)", "Dew Point"]),
        "Precipitation": _find_col(df, ["Precipitation(mm)", "Precipitation (mm)", "Precipitation"]),
        "Traffic_Volume": _find_col(df, ["Total"]),
        "Traffic_Density": _find_col(df, ["Traffic Density", "Traffic_Density"]),
        "Condition": _find_col(df, ["Condition"]),
    }

    return pd.DataFrame({
        "Road": road,
        "Season": season,
        "Temperature": pd.to_numeric(df[colmap["Temperature"]], errors="coerce"),
        "Dew_Point": pd.to_numeric(df[colmap["Dew_Point"]], errors="coerce"),
        "Precipitation": pd.to_numeric(df[colmap["Precipitation"]], errors="coerce"),
        "Traffic_Volume": pd.to_numeric(df[colmap["Traffic_Volume"]], errors="coerce"),
        "Traffic_Density": pd.to_numeric(df[colmap["Traffic_Density"]], errors="coerce"),
        "Condition": df[colmap["Condition"]].astype(str).str.strip(),
    })


def _resolve_workbook(canonical_name, original_name):
    """Accept either the repository-friendly filename or the original workbook name."""
    canonical = DATA_DIR / canonical_name
    original = DATA_DIR / original_name
    if canonical.exists():
        return canonical
    if original.exists():
        return original
    raise FileNotFoundError(
        f"Required workbook not found. Expected either '{canonical_name}' "
        f"or '{original_name}' in {DATA_DIR}."
    )


def load_data():
    """Load the four road-season sheets used by the regression analysis."""
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
    d = data[(data["Season"] == season) & (data["Road"] == road)].copy()
    cols = ["Temperature", "Dew_Point", "Precipitation", outcome]
    return d[cols].dropna()
