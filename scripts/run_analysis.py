from pathlib import Path
import sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from src.data_preparation import load_data,model_subset
from src.regression_models import fit_ols,model_summary,coefficient_table,anova_table,vif_table,validate_holdout,validate_chronological,document_reference_values
from src.visualization import actual_vs_predicted,residual_plot
RESULTS=ROOT/"results"
for d in ["tables","figures","predictions"]: (RESULTS/d).mkdir(parents=True,exist_ok=True)
def run():
    data=load_data(); data.to_csv(RESULTS/"tables"/"cleaned_combined_dataset.csv",index=False); summary_rows=[]; coef_frames=[]; anova_frames=[]; vif_frames=[]; validation_rows=[]; chronological_rows=[]
    for season in ["Dry","Wet"]:
        for road in ["Broad Street","Marina Road"]:
            for outcome in ["Traffic_Volume","Traffic_Density"]:
                d=model_subset(data,season,road,outcome); model=fit_ols(d,outcome); summary_rows.append(model_summary(model,outcome,season,road)); coef_frames.append(coefficient_table(model,d,outcome,season,road)); anova_frames.append(anova_table(model,season,road,outcome)); vif_frames.append(vif_table(d,season,road)); metrics,predictions,_=validate_holdout(d,outcome,season,road); validation_rows.append(metrics); chrono_metrics,chrono_predictions,_=validate_chronological(d,outcome,season,road); chronological_rows.append(chrono_metrics); tag=f"{season}_{road.replace(' ','_')}_{outcome}"; predictions.to_csv(RESULTS/"predictions"/f"{tag}_random_holdout_predictions.csv",index=False); chrono_predictions.to_csv(RESULTS/"predictions"/f"{tag}_chronological_predictions.csv",index=False); actual_vs_predicted(predictions[outcome],predictions["Predicted"],f"{season} - {road} - {outcome}: Random Holdout",RESULTS/"figures"/f"{tag}_random_holdout_actual_vs_predicted.png"); residual_plot(predictions[outcome],predictions["Predicted"],f"{season} - {road} - {outcome}: Random Holdout Residuals",RESULTS/"figures"/f"{tag}_random_holdout_residuals.png")
    pd.DataFrame(summary_rows).to_csv(RESULTS/"tables"/"model_summary.csv",index=False); pd.concat(coef_frames,ignore_index=True).to_csv(RESULTS/"tables"/"coefficients.csv",index=False); pd.concat(anova_frames,ignore_index=True).to_csv(RESULTS/"tables"/"anova.csv",index=False); pd.concat(vif_frames,ignore_index=True).to_csv(RESULTS/"tables"/"vif.csv",index=False); pd.DataFrame(validation_rows).to_csv(RESULTS/"tables"/"random_holdout_validation.csv",index=False); pd.DataFrame(chronological_rows).to_csv(RESULTS/"tables"/"chronological_validation.csv",index=False); refs=document_reference_values(); refs.to_csv(RESULTS/"tables"/"document_reference_values.csv",index=False); actual=pd.DataFrame(summary_rows); actual=actual[actual["Outcome"]=="Traffic_Volume"].copy(); compare=refs.rename(columns={"Standard_Error":"Standard_Error_of_Estimate"}).merge(actual,on=["Season","Road","Outcome"],suffixes=("_Document","_Recomputed"))
    for metric in ["R","R_Squared","Adjusted_R_Squared","Standard_Error_of_Estimate"]: compare[f"{metric}_Difference"]=compare[f"{metric}_Recomputed"]-compare[f"{metric}_Document"]
    compare.to_csv(RESULTS/"tables"/"document_vs_recomputed_comparison.csv",index=False)
    with open(RESULTS/"model_equations.txt","w",encoding="utf-8") as f:
        for season in ["Dry","Wet"]:
            for road in ["Broad Street","Marina Road"]:
                m=fit_ols(model_subset(data,season,road,"Traffic_Volume"),"Traffic_Volume"); f.write(f"{season} | {road}\nTotal = {m.params['const']:.6f} {m.params['Temperature']:+.6f}*Temperature {m.params['Dew_Point']:+.6f}*Dew_Point {m.params['Precipitation']:+.6f}*Precipitation\n\n")
    print(f"Analysis complete. Results: {RESULTS}")
if __name__=="__main__": run()
