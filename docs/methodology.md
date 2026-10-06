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
