# Reproducible methodology

## Study design
This repository implements the statistical analysis for the study Impact of Weather on Traffic Flow Characteristics of Roads in Lagos State, Nigeria. Dry-season observations from Marina Road and Broad Street are grouped as Dry, and wet-season observations from the same roads are grouped as Wet. The wet-season auxiliary weather-only worksheet is excluded because it does not contain the traffic variables required by the regression workflow.

## Primary model
The primary model reproduces the supplied model-performance document: Traffic Volume = beta0 + beta1 Temperature + beta2 Dew Point + beta3 Precipitation + error. It is estimated separately for Dry/Broad Street, Dry/Marina Road, Wet/Broad Street, and Wet/Marina Road. The repository does not add Condition to this primary model because the supplied model-performance document specifies only temperature, dew point and precipitation as predictors.

Traffic Density is analysed in a parallel extension using the same three predictors. This extension should be reported separately from the document-reproduction volume model.

## Statistical outputs
The code reports R, R-squared, adjusted R-squared, standard error of estimate, F-statistic, overall p-value, coefficients, standard errors, t-statistics, p-values, confidence intervals, standardized beta coefficients, ANOVA quantities, VIF, AIC and BIC.

## Validation
Two out-of-sample checks are produced: an 80/20 random holdout with random_state=42, and a chronological holdout using the final 20 percent of time-ordered observations. The chronological check is included because traffic and weather observations are time ordered. Neither validation R-squared should be confused with the fitted-sample OLS R-squared used in the regression tables.

## Hypotheses
H0: Temperature, dew point and precipitation have no statistically significant joint effect on traffic volume.

H1: At least one of temperature, dew point and precipitation has a statistically significant effect on traffic volume.
