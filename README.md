# Lagos Weather-Traffic Flow Analysis

Reproducible Python analysis for the research study **Impact of Weather on Traffic Flow Characteristics of Roads in Lagos State, Nigeria**.

## Research focus

The study examines how rainfall intensity, temperature and dew point relate to traffic flow on Marina Road and Broad Street across dry and wet seasons. The broader thesis also considers road capacity, congestion, infrastructure performance and vehicle composition under different weather conditions.

## Primary statistical model

The primary document-reproduction model is classical **Multiple Linear Regression using ordinary least squares (OLS)**:

**Traffic Volume = β0 + β1 Temperature + β2 Dew Point + β3 Precipitation + ε**

The model is fitted separately for:

- Dry season - Broad Street
- Dry season - Marina Road
- Wet season - Broad Street
- Wet season - Marina Road

A parallel Traffic Density analysis uses the same three predictors. Weather Condition is deliberately kept outside the primary regression because the supplied model-performance document specifies temperature, dew point and precipitation as its predictors.

## Repository structure

- `data/` - local raw workbooks
- `src/` - reusable analysis modules
- `scripts/` - executable analysis entry point
- `tests/` - automated tests
- `docs/` - methodology
- `results/` - local generated outputs

Raw workbooks and generated outputs are ignored by Git.

## Data

Raw Excel workbooks are not committed to this public repository. Place these files in `data/` locally:

- `DRY_SEASON_DATASET.xlsx`, or the original `DRY_SEASON_DATASET DEC- JAN.xlsx`
- `WET_SEASON_DATASET.xlsx`, or the original `WET_SEASON_DATASET APR- MAY.xlsx`

Expected traffic sheets are `Marina Road` and `Broad Street` in both workbooks. The wet-season auxiliary weather-only sheet is excluded from the traffic regression workflow.

## Installation

Clone the repository, create a Python virtual environment, and install `requirements.txt`. Python 3.11 is used by the continuous-integration workflow.

## Run

After placing the two workbooks in `data/`, run:

```bash
python scripts/run_analysis.py
```

Generated tables, diagnostic figures, prediction files and model equations are written to `results/`. These outputs are ignored by Git so the public repository does not accidentally publish derived datasets or large files.

## Validation

The pipeline reports both:

1. an 80/20 random holdout with a fixed seed of 42, and
2. a chronological holdout using the final 20 percent of time-ordered observations.

Validation metrics are explicitly separated from the fitted-sample OLS R-squared reported in the thesis model tables.

## Testing

```bash
pytest -q tests
```

GitHub Actions runs the same test suite on pushes and pull requests.

## Reproducibility

The scripts do not hard-code regression coefficients. Values transcribed from the supplied model-performance document are stored separately as reference values and compared with coefficients and fit statistics recomputed from the data.

The repository is intended for academic reproducibility. Statistical results should be interpreted with the study design and data limitations in mind, especially the modest explanatory power of the weather-only models.

## Citation

See `CITATION.cff` for software citation metadata.
