import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis

def get_descriptive_stats(df, column):
    """Calculates descriptive statistics for a numerical column."""
    if df is None or df.empty or column not in df.columns:
        return {}
        
    s = df[column].dropna()
    if s.empty:
        return {"Count": 0}
        
    stats = {
        "Count": len(s),
        "Mean": np.mean(s),
        "Median": np.median(s),
        "Min": np.min(s),
        "Max": np.max(s),
        "Range": np.max(s) - np.min(s),
    }
    
    # Mode handling
    mode_val = s.mode()
    stats["Mode"] = mode_val.iloc[0] if not mode_val.empty else "N/A"
    
    # Variation
    if len(s) > 1:
        stats["Variance (Sample)"] = np.var(s, ddof=1)
        stats["Std Dev (Sample)"] = np.std(s, ddof=1)
    else:
        stats["Variance (Sample)"] = "Insufficient data"
        stats["Std Dev (Sample)"] = "Insufficient data"
        
    # Quartiles & Percentiles
    stats["Q1 (25th)"] = np.percentile(s, 25)
    stats["Q2 (Median)"] = np.percentile(s, 50)
    stats["Q3 (75th)"] = np.percentile(s, 75)
    stats["IQR"] = stats["Q3 (75th)"] - stats["Q1 (25th)"]
    
    stats["10th Percentile"] = np.percentile(s, 10)
    stats["90th Percentile"] = np.percentile(s, 90)
    
    # Skewness and Kurtosis
    if np.std(s) == 0:
        stats["Skewness"] = "Undefined (Constant)"
        stats["Kurtosis"] = "Undefined (Constant)"
    elif len(s) < 3:
        stats["Skewness"] = "Insufficient data"
        stats["Kurtosis"] = "Insufficient data"
    else:
        stats["Skewness"] = float(skew(s, bias=False))
        stats["Kurtosis"] = float(kurtosis(s, bias=False))
        
    stats["Missing Count"] = df[column].isnull().sum()
    
    return stats

def get_subject_wise_stats(df, value_col="total_marks"):
    """Calculates summary statistics grouped by subject."""
    if df is None or df.empty or 'subject' not in df.columns or value_col not in df.columns:
        return pd.DataFrame()
        
    summary = df.groupby('subject')[value_col].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).reset_index()
    
    summary = summary.rename(columns={
        'count': 'Students',
        'mean': 'Avg Marks',
        'median': 'Median Marks',
        'std': 'Std Dev'
    })
    return summary
