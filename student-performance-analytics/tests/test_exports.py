import io
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.exports import df_to_csv_bytes, df_to_excel_bytes, fig_to_png_bytes

def test_df_to_csv_bytes():
    df = pd.DataFrame({'name': ['Alice'], 'score': [90]})
    res = df_to_csv_bytes(df)
    assert isinstance(res, bytes)
    assert b'Alice' in res

def test_df_to_excel_bytes():
    df = pd.DataFrame({'name': ['Bob'], 'score': [85]})
    res = df_to_excel_bytes(df)
    assert isinstance(res, bytes)
    assert len(res) > 0

def test_fig_to_png_bytes():
    fig, ax = plt.subplots()
    ax.plot([1, 2], [3, 4])
    buf = fig_to_png_bytes(fig)
    assert isinstance(buf, io.BytesIO)
    assert len(buf.getvalue()) > 0
    plt.close(fig)
