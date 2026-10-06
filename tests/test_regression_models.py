import numpy as np
import pandas as pd
from src.regression_models import PREDICTORS, fit_ols, model_summary, validate_chronological, validate_holdout, vif_table

def sample_data(n=80):
    rng = np.random.default_rng(123)
    temp = rng.normal(28, 2, n)
    dew = rng.normal(24, 2, n)
    rain = rng.gamma(1.5, 2, n)
    y = 900 - 8 * temp + 15 * dew - 20 * rain + rng.normal(0, 20, n)
    return pd.DataFrame({
        "Date_Time": pd.date_range("2026-01-01", periods=n, freq="h"),
        "Temperature": temp, "Dew_Point": dew, "Precipitation": rain,
        "Traffic_Volume": y,
    })

def test_fit_ols_has_expected_predictors():
    model = fit_ols(sample_data(), "Traffic_Volume")
    assert set(PREDICTORS).issubset(model.params.index)
    assert np.isfinite(model.rsquared)

def test_summary_reports_expected_sample_size():
    data = sample_data()
    summary = model_summary(fit_ols(data, "Traffic_Volume"), "Traffic_Volume", "Dry", "Broad Street")
    assert summary["N"] == len(data)
    assert 0 <= summary["R_Squared"] <= 1

def test_validation_is_reproducible():
    data = sample_data()
    first, _, _ = validate_holdout(data, "Traffic_Volume", "Dry", "Broad Street")
    second, _, _ = validate_holdout(data, "Traffic_Volume", "Dry", "Broad Street")
    assert first == second

def test_chronological_validation_uses_actual_dates():
    data = sample_data().sample(frac=1, random_state=99).reset_index(drop=True)
    metrics, predictions, _ = validate_chronological(data, "Traffic_Volume", "Dry", "Broad Street")
    assert metrics["Validation"] == "Chronological"
    assert len(predictions) > 0
    assert metrics["Test_Start_Date"] <= metrics["Test_End_Date"]

def test_vif_is_finite_and_one_row_per_predictor():
    result = vif_table(sample_data(), "Dry", "Broad Street")
    assert list(result["Predictor"]) == PREDICTORS
    assert len(result) == len(PREDICTORS)
    assert np.isfinite(result["VIF"]).all()
