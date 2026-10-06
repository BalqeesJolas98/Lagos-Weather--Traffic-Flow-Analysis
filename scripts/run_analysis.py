"""Run the paper-aligned Lagos weather-traffic analysis."""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data_preparation import load_data, model_subset
from src.regression_models import (
    anova_table, coefficient_table, document_reference_values, fit_ols,
    model_summary, validate_chronological, validate_holdout, vif_table,
)
from src.visualization import actual_vs_predicted, residual_plot

RESULTS = ROOT / "results"
for directory in ["tables", "figures", "predictions"]:
    (RESULTS / directory).mkdir(parents=True, exist_ok=True)


def run():
    data = load_data()
    data.to_csv(RESULTS / "tables" / "cleaned_combined_dataset.csv", index=False)

    summary_rows, coefficient_frames, anova_frames = [], [], []
    vif_frames, validation_rows, chronological_rows = [], [], []

    for season in ["Dry", "Wet"]:
        for road in ["Broad Street", "Marina Road"]:
            # VIF depends only on the three weather predictors, so calculate
            # it once per road-season rather than once per outcome.
            volume_data = model_subset(data, season, road, "Traffic_Volume")
            vif_frames.append(vif_table(volume_data, season, road))

            for outcome in ["Traffic_Volume", "Traffic_Density"]:
                model_data = model_subset(data, season, road, outcome)
                model = fit_ols(model_data, outcome)

                summary_rows.append(model_summary(model, outcome, season, road))
                coefficient_frames.append(
                    coefficient_table(model, model_data, outcome, season, road)
                )
                anova_frames.append(anova_table(model, season, road, outcome))

                random_metrics, predictions, _ = validate_holdout(
                    model_data, outcome, season, road
                )
                validation_rows.append(random_metrics)

                chronological_metrics, chronological_predictions, _ = validate_chronological(
                    model_data, outcome, season, road
                )
                chronological_rows.append(chronological_metrics)

                tag = f"{season}_{road.replace(' ', '_')}_{outcome}"
                predictions.to_csv(
                    RESULTS / "predictions" / f"{tag}_random_holdout_predictions.csv",
                    index=False,
                )
                chronological_predictions.to_csv(
                    RESULTS / "predictions" / f"{tag}_chronological_predictions.csv",
                    index=False,
                )

                actual_vs_predicted(
                    predictions[outcome],
                    predictions["Predicted"],
                    f"{season} - {road} - {outcome}: Random Holdout",
                    RESULTS / "figures" / f"{tag}_random_holdout_actual_vs_predicted.png",
                )
                residual_plot(
                    predictions[outcome],
                    predictions["Predicted"],
                    f"{season} - {road} - {outcome}: Random Holdout Residuals",
                    RESULTS / "figures" / f"{tag}_random_holdout_residuals.png",
                )

    pd.DataFrame(summary_rows).to_csv(RESULTS / "tables" / "model_summary.csv", index=False)
    pd.concat(coefficient_frames, ignore_index=True).to_csv(
        RESULTS / "tables" / "coefficients.csv", index=False
    )
    pd.concat(anova_frames, ignore_index=True).to_csv(
        RESULTS / "tables" / "anova.csv", index=False
    )
    pd.concat(vif_frames, ignore_index=True).to_csv(
        RESULTS / "tables" / "vif.csv", index=False
    )
    pd.DataFrame(validation_rows).to_csv(
        RESULTS / "tables" / "random_holdout_validation.csv", index=False
    )
    pd.DataFrame(chronological_rows).to_csv(
        RESULTS / "tables" / "chronological_validation.csv", index=False
    )

    references = document_reference_values()
    references.to_csv(
        RESULTS / "tables" / "document_reference_values.csv", index=False
    )

    actual = pd.DataFrame(summary_rows)
    actual = actual[actual["Outcome"] == "Traffic_Volume"].copy()
    comparison = references.rename(
        columns={"Standard_Error": "Standard_Error_of_Estimate"}
    ).merge(
        actual,
        on=["Season", "Road", "Outcome"],
        suffixes=("_Document", "_Recomputed"),
    )
    for metric in ["R", "R_Squared", "Adjusted_R_Squared", "Standard_Error_of_Estimate"]:
        comparison[f"{metric}_Difference"] = (
            comparison[f"{metric}_Recomputed"] - comparison[f"{metric}_Document"]
        )
    comparison.to_csv(
        RESULTS / "tables" / "document_vs_recomputed_comparison.csv", index=False
    )

    with open(RESULTS / "model_equations.txt", "w", encoding="utf-8") as handle:
        for season in ["Dry", "Wet"]:
            for road in ["Broad Street", "Marina Road"]:
                model_data = model_subset(data, season, road, "Traffic_Volume")
                model = fit_ols(model_data, "Traffic_Volume")
                handle.write(
                    f"{season} | {road}\n"
                    f"Total = {model.params['const']:.6f} "
                    f"{model.params['Temperature']:+.6f}*Temperature "
                    f"{model.params['Dew_Point']:+.6f}*Dew_Point "
                    f"{model.params['Precipitation']:+.6f}*Precipitation\n\n"
                )

    print(f"Analysis complete. Results: {RESULTS}")


if __name__ == "__main__":
    run()
