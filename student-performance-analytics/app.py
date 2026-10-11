import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# IMPORTS
# ==========================================
from modules.data_loader import load_sample, load_uploaded
from modules.data_validation import validate_dataset
from modules.data_cleaning import clean_data
from modules.statistics import get_descriptive_stats, get_subject_wise_stats
from modules.insights import generate_insights
from modules.exports import fig_to_png_bytes, df_to_csv_bytes, df_to_excel_bytes
from modules.theme import get_theme
import modules.visualizations as vis
from modules.student_profile import (
    get_student_list, get_student_data, get_student_summary,
    get_percentile_rank, radar_chart, comparison_bar, subject_comparison_hist
)


# ==========================================
# HELPERS
# ==========================================
def page_header(title, subtitle=''):
    """Reusable page header component."""
    t = get_theme(dark)
    st.markdown(f'<h1 style="font-size:1.5rem;font-weight:700;color:{t["text_primary"]};margin:0 0 4px 0;">{title}</h1>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p style="font-size:0.9rem;color:{t["text_muted"]};margin:0 0 18px 0;">{subtitle}</p>', unsafe_allow_html=True)


def section_title(text):
    """Reusable section sub-heading."""
    t = get_theme(dark)
    st.markdown(f"<h4 style='font-size:0.95rem;font-weight:600;color:{t['text_primary']};margin-bottom:8px;'>{text}</h4>", unsafe_allow_html=True)


def spacer(px=20):
    """Vertical spacer."""
    st.markdown(f"<div style='margin-top:{px}px;'></div>", unsafe_allow_html=True)


def hr():
    """Horizontal rule."""
    t = get_theme(dark)
    st.markdown(f"<hr style='border:0;border-top:1px solid {t['border']};margin:20px 0;'>", unsafe_allow_html=True)


# ==========================================
# STATE INIT
# ==========================================
if 'raw_df' not in st.session_state:
    st.session_state['raw_df'] = None
    st.session_state['clean_df'] = None
    st.session_state['validation_report'] = None
    st.session_state['data_source'] = 'sample'
if 'dark_mode' not in st.session_state:
    st.session_state['dark_mode'] = False

dark = st.session_state.get('dark_mode', False)
t = get_theme(dark)


# ==========================================
# DYNAMIC CSS
# ==========================================
def inject_css(t):
    css = f"""
    <style>
        /* CSS Variables synchronization */
        :root, .stApp {{
            --text-color: {t['text_primary']} !important;
            --background-color: {t['bg_app']} !important;
            --secondary-background-color: {t['bg_sidebar']} !important;
            --primary-color: {t['accent_blue']} !important;
        }}

        /* Smooth slow transition across all theme properties */
        *, *::before, *::after {{
            transition: background-color 0.45s cubic-bezier(0.4, 0, 0.2, 1),
                        color 0.45s cubic-bezier(0.4, 0, 0.2, 1),
                        border-color 0.45s cubic-bezier(0.4, 0, 0.2, 1),
                        box-shadow 0.45s cubic-bezier(0.4, 0, 0.2, 1),
                        fill 0.45s cubic-bezier(0.4, 0, 0.2, 1),
                        stroke 0.45s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* Whole Page & Main Block Container */
        html, body, [class*="css"], .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        .block-container {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            color: {t['text_primary']} !important;
            background-color: {t['bg_app']} !important;
        }}

        /* Subtle smooth content fade animation on theme change */
        .block-container {{
            padding-top: 1.25rem !important;
            padding-bottom: 2rem !important;
            max-width: 95% !important;
            animation: themeFade 0.45s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        @keyframes themeFade {{
            0% {{ opacity: 0.82; }}
            100% {{ opacity: 1; }}
        }}

        /* Chart smooth fade transition */
        [data-testid="stImage"] img, [data-testid="stPyplot"] img, [data-testid="stPlotlyChart"] {{
            animation: chartFadeIn 0.45s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        @keyframes chartFadeIn {{
            0% {{ opacity: 0.65; transform: scale(0.995); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}

        header[data-testid="stHeader"] {{
            height: 1.5rem !important;
            background: transparent !important;
        }}

        /* Hide Deploy */
        .stDeployButton,
        [data-testid="stBaseButton-header"],
        [data-testid="stToolbarActions"],
        header[data-testid="stHeader"] .stDeployButton {{
            display: none !important;
            visibility: hidden !important;
        }}

        /* Sidebar Styling */
        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"],
        [data-testid="stSidebarUserContent"] {{
            background-color: {t['bg_sidebar']} !important;
            border-right: 1px solid {t['border']} !important;
        }}
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown span {{
            color: {t['text_primary']} !important;
        }}
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
            color: {t['text_primary']} !important;
            font-size: 0.92rem !important;
            font-weight: 600 !important;
        }}

        /* Widget Labels - High visibility */
        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] label,
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] span,
        [data-testid="stWidgetLabel"] div,
        label {{
            color: {t['text_primary']} !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            line-height: 1.4 !important;
        }}

        /* MultiSelect & SelectBox Container (React-Aria & BaseWeb) */
        div[data-testid="stMultiSelect"] div[data-rac][role="group"],
        div[data-testid="stSelectbox"] div[data-rac][role="group"],
        .react-aria-ComboBox div[data-rac][role="group"],
        div[data-baseweb="select"] > div {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 6px !important;
            color: {t['text_primary']} !important;
        }}
        div[data-testid="stMultiSelect"] div[data-rac][role="group"]:focus-within,
        div[data-testid="stSelectbox"] div[data-rac][role="group"]:focus-within,
        div[data-baseweb="select"] > div:focus-within {{
            border-color: {t['accent_blue']} !important;
            box-shadow: 0 0 0 1px {t['accent_blue']} !important;
        }}

        /* MultiSelect & SelectBox Inputs */
        div[data-testid="stMultiSelect"] input,
        div[data-testid="stSelectbox"] input,
        .react-aria-ComboBox input,
        div[data-baseweb="select"] input {{
            color: {t['text_primary']} !important;
            background-color: transparent !important;
        }}
        div[data-testid="stMultiSelect"] input::placeholder,
        div[data-testid="stSelectbox"] input::placeholder,
        .react-aria-ComboBox input::placeholder,
        div[data-baseweb="select"] input::placeholder {{
            color: {t['text_muted']} !important;
        }}

        /* MultiSelect Tags / Badges / Pills */
        span[data-tag],
        span[data-baseweb="tag"],
        [data-testid="stMultiSelectTagsContainer"] span[data-tag] {{
            background-color: {t['tag_bg']} !important;
            border: 1px solid {t['tag_border']} !important;
            border-radius: 4px !important;
            color: {t['tag_text']} !important;
            padding: 2px 6px !important;
        }}
        span[data-tag] span,
        span[data-tag] p,
        span[data-tag] div,
        span[data-baseweb="tag"] span,
        span[data-baseweb="tag"] p,
        span[data-baseweb="tag"] div,
        [data-testid="stMultiSelectTagsContainer"] span[data-tag] span {{
            color: {t['tag_text']} !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
        }}
        span[data-tag] button,
        span[data-baseweb="tag"] button {{
            background: transparent !important;
            color: {t['tag_text']} !important;
            border: none !important;
            cursor: pointer !important;
        }}
        span[data-tag] button svg,
        span[data-baseweb="tag"] svg {{
            stroke: {t['tag_text']} !important;
            fill: {t['tag_text']} !important;
        }}
        span[data-tag] button:hover svg,
        span[data-baseweb="tag"] button:hover svg {{
            stroke: {t['text_primary']} !important;
            fill: {t['text_primary']} !important;
        }}

        /* MultiSelect & Selectbox Icons (Clear all & Open arrow) */
        div[data-testid="stMultiSelect"] button[data-rac],
        div[data-testid="stSelectbox"] button[data-rac],
        .react-aria-ComboBox button {{
            background: transparent !important;
            color: {t['text_muted']} !important;
            border: none !important;
        }}
        div[data-testid="stMultiSelect"] button[data-rac] svg,
        div[data-testid="stSelectbox"] button[data-rac] svg,
        .react-aria-ComboBox button svg {{
            fill: {t['text_muted']} !important;
        }}
        div[data-testid="stMultiSelect"] button[data-rac]:hover svg,
        div[data-testid="stSelectbox"] button[data-rac]:hover svg,
        .react-aria-ComboBox button:hover svg {{
            fill: {t['text_primary']} !important;
        }}

        /* Dropdown Popovers & Options */
        div.react-aria-Popover,
        div[data-rac][role="listbox"],
        div[data-rac][role="dialog"],
        ul[role="listbox"],
        div[role="listbox"],
        div[data-baseweb="popover"],
        div[data-baseweb="menu"] {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
            border-radius: 6px !important;
        }}
        [role="option"],
        div[data-rac][role="option"],
        li[role="option"],
        li[data-baseweb="menu-item"] {{
            background-color: {t['bg_card']} !important;
            color: {t['text_primary']} !important;
        }}
        [role="option"] *,
        div[data-rac][role="option"] *,
        li[role="option"] * {{
            color: {t['text_primary']} !important;
        }}
        [role="option"]:hover,
        [role="option"][aria-selected="true"],
        [role="option"][data-focused="true"],
        [role="option"][data-selected="true"],
        div[data-rac][role="option"]:hover,
        div[data-rac][role="option"][data-focused="true"],
        div[data-rac][role="option"][data-selected="true"],
        li[role="option"]:hover,
        li[role="option"][aria-selected="true"],
        li[data-baseweb="menu-item"]:hover {{
            background-color: {t['bg_hover']} !important;
            color: {t['text_primary']} !important;
        }}

        /* Text inputs & Number inputs */
        [data-testid="stTextInputRootElement"],
        [data-testid="stNumberInputContainer"],
        div[data-baseweb="input"] > div,
        div[data-baseweb="base-input"] {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 6px !important;
        }}
        [data-testid="stTextInputRootElement"]:focus-within,
        [data-testid="stNumberInputContainer"]:focus-within {{
            border-color: {t['accent_blue']} !important;
            box-shadow: 0 0 0 1px {t['accent_blue']} !important;
        }}
        input[data-testid="stTextInputField"],
        input[data-testid="stNumberInputField"],
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        input[type="text"],
        input[type="number"],
        input {{
            background-color: {t['bg_card']} !important;
            color: {t['text_primary']} !important;
            border-color: {t['border']} !important;
        }}
        input::placeholder,
        input[data-testid="stTextInputField"]::placeholder {{
            color: {t['text_muted']} !important;
        }}
        [data-testid="stNumberInput"] button {{
            background-color: {t['bg_card']} !important;
            color: {t['text_primary']} !important;
            border-color: {t['border']} !important;
        }}
        [data-testid="stNumberInput"] button:hover {{
            background-color: {t['bg_hover']} !important;
        }}
        [data-testid="stNumberInput"] button svg {{
            fill: {t['text_secondary']} !important;
        }}

        /* Slider Controls */
        div[data-testid="stSlider"] label,
        div[data-testid="stSlider"] label p,
        div[data-testid="stSlider"] div,
        div[data-testid="stSlider"] p {{
            color: {t['text_secondary']} !important;
        }}
        div[data-testid="stSliderThumbValue"],
        div[data-testid="stThumbValue"] {{
            background-color: {t['bg_hover']} !important;
            border: 1px solid {t['border_light']} !important;
            border-radius: 4px !important;
            padding: 1px 6px !important;
        }}
        div[data-testid="stSliderThumbValue"] p,
        div[data-testid="stThumbValue"] p {{
            color: {t['text_primary']} !important;
            font-weight: 600 !important;
        }}
        div[data-testid="stSliderTickBar"],
        div[data-testid="stTickBarMin"],
        div[data-testid="stTickBarMax"] {{
            color: {t['text_muted']} !important;
        }}
        div[data-testid="stSliderTickBar"] p {{
            color: {t['text_muted']} !important;
            font-size: 0.8rem !important;
        }}

        /* Forms & Form Submit Button */
        [data-testid="stForm"],
        .stForm {{
            border: 1px solid {t['border']} !important;
            border-radius: 8px !important;
            background-color: {t['bg_card']} !important;
            padding: 16px !important;
        }}
        [data-testid="stSidebar"] [data-testid="stForm"] {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
        }}

        /* All Buttons (Standard, Form Submit, Secondary, Primary) */
        .stButton > button,
        .stFormSubmitButton > button,
        [data-testid="stFormSubmitButton"] button,
        button[data-testid="stBaseButton-secondaryFormSubmit"],
        button[data-testid="stBaseButton-primaryFormSubmit"],
        button[data-testid="stBaseButton-secondary"],
        button[data-testid="stBaseButton-primary"],
        button[kind="secondaryFormSubmit"],
        button[kind="primaryFormSubmit"] {{
            background-color: {t['btn_bg']} !important;
            color: {t['btn_text']} !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            border-radius: 6px !important;
            border: 1px solid {t['btn_border']} !important;
            padding: 0.55rem 1rem !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12) !important;
            width: 100% !important;
            cursor: pointer !important;
        }}
        .stButton > button:hover,
        .stFormSubmitButton > button:hover,
        [data-testid="stFormSubmitButton"] button:hover,
        button[data-testid="stBaseButton-secondaryFormSubmit"]:hover,
        button[data-testid="stBaseButton-primaryFormSubmit"]:hover,
        button[data-testid="stBaseButton-secondary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover,
        button[kind="secondaryFormSubmit"]:hover,
        button[kind="primaryFormSubmit"]:hover {{
            background-color: {t['btn_hover']} !important;
            border-color: {t['btn_hover']} !important;
        }}
        .stButton > button p,
        .stButton > button span,
        .stButton > button div,
        .stFormSubmitButton > button p,
        .stFormSubmitButton > button span,
        .stFormSubmitButton > button div,
        [data-testid="stFormSubmitButton"] button p,
        [data-testid="stFormSubmitButton"] button span,
        [data-testid="stFormSubmitButton"] button div,
        button[data-testid="stBaseButton-secondaryFormSubmit"] p,
        button[data-testid="stBaseButton-secondaryFormSubmit"] span,
        button[data-testid="stBaseButton-secondaryFormSubmit"] div,
        button[data-testid="stBaseButton-secondary"] p,
        button[data-testid="stBaseButton-secondary"] span,
        button[data-testid="stBaseButton-secondary"] div {{
            color: {t['btn_text']} !important;
            font-weight: 600 !important;
        }}

        /* Download Buttons */
        .stDownloadButton > button,
        [data-testid="stDownloadButton"] button {{
            background-color: {t['btn_excel_bg']} !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            border-radius: 6px !important;
            border: 1px solid {t['btn_excel_hover']} !important;
            padding: 0.55rem 1.1rem !important;
            box-shadow: 0 2px 4px rgba(5, 150, 105, 0.18) !important;
            width: 100% !important;
        }}
        .stDownloadButton > button:hover,
        [data-testid="stDownloadButton"] button:hover {{
            background-color: {t['btn_excel_hover']} !important;
            box-shadow: 0 4px 8px rgba(5, 150, 105, 0.28) !important;
        }}
        .stDownloadButton > button p,
        .stDownloadButton > button span,
        .stDownloadButton > button div,
        [data-testid="stDownloadButton"] button p,
        [data-testid="stDownloadButton"] button span,
        [data-testid="stDownloadButton"] button div {{
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }}

        /* Tables & DataFrames */
        .stDataFrame,
        [data-testid="stDataFrame"],
        [data-testid="stDataFrameResizable"],
        [data-testid="stFullScreenFrame"] {{
            background-color: {t['bg_card']} !important;
            color: {t['text_primary']} !important;
            border-color: {t['border']} !important;
        }}
        [data-testid="stDataFrameResizable"] {{
            border: 1px solid {t['border']} !important;
            border-radius: 0.5rem !important;
        }}

        /* Glide Data Grid Variables Override for HTML5 Canvas */
        .stDataFrame,
        [data-testid="stDataFrame"],
        [data-testid="stDataFrameResizable"],
        .stDataFrameGlideDataEditor,
        div[class*="gdg-"],
        div[data-testid="stFullScreenFrame"] {{
            --gdg-accent-color: {t['accent_blue']} !important;
            --gdg-accent-fg: #FFFFFF !important;
            --gdg-accent-light: rgba(96, 165, 250, 0.18) !important;
            --gdg-text-dark: {t['text_primary']} !important;
            --gdg-text-medium: {t['text_secondary']} !important;
            --gdg-text-light: {t['text_muted']} !important;
            --gdg-text-bubble: {t['text_secondary']} !important;
            --gdg-bg-icon-header: {t['text_muted']} !important;
            --gdg-fg-icon-header: {t['bg_card']} !important;
            --gdg-text-header: {t['text_primary']} !important;
            --gdg-text-group-header: {t['text_primary']} !important;
            --gdg-bg-group-header: {t['bg_app']} !important;
            --gdg-bg-group-header-hovered: {t['bg_hover']} !important;
            --gdg-text-header-selected: #FFFFFF !important;
            --gdg-bg-cell: {t['bg_card']} !important;
            --gdg-bg-cell-medium: {t['bg_card']} !important;
            --gdg-bg-header: {t['bg_app']} !important;
            --gdg-bg-header-has-focus: {t['bg_hover']} !important;
            --gdg-bg-header-hovered: {t['bg_hover']} !important;
            --gdg-bg-bubble: {t['bg_hover']} !important;
            --gdg-bg-bubble-selected: {t['border_light']} !important;
            --gdg-bg-search-result: rgba(96, 165, 250, 0.25) !important;
            --gdg-border-color: {t['border']} !important;
            --gdg-horizontal-border-color: {t['border']} !important;
            --gdg-drilldown-border: {t['border_light']} !important;
            --gdg-link-color: {t['accent_blue']} !important;
            --gdg-resize-indicator-color: {t['accent_blue']} !important;
        }}

        canvas[data-testid="data-grid-canvas"] {{
            background-color: {t['bg_card']} !important;
        }}

        /* DataFrame Toolbar */
        [data-testid="stElementToolbar"] {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 6px !important;
        }}
        [data-testid="stElementToolbar"] button,
        button[data-testid="stBaseButton-elementToolbar"] {{
            color: {t['text_secondary']} !important;
            background-color: transparent !important;
        }}
        [data-testid="stElementToolbar"] button:hover,
        button[data-testid="stBaseButton-elementToolbar"]:hover {{
            color: {t['text_primary']} !important;
            background-color: {t['bg_hover']} !important;
        }}
        [data-testid="stElementToolbar"] svg,
        button[data-testid="stBaseButton-elementToolbar"] svg {{
            fill: currentColor !important;
        }}

        table {{
            background-color: {t['bg_card']} !important;
            color: {t['text_primary']} !important;
        }}
        th, td {{
            color: {t['text_primary']} !important;
            border-color: {t['border']} !important;
        }}

        /* Radio Buttons */
        div[data-testid="stRadio"] label,
        div[data-testid="stRadio"] label p,
        div[data-testid="stRadio"] label span,
        div[data-testid="stRadio"] div {{
            color: {t['text_primary']} !important;
        }}

        /* Toggle & Checkbox */
        [data-testid="stToggle"] label p,
        [data-testid="stToggle"] label span,
        [data-testid="stCheckbox"] label p,
        [data-testid="stCheckbox"] label span {{
            color: {t['text_primary']} !important;
            font-weight: 600 !important;
        }}

        /* Metric Cards */
        [data-testid="stMetric"] {{
            background: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 8px !important;
            padding: 16px !important;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04) !important;
        }}
        [data-testid="stMetricLabel"] p,
        [data-testid="stMetricLabel"] span {{
            color: {t['text_muted']} !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.4px !important;
        }}
        [data-testid="stMetricValue"] div,
        [data-testid="stMetricValue"] span {{
            color: {t['text_primary']} !important;
            font-size: 1.65rem !important;
            font-weight: 700 !important;
        }}

        /* Expanders */
        div[data-testid="stExpander"],
        div[data-testid="stExpander"] details {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 8px !important;
        }}
        div[data-testid="stExpander"] summary,
        div[data-testid="stExpander"] summary p,
        div[data-testid="stExpander"] summary span,
        div[data-testid="stExpander"] summary svg {{
            color: {t['text_primary']} !important;
            fill: {t['text_primary']} !important;
        }}

        /* Tabs */
        [data-testid="stTabs"] [role="tablist"] {{
            border-bottom: 1px solid {t['border']} !important;
        }}
        [data-testid="stTabs"] button[role="tab"],
        button[data-baseweb="tab"] {{
            color: {t['text_secondary']} !important;
            background: transparent !important;
        }}
        [data-testid="stTabs"] button[role="tab"][aria-selected="true"],
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {t['accent_blue']} !important;
            border-bottom-color: {t['accent_blue']} !important;
        }}

        /* File Uploader */
        [data-testid="stFileUploader"] section {{
            background-color: {t['bg_card']} !important;
            border: 1px dashed {t['border']} !important;
            border-radius: 8px !important;
        }}
        [data-testid="stFileUploaderDropzoneInstructions"],
        [data-testid="stFileUploaderDropzoneInstructions"] p,
        [data-testid="stFileUploaderDropzoneInstructions"] span,
        [data-testid="stFileUploaderDropzoneInstructions"] small {{
            color: {t['text_muted']} !important;
        }}

        /* Markdown & Headings */
        h1, h2, h3, h4, h5, h6 {{
            color: {t['text_primary']} !important;
        }}
        p, li, span, small, strong, em {{
            color: {t['text_primary']};
        }}
        a {{
            color: {t['accent_blue']} !important;
        }}
        .stCaption, [data-testid="stCaptionContainer"] p {{
            color: {t['text_muted']} !important;
        }}
        hr {{
            border: 0 !important;
            border-top: 1px solid {t['border']} !important;
            margin: 16px 0 !important;
        }}

        /* Header action elements */
        [data-testid="stHeaderActionElements"] a,
        [data-testid="stHeaderActionElements"] svg {{
            color: {t['text_muted']} !important;
            stroke: {t['text_muted']} !important;
        }}

        /* Cards & Strips */
        .insight-card {{
            background: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-left: 3px solid {t['accent_blue']} !important;
            border-radius: 6px !important;
            padding: 14px 18px !important;
            margin-bottom: 10px !important;
        }}
        .stats-strip {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            padding: 12px 18px;
            background: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 8px !important;
            margin-bottom: 24px !important;
        }}
        .stats-strip-item {{
            font-size: 0.88rem;
            color: {t['text_secondary']} !important;
            font-weight: 500;
        }}

        /* Alerts & Tooltips */
        div[data-testid="stAlert"] {{
            background-color: {t['bg_card']} !important;
            border: 1px solid {t['border']} !important;
            color: {t['text_primary']} !important;
        }}
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] span {{
            color: {t['text_primary']} !important;
        }}
        [data-testid="stTooltipContent"],
        div[data-baseweb="tooltip"],
        div[role="tooltip"] {{
            background-color: {t['bg_hover']} !important;
            color: {t['text_primary']} !important;
            border: 1px solid {t['border']} !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


inject_css(t)


# ==========================================
# SIDEBAR
# ==========================================
# Brand header
st.sidebar.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;padding:2px 0 16px 0;">
    <div style="background:{t['brand_gradient']};border-radius:10px;width:42px;height:42px;display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 2px 6px rgba(15,23,42,0.12);">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{t['brand_icon']}" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/>
            <path d="M6 6h10"/><path d="M6 10h10"/><path d="M6 14h6"/>
        </svg>
    </div>
    <div style="overflow:hidden;">
        <div style="font-size:1.05rem;font-weight:700;color:{t['brand_text']};letter-spacing:-0.2px;line-height:1.25;">
            EduMetrics <span style="font-size:0.72rem;font-weight:600;color:{t['brand_badge_text']};background:{t['brand_badge_bg']};border:1px solid {t['brand_badge_border']};padding:1px 6px;border-radius:4px;vertical-align:middle;margin-left:2px;">PRO</span>
        </div>
        <p style="margin:2px 0 0 0;font-size:0.75rem;color:{t['text_muted']};font-weight:500;letter-spacing:0.1px;">Academic Performance Intelligence</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Dark mode toggle - bound directly to session state for instant single-pass update
st.sidebar.toggle("🌙 Dark Mode", key="dark_mode")

# Data source
data_source = st.sidebar.radio("Data Source", ["Semester 5 Dataset", "Upload Custom CSV"], label_visibility="collapsed")

if data_source == "Semester 5 Dataset":
    if st.session_state['data_source'] != 'sample' or st.session_state['raw_df'] is None:
        df, err = load_sample()
        if err:
            st.error(err)
        else:
            st.session_state['raw_df'] = df
            st.session_state['clean_df'] = clean_data(df)
            st.session_state['validation_report'] = validate_dataset(df)
            st.session_state['data_source'] = 'sample'
else:
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file is not None:
        df, err = load_uploaded(uploaded_file)
        if err:
            st.error(err)
        else:
            st.session_state['raw_df'] = df
            st.session_state['clean_df'] = clean_data(df)
            st.session_state['validation_report'] = validate_dataset(df)
            st.session_state['data_source'] = 'upload'

st.sidebar.markdown(f"<hr style='border:0;border-top:1px solid {t['border']};margin:14px 0;'>", unsafe_allow_html=True)

# ==========================================
# FILTERS
# ==========================================
st.sidebar.markdown(f"<p style='color:{t['text_label']};font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.4px;margin-bottom:8px;'>Filters</p>", unsafe_allow_html=True)

df_clean = st.session_state.get('clean_df')
if df_clean is None and st.session_state.get('raw_df') is not None:
    df_clean = clean_data(st.session_state['raw_df'])
    st.session_state['clean_df'] = df_clean

if df_clean is not None and not df_clean.empty:
    with st.sidebar.form("filter_form"):
        subjects = sorted(df_clean['subject'].dropna().unique().tolist()) if 'subject' in df_clean.columns else []
        selected_subjects = st.multiselect("Subjects", subjects, default=subjects)

        if 'result' in df_clean.columns:
            res_series = df_clean['result'].fillna('NA').replace({'N/A': 'NA'})
            raw_res = res_series.unique().tolist()
            order = ['Pass', 'Fail', 'NA']
            results = [r for r in order if r in raw_res] + [r for r in raw_res if r not in order]
        else:
            results = ['Pass', 'Fail', 'NA']

        selected_results = st.multiselect("Result Status", results, default=results)

        marks_min, marks_max = 0.0, 100.0
        if 'total_marks' in df_clean.columns:
            valid_marks = df_clean['total_marks'].dropna()
            if not valid_marks.empty:
                marks_min = float(valid_marks.min())
                marks_max = float(valid_marks.max())

        selected_marks = st.slider("Total Marks Range", min_value=0.0, max_value=100.0, value=(marks_min, marks_max))
        apply_filters = st.form_submit_button("Apply Filters")

    df_filtered = df_clean.copy()
    if 'result' in df_filtered.columns:
        df_filtered['result'] = df_filtered['result'].fillna('NA').replace({'N/A': 'NA'})
    if selected_subjects and 'subject' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['subject'].isin(selected_subjects)]
    if selected_results and 'result' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['result'].isin(selected_results)]
    if 'total_marks' in df_filtered.columns:
        df_filtered = df_filtered[
            (df_filtered['total_marks'].isna()) |
            ((df_filtered['total_marks'] >= selected_marks[0]) &
             (df_filtered['total_marks'] <= selected_marks[1]))]
else:
    df_filtered = pd.DataFrame()

# ==========================================
# NAVIGATION
# ==========================================
st.sidebar.markdown(f"<hr style='border:0;border-top:1px solid {t['border']};margin:14px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color:{t['text_label']};font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.4px;margin-bottom:8px;'>Navigation</p>", unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", [
    "Overview",
    "Dataset Explorer",
    "Statistical Analysis",
    "Student Profile",
    "Comparative Analysis",
    "Matplotlib Studio",
    "Insights & Findings",
    "About Project"
], label_visibility="collapsed")

# Sidebar footer
st.sidebar.markdown(f"""
<div style="position:fixed;bottom:0;padding:10px 16px;font-size:0.7rem;color:{t['text_muted']};border-top:1px solid {t['border']};background:{t['bg_sidebar']};width:inherit;max-width:inherit;">
    v1.0 &nbsp;•&nbsp; Built with Streamlit &nbsp;•&nbsp; Python + Pandas
</div>
""", unsafe_allow_html=True)

# ==========================================
# GUARD
# ==========================================
if df_filtered.empty and page not in ("About Project",):
    st.warning("No records match your selected filters. Please adjust the settings in the sidebar.")
    st.stop()


# ==========================================
# PAGE: OVERVIEW
# ==========================================
if page == "Overview":
    page_header("Student Academic Performance", "Aggregate summary metrics and performance distributions")

    # --- Metric cards ---
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Records", len(df_filtered))

    if 'student_id' in df_filtered.columns:
        col2.metric("Enrolled Students", df_filtered['student_id'].nunique())
    else:
        col2.metric("Enrolled Students", "N/A")

    if 'total_marks' in df_filtered.columns:
        vm = df_filtered['total_marks'].dropna()
        col3.metric("Average Marks", f"{vm.mean():.1f}" if not vm.empty else "N/A")
        col4.metric("Median Marks", f"{vm.median():.1f}" if not vm.empty else "N/A")
    else:
        col3.metric("Average Marks", "N/A")
        col4.metric("Median Marks", "N/A")

    if 'attendance_pct' in df_filtered.columns:
        va = df_filtered['attendance_pct'].dropna()
        col5.metric("Avg Attendance", f"{va.mean():.1f}%" if not va.empty else "N/A")
    else:
        col5.metric("Avg Attendance", "N/A")

    if 'result' in df_filtered.columns:
        passes = (df_filtered['result'] == 'Pass').sum()
        total_graded = df_filtered['result'].isin(['Pass', 'Fail']).sum()
        pass_rate = (passes / total_graded * 100) if total_graded > 0 else 0
        col6.metric("Pass Rate", f"{pass_rate:.1f}%")
    else:
        col6.metric("Pass Rate", "N/A")

    # --- Quick stats strip ---
    if 'subject' in df_filtered.columns and 'total_marks' in df_filtered.columns:
        subj_avgs = df_filtered.groupby('subject')['total_marks'].mean()
        top_subj = subj_avgs.idxmax() if not subj_avgs.empty else '—'
        weak_subj = subj_avgs.idxmin() if not subj_avgs.empty else '—'
        absent_count = (df_filtered['result'] == 'NA').sum() if 'result' in df_filtered.columns else 0

        st.markdown(f"""
        <div class="stats-strip">
            <span class="stats-strip-item">🏆 <strong>Top Subject:</strong> {top_subj} ({subj_avgs.max():.1f})</span>
            <span class="stats-strip-item">⚠️ <strong>Needs Attention:</strong> {weak_subj} ({subj_avgs.min():.1f})</span>
            <span class="stats-strip-item">📉 <strong>Absent Records:</strong> {absent_count}</span>
        </div>
        """, unsafe_allow_html=True)

    spacer(8)

    # --- Charts row 1 ---
    c1, c2 = st.columns(2)
    with c1:
        section_title("Subject Average Marks")
        fig1 = vis.bar_subject_avg(df_filtered, dark_mode=dark)
        st.pyplot(fig1)
        plt.close(fig1)
    with c2:
        section_title("Score Distribution")
        fig2 = vis.histogram_marks(df_filtered, dark_mode=dark)
        st.pyplot(fig2)
        plt.close(fig2)

    spacer(8)

    # --- Charts row 2 ---
    c3, c4 = st.columns(2)
    with c3:
        section_title("Attendance vs Total Marks")
        fig3 = vis.scatter_xy(df_filtered, 'attendance_pct', 'total_marks',
                              title="Attendance vs Total Marks", show_trend=True, dark_mode=dark)
        st.pyplot(fig3)
        plt.close(fig3)
    with c4:
        section_title("Result Distribution")
        fig_donut = vis.donut_result(df_filtered, dark_mode=dark)
        st.pyplot(fig_donut)
        plt.close(fig_donut)

    spacer(8)

    # --- Charts row 3 ---
    c5, c6 = st.columns(2)
    with c5:
        section_title("Correlation Matrix")
        fig4 = vis.heatmap_corr(df_filtered, dark_mode=dark)
        st.pyplot(fig4)
        plt.close(fig4)
    with c6:
        section_title("Result Breakdown")
        fig_rb = vis.result_bar(df_filtered, dark_mode=dark)
        st.pyplot(fig_rb)
        plt.close(fig_rb)

    # --- Top 5 / Bottom 5 ---
    if 'student_id' in df_filtered.columns and 'total_marks' in df_filtered.columns:
        spacer(8)
        with st.expander("🏆 Top 5 & Bottom 5 Performers", expanded=False):
            student_avgs = df_filtered.groupby('student_id').agg(
                Name=('student_name', 'first') if 'student_name' in df_filtered.columns else ('student_id', 'first'),
                Avg_Marks=('total_marks', 'mean'),
                Subjects=('subject', 'count')
            ).sort_values('Avg_Marks', ascending=False)

            student_avgs['Avg_Marks'] = student_avgs['Avg_Marks'].round(1)

            t5, b5 = st.columns(2)
            with t5:
                st.markdown(f"<p style='font-weight:600;color:{t['pass_color']};'>▲ Top 5</p>", unsafe_allow_html=True)
                st.dataframe(student_avgs.head(5), use_container_width=True)
            with b5:
                st.markdown(f"<p style='font-weight:600;color:{t['fail_color']};'>▼ Bottom 5</p>", unsafe_allow_html=True)
                st.dataframe(student_avgs.tail(5), use_container_width=True)


# ==========================================
# PAGE: DATASET EXPLORER
# ==========================================
elif page == "Dataset Explorer":
    page_header("Dataset Explorer", f"Displaying {len(df_filtered)} records")

    # Search bar
    search_query = st.text_input("🔍 Search student name, enrollment, or subject:", "")
    if search_query.strip():
        mask = pd.Series([False] * len(df_filtered), index=df_filtered.index)
        for col in df_filtered.columns:
            mask = mask | df_filtered[col].astype(str).str.contains(search_query.strip(), case=False, na=False)
        df_display = df_filtered[mask]
        st.caption(f"Showing {len(df_display)} matching records")
    else:
        df_display = df_filtered

    display_cols = st.multiselect("Columns to display:", df_display.columns.tolist(), default=df_display.columns.tolist())

    # Conditional formatting via styled dataframe
    def style_table(df_sub):
        styled = df_sub.style.set_properties(**{'background-color': t['bg_card'], 'color': t['text_primary']})
        if 'total_marks' in df_sub.columns:
            def color_marks(val):
                try:
                    v = float(val)
                    if v >= 60:
                        return f'color: {t["pass_color"]}; font-weight: 600'
                    elif v >= 40:
                        return f'color: {t["accent_amber"]}; font-weight: 600'
                    else:
                        return f'color: {t["fail_color"]}; font-weight: 600'
                except (ValueError, TypeError):
                    return ''
            styled = styled.map(color_marks, subset=['total_marks'] if 'total_marks' in df_sub.columns else [])
        if 'result' in df_sub.columns:
            def color_result(val):
                if val == 'Pass':
                    return f'color: {t["pass_color"]}; font-weight: 700'
                elif val == 'Fail':
                    return f'color: {t["fail_color"]}; font-weight: 700'
                return f'color: {t["na_color"]}; font-weight: 600'
            styled = styled.map(color_result, subset=['result'] if 'result' in df_sub.columns else [])

        styled = styled.set_table_styles([
            {'selector': 'th', 'props': [('background-color', t['bg_card']), ('color', t['text_primary']), ('border-color', t['border'])]},
            {'selector': 'td', 'props': [('background-color', t['bg_card']), ('color', t['text_primary']), ('border-color', t['border'])]}
        ])
        return styled

    st.dataframe(style_table(df_display[display_cols]), use_container_width=True, height=450)
    st.caption("💡 Click any column header to sort")

    col_dl1, col_dl2, _ = st.columns([1.3, 1.1, 2.6])
    with col_dl1:
        st.download_button(
            label="📊 Download Excel (.xlsx)",
            data=df_to_excel_bytes(df_display[display_cols]),
            file_name="filtered_student_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with col_dl2:
        st.download_button(
            label="📄 Download CSV",
            data=df_to_csv_bytes(df_display[display_cols]),
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )


# ==========================================
# PAGE: STATISTICAL ANALYSIS
# ==========================================
elif page == "Statistical Analysis":
    page_header("Descriptive Statistics", "Measures of central tendency, spread, and shape")

    ignored_cols = {'student_id', 'enrollment_no', 'semester'}
    num_cols = [c for c in df_filtered.select_dtypes(include=['float64', 'int64']).columns if c.lower() not in ignored_cols]

    if num_cols:
        default_idx = num_cols.index('total_marks') if 'total_marks' in num_cols else 0
        selected_col = st.selectbox("Select Numeric Variable:", num_cols, index=default_idx)
        stats = get_descriptive_stats(df_filtered, selected_col)

        c1, c2 = st.columns(2)
        with c1:
            section_title("Central Tendency & Variation")
            disp_items = ['Count', 'Mean', 'Median', 'Mode', 'Min', 'Max', 'Range', 'Variance (Sample)', 'Std Dev (Sample)']
            disp_df = pd.DataFrame([{"Metric": k, "Value": f"{v:.2f}" if isinstance(v, (int, float)) else str(v)}
                                    for k, v in stats.items() if k in disp_items])
            st.dataframe(disp_df, use_container_width=True, hide_index=True)

        with c2:
            section_title("Quartiles & Shape")
            shape_items = ['Q1 (25th)', 'Q2 (Median)', 'Q3 (75th)', 'IQR', '10th Percentile', '90th Percentile', 'Skewness', 'Kurtosis', 'Missing Count']
            shape_df = pd.DataFrame([{"Metric": k, "Value": f"{v:.2f}" if isinstance(v, (int, float)) else str(v)}
                                     for k, v in stats.items() if k in shape_items])
            st.dataframe(shape_df, use_container_width=True, hide_index=True)

        hr()
        section_title("Subject Breakdown")
        subj_stats = get_subject_wise_stats(df_filtered, selected_col)
        st.dataframe(subj_stats, use_container_width=True, hide_index=True)
    else:
        st.info("No numeric fields available.")


# ==========================================
# PAGE: STUDENT PROFILE
# ==========================================
elif page == "Student Profile":
    page_header("Student Profile", "Individual report card, radar chart, and percentile ranking")

    students = get_student_list(df_filtered)
    if not students:
        st.info("No students found in the current filtered data.")
        st.stop()

    options = {label: sid for sid, label in students}
    selected_label = st.selectbox("Select Student:", list(options.keys()))
    selected_sid = options[selected_label]

    summary = get_student_summary(df_filtered, selected_sid)
    if summary is None:
        st.warning("No data found for the selected student.")
        st.stop()

    rank, total, percentile = get_percentile_rank(df_filtered, selected_sid)

    # --- Info cards ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Student", summary.get('name', 'N/A'))
    m2.metric("Avg Marks", f"{summary.get('avg_marks', 'N/A')}")
    m3.metric("Avg Attendance", f"{summary.get('avg_attendance', 'N/A')}%")
    if rank:
        m4.metric("Class Rank", f"{rank} / {total}", f"Top {percentile}%")
    else:
        m4.metric("Class Rank", "N/A")

    spacer(12)

    # --- Result summary strip ---
    pass_c = summary.get('pass_count', 0)
    fail_c = summary.get('fail_count', 0)
    na_c = summary.get('na_count', 0)
    st.markdown(f"""
    <div class="stats-strip">
        <span class="stats-strip-item" style="color:{t['pass_color']};">✅ Passed: <strong>{pass_c}</strong></span>
        <span class="stats-strip-item" style="color:{t['fail_color']};">❌ Failed: <strong>{fail_c}</strong></span>
        <span class="stats-strip-item" style="color:{t['na_color']};">➖ Absent: <strong>{na_c}</strong></span>
        <span class="stats-strip-item">📚 Subjects: <strong>{summary.get('subjects', 0)}</strong></span>
    </div>
    """, unsafe_allow_html=True)

    spacer(8)

    # --- Radar + subject table ---
    c_radar, c_table = st.columns([1, 1.2])
    with c_radar:
        section_title("Subject Performance Radar")
        sdf = get_student_data(df_filtered, selected_sid)
        fig_radar = radar_chart(sdf, dark_mode=dark)
        st.pyplot(fig_radar)
        plt.close(fig_radar)

    with c_table:
        section_title("Subject-wise Breakdown")
        if not sdf.empty:
            show_cols = [c for c in ['subject', 'internal_marks', 'external_marks', 'total_marks',
                                     'attendance_pct', 'result'] if c in sdf.columns]
            st.dataframe(sdf[show_cols].reset_index(drop=True), use_container_width=True, hide_index=True)


# ==========================================
# PAGE: COMPARATIVE ANALYSIS
# ==========================================
elif page == "Comparative Analysis":
    page_header("Comparative Analysis", "Side-by-side comparison of students or subjects")

    compare_mode = st.radio("Compare:", ["Two Students", "Two Subjects"], horizontal=True)

    if compare_mode == "Two Students":
        students = get_student_list(df_filtered)
        if len(students) < 2:
            st.info("Need at least 2 students to compare.")
            st.stop()

        options = {label: sid for sid, label in students}
        labels = list(options.keys())
        c1, c2 = st.columns(2)
        with c1:
            s1_label = st.selectbox("Student A:", labels, index=0)
        with c2:
            default_b = 1 if len(labels) > 1 else 0
            s2_label = st.selectbox("Student B:", labels, index=default_b)

        sid1 = options[s1_label]
        sid2 = options[s2_label]

        if sid1 == sid2:
            st.warning("Please select two different students.")
        else:
            # Side-by-side metrics
            sum1 = get_student_summary(df_filtered, sid1)
            sum2 = get_student_summary(df_filtered, sid2)
            r1 = get_percentile_rank(df_filtered, sid1)
            r2 = get_percentile_rank(df_filtered, sid2)

            mc1, mc2 = st.columns(2)
            with mc1:
                st.markdown(f"<div style='text-align:center;font-weight:700;color:{t['accent_blue']};font-size:1rem;margin-bottom:8px;'>{sum1['name']}</div>", unsafe_allow_html=True)
                st.metric("Avg Marks", sum1.get('avg_marks', 'N/A'))
                st.metric("Rank", f"{r1[0]} / {r1[1]}" if r1[0] else 'N/A')
            with mc2:
                st.markdown(f"<div style='text-align:center;font-weight:700;color:{t['accent_amber']};font-size:1rem;margin-bottom:8px;'>{sum2['name']}</div>", unsafe_allow_html=True)
                st.metric("Avg Marks", sum2.get('avg_marks', 'N/A'))
                st.metric("Rank", f"{r2[0]} / {r2[1]}" if r2[0] else 'N/A')

            spacer(12)
            section_title("Marks Comparison")
            fig_cmp = comparison_bar(df_filtered, sid1, sid2, dark_mode=dark)
            st.pyplot(fig_cmp)
            plt.close(fig_cmp)

    else:  # Two Subjects
        if 'subject' not in df_filtered.columns:
            st.info("No subject column found.")
            st.stop()

        subjects = sorted(df_filtered['subject'].dropna().unique().tolist())
        if len(subjects) < 2:
            st.info("Need at least 2 subjects to compare.")
            st.stop()

        c1, c2 = st.columns(2)
        with c1:
            subj1 = st.selectbox("Subject A:", subjects, index=0)
        with c2:
            subj2 = st.selectbox("Subject B:", subjects, index=min(1, len(subjects) - 1))

        if subj1 == subj2:
            st.warning("Please select two different subjects.")
        else:
            # Subject metrics
            d1 = df_filtered[df_filtered['subject'] == subj1]['total_marks'].dropna()
            d2 = df_filtered[df_filtered['subject'] == subj2]['total_marks'].dropna()

            mc1, mc2 = st.columns(2)
            with mc1:
                st.markdown(f"<div style='text-align:center;font-weight:700;color:{t['accent_blue']};font-size:1rem;margin-bottom:8px;'>{subj1}</div>", unsafe_allow_html=True)
                st.metric("Mean", f"{d1.mean():.1f}" if not d1.empty else "N/A")
                st.metric("Median", f"{d1.median():.1f}" if not d1.empty else "N/A")
                st.metric("Std Dev", f"{d1.std():.1f}" if not d1.empty else "N/A")
            with mc2:
                st.markdown(f"<div style='text-align:center;font-weight:700;color:{t['accent_amber']};font-size:1rem;margin-bottom:8px;'>{subj2}</div>", unsafe_allow_html=True)
                st.metric("Mean", f"{d2.mean():.1f}" if not d2.empty else "N/A")
                st.metric("Median", f"{d2.median():.1f}" if not d2.empty else "N/A")
                st.metric("Std Dev", f"{d2.std():.1f}" if not d2.empty else "N/A")

            spacer(12)
            section_title("Distribution Overlay")
            fig_sh = subject_comparison_hist(df_filtered, subj1, subj2, dark_mode=dark)
            st.pyplot(fig_sh)
            plt.close(fig_sh)


# ==========================================
# PAGE: MATPLOTLIB STUDIO
# ==========================================
elif page == "Matplotlib Studio":
    page_header("Matplotlib Studio", "General plotting and figure export")

    chart_type = st.selectbox("Chart Type:", [
        "Subject Average (Bar Chart)",
        "Marks Distribution (Histogram)",
        "Attendance vs Marks (Scatter Plot)",
        "Result Distribution (Bar Chart)"
    ])

    col_settings, col_chart = st.columns([1, 2.5])

    with col_settings:
        section_title("Options")
        chart_title = st.text_input("Title", value=chart_type.split(" (")[0])
        show_grid = st.checkbox("Show Grid", value=True)

        bins = 10
        show_mean = True
        show_median = True
        show_trend = False
        category_col = 'subject'

        if "Histogram" in chart_type:
            bins = st.slider("Bins", min_value=5, max_value=30, value=12)
            show_mean = st.checkbox("Show Mean", value=True)
            show_median = st.checkbox("Show Median", value=True)
        elif "Scatter" in chart_type:
            cat_options = [c for c in ['subject', 'gender', 'result'] if c in df_filtered.columns]
            category_col = st.selectbox("Color Category", cat_options, index=0 if cat_options else 0)
            show_trend = st.checkbox("Fit Trendline", value=True)

    with col_chart:
        if "Subject Average" in chart_type:
            fig = vis.bar_subject_avg(df_filtered, title=chart_title, show_grid=show_grid, dark_mode=dark)
        elif "Histogram" in chart_type:
            fig = vis.histogram_marks(df_filtered, bins=bins, title=chart_title,
                                      show_mean=show_mean, show_median=show_median, dark_mode=dark)
        elif "Scatter" in chart_type:
            fig = vis.scatter_xy(df_filtered, 'attendance_pct', 'total_marks',
                                 category_col=category_col, title=chart_title,
                                 show_trend=show_trend, dark_mode=dark)
            if show_grid and fig.axes:
                fig.axes[0].grid(True)
        else:
            fig = vis.result_bar(df_filtered, dark_mode=dark)

        st.pyplot(fig)
        st.download_button(label="Download PNG", data=fig_to_png_bytes(fig),
                           file_name="matplotlib_chart.png", mime="image/png")
        plt.close(fig)




# ==========================================
# PAGE: INSIGHTS & FINDINGS
# ==========================================
elif page == "Insights & Findings":
    page_header("Insights & Findings", "Analytical observations derived from active data")

    insights = generate_insights(df_filtered)

    for ins in insights:
        if isinstance(ins, dict):
            st.markdown(f"""
            <div class="insight-card">
                <h5 style="margin:0 0 4px 0;color:{t['text_primary']};font-size:0.95rem;font-weight:600;">{ins['title']}</h5>
                <p style="margin:0;color:{t['text_secondary']};font-size:0.9rem;">{ins['text']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(ins)

    st.markdown(f"""
    <div style="background:{t['bg_sidebar']};border-radius:6px;padding:10px 14px;margin-top:20px;color:{t['text_muted']};font-size:0.8rem;">
        Note: Insights are computed based on the selected filters. Correlation metrics describe linear associations and do not imply causality.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PAGE: ABOUT PROJECT
# ==========================================
elif page == "About Project":
    page_header("About the Project", "Academic Information & Student Details")

    st.markdown(f"""
    <div style="background:{t['bg_card']};border:1px solid {t['border']};border-left:4px solid {t['accent_blue']};border-radius:8px;padding:20px 24px;margin-bottom:24px;box-shadow:0 2px 6px rgba(0,0,0,0.08);">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
            <div style="font-size:1.6rem;background:{t['bg_hover']};border:1px solid {t['border_light']};border-radius:8px;width:44px;height:44px;display:flex;align-items:center;justify-content:center;">🎓</div>
            <div>
                <h3 style="margin:0;font-size:1.15rem;font-weight:700;color:{t['text_primary']};">Project Presentation Details</h3>
                <p style="margin:2px 0 0 0;font-size:0.82rem;color:{t['text_muted']};">Data Science Academic Project & Viva Submission</p>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));gap:14px;">
            <div style="background:{t['bg_hover']};border:1px solid {t['border_light']};border-radius:6px;padding:12px 16px;">
                <div style="font-size:0.75rem;text-transform:uppercase;color:{t['text_muted']};font-weight:600;letter-spacing:0.4px;">Presented By</div>
                <div style="font-size:1.02rem;font-weight:700;color:{t['text_primary']};margin-top:4px;">UBHADIYA HARIKRUSHN DHIRAJLAL</div>
            </div>
            <div style="background:{t['bg_hover']};border:1px solid {t['border_light']};border-radius:6px;padding:12px 16px;">
                <div style="font-size:0.75rem;text-transform:uppercase;color:{t['text_muted']};font-weight:600;letter-spacing:0.4px;">Enrollment Number</div>
                <div style="font-size:1.02rem;font-weight:700;color:{t['accent_blue']};margin-top:4px;">240310116034</div>
            </div>
            <div style="background:{t['bg_hover']};border:1px solid {t['border_light']};border-radius:6px;padding:12px 16px;">
                <div style="font-size:0.75rem;text-transform:uppercase;color:{t['text_muted']};font-weight:600;letter-spacing:0.4px;">Course & Semester</div>
                <div style="font-size:0.95rem;font-weight:600;color:{t['text_primary']};margin-top:4px;">B.E. — Semester 5 (Data Science)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    ### Gujarat Technological University (GTU)
    - **Programme:** Bachelor of Engineering (BE)
    - **Semester:** 5
    - **Subject:** Data Science (BE05016021)
    - **Project Title:** Student Performance Analytics Dashboard Using Matplotlib & Seaborn
    - **Presented By:** UBHADIYA HARIKRUSHN DHIRAJLAL (Enrollment No: **240310116034**)

    ---

    #### Core Objectives
    1. **Data Handling:** Safe dataset loading, cleaning, and absent (`AB`) student tracking without arbitrary imputation.
    2. **Descriptive Analytics:** Computation of mean, median, IQR, percentiles, sample variance, skewness, and kurtosis.
    3. **Visualizations:** Distinct implementation of Matplotlib for general plotting and Seaborn for statistical distributions.
    4. **Interactive Filters:** Dynamic query refinement across subjects, scores, and results.

    ---

    #### Technology Stack
    - Python 3.11+
    - Streamlit
    - Pandas & NumPy
    - Matplotlib & Seaborn
    - SciPy
    - Pytest
    """)
