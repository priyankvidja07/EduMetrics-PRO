"""
Centralized color theme tokens for Student Performance Analytics.
Supports Light and Dark modes.
"""

# ==========================================
# LIGHT MODE
# ==========================================
LIGHT = {
    # Backgrounds
    'bg_app': '#F8FAFC',
    'bg_card': '#FFFFFF',
    'bg_sidebar': '#F1F5F9',
    'bg_input': '#FFFFFF',
    'bg_hover': '#F1F5F9',

    # Borders
    'border': '#E2E8F0',
    'border_light': '#F1F5F9',

    # Text
    'text_primary': '#0F172A',
    'text_secondary': '#334155',
    'text_muted': '#64748B',
    'text_label': '#475569',

    # Accents
    'accent_blue': '#2563EB',
    'accent_teal': '#0D9488',
    'accent_amber': '#D97706',
    'accent_rose': '#E11D48',
    'accent_violet': '#7C3AED',
    'accent_emerald': '#059669',
    'accent_sky': '#0284C7',

    # Status
    'pass_color': '#059669',
    'fail_color': '#E11D48',
    'na_color': '#94A3B8',

    # Chart
    'chart_bg': '#FFFFFF',
    'chart_grid': '#E2E8F0',
    'chart_edge': '#CBD5E1',
    'chart_text': '#334155',
    'chart_title': '#0F172A',

    # Tags / badges - lighter, softer text
    'tag_bg': '#F1F5F9',
    'tag_text': '#64748B',
    'tag_border': '#E2E8F0',

    # Buttons - clean, modern, professional blue in light mode
    'btn_bg': '#2563EB',
    'btn_hover': '#1D4ED8',
    'btn_text': '#FFFFFF',
    'btn_border': '#2563EB',
    'btn_excel_bg': '#059669',
    'btn_excel_hover': '#047857',

    # Sidebar brand
    'brand_gradient': 'linear-gradient(135deg, #1E293B 0%, #334155 100%)',
    'brand_text': '#0F172A',
    'brand_icon': '#F8FAFC',
    'brand_badge_bg': '#EFF6FF',
    'brand_badge_text': '#2563EB',
    'brand_badge_border': '#DBEAFE',

    # Metric card accent borders (left-side color accents)
    'metric_accents': ['#2563EB', '#0D9488', '#D97706', '#7C3AED', '#059669', '#E11D48'],

    # Histogram fill
    'hist_fill': '#3B82F6',
    'mean_line': '#DC2626',
    'median_line': '#059669',
}

# ==========================================
# DARK MODE
# ==========================================
DARK = {
    # Backgrounds
    'bg_app': '#0F172A',
    'bg_card': '#1E293B',
    'bg_sidebar': '#1E293B',
    'bg_input': '#334155',
    'bg_hover': '#334155',

    # Borders
    'border': '#334155',
    'border_light': '#475569',

    # Text
    'text_primary': '#F1F5F9',
    'text_secondary': '#CBD5E1',
    'text_muted': '#94A3B8',
    'text_label': '#CBD5E1',

    # Accents
    'accent_blue': '#60A5FA',
    'accent_teal': '#2DD4BF',
    'accent_amber': '#FBBF24',
    'accent_rose': '#FB7185',
    'accent_violet': '#A78BFA',
    'accent_emerald': '#34D399',
    'accent_sky': '#38BDF8',

    # Status
    'pass_color': '#34D399',
    'fail_color': '#FB7185',
    'na_color': '#64748B',

    # Chart
    'chart_bg': '#1E293B',
    'chart_grid': '#334155',
    'chart_edge': '#475569',
    'chart_text': '#CBD5E1',
    'chart_title': '#F1F5F9',

    # Tags / badges
    'tag_bg': '#334155',
    'tag_text': '#E2E8F0',
    'tag_border': '#475569',

    # Buttons
    'btn_bg': '#2563EB',
    'btn_hover': '#1D4ED8',
    'btn_text': '#FFFFFF',
    'btn_border': '#2563EB',
    'btn_excel_bg': '#059669',
    'btn_excel_hover': '#047857',

    # Sidebar brand
    'brand_gradient': 'linear-gradient(135deg, #334155 0%, #475569 100%)',
    'brand_text': '#F1F5F9',
    'brand_icon': '#F8FAFC',
    'brand_badge_bg': '#1E3A5F',
    'brand_badge_text': '#60A5FA',
    'brand_badge_border': '#2563EB',

    # Metric card accent borders (left-side color accents)
    'metric_accents': ['#60A5FA', '#2DD4BF', '#FBBF24', '#A78BFA', '#34D399', '#FB7185'],

    # Histogram fill
    'hist_fill': '#60A5FA',
    'mean_line': '#FB7185',
    'median_line': '#34D399',
}

# ==========================================
# CHART PALETTES
# ==========================================
SUBJECT_PALETTE = ['#2563EB', '#0D9488', '#D97706', '#E11D48', '#7C3AED', '#0284C7', '#4F46E5']
SUBJECT_PALETTE_DARK = ['#60A5FA', '#2DD4BF', '#FBBF24', '#FB7185', '#A78BFA', '#38BDF8', '#818CF8']

RESULT_COLORS = {'Pass': '#059669', 'Fail': '#E11D48', 'NA': '#94A3B8'}
RESULT_COLORS_DARK = {'Pass': '#34D399', 'Fail': '#FB7185', 'NA': '#64748B'}


def get_theme(dark_mode=False):
    """Return the active color theme dictionary."""
    return DARK if dark_mode else LIGHT


def get_palette(dark_mode=False):
    """Return the chart subject color palette."""
    return SUBJECT_PALETTE_DARK if dark_mode else SUBJECT_PALETTE


def get_result_colors(dark_mode=False):
    """Return the result status color map."""
    return RESULT_COLORS_DARK if dark_mode else RESULT_COLORS
