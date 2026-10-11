import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.statistics import get_descriptive_stats

def test_get_descriptive_stats():
    df = pd.DataFrame({'marks': [10, 20, 30, 40, 50]})
    stats = get_descriptive_stats(df, 'marks')
    
    assert stats['Mean'] == 30.0
    assert stats['Median'] == 30.0
    assert stats['Min'] == 10
    assert stats['Max'] == 50
    assert stats['Count'] == 5

def test_constant_column():
    df = pd.DataFrame({'marks': [20, 20, 20, 20]})
    stats = get_descriptive_stats(df, 'marks')
    
    assert stats['Std Dev (Sample)'] == 0.0
    assert 'Undefined' in str(stats['Skewness'])
    assert 'Undefined' in str(stats['Kurtosis'])

def test_empty_dataset():
    df = pd.DataFrame()
    stats = get_descriptive_stats(df, 'marks')
    assert stats == {}
