import pandas as pd
import os
import streamlit as st

def load_sample():
    """Loads the bundled sample dataset."""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sample_student_performance.csv')
    try:
        df = pd.read_csv(file_path)
        return df, None
    except Exception as e:
        return None, f"Error loading sample data: {str(e)}"

def load_uploaded(file):
    """Loads a user-uploaded CSV file."""
    try:
        df = pd.read_csv(file)
        return df, None
    except Exception as e:
        return None, f"Error reading uploaded file: {str(e)}"
