import numpy as np
import pandas as pd
from src.paper_analysis import combined_weather_regression, precipitation_binary_comparison, traffic_composition


def sample_paper_data():
    return pd.DataFrame({
        "Season": ["Dry", "Dry", "Wet", "Wet"],
        "Temperature": [28, 30, 27, 29],
        "Dew_Point": [23, 24, 22, 25],
        "Precipitation": [0, 2, 0, 5],
        "Traffic_Volume": [1000, 800, 1100, 700],
        "Traffic_Density": [60, 50, 65, 45],
        "Private_Vehicle": [500, 400, 550, 350],
        "Commercial_Bus": [480, 380, 530, 330],
        "Truck": [20, 20, 20, 20],
    })


def test_traffic_composition_preserves_seasonal_counts():
    result = traffic_composition(sample_paper_data())
    assert set(result["Season"]) == {"Dry", "Wet"}
    assert np.isclose(result.loc[result["Season"] == "Dry", "Commercial_Bus_Percent"].iloc[0],
                      860 / 1800 * 100)


def test_rainfall_comparison_uses_zero_vs_positive_precipitation():
    result = precipitation_binary_comparison(sample_paper_data())
    volume = result.loc[result["Traffic_Metric"] == "Traffic_Volume"].iloc[0]
    assert volume["No_Rain_Average"] == 1050
    assert volume["Rain_Average"] == 750
    assert np.isclose(volume["Percentage_Reduction"], 28.5714285714)


def test_combined_weather_regression_returns_both_outcomes():
    result = combined_weather_regression(sample_paper_data())
    assert set(result["Outcome"]) == {"Traffic_Volume", "Traffic_Density"}
    assert set(result["Variable"]) == {"Temperature", "Dew_Point", "Precipitation"}
