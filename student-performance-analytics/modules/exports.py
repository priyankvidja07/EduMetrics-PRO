import io
import pandas as pd
import matplotlib.pyplot as plt

def fig_to_png_bytes(fig):
    """Converts a Matplotlib figure to a BytesIO object for Streamlit download."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    return buf

def df_to_csv_bytes(df):
    """Converts a DataFrame to a BytesIO object for Streamlit download."""
    return df.to_csv(index=False).encode('utf-8')

def df_to_excel_bytes(df):
    """Converts a DataFrame to an Excel (.xlsx) BytesIO object for Streamlit download."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Student_Performance')
    buf.seek(0)
    return buf.getvalue()

