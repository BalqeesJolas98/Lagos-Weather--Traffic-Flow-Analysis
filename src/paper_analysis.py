"""Additional analyses explicitly reported in the paper."""
import numpy as np
import pandas as pd
import statsmodels.api as sm

VEHICLE_TYPES = ["Private_Vehicle", "Commercial_Bus", "Truck"]


def traffic_composition(data):
    """Aggregate vehicle counts and percentages by season."""
    cols = [c for c in VEHICLE_TYPES if c in data.columns]
    grouped = data.groupby("Season")[cols].sum(min_count=1)
    totals = grouped.sum(axis=1)
    result = grouped.copy()
    for col in cols:
        result[f"{col}_Percent"] = grouped[col] / totals * 100
    return result.reset_index()


def precipitation_binary_comparison(data):
    """Compare mean traffic volume/density for no-rain versus rainfall-present observations.

    The paper defines rainfall present as precipitation of 1+ (equivalent to > 0
    for non-negative precipitation measurements).
    """
    frame = data.copy()
    frame["Rainfall_Status"] = np.where(
        pd.to_numeric(frame["Precipitation"], errors="coerce") > 0,
        "Rainfall present (1+)",
        "No rainfall (0)",
    )
    rows = []
    for outcome in ["Traffic_Volume", "Traffic_Density"]:
        means = frame.groupby("Rainfall_Status")[outcome].mean()
        no_rain = means.get("No rainfall (0)", np.nan)
        rain = means.get("Rainfall present (1+)", np.nan)
        reduction = (no_rain - rain) / no_rain * 100 if no_rain else np.nan
        rows.append(
            {
                "Traffic_Metric": outcome,
                "No_Rain_Average": no_rain,
                "Rain_Average": rain,
                "Percentage_Reduction": reduction,
            }
        )
    return pd.DataFrame(rows)


def combined_weather_regression(data):
    """Fit the paper's combined-data weather regressions for Table 1-style slopes."""
    rows = []
    for outcome in ["Traffic_Volume", "Traffic_Density"]:
        cols = [outcome, "Temperature", "Dew_Point", "Precipitation"]
        frame = data[cols].apply(pd.to_numeric, errors="coerce").dropna()
        model = sm.OLS(
            frame[outcome],
            sm.add_constant(frame[["Temperature", "Dew_Point", "Precipitation"]], has_constant="add"),
        ).fit()
        for predictor in ["Temperature", "Dew_Point", "Precipitation"]:
            rows.append(
                {
                    "Outcome": outcome,
                    "Variable": predictor,
                    "Coefficient": model.params[predictor],
                    "P_value": model.pvalues[predictor],
                    "Effect_Direction": "Positive" if model.params[predictor] >= 0 else "Negative",
                    "N": len(frame),
                }
            )
    return pd.DataFrame(rows)


def rainfall_boxplot(data, outcome, title, out_file):
    import matplotlib.pyplot as plt

    frame = data[[outcome, "Precipitation"]].dropna().copy()
    frame["Rainfall_Level"] = np.where(frame["Precipitation"] > 0, "Rainfall present (1+)", "No rainfall (0)")
    groups = [
        frame.loc[frame["Rainfall_Level"] == "No rainfall (0)", outcome],
        frame.loc[frame["Rainfall_Level"] == "Rainfall present (1+)", outcome],
    ]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.boxplot(groups, labels=["No rainfall (0)", "Rainfall present (1+)"])
    ax.set_ylabel(outcome.replace("_", " "))
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(out_file, dpi=300)
    plt.close(fig)


def weather_scatter(data, outcome, predictor, title, out_file):
    import matplotlib.pyplot as plt

    frame = data[[outcome, predictor]].dropna()
    model = sm.OLS(
        frame[outcome],
        sm.add_constant(frame[[predictor]], has_constant="add"),
    ).fit()
    x = np.linspace(frame[predictor].min(), frame[predictor].max(), 100)
    y = model.params["const"] + model.params[predictor] * x

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(frame[predictor], frame[outcome], alpha=0.45)
    ax.plot(x, y, linewidth=1.5)
    ax.set_xlabel(predictor.replace("_", " "))
    ax.set_ylabel(outcome.replace("_", " "))
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(out_file, dpi=300)
    plt.close(fig)
