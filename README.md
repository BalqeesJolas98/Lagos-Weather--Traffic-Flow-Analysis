# Data directory

The raw Excel workbooks used in the study are not included in this public repository.

Place the following files in this directory before running the analysis:

- `DRY_SEASON_DATASET.xlsx`
- `WET_SEASON_DATASET.xlsx`

The analysis expects the road sheets described in the thesis dataset:

- Dry season: `Marina Road`, `Broad Street`
- Wet season: `Marina Road`, `Broad Street`

The wet-season auxiliary weather-only sheet is not used by the traffic regression workflow.

## Variables used by the regression models

- Traffic Volume (`Total` / equivalent standardized column)
- Traffic Density
- Temperature
- Dew Point
- Precipitation

The primary model reproduces the model-performance document: traffic volume is modeled as a function of temperature, dew point, and precipitation, separately by road and season.
