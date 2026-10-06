"""Diagnostic plots used by the analysis pipeline."""
import matplotlib.pyplot as plt
import numpy as np
def actual_vs_predicted(actual,predicted,title,out_file):
    fig,ax=plt.subplots(figsize=(7,6)); ax.scatter(actual,predicted,alpha=0.55); lo,hi=min(np.min(actual),np.min(predicted)),max(np.max(actual),np.max(predicted)); ax.plot([lo,hi],[lo,hi],linestyle="--",linewidth=1.5,label="Ideal fit"); ax.set_xlabel("Actual"); ax.set_ylabel("Predicted"); ax.set_title(title); ax.legend(); fig.tight_layout(); fig.savefig(out_file,dpi=300); plt.close(fig)
def residual_plot(actual,predicted,title,out_file):
    residual=np.asarray(actual)-np.asarray(predicted); fig,ax=plt.subplots(figsize=(7,5)); ax.scatter(predicted,residual,alpha=0.55); ax.axhline(0,linestyle="--",linewidth=1.2); ax.set_xlabel("Predicted"); ax.set_ylabel("Residual"); ax.set_title(title); fig.tight_layout(); fig.savefig(out_file,dpi=300); plt.close(fig)
