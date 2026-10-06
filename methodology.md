# Methodology implemented in the repository

## Primary regression model

The documented model-performance analysis specifies Multiple Linear Regression with **Total Traffic Volume** as the dependent variable and three continuous weather predictors:

\[
Traffic\ Volume = \beta_0 + \beta_1 Temperature + \beta_2 Dew\ Point + \beta_3 Precipitation + \epsilon
\]

The model is estimated separately for:

1. Dry season - Broad Street
2. Dry season - Marina Road
3. Wet season - Broad Street
4. Wet season - Marina Road

The repository also applies the same predictor specification to Traffic Density as a parallel thesis analysis.

## Model statistics

For each model, the scripts calculate:

- Multiple correlation coefficient (R)
- R-squared
- Adjusted R-squared
- Standard error of the estimate
- F-statistic and overall model p-value
- Regression coefficients
- Standard errors, t-statistics and p-values
- 95% confidence intervals
- Standardized beta coefficients
- ANOVA quantities
- Variance Inflation Factor (VIF)
- AIC and BIC

## Validation

An 80/20 holdout split with a fixed random seed is used to provide a reproducible out-of-sample check. Validation R-squared is kept separate from the regression model R-squared reported for the fitted sample.

## Weather condition variable

The categorical `Condition` variable is not included in the primary document-reproduction regression because the model-performance document specifies temperature, dew point and precipitation as the predictors. A categorical-weather analysis can be maintained as a separate thesis analysis rather than silently changing the documented model.
