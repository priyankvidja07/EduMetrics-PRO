import pandas as pd
import sys
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.student_profile import (
    get_student_list,
    get_student_data,
    get_student_summary,
    get_percentile_rank,
    radar_chart,
    comparison_bar,
    subject_comparison_hist
)

def _sample_df():
    return pd.DataFrame({
        'student_id': ['S01', 'S01', 'S01', 'S02', 'S02', 'S02'],
        'student_name': ['Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob'],
        'enrollment_no': ['E01', 'E01', 'E01', 'E02', 'E02', 'E02'],
        'subject': ['DS', 'ADA', 'ADBMS', 'DS', 'ADA', 'ADBMS'],
        'total_marks': [25.0, 20.0, 28.0, 15.0, 18.0, 22.0],
        'attendance_pct': [90.0, 85.0, 95.0, 70.0, 75.0, 80.0],
        'result': ['Pass', 'Pass', 'Pass', 'Fail', 'Pass', 'Pass']
    })

def test_get_student_list():
    df = _sample_df()
    students = get_student_list(df)
    assert len(students) == 2
    assert students[0][0] == 'S01'

def test_get_student_summary():
    df = _sample_df()
    summary = get_student_summary(df, 'S01')
    assert summary is not None
    assert summary['name'] == 'Alice'
    assert summary['subjects'] == 3
    assert summary['pass_count'] == 3
    assert summary['fail_count'] == 0

def test_get_percentile_rank():
    df = _sample_df()
    rank, total, pct = get_percentile_rank(df, 'S01')
    assert rank == 1
    assert total == 2
    assert pct == 100.0

def test_radar_chart():
    df = _sample_df()
    s1 = get_student_data(df, 'S01')
    fig = radar_chart(s1)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_comparison_bar():
    df = _sample_df()
    fig = comparison_bar(df, 'S01', 'S02')
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_subject_comparison_hist():
    df = _sample_df()
    fig = subject_comparison_hist(df, 'DS', 'ADA')
    assert isinstance(fig, plt.Figure)
    plt.close(fig)
