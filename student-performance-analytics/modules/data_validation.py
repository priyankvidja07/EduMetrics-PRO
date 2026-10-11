import pandas as pd
import numpy as np

REQUIRED_COLUMNS = [
    'student_id', 'student_name', 'semester', 'subject',
    'internal_marks', 'external_marks', 'total_marks', 
    'attendance_pct', 'study_hours'
]

def validate_dataset(df):
    """
    Validates the dataset for required columns, missing values, duplicates, and out-of-range bounds.
    Returns a dictionary of issues.
    """
    report = {
        'is_valid': True,
        'missing_columns': [],
        'missing_values': {},
        'out_of_range': [],
        'duplicates': 0,
        'duplicate_student_subject': 0
    }
    
    if df is None or df.empty:
        report['is_valid'] = False
        return report

    # Check missing columns
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            report['missing_columns'].append(col)
            report['is_valid'] = False

    if not report['is_valid']:
        return report
        
    # Check missing values
    missing = df.isnull().sum()
    report['missing_values'] = missing[missing > 0].to_dict()
    
    # Check bounds
    if 'internal_marks' in df.columns:
        invalid_internal = df[(df['internal_marks'] < 0) | (df['internal_marks'] > 30)]
        if not invalid_internal.empty:
            report['out_of_range'].append(f"{len(invalid_internal)} rows with internal marks out of 0-30")
            
    if 'external_marks' in df.columns:
        invalid_external = df[(df['external_marks'] < 0) | (df['external_marks'] > 70)]
        if not invalid_external.empty:
            report['out_of_range'].append(f"{len(invalid_external)} rows with external marks out of 0-70")
            
    if 'attendance_pct' in df.columns:
        invalid_att = df[(df['attendance_pct'] < 0) | (df['attendance_pct'] > 100)]
        if not invalid_att.empty:
            report['out_of_range'].append(f"{len(invalid_att)} rows with attendance out of 0-100")
            
    # Check duplicates
    report['duplicates'] = int(df.duplicated().sum())
    
    if 'student_id' in df.columns and 'subject' in df.columns:
        report['duplicate_student_subject'] = int(df.duplicated(subset=['student_id', 'subject']).sum())

    return report
