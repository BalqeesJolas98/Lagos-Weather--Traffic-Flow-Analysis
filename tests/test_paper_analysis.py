import numpy as np
import pandas as pd

from src.paper_analysis import (
    combined_weather_regression,
    paper_validation,
    precipitation_binary_comparison,
    rainfall_boxplot,
    traffic_composition,
    vehicle_composition_plot,
    weather_scatter,
)


def sample_paper_data():
    temperatures = list(range(28, 38)) + list(range(27, 37))
    dew_offsets = [5, 4, 6, 5, 4, 6, 5, 4, 6, 5] * 2
    return pd.DataFrame({
        "Season": ["Dry"] * 10 + ["Wet"] * 10,
        "Temperature": temperatures,
        "Dew_Point": [t - offset for t, offset in zip(temperatures, dew_offsets)],
        "Precipitation": [0, 2, 0, 5, 1, 0, 3, 0, 4, 0] * 2,
        "Traffic_Volume": list(range(1000, 1100, 10)) + list(range(900, 1000, 10)),
        "Traffic_Density": list(range(60, 70)) + list(range(50, 60)),
        "Private_Vehicle": [500] * 20,
        "Commercial_Bus": [480] * 20,
        "Truck": [20] * 20,
    })


def test_traffic_composition_preserves_seasonal_counts():
    result = traffic_composition(sample_paper_data())
    assert set(result["Season"]) == {"Dry", "Wet"}
    assert np.isclose(
        result.loc[
            result["Season"] == "Dry", "Commercial_Bus_Percent"
        ].iloc[0],
        480 / 1000 * 100,
    )


def test_rainfall_comparison_uses_zero_vs_positive_precipitation():
    result = precipitation_binary_comparison(sample_paper_data())
    volume = result.loc[result["Traffic_Metric"] == "Traffic_Volume"].iloc[0]
    assert volume["No_Rain_Average"] == 996
    assert volume["Rain_Average"] == 994
    assert np.isclose(
        volume["Percentage_Reduction"],
        0.2008032129,
    )

    density = result.loc[
        result["Traffic_Metric"] == "Traffic_Density"
    ].iloc[0]
    assert density["No_Rain_Average"] == 59.6
    assert density["Rain_Average"] == 59.4
    assert np.isclose(
        density["Percentage_Reduction"],
        0.3355704698,
    )


def test_combined_weather_regression_returns_both_outcomes():
    result = combined_weather_regression(sample_paper_data())
    assert set(result["Outcome"]) == {"Traffic_Volume", "Traffic_Density"}
    assert set(result["Variable"]) == {
        "Temperature",
        "Dew_Point",
        "Precipitation",
    }


def test_paper_validation_is_season_level_and_reproducible():
    first, first_predictions = paper_validation(sample_paper_data())
    second, second_predictions = paper_validation(sample_paper_data())
    pd.testing.assert_frame_equal(first, second)
    for key in first_predictions:
        pd.testing.assert_frame_equal(
            first_predictions[key], second_predictions[key]
        )
    assert set(first["Validation"]) == {"Paper_Season_Level_80_20_Holdout"}
    assert set(first["Season"]) == {"Dry", "Wet"}
    assert set(first["Outcome"]) == {"Traffic_Volume", "Traffic_Density"}


def test_rainfall_boxplot_writes_figure(tmp_path):
    rainfall_boxplot(
        sample_paper_data(),
        "Traffic_Volume",
        "Test rainfall",
        tmp_path / "rainfall.png",
    )
    assert (tmp_path / "rainfall.png").exists()


def test_vehicle_composition_plot_writes_figure(tmp_path):
    vehicle_composition_plot(
        sample_paper_data(),
        tmp_path / "composition.png",
    )
    assert (tmp_path / "composition.png").exists()


def test_weather_scatter_writes_figure(tmp_path):
    weather_scatter(
        sample_paper_data(),
        "Traffic_Volume",
        "Temperature",
        "Test temperature",
        tmp_path / "scatter.png",
    )
    assert (tmp_path / "scatter.png").exists()
