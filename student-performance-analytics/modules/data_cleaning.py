import pandas as pd
import numpy as np

def clean_data(df, drop_missing=False):
    """
    Cleans the dataframe by standardizing strings, converting types,
    and optionally dropping rows with missing marks.
    """
    if df is None or df.empty:
        return df
        
    clean_df = df.copy()
    
    # Normalize categories
    if 'subject' in clean_df.columns:
        clean_df['subject'] = clean_df['subject'].astype(str).str.strip().str.title()
    
    if 'gender' in clean_df.columns:
        clean_df['gender'] = clean_df['gender'].astype(str).str.strip().str.capitalize()
        
    # Ensure identifiers are strings
    for id_col in ['student_id', 'enrollment_no', 'semester']:
        if id_col in clean_df.columns:
            clean_df[id_col] = clean_df[id_col].astype(str)
            
    # Convert types safely
    numeric_cols = ['internal_marks', 'external_marks', 'total_marks', 'attendance_pct', 'study_hours', 'assignment_score']
    for col in numeric_cols:
        if col in clean_df.columns:
            clean_df[col] = pd.to_numeric(clean_df[col], errors='coerce')
            
    # Drop missing values if requested
    if drop_missing:
        subset = [c for c in ['internal_marks', 'external_marks'] if c in clean_df.columns]
        if subset:
            clean_df = clean_df.dropna(subset=subset)
            
    return clean_df
