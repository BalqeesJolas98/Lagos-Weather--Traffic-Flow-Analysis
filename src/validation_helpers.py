"""Small validation helpers used by the analysis pipeline."""

import pandas as pd

from src.regression_models import validate_chronological


def chronological_validation_or_skip(model_data, outcome, season, road):
    """Run chronological validation when enough valid dates are available."""
    if model_data["Date_Time"].notna().sum() >= 5:
        metrics, predictions, model = validate_chronological(
            model_data, outcome, season, road
        )
        return metrics, predictions, model

    return (
        {
            "Season": season,
            "Road": road,
            "Outcome": outcome,
            "Validation": "Chronological",
            "Status": "Skipped",
            "Reason": "Fewer than five valid Date_Time observations.",
        },
        pd.DataFrame(),
        None,
    )
