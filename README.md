# Weather and Traffic Flow Analysis in Lagos State

Reproducible Python workflow for the statistical analysis supporting the research project **“Impact of Weather on Traffic Flow Characteristics of Roads in Lagos State.”**

The repository implements Multiple Linear Regression (MLR) for examining the relationship between weather variables and urban traffic flow on Marina Road and Broad Street across dry and wet seasons.

## Research focus

The analysis examines the influence of:

- Temperature
- Dew point
- Precipitation

on:

- Traffic volume
- Traffic density

The primary model follows the model-performance specification used in the research: **Total Traffic Volume** is the dependent variable and **Temperature, Dew Point, and Precipitation** are the predictors. Models are estimated separately by road and season.

## Study structure

| Season | Road |
|---|---|
| Dry | Broad Street |
| Dry | Marina Road |
| Wet | Broad Street |
| Wet | Marina Road |

The wet-season auxiliary weather-only worksheet is excluded from the traffic regression workflow because it does not contain the required traffic variables.

## Repository structure

```text
lagos-weather-traffic-analysis/
├── README.md
├── LICENSE
├── CITATION.cff
├── .gitignore
├── requirements.txt
├── data/
│   └── README.md
├── scripts/
│   └── 01_run_analysis.py
├── src/
│   ├── __init__.py
│   ├── data_preparation.py
│   ├── regression_models.py
│   └── visualization.py
├── docs/
│   └── methodology.md
└── results/
    ├── tables/
    ├── figures/
    └── predictions/
```

## Data

Raw Excel workbooks are intentionally **not committed to the public repository**. This avoids publishing the underlying research observations without a separate decision about data sharing and permissions.

To reproduce the analysis, place the two workbooks in `data/` using these names:

```text
data/DRY_SEASON_DATASET.xlsx
data/WET_SEASON_DATASET.xlsx
```

See [`data/README.md`](data/README.md) for the expected sheets and variables.

## Installation

Python 3.10 or newer is recommended.

Create an environment and install the dependencies:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
```

## Run the analysis

From the repository root:

```bash
python scripts/run_analysis.py
```

The workflow will:

1. Read and standardize the dry- and wet-season workbooks.
2. Identify the Marina Road and Broad Street observations.
3. Fit the traffic-volume regression models separately by season and road.
4. Fit the parallel traffic-density models.
5. Calculate model statistics and coefficient tables.
6. Calculate ANOVA and VIF diagnostics.
7. Perform reproducible 80/20 holdout validation.
8. Generate predictions and diagnostic figures.
9. Save the results under `results/`.

## Model specification

The primary regression is:

```text
Traffic Volume = β0 + β1(Temperature) + β2(Dew Point) + β3(Precipitation) + ε
```

The same predictor structure is also applied to Traffic Density as a parallel analysis.

### Important methodological distinction

The regression model's in-sample R² and the holdout validation R² are different quantities. The code reports them separately so that validation performance is not confused with the explanatory power of the fitted model.

The `Condition` weather category is **not added to the primary regression model**, because doing so would change the documented specification. It can be analyzed separately as a categorical-weather analysis.

## Outputs

After execution, the repository produces:

- `results/tables/model_summary.csv`
- `results/tables/coefficients.csv`
- `results/tables/anova.csv`
- `results/tables/vif.csv`
- `results/tables/holdout_validation.csv`
- `results/tables/document_reference_values.csv`
- prediction CSV files
- actual-versus-predicted figures
- residual diagnostic figures

Generated outputs are ignored by Git by default. This keeps the public repository focused on the reproducible code and prevents accidental publication of locally generated research files.

## Reproducibility and research transparency

The code does not hard-code the regression coefficients reported in the research document. Document values are stored separately as reference values and compared against the values recalculated from the supplied datasets.

This allows another researcher to distinguish between:

- values reported in the research document, and
- values independently recalculated by the Python workflow.

## Limitations

This repository implements the specified statistical analysis. It does not establish causal effects by itself. Regression coefficients should be interpreted in the context of the study design, data collection procedure, sample size, measurement quality, model assumptions, and possible omitted variables.

## Citation

If you use this repository or adapt the code, please cite the associated thesis/research work. The repository includes a `CITATION.cff` file for GitHub's citation interface.

## License

The Python source code is released under the MIT License. The license does not grant rights to the underlying research data that are not included in this repository.

## Publishing note

This repository is designed to be public. Before publishing, confirm that your research institution, supervisor, ethics/data-management requirements, and any applicable data-collection permissions allow the underlying observations to be shared. The default `.gitignore` prevents Excel workbooks from being committed accidentally.
