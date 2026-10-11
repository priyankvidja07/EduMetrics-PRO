import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from modules.theme import get_theme, get_palette, get_result_colors

# Professional academic styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

# ==========================================
# HELPERS
# ==========================================

def _setup_fig(figsize=(8, 4.8), dark_mode=False):
    """Create a figure + axes with themed background."""
    t = get_theme(dark_mode)
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(t['chart_bg'])
    ax.set_facecolor(t['chart_bg'])
    return fig, ax, t


def _style_axes(ax, t, title='', xlabel='', ylabel='', grid_axis='y'):
    """Apply consistent styling to axes."""
    ax.set_title(title, pad=14, fontsize=12, fontweight='bold', color=t['chart_title'])
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, color=t['chart_text'], fontweight='500')
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, color=t['chart_text'], fontweight='500')
    ax.tick_params(colors=t['chart_text'], labelsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(t['chart_edge'])
    ax.spines['bottom'].set_color(t['chart_edge'])
    if grid_axis:
        ax.grid(axis=grid_axis, linestyle='--', alpha=0.5, color=t['chart_grid'])
        ax.set_axisbelow(True)


def _legend(ax, t, **kwargs):
    """Apply consistent legend styling."""
    defaults = dict(frameon=True, facecolor=t['chart_bg'], edgecolor=t['chart_edge'],
                    fontsize=8.5, loc='best', labelcolor=t['chart_text'])
    defaults.update(kwargs)
    ax.legend(**defaults)


# ==========================================
# MATPLOTLIB CHARTS
# ==========================================

def bar_subject_avg(df, title="Average Marks by Subject", show_grid=True, dark_mode=False):
    fig, ax, t = _setup_fig(dark_mode=dark_mode)
    palette = get_palette(dark_mode)

    if df.empty or 'subject' not in df.columns or 'total_marks' not in df.columns:
        ax.text(0.5, 0.5, "Insufficient data", ha='center', va='center', color=t['text_muted'])
        ax.axis('off')
        return fig

    avg = df.groupby('subject')['total_marks'].mean().sort_values(ascending=False)
    colors = [palette[i % len(palette)] for i in range(len(avg))]
    bars = ax.bar(avg.index, avg.values, color=colors, edgecolor='#FFFFFF', linewidth=1.2, width=0.55)

    _style_axes(ax, t, title=title, ylabel='Mean Total Marks', xlabel='Subject',
                grid_axis='y' if show_grid else None)
    plt.xticks(rotation=25, ha='right')

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}', xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords='offset points',
                    ha='center', va='bottom', fontsize=9, color=t['chart_title'], fontweight='bold')

    fig.tight_layout()
    return fig


def histogram_marks(df, column='total_marks', bins=10, title="Marks Distribution",
                    show_mean=True, show_median=True, dark_mode=False):
    fig, ax, t = _setup_fig(dark_mode=dark_mode)

    if df.empty or column not in df.columns:
        ax.text(0.5, 0.5, "Insufficient data", ha='center', va='center', color=t['text_muted'])
        ax.axis('off')
        return fig

    data = df[column].dropna()
    if data.empty:
        ax.text(0.5, 0.5, "No valid numeric data", ha='center', va='center', color=t['text_muted'])
        ax.axis('off')
        return fig

    ax.hist(data, bins=bins, color=t['hist_fill'], edgecolor='#FFFFFF', linewidth=1.2, alpha=0.88)

    if show_mean:
        m = data.mean()
        ax.axvline(m, color=t['mean_line'], linestyle='--', linewidth=2.0, label=f'Mean: {m:.1f}')
    if show_median:
        md = data.median()
        ax.axvline(md, color=t['median_line'], linestyle=':', linewidth=2.2, label=f'Median: {md:.1f}')

    _style_axes(ax, t, title=title,
                xlabel=column.replace('_', ' ').title(), ylabel='Student Frequency')

    if show_mean or show_median:
        _legend(ax, t, loc='upper right')

    fig.tight_layout()
    return fig


def scatter_xy(df, x_col, y_col, category_col='subject', title="Scatter Plot",
               show_trend=False, dark_mode=False):
    fig, ax, t = _setup_fig(dark_mode=dark_mode)
    palette = get_palette(dark_mode)

    if df.empty or x_col not in df.columns or y_col not in df.columns:
        ax.text(0.5, 0.5, "Insufficient data", ha='center', va='center', color=t['text_muted'])
        ax.axis('off')
        return fig

    cols_check = [x_col, y_col]
    if category_col and category_col in df.columns:
        cols_check.append(category_col)

    valid = df.dropna(subset=cols_check).copy()
    if valid.empty:
        ax.text(0.5, 0.5, "No valid pairs", ha='center', va='center', color=t['text_muted'])
        ax.axis('off')
        return fig

    if category_col and category_col in valid.columns:
        cats = sorted(valid[category_col].unique())
        cmap = {c: palette[i % len(palette)] for i, c in enumerate(cats)}
        for cat in cats:
            sub = valid[valid[category_col] == cat]
            ax.scatter(sub[x_col], sub[y_col], label=str(cat), color=cmap[cat],
                       alpha=0.85, edgecolors='#FFFFFF', s=55, linewidth=1.0)
    else:
        ax.scatter(valid[x_col], valid[y_col], color=palette[0],
                   alpha=0.85, edgecolors='#FFFFFF', s=55, linewidth=1.0)

    if show_trend and len(valid) > 1 and valid[x_col].std() > 0:
        z = np.polyfit(valid[x_col], valid[y_col], 1)
        p = np.poly1d(z)
        xv = np.linspace(valid[x_col].min(), valid[x_col].max(), 100)
        ax.plot(xv, p(xv), color=t['chart_title'], linestyle='--', linewidth=1.8, label='Overall Trend')

    _style_axes(ax, t, title=title,
                xlabel=x_col.replace('_', ' ').title(),
                ylabel=y_col.replace('_', ' ').title())
    _legend(ax, t)

    fig.tight_layout()
    return fig


def result_bar(df, horizontal=False, dark_mode=False):
    fig, ax, t = _setup_fig(figsize=(8, 3.8), dark_mode=dark_mode)
    rc = get_result_colors(dark_mode)

    if df.empty or 'result' not in df.columns:
        ax.text(0.5, 0.5, "Insufficient data", ha='center', va='center', color=t['text_muted'])
        ax.axis('off')
        return fig

    counts = df['result'].value_counts()
    colors = [rc.get(r, t['text_muted']) for r in counts.index]

    if horizontal:
        ax.barh(counts.index, counts.values, color=colors, height=0.5, edgecolor='#FFFFFF', linewidth=1.2)
        _style_axes(ax, t, title='Result Breakdown', xlabel='Count', grid_axis='x')
    else:
        bars = ax.bar(counts.index, counts.values, color=colors, width=0.45, edgecolor='#FFFFFF', linewidth=1.2)
        _style_axes(ax, t, title='Result Breakdown', ylabel='Count', grid_axis='y')
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f'{int(h)}', xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 4), textcoords='offset points',
                        ha='center', va='bottom', fontsize=9, color=t['chart_title'], fontweight='bold')

    fig.tight_layout()
    return fig


def donut_result(df, dark_mode=False):
    """Pass / Fail / NA donut chart for Overview page."""
    t = get_theme(dark_mode)
    rc = get_result_colors(dark_mode)

    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor(t['chart_bg'])
    ax.set_facecolor(t['chart_bg'])

    if df.empty or 'result' not in df.columns:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center', color=t['text_muted'])
        ax.axis('off')
        return fig

    order = ['Pass', 'Fail', 'NA']
    counts = df['result'].value_counts()
    labels = [r for r in order if r in counts.index]
    sizes = [counts[r] for r in labels]
    colors = [rc.get(r, t['text_muted']) for r in labels]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=90, pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor=t['chart_bg'], linewidth=2.5))

    for txt in texts:
        txt.set_color(t['chart_text'])
        txt.set_fontsize(10)
        txt.set_fontweight('600')
    for at in autotexts:
        at.set_color(t['chart_title'])
        at.set_fontsize(9)
        at.set_fontweight('bold')

    ax.set_title('Result Distribution', pad=16, fontsize=12, fontweight='bold', color=t['chart_title'])
    fig.tight_layout()
    return fig


# ==========================================
# SEABORN CHARTS
# ==========================================

def heatmap_corr(df, title="Correlation Heatmap", dark_mode=False):
    fig, ax, t = _setup_fig(figsize=(8, 5.2), dark_mode=dark_mode)

    numerics = df.select_dtypes(include=[np.number])
    ignored = {'student_id', 'enrollment_no', 'semester'}
    valid_cols = [c for c in numerics.columns if c.lower() not in ignored]

    if len(valid_cols) < 2:
        ax.text(0.5, 0.5, "Not enough numeric variables", ha='center', va='center', color=t['text_muted'])
        ax.axis('off')
        return fig

    corr = numerics[valid_cols].corr()
    sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, fmt='.2f', ax=ax,
                vmin=-1, vmax=1, linewidths=1.0, linecolor=t['chart_bg'],
                cbar_kws={'shrink': 0.85, 'label': 'Pearson r'},
                annot_kws={'size': 9, 'weight': 'bold'})

    _style_axes(ax, t, title=title, grid_axis=None)
    ax.tick_params(colors=t['chart_text'], labelsize=8.5)
    plt.xticks(rotation=25, ha='right')
    plt.yticks(rotation=0)

    # Style colorbar ticks and label for dark mode visibility
    if ax.collections and ax.collections[0].colorbar:
        cb = ax.collections[0].colorbar
        cb.ax.tick_params(colors=t['chart_text'], labelsize=8)
        cb.ax.yaxis.label.set_color(t['chart_text'])
        cb.outline.set_edgecolor(t['chart_edge'])

    fig.tight_layout()
    return fig



