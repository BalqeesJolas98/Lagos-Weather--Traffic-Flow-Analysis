"""Additional analyses explicitly reported in the paper."""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

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
    """Reproduce the paper's combined 0 versus 1+ rainfall comparison."""
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
    """Reproduce the paper's combined-data Table 1-style regression summary."""
    rows = []
    for outcome in ["Traffic_Volume", "Traffic_Density"]:
        cols = [outcome, "Temperature", "Dew_Point", "Precipitation"]
        frame = data[cols].apply(pd.to_numeric, errors="coerce").dropna()
        model = sm.OLS(
            frame[outcome],
            sm.add_constant(
                frame[["Temperature", "Dew_Point", "Precipitation"]],
                has_constant="add",
            ),
        ).fit()
        for predictor in ["Temperature", "Dew_Point", "Precipitation"]:
            rows.append(
                {
                    "Outcome": outcome,
                    "Variable": predictor,
                    "Coefficient": model.params[predictor],
                    "P_value": model.pvalues[predictor],
                    "Effect_Direction": (
                        "Positive" if model.params[predictor] >= 0 else "Negative"
                    ),
                    "N": len(frame),
                }
            )
    return pd.DataFrame(rows)


def rainfall_boxplot(data, outcome, title, out_file):
    """Reproduce Figures 4-5 using the observed precipitation levels."""
    import matplotlib.pyplot as plt

    frame = data[[outcome, "Precipitation"]].dropna().copy()
    levels = sorted(frame["Precipitation"].unique())
    groups = [frame.loc[frame["Precipitation"] == level, outcome] for level in levels]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.boxplot(groups, labels=[f"{level:g}" for level in levels])
    ax.set_xlabel("Precipitation (mm)")
    ax.set_ylabel(outcome.replace("_", " "))
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(out_file, dpi=300)
    plt.close(fig)


def vehicle_composition_plot(data, out_file):
    """Reproduce Figure 3 as seasonal vehicle-composition percentages."""
    import matplotlib.pyplot as plt

    composition = traffic_composition(data)
    long = composition.melt(
        id_vars="Season",
        value_vars=[f"{c}_Percent" for c in VEHICLE_TYPES],
        var_name="Vehicle_Type",
        value_name="Percentage",
    )
    labels = {
        "Private_Vehicle_Percent": "Private Vehicle",
        "Commercial_Bus_Percent": "Commercial Bus",
        "Truck_Percent": "Truck",
    }
    long["Vehicle_Type"] = long["Vehicle_Type"].map(labels)
    pivot = long.pivot(index="Vehicle_Type", columns="Season", values="Percentage")
    ax = pivot.plot(kind="bar", figsize=(8, 5))
    ax.set_xlabel("Vehicle Type")
    ax.set_ylabel("Percentage of Traffic (%)")
    ax.set_title("Traffic Composition by Season")
    ax.legend(title="Season")
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(out_file, dpi=300)
    plt.close(fig)


def paper_validation(data):
    """Reproduce the paper's season-level validation convention.

    The paper reports actual-versus-predicted validation plots for combined
    road observations within each season. The same three weather predictors
    are used in an 80/20 random holdout with a fixed seed for reproducibility.
    This is an additional validation reproduction and does not alter the
    primary season-road OLS models.
    """
    rows = []
    predictions = {}

    for season in ["Dry", "Wet"]:
        season_data = data.loc[data["Season"] == season].copy()
        for outcome in ["Traffic_Volume", "Traffic_Density"]:
            columns = [
                outcome,
                "Temperature",
                "Dew_Point",
                "Precipitation",
            ]
            frame = season_data[columns].apply(pd.to_numeric, errors="coerce").dropna()
            train, test = train_test_split(
                frame,
                test_size=0.20,
                random_state=42,
            )
            model = sm.OLS(
                train[outcome],
                sm.add_constant(
                    train[["Temperature", "Dew_Point", "Precipitation"]],
                    has_constant="add",
                ),
            ).fit()
            pred = model.predict(
                sm.add_constant(
                    test[["Temperature", "Dew_Point", "Precipitation"]],
                    has_constant="add",
                )
            )
            rows.append(
                {
                    "Season": season,
                    "Outcome": outcome,
                    "Validation": "Paper_Season_Level_80_20_Holdout",
                    "Train_N": len(train),
                    "Test_N": len(test),
                    "Test_Size": 0.20,
                    "Random_State": 42,
                    "Validation_R2": r2_score(test[outcome], pred),
                }
            )
            predictions[(season, outcome)] = pd.DataFrame(
                {
                    "Actual": test[outcome].to_numpy(),
                    "Predicted": np.asarray(pred),
                }
            )

    return pd.DataFrame(rows), predictions


def weather_scatter(data, outcome, predictor, title, out_file):
    """Reproduce Figures 6-9 with a simple linear fitted line."""
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


def paper_validation_reference_values():
    """Validation R² values reported in Figures 10-13, for comparison only."""
    return pd.DataFrame(
        [
            ["Dry", "Traffic_Volume", 0.098],
            ["Dry", "Traffic_Density", 0.299],
            ["Wet", "Traffic_Volume", 0.068],
            ["Wet", "Traffic_Density", 0.345],
        ],
        columns=["Season", "Outcome", "Paper_Validation_R2"],
    )
