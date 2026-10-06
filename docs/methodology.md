# Reproducible methodology

This repository follows the supplied paper, **Impact of Weather on Traffic Flow Characteristics of Roads in Lagos State, Nigeria**.

## Study design

Traffic and weather observations were collected over four months:

- Dry season: December and January
- Wet season: April and May

The analysis covers Marina Road and Broad Street. The wet-season auxiliary weather-only worksheet is excluded from the traffic regression because it does not contain the traffic variables required by the paper.

## Traffic variables

The paper considers traffic volume and traffic density. Traffic speed was assumed constant throughout the study. The paper identifies this assumption as a limitation because speed, volume and density are interdependent.

## Weather predictors

The reported regression models use temperature, dew point and precipitation:

Y = beta0 + beta1 Temperature + beta2 Dew Point + beta3 Precipitation + error

Models are estimated separately for each road and season.

## Weather Condition

The paper describes Weather Condition as a categorical variable and mentions one-hot encoding during preprocessing. However, the reported model-performance tables and coefficient tables use only temperature, dew point and precipitation. The code therefore preserves Weather Condition but does not add it to the primary Tables 3-8 reproduction.

## Statistical outputs

The code reproduces or supports the reported R, R-squared, adjusted R-squared, standard error of estimate, F-statistic, overall p-value, regression coefficients, standard errors, t-statistics, predictor p-values, standardized beta coefficients and ANOVA quantities.

Additional VIF, AIC/BIC and validation diagnostics are included as reproducibility checks.

## VIF

VIF is calculated once for each season-road predictor set because the predictors are identical for the volume and density models. The VIF design matrix includes an intercept, while the intercept itself is not reported as a predictor VIF.

## Validation

The repository reports two validation diagnostics:

1. An 80/20 random holdout with random_state=42.
2. A chronological holdout using the final 20 percent after sorting by the actual Date_Time field.

The chronological check is an additional robustness diagnostic. It does not replace the fitted OLS statistics or the paper's reported validation values.

## Significance

The paper uses a 5% significance threshold, p < 0.05.


## Coverage of the paper's results section

The executable pipeline also covers the non-ML descriptive analyses reported before the season-road regression tables:

- traffic composition by season for private vehicles, commercial buses and trucks;
- the combined no-rain versus rainfall-present comparison using the paper's 0 versus 1+ precipitation definition;
- precipitation boxplots for traffic volume and density;
- traffic-volume and traffic-density relationships with temperature and dew point;
- combined-data weather regression summaries corresponding to the paper's Table 1-style analysis.

The paper's discussion of infrastructure durability/performance, flooding, heat effects and road capacity is not converted into a quantitative model because the supplied dataset does not contain a direct infrastructure-condition or capacity outcome. Doing so would introduce variables and methodology that are not supported by the study data.

The primary season-road OLS model remains unchanged: temperature, dew point and precipitation are the predictors, with traffic volume and traffic density as the outcomes. Weather Condition remains available descriptively and is not inserted into the reported Tables 3-8 specification.


## Paper-level validation reproduction

The paper presents four actual-versus-predicted validation figures: dry-season traffic volume, dry-season traffic density, wet-season traffic volume, and wet-season traffic density. These validation figures are described at the season level rather than as four separate road-specific validation models.

Accordingly, the repository includes a separate paper-validation routine that pools the two roads within each season, uses the same three continuous weather predictors as the primary model, and evaluates the held-out observations with test-set R². The implementation uses an 80/20 random split with a fixed random seed (42) to make the validation implementation deterministic. Because the paper does not state enough sampling details to identify its exact split and seed, the repository does not claim to reproduce the paper's numerical R² values exactly.

The paper-reported validation R² values are kept as document reference values rather than hard-coded model outputs: 0.098 and 0.299 for dry-season volume and density, and 0.068 and 0.345 for wet-season volume and density. The generated `paper_validation_vs_reference.csv` explicitly shows the difference between the reproducible implementation and those reported values.

The existing road-season random holdout and chronological validation routines are retained only as supplementary reproducibility diagnostics. They do not modify the paper's core regression code or replace the paper-level validation reproduction.

## Descriptive analyses reproduced from the paper

The repository additionally reproduces the paper's reported descriptive analyses:

- seasonal vehicle composition for private vehicles, commercial buses and trucks, including Figure 3-style percentages;
- precipitation-level boxplots for traffic volume and density, corresponding to Figures 4 and 5;
- the combined 0-versus-1+ rainfall comparison and percentage reduction reported in Table 2;
- traffic volume and density against temperature, corresponding to Figures 6 and 7;
- traffic volume and density against dew point, corresponding to Figures 8 and 9;
- the combined-data weather regression summary corresponding to Table 1.

These additions are separate from the primary season-road regression tables. The primary OLS specification remains unchanged.

Weather Condition is deliberately left as it appears in the existing paper-aligned code. It is not added to or removed from the primary regression specification.
