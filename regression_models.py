import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

PREDICTORS = ["Temperature", "Dew_Point", "Precipitation"]

def fit_ols(df, outcome):
    X = sm.add_constant(df[PREDICTORS])
    y = df[outcome]
    model = sm.OLS(y, X).fit()
    return model

def standardized_betas(df, outcome):
    z = df[[outcome] + PREDICTORS].copy()
    z = (z - z.mean()) / z.std(ddof=1)
    model = sm.OLS(z[outcome], sm.add_constant(z[PREDICTORS])).fit()
    return model.params.drop("const")

def model_summary(model, outcome, season, road):
    return {
        "Season": season,
        "Road": road,
        "Outcome": outcome,
        "N": int(model.nobs),
        "R": float(np.sqrt(max(model.rsquared, 0))),
        "R_Squared": float(model.rsquared),
        "Adjusted_R_Squared": float(model.rsquared_adj),
        "Standard_Error_of_Estimate": float(np.sqrt(model.mse_resid)),
        "F": float(model.fvalue),
        "F_p_value": float(model.f_pvalue),
        "AIC": float(model.aic),
        "BIC": float(model.bic),
    }

def coefficient_table(model, df, outcome, season, road):
    betas = standardized_betas(df, outcome)
    rows = []
    for term in ["const"] + PREDICTORS:
        name = "Constant" if term == "const" else term
        rows.append({
            "Season": season,
            "Road": road,
            "Outcome": outcome,
            "Term": name,
            "Coefficient": model.params[term],
            "Std_Error": model.bse[term],
            "t": model.tvalues[term],
            "P_value": model.pvalues[term],
            "CI_Lower": model.conf_int().loc[term, 0],
            "CI_Upper": model.conf_int().loc[term, 1],
            "Standardized_Beta": np.nan if term == "const" else betas[term],
        })
    return pd.DataFrame(rows)

def anova_table(model, season, road, outcome):
    aov = pd.DataFrame({
        "Source": ["Regression", "Residual", "Total"],
        "Df": [model.df_model, model.df_resid, model.df_model + model.df_resid],
        "Sum_of_Squares": [
            model.ess, model.ssr, model.ess + model.ssr
        ],
        "Mean_Square": [
            model.mse_model, model.mse_resid, np.nan
        ],
        "F": [model.fvalue, np.nan, np.nan],
        "P_value": [model.f_pvalue, np.nan, np.nan],
    })
    aov.insert(0, "Outcome", outcome)
    aov.insert(0, "Road", road)
    aov.insert(0, "Season", season)
    return aov

def vif_table(df, season, road):
    X = df[PREDICTORS].copy()
    rows = []
    for i, c in enumerate(PREDICTORS):
        rows.append({
            "Season": season,
            "Road": road,
            "Predictor": c,
            "VIF": variance_inflation_factor(X.values, i),
        })
    return pd.DataFrame(rows)

def validate_holdout(df, outcome, season, road, test_size=0.20, random_state=42):
    train, test = train_test_split(
        df, test_size=test_size, random_state=random_state
    )
    model = fit_ols(train, outcome)
    X_test = sm.add_constant(test[PREDICTORS], has_constant="add")
    pred = model.predict(X_test)

    actual = test[outcome].to_numpy()
    pred = np.asarray(pred)

    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    nonzero = actual != 0
    mape = np.mean(np.abs((actual[nonzero] - pred[nonzero]) / actual[nonzero])) * 100

    predictions = test.copy()
    predictions["Predicted"] = pred
    predictions["Residual"] = actual - pred
    predictions["Absolute_Error"] = np.abs(actual - pred)
    predictions["Absolute_Percentage_Error"] = np.where(
        actual != 0, np.abs((actual - pred) / actual) * 100, np.nan
    )
    predictions["Season"] = season
    predictions["Road"] = road
    predictions["Outcome"] = outcome

    metrics = {
        "Season": season,
        "Road": road,
        "Outcome": outcome,
        "Train_N": len(train),
        "Test_N": len(test),
        "Test_R2": r2_score(actual, pred),
        "Test_RMSE": rmse,
        "Test_MAE": mae,
        "Test_MAPE_percent": mape,
        "Random_State": random_state,
        "Test_Size": test_size,
    }
    return metrics, predictions, model

def document_reference_values():
    # Values transcribed from the supplied Regression Model Performance document.
    return pd.DataFrame([
        ["Dry","Broad Street","Traffic_Volume",0.211,0.045,0.037,264.629,6.209,0.000395,
         -8.65,39.16,195.70],
        ["Dry","Marina Road","Traffic_Volume",0.374,0.140,0.133,278.107,7.603,5.516e-13,
         13.94,137.05,99.80],
        ["Wet","Broad Street","Traffic_Volume",0.246,0.060,0.053,163.1,8.546,1.638e-05,
         -5.45,25.79,-46.07],
        ["Wet","Marina Road","Traffic_Volume",0.268,0.072,0.064,100.117,9.918,2.58795e-06,
         -16.56,10.73,-58.78],
    ], columns=[
        "Season","Road","Outcome","R","R_Squared","Adjusted_R_Squared",
        "Standard_Error","F","F_p_value","Temperature_Coefficient",
        "Dew_Point_Coefficient","Precipitation_Coefficient"
    ])
