"""
Student Profile module — individual report card, radar chart, rank, comparison.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_student_list(df):
    """Return sorted list of (student_id, display_label) tuples."""
    if df is None or df.empty or 'student_id' not in df.columns:
        return []

    cols = ['student_id']
    if 'student_name' in df.columns:
        cols.append('student_name')

    students = df[cols].drop_duplicates().sort_values('student_id')

    if 'student_name' in cols:
        return [(row['student_id'], f"{row['student_name']}  ({row['student_id']})")
                for _, row in students.iterrows()]
    return [(row['student_id'], str(row['student_id']))
            for _, row in students.iterrows()]


def get_student_data(df, student_id):
    """Get all records for a specific student."""
    if df is None or df.empty or 'student_id' not in df.columns:
        return pd.DataFrame()
    return df[df['student_id'] == student_id].copy()


def get_student_summary(df, student_id):
    """Return a summary dict for the student."""
    sdf = get_student_data(df, student_id)
    if sdf.empty:
        return None

    summary = {
        'student_id': student_id,
        'name': sdf['student_name'].iloc[0] if 'student_name' in sdf.columns else 'N/A',
        'enrollment': sdf['enrollment_no'].iloc[0] if 'enrollment_no' in sdf.columns else 'N/A',
        'subjects': len(sdf),
    }

    if 'total_marks' in sdf.columns:
        valid = sdf['total_marks'].dropna()
        summary['avg_marks'] = round(valid.mean(), 1) if not valid.empty else None
        summary['max_marks'] = round(valid.max(), 1) if not valid.empty else None
        summary['min_marks'] = round(valid.min(), 1) if not valid.empty else None

    if 'attendance_pct' in sdf.columns:
        valid = sdf['attendance_pct'].dropna()
        summary['avg_attendance'] = round(valid.mean(), 1) if not valid.empty else None

    if 'result' in sdf.columns:
        vc = sdf['result'].value_counts()
        summary['pass_count'] = int(vc.get('Pass', 0))
        summary['fail_count'] = int(vc.get('Fail', 0))
        summary['na_count'] = int(vc.get('NA', 0))

    return summary


def get_percentile_rank(df, student_id):
    """
    Calculate the student's rank and percentile based on average total marks.
    Returns (rank, total_students, percentile) or (None, None, None).
    """
    if df is None or df.empty:
        return None, None, None
    if 'student_id' not in df.columns or 'total_marks' not in df.columns:
        return None, None, None

    avgs = df.groupby('student_id')['total_marks'].mean().dropna().sort_values(ascending=False)
    if student_id not in avgs.index:
        return None, None, None

    rank = int((avgs > avgs[student_id]).sum() + 1)
    total = len(avgs)
    percentile = round((1 - (rank - 1) / total) * 100, 1) if total > 0 else 0
    return rank, total, percentile


def radar_chart(student_df, dark_mode=False):
    """Create a radar / spider chart of the student's marks across subjects."""
    bg = '#1E293B' if dark_mode else '#FFFFFF'
    txt = '#F1F5F9' if dark_mode else '#0F172A'
    grid_c = '#475569' if dark_mode else '#E2E8F0'
    fill_c = '#60A5FA' if dark_mode else '#2563EB'
    line_c = '#93C5FD' if dark_mode else '#1D4ED8'

    if student_df.empty or 'subject' not in student_df.columns or 'total_marks' not in student_df.columns:
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)
        ax.text(0.5, 0.5, 'Insufficient data', ha='center', va='center', color=txt)
        ax.axis('off')
        return fig

    sm = student_df.groupby('subject')['total_marks'].first().dropna()
    if len(sm) < 3:
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)
        ax.text(0.5, 0.5, 'Need ≥ 3 subjects for radar chart', ha='center', va='center', color=txt)
        ax.axis('off')
        return fig

    cats = sm.index.tolist()
    vals = sm.values.tolist() + sm.values.tolist()[:1]
    N = len(cats)
    angles = [n / N * 2 * np.pi for n in range(N)] + [0]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    ax.plot(angles, vals, 'o-', linewidth=2.2, color=line_c, markersize=7, markerfacecolor=fill_c, markeredgecolor='#FFFFFF', markeredgewidth=1)
    ax.fill(angles, vals, alpha=0.18, color=fill_c)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(cats, fontsize=9, color=txt, fontweight='600')
    ax.set_ylim(0, max(max(vals) * 1.15, 30))
    tick_c = '#94A3B8' if dark_mode else '#475569'
    ax.tick_params(axis='y', labelsize=7.5, colors=tick_c)
    ax.grid(color=grid_c, linestyle='--', alpha=0.6)
    ax.spines['polar'].set_color(grid_c)
    ax.set_title('Subject Performance Radar', pad=22, fontsize=13, fontweight='bold', color=txt)
    fig.tight_layout()
    return fig


def comparison_bar(df, sid1, sid2, dark_mode=False):
    """Grouped bar chart comparing two students across subjects."""
    bg = '#1E293B' if dark_mode else '#FFFFFF'
    txt = '#F1F5F9' if dark_mode else '#0F172A'
    grid_c = '#475569' if dark_mode else '#E2E8F0'

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    s1 = get_student_data(df, sid1)
    s2 = get_student_data(df, sid2)

    if s1.empty or s2.empty or 'subject' not in df.columns or 'total_marks' not in df.columns:
        ax.text(0.5, 0.5, 'Insufficient data for comparison', ha='center', va='center', color=txt)
        ax.axis('off')
        return fig

    m1 = s1.groupby('subject')['total_marks'].first().dropna()
    m2 = s2.groupby('subject')['total_marks'].first().dropna()
    common = sorted(set(m1.index) & set(m2.index))

    if not common:
        ax.text(0.5, 0.5, 'No common subjects', ha='center', va='center', color=txt)
        ax.axis('off')
        return fig

    x = np.arange(len(common))
    w = 0.35
    c1 = '#60A5FA' if dark_mode else '#2563EB'
    c2 = '#FBBF24' if dark_mode else '#D97706'

    n1 = s1['student_name'].iloc[0] if 'student_name' in s1.columns else str(sid1)
    n2 = s2['student_name'].iloc[0] if 'student_name' in s2.columns else str(sid2)

    b1 = ax.bar(x - w / 2, [m1[s] for s in common], w, label=n1, color=c1, edgecolor='#FFFFFF', linewidth=1)
    b2 = ax.bar(x + w / 2, [m2[s] for s in common], w, label=n2, color=c2, edgecolor='#FFFFFF', linewidth=1)

    ax.set_xticks(x)
    ax.set_xticklabels(common, rotation=25, ha='right', fontsize=9, color=txt)
    ax.set_ylabel('Total Marks', fontsize=10, color=txt)
    ax.set_title('Student Comparison', pad=14, fontsize=12, fontweight='bold', color=txt)
    ax.legend(frameon=True, facecolor=bg, edgecolor=grid_c, fontsize=9, labelcolor=txt)
    ax.tick_params(colors=txt, labelsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(grid_c)
    ax.spines['bottom'].set_color(grid_c)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color=grid_c)
    ax.set_axisbelow(True)

    for bar in list(b1) + list(b2):
        h = bar.get_height()
        ax.annotate(f'{h:.0f}', xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords='offset points',
                    ha='center', va='bottom', fontsize=8, color=txt, fontweight='bold')

    fig.tight_layout()
    return fig


def subject_comparison_hist(df, subj1, subj2, dark_mode=False):
    """Overlaid histogram comparing mark distributions of two subjects."""
    bg = '#1E293B' if dark_mode else '#FFFFFF'
    txt = '#F1F5F9' if dark_mode else '#0F172A'
    grid_c = '#475569' if dark_mode else '#E2E8F0'

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    if df.empty or 'subject' not in df.columns or 'total_marks' not in df.columns:
        ax.text(0.5, 0.5, 'Insufficient data', ha='center', va='center', color=txt)
        ax.axis('off')
        return fig

    d1 = df[df['subject'] == subj1]['total_marks'].dropna()
    d2 = df[df['subject'] == subj2]['total_marks'].dropna()

    c1 = '#60A5FA' if dark_mode else '#2563EB'
    c2 = '#FBBF24' if dark_mode else '#D97706'

    ax.hist(d1, bins=12, alpha=0.65, label=subj1, color=c1, edgecolor='#FFFFFF', linewidth=0.8)
    ax.hist(d2, bins=12, alpha=0.65, label=subj2, color=c2, edgecolor='#FFFFFF', linewidth=0.8)

    ax.set_title(f'{subj1} vs {subj2} — Mark Distribution', pad=14, fontsize=12, fontweight='bold', color=txt)
    ax.set_xlabel('Total Marks', fontsize=10, color=txt)
    ax.set_ylabel('Frequency', fontsize=10, color=txt)
    ax.legend(frameon=True, facecolor=bg, edgecolor=grid_c, fontsize=9, labelcolor=txt)
    ax.tick_params(colors=txt, labelsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(grid_c)
    ax.spines['bottom'].set_color(grid_c)
    ax.grid(axis='y', linestyle='--', alpha=0.5, color=grid_c)
    ax.set_axisbelow(True)

    fig.tight_layout()
    return fig
