import pandas as pd
import numpy as np

def generate_insights(df):
    """
    Generates rule-based insights from the current dataset.
    """
    insights = []
    
    if df is None or df.empty:
        return ["No data available to generate insights."]
        
    if 'subject' in df.columns and 'total_marks' in df.columns:
        subj_stats = df.groupby('subject')['total_marks'].mean()
        if not subj_stats.empty:
            highest_subj = subj_stats.idxmax()
            lowest_subj = subj_stats.idxmin()
            insights.append({
                "title": "Highest Performance",
                "text": f"**{highest_subj}** has the highest average total marks ({subj_stats[highest_subj]:.1f})."
            })
            insights.append({
                "title": "Lowest Performance",
                "text": f"**{lowest_subj}** has the lowest average total marks ({subj_stats[lowest_subj]:.1f})."
            })
            
        subj_var = df.groupby('subject')['total_marks'].std()
        if not subj_var.empty and not subj_var.isnull().all():
            most_var = subj_var.idxmax()
            insights.append({
                "title": "Highest Variability",
                "text": f"**{most_var}** shows the most variability in scores (Std Dev: {subj_var[most_var]:.1f})."
            })
            
    if 'result' in df.columns:
        total = len(df['result'].dropna())
        if total > 0:
            passes = (df['result'] == 'Pass').sum()
            pass_rate = (passes / total) * 100
            insights.append({
                "title": "Overall Pass Rate",
                "text": f"The overall pass rate is **{pass_rate:.1f}%** across all selected records."
            })
            
    if 'attendance_pct' in df.columns and 'total_marks' in df.columns:
        valid = df.dropna(subset=['attendance_pct', 'total_marks'])
        if len(valid) > 2 and valid['attendance_pct'].std() > 0 and valid['total_marks'].std() > 0:
            corr = valid['attendance_pct'].corr(valid['total_marks'])
            strength = "strong" if abs(corr) > 0.6 else "moderate" if abs(corr) > 0.3 else "weak"
            insights.append({
                "title": "Attendance vs Marks",
                "text": f"There is a **{strength} correlation** ({corr:.2f}) between attendance and total marks. *(Note: Correlation does not imply causation)*."
            })

    missing_total = df.isnull().sum().sum()
    if missing_total > 0:
        insights.append({
            "title": "Data Quality",
            "text": f"There are **{missing_total} missing values** across the dataset that may affect analysis."
        })
        
    return insights
