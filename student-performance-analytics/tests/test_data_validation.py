import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.data_validation import validate_dataset

def test_validate_valid_dataset():
    df = pd.DataFrame({
        'student_id': ['1', '2'],
        'student_name': ['A', 'B'],
        'semester': [5, 5],
        'subject': ['Math', 'Science'],
        'internal_marks': [20, 25],
        'external_marks': [60, 65],
        'total_marks': [80, 90],
        'attendance_pct': [85, 95],
        'study_hours': [5, 6]
    })
    report = validate_dataset(df)
    assert report['is_valid'] == True
    assert len(report['missing_columns']) == 0
    assert len(report['out_of_range']) == 0

def test_validate_missing_columns():
    df = pd.DataFrame({'student_id': ['1']})
    report = validate_dataset(df)
    assert report['is_valid'] == False
    assert 'subject' in report['missing_columns']

def test_validate_out_of_range():
    df = pd.DataFrame({
        'student_id': ['1'], 'student_name': ['A'], 'semester': [5], 'subject': ['Math'],
        'internal_marks': [35],  # Invalid > 30
        'external_marks': [60], 'total_marks': [95], 'attendance_pct': [105], # Invalid > 100
        'study_hours': [5]
    })
    report = validate_dataset(df)
    assert len(report['out_of_range']) > 0
    assert any('internal marks' in msg for msg in report['out_of_range'])
    assert any('attendance' in msg for msg in report['out_of_range'])

def test_empty_dataset():
    df = pd.DataFrame()
    report = validate_dataset(df)
    assert report['is_valid'] == False
