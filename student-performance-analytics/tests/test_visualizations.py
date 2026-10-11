import pandas as pd
import sys
import os
import matplotlib

# Set backend to avoid UI popping up during tests
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.visualizations import bar_subject_avg, heatmap_corr

def test_bar_subject_avg():
    df = pd.DataFrame({
        'subject': ['Math', 'Math', 'Science'],
        'total_marks': [80, 90, 70]
    })
    fig = bar_subject_avg(df)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_heatmap_corr_empty():
    df = pd.DataFrame()
    fig = heatmap_corr(df)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)

def test_heatmap_corr_valid():
    df = pd.DataFrame({
        'marks1': [10, 20, 30],
        'marks2': [30, 20, 10]
    })
    fig = heatmap_corr(df)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)
