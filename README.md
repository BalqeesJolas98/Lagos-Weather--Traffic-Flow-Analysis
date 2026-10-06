# Lagos Weather-Traffic Flow Analysis

**Impact of Weather on Traffic Flow Characteristics of Roads in Lagos State, Nigeria**.

## Research basis

This repository follows the methodology, results and discussion in the associated paper. 

The paper investigates traffic observations from **Marina Road and Broad Street** during the **dry season (December and January)** and **wet season (April and May)**. Traffic data were obtained through video-based traffic counting and weather data were obtained from the Nigerian Meteorological Agency (NIMET).

The traffic flow variables considered are traffic volume and traffic density. Traffic speed was held constant as a study assumption, and the paper identifies this as a limitation.

## Primary regression specification

The reported model-performance tables use the three continuous weather predictors:

- Temperature
- Dew Point
- Precipitation

The model is fitted separately for:

1. Dry season - Broad Street
2. Dry season - Marina Road
3. Wet season - Broad Street
4. Wet season - Marina Road

The general model is:

Y = beta0 + beta1 Temperature + beta2 Dew Point + beta3 Precipitation + error

The same three predictors are used for the parallel traffic-density analysis.

## Weather Condition

The paper discusses Weather Condition as a categorical variable and describes categorical encoding during preprocessing. However, Tables 3-8 and their reported coefficients, ANOVA results and model-performance discussion identify temperature, dew point and precipitation as the predictors in the reported regression models.

The repository therefore preserves Weather Condition in the standardized data but does not insert it into the primary Tables 3-8 reproduction. Adding it would create a different model from the one reported in the paper.

## Statistical outputs

The pipeline reproduces the paper's reported descriptive analyses and keeps the paper's primary season-road OLS model unchanged. It includes traffic composition, the combined 0-versus-1+ rain/no-rain comparison, precipitation-level boxplots, temperature and dew-point relationship plots, and the paper's combined-data Table 1-style regression summary.

The repository does **not** invent an infrastructure-durability outcome or a road-capacity model. Although the paper discusses flooding, heat, infrastructure performance and capacity conceptually, the supplied traffic dataset does not contain a direct infrastructure-condition or capacity outcome, so those topics are treated as discussion/limitations rather than fabricated quantitative models.

The pipeline produces:

- R and R-squared
- Adjusted R-squared
- Standard error of the estimate
- F-statistic and overall model p-value
- Regression coefficients
- Standard errors
- t-statistics
- predictor p-values
- confidence intervals
- standardized beta coefficients
- ANOVA quantities

Additional reproducibility diagnostics are provided for the same model: VIF, AIC/BIC, random 80/20 holdout validation, chronological holdout validation, actual-versus-predicted plots and residual plots.

## Fitted R-squared versus validation R-squared

The R-squared values in the fitted regression tables are not the same quantity as an out-of-sample validation R-squared. The repository keeps these analyses in separate output tables so that validation results are not substituted for the paper's fitted model statistics.

## Data availability and provenance

Raw Excel workbooks are not committed to this public repository. The code, tests and processing workflow are public, but the empirical results cannot be reproduced from a clean clone without access to the study workbooks.

Place the study workbooks in data/ locally:

- DRY_SEASON_DATASET.xlsx, or DRY_SEASON_DATASET DEC- JAN.xlsx
- WET_SEASON_DATASET.xlsx, or WET_SEASON_DATASET APR- MAY.xlsx

The traffic sheets used are Marina Road and Broad Street. The wet-season auxiliary weather-only worksheet is excluded from the traffic regression because it does not contain the traffic variables required by the traffic-flow analysis.

The study uses weather observations obtained from the Nigerian Meteorological Agency (NIMET) and traffic observations obtained through video-based traffic counting. Exact source files, station identifiers, observation timestamps, counting intervals, collection procedures and restricted source material should be retained with the research records so that the provenance of each analysis input can be established. These details are not invented here because they are not encoded in the public repository.

For supervisory or research review, the data-access arrangement should be stated explicitly, including whether the source workbooks can be shared with reviewers or provided privately for verification.

## Installation

Runtime dependencies:

    pip install -r requirements.txt

Development and testing dependencies:

    pip install -r requirements-dev.txt

Python 3.11 is used by continuous integration.

## Run

After placing the two workbooks in data/:

    python scripts/run_analysis.py

Generated tables, figures, predictions and equations are written to results/.

## Testing

    pytest -q tests

Tests cover regression construction, model summaries, random holdout reproducibility, date-based chronological validation, VIF construction, source-column standardization, traffic composition, rain/no-rain comparison, combined weather regression and the explicit paper-validation reproduction.

## Reproducibility

Regression coefficients are not hard-coded as model inputs. Values transcribed from the paper's Tables 3-8 are kept separately as reference values and compared with results recomputed from the datasets.

The paper reports modest explanatory power and interprets the weather-only models primarily in terms of directional effects. The repository follows that interpretation.

## Limitations and future research

The principal methodological limitation is the assumption of constant traffic speed. Because traffic speed, volume and density are interdependent, future work should collect or derive observed speed and examine the three traffic-flow variables jointly.

The weather-only regression should also be interpreted as an association model rather than a complete traffic-prediction model. Future work can incorporate traffic demand, time of day, day of week, road characteristics, incidents and other relevant temporal or spatial factors to determine how much additional explanatory power weather contributes.

The study's empirical reproducibility is also limited by the public unavailability of the raw workbooks. Where permitted, future releases should provide a documented data package or access procedure, together with provenance information for the weather source, traffic-counting protocol, observation period and data-cleaning decisions.

## Authorship

Repository author and maintainer: **Balqees Omobolanle Jolaosho**.


### Validation reproduction and supplementary diagnostics

The paper reports actual-versus-predicted validation figures at the **season level**, pooling the two study roads within each season, for traffic volume and traffic density. The repository therefore generates a separate `paper_validation.csv` and four corresponding actual-versus-predicted figures using the same three weather predictors as the primary model. This is a paper-aligned validation reproduction, not a claim that the paper's exact numerical R² values can be regenerated without the paper's original split/sample-selection details.

The paper's reported validation R² values are documented separately for comparison:

- Dry season, traffic volume: 0.098
- Dry season, traffic density: 0.299
- Wet season, traffic volume: 0.068
- Wet season, traffic density: 0.345

The implementation uses an explicit 80/20 random holdout with `random_state=42` so that the validation implementation is deterministic. The paper does not state enough split/seed details to establish that this exact sampling procedure produced its reported R² values. Therefore, the paper R² values are retained only as reference values, and the generated comparison table reports any difference rather than forcing agreement.

The existing road-season random holdout and chronological validation diagnostics remain in the repository as **supplementary diagnostics**. They do not replace or alter the paper-level validation reproduction and do not change the primary regression results.
