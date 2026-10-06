import numpy as np
import pandas as pd
from src.regression_models import fit_ols,PREDICTORS,model_summary,validate_holdout,validate_chronological
def sample_data(n=80):
    rng=np.random.default_rng(123); temp=rng.normal(28,2,n); dew=rng.normal(24,2,n); rain=rng.gamma(1.5,2,n); y=900-8*temp+15*dew-20*rain+rng.normal(0,20,n); return pd.DataFrame({"Temperature":temp,"Dew_Point":dew,"Precipitation":rain,"Traffic_Volume":y})
def test_fit_ols_has_expected_predictors():
    model=fit_ols(sample_data(),"Traffic_Volume"); assert set(PREDICTORS).issubset(model.params.index); assert np.isfinite(model.rsquared)
def test_summary_reports_expected_sample_size():
    d=sample_data(); s=model_summary(fit_ols(d,"Traffic_Volume"),"Traffic_Volume","Dry","Broad Street"); assert s["N"]==len(d); assert 0<=s["R_Squared"]<=1
def test_validation_is_reproducible():
    d=sample_data(); a,_,_=validate_holdout(d,"Traffic_Volume","Dry","Broad Street"); b,_,_=validate_holdout(d,"Traffic_Volume","Dry","Broad Street"); assert a==b
def test_chronological_validation_returns_metrics():
    d=sample_data(); m,p,_=validate_chronological(d,"Traffic_Volume","Dry","Broad Street"); assert m["Validation"]=="Chronological"; assert len(p)>0
