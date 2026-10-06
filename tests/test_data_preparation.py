import pandas as pd
from src.data_preparation import standardize_sheet

def test_standardize_sheet_handles_source_column_variants():
    source = pd.DataFrame({
        "DATE/TIME": ["2026-01-01 08:00"], "Total": ["100"],
        "Traffic Density": ["20"], "Temp ( °C)": ["28"],
        "Dew Point ( °C)": ["24"], "Precipitation(mm)": ["0"],
        "Condition": ["Clear"],
    })
    result = standardize_sheet(source, "Broad Street", "Dry")
    assert result.loc[0, "Road"] == "Broad Street"
    assert result.loc[0, "Season"] == "Dry"
    assert result.loc[0, "Traffic_Volume"] == 100
    assert result.loc[0, "Traffic_Density"] == 20
    assert result.loc[0, "Temperature"] == 28
    assert result.loc[0, "Dew_Point"] == 24
    assert result.loc[0, "Precipitation"] == 0
    assert result.loc[0, "Condition"] == "Clear"
    assert pd.notna(result.loc[0, "Date_Time"])
