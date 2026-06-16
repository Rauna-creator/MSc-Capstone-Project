import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------
st.set_page_config(
    page_title='NMC Medical Aid Dashboard',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# ----------------------------------------------------------------
# LOAD DATA AND MODEL
# ----------------------------------------------------------------
df = pd.read_csv('NMC_survey_cleaned.csv')
model = joblib.load('model_rf.pkl')
feature_names = joblib.load('feature_names.pkl')

# ----------------------------------------------------------------
# COLOUR PALETTE (consistent across all charts)
# ----------------------------------------------------------------
NAVY = '#003366'
MID_BLUE = '#5B8DB8'
LIGHT_BLUE = '#AEC6CF'
ACCENT = '#2E86C1'
BG_CARD = 'rgba(255,255,255,0.03)'

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#E0E0E0', size=13),
    title_font=dict(size=16, color='#FFFFFF'),
    margin=dict(l=10, r=10, t=50, b=10),
)

# ----------------------------------------------------------------
# CUSTOM CSS
# ----------------------------------------------------------------
st.markdown(f"""
<style>
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    .hero {{
        padding: 2rem 2.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, {NAVY} 0%, {MID_BLUE} 100%);
        margin-bottom: 1.5rem;
    }}
    .hero h1 {{
        color: white;
        margin: 0;
        font-size: 2rem;
    }}
    .hero p {{
        color: rgba(255,255,255,0.85);
        margin-top: 0.5rem;
        font-size: 1rem;
    }}
    .metric-card {{
        background: {BG_CARD};
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        text-align: left;
    }}
    .metric-card .label {{
        font-size: 0.8rem;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }}
    .metric-card .value {{
        font-size: 1.9rem;
        font-weight: 700;
        color: #FFFFFF;
    }}
    .section-card {{
        background: {BG_CARD};
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }}
    .section-card h3 {{
        margin-top: 0;
        color: #FFFFFF;
    }}
    .section-card p.subtitle {{
        color: #9CA3AF;
        font-size: 0.9rem;
        margin-top: -0.5rem;
        margin-bottom: 1rem;
    }}
    .pill {{
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        background: rgba(91,141,184,0.2);
        color: {LIGHT_BLUE};
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# HERO / INTRO
# ----------------------------------------------------------------
st.markdown("""
<div class="hero">
    <span class="pill">NMC \u2022 MARKETING ANALYTICS</span>
    <h1>Medical Aid Uptake Dashboard</h1>
    <p>Predicting which young Namibians are most likely to sign up for medical aid, what's
    stopping the rest, and how to talk to each group \u2014 built from 553 survey responses,
    three machine learning models, and natural language analysis of open-text feedback.</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# SECTION 1 - OVERVIEW METRICS
# ----------------------------------------------------------------
total = len(df)
no_aid = len(df[df['has_medical_aid'] == 'No'])
yes_aid = len(df[df['has_medical_aid'] == 'Yes'])
pct_no = round((no_aid / total) * 100)

col1, col2, col3, col4 = st.columns(4)
metrics = [
    ('Total Respondents', f'{total}'),
    ('Without Medical Aid', f'{no_aid}'),
    ('With Medical Aid', f'{yes_aid}'),
    ('% Without Medical Aid', f'{pct_no}%'),
]
for col, (label, value) in zip([col1, col2, col3, col4], metrics):
    col.markdown(f"""
    <div class="metric-card">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------------------------------------------------------
# SECTION 2 - SEGMENT EXPLORER (interactive)
# ----------------------------------------------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('### Segment Explorer')
st.markdown('<p class="subtitle">Filter respondents by age, employment and income to see how medical aid membership varies by segment.</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    age_filter = st.selectbox('Age Group', ['All'] + sorted(df['age'].dropna().unique().tolist()))
with col2:
    employment_filter = st.selectbox('Employment Status', ['All'] + sorted(df['employment'].dropna().unique().tolist()))
with col3:
    income_filter = st.selectbox('Income Bracket', ['All'] + sorted(df['income'].dropna().unique().tolist()))

filtered = df.copy()
if age_filter != 'All':
    filtered = filtered[filtered['age'] == age_filter]
if employment_filter != 'All':
    filtered = filtered[filtered['employment'] == employment_filter]
if income_filter != 'All':
    filtered = filtered[filtered['income'] == income_filter]

if len(filtered) > 0:
    seg_pct_no = round((len(filtered[filtered['has_medical_aid'] == 'No']) / len(filtered)) * 100)
    seg_pct_yes = 100 - seg_pct_no

    left, right = st.columns([1, 2])

    with left:
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom: 0.8rem;">
            <div class="label">Respondents in Segment</div>
            <div class="value">{len(filtered)}</div>
        </div>
        <div class="metric-card" style="margin-bottom: 0.8rem;">
            <div class="label">Without Medical Aid</div>
            <div class="value">{seg_pct_no}%</div>
        </div>
        <div class="metric-card">
            <div class="label">With Medical Aid</div>
            <div class="value">{seg_pct_yes}%</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        seg_counts = filtered['has_medical_aid'].value_counts().reindex(['Yes', 'No']).fillna(0)
        fig = go.Figure(data=[
            go.Bar(
                x=seg_counts.index,
                y=seg_counts.values,
                marker_color=[LIGHT_BLUE, NAVY],
                text=seg_counts.values,
                textposition='outside',
                width=0.5,
            )
        ])
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title='Medical Aid Membership \u2014 Selected Segment',
            height=320,
            xaxis_title='',
            yaxis_title='Number of Respondents',
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info('No respondents match this combination of filters.')

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------
# SECTION 3 - MODEL PERFORMANCE
# ----------------------------------------------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('### Model Performance')
st.markdown('<p class="subtitle">Three classification models were trained and compared. XGBoost was selected as the best performing model.</p>', unsafe_allow_html=True)

model_names = ['Logistic Regression', 'Random Forest', 'XGBoost']
model_scores = [91, 88, 92]
model_colors = [LIGHT_BLUE, MID_BLUE, NAVY]

fig = go.Figure(data=[
    go.Bar(
        x=model_names,
        y=model_scores,
        marker_color=model_colors,
        text=[f'{s}%' for s in model_scores],
        textposition='outside',
        width=0.45,
    )
])
fig.update_layout(
    **PLOTLY_LAYOUT,
    height=320,
    yaxis=dict(range=[75, 100], title='Accuracy (%)'),
    xaxis_title='',
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('<span class="pill">XGBoost selected \u2014 92% accuracy</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------
# SECTION 4 - FEATURE IMPORTANCE
# ----------------------------------------------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('### What Drives Medical Aid Uptake')
st.markdown('<p class="subtitle">Feature importance from the model shows which factors matter most in predicting medical aid membership.</p>', unsafe_allow_html=True)

importance = pd.Series(model.feature_importances_, index=feature_names)
importance = importance.sort_values(ascending=True).tail(10)

fig = go.Figure(data=[
    go.Bar(
        x=importance.values,
        y=importance.index,
        orientation='h',
        marker_color=ACCENT,
    )
])
fig.update_layout(
    **PLOTLY_LAYOUT,
    height=420,
    xaxis_title='Importance Score',
    yaxis_title='',
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------
# SECTION 5 - TOP BARRIERS & WILLINGNESS TO PAY (side by side)
# ----------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('### Top Barriers to Uptake')
    st.markdown('<p class="subtitle">Most common reasons given by respondents without medical aid.</p>', unsafe_allow_html=True)

    no_aid_df = df[df['has_medical_aid'] == 'No']
    barriers = no_aid_df['why_no_medical_aid'].dropna().str.split(';').explode().str.strip()
    barrier_counts = barriers.value_counts().head(5).sort_values(ascending=True)

    fig = go.Figure(data=[
        go.Bar(
            x=barrier_counts.values,
            y=barrier_counts.index,
            orientation='h',
            marker_color=MID_BLUE,
        )
    ])
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=380,
        xaxis_title='Number of Respondents',
        yaxis_title='',
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('### Willingness to Pay')
    st.markdown('<p class="subtitle">What respondents say they would pay for medical aid per month.</p>', unsafe_allow_html=True)

    order = ['Under N$500', 'N$500 - N$1,000', 'N$1,000 - N$2,000', 'Above N$2,000', 'I would not pay for it at all']
    wtp_counts = df['willingness_to_pay'].value_counts().reindex(order).fillna(0)

    fig = go.Figure(data=[
        go.Bar(
            x=wtp_counts.index,
            y=wtp_counts.values,
            marker_color=ACCENT,
        )
    ])
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=380,
        xaxis_title='',
        yaxis_title='Number of Respondents',
        xaxis=dict(tickangle=-20),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------
# SECTION 6 - NLP INSIGHTS
# ----------------------------------------------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('### NLP Insights')

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('**Sentiment Analysis**')
    st.markdown('<p class="subtitle">How young Namibians feel about medical aid in their own words.</p>', unsafe_allow_html=True)

    sentiment_counts = df['sentiment'].value_counts().reindex(['Negative', 'Neutral', 'Positive']).fillna(0)

    fig = go.Figure(data=[
        go.Bar(
            x=sentiment_counts.index,
            y=sentiment_counts.values,
            marker_color=[NAVY, MID_BLUE, LIGHT_BLUE],
            text=sentiment_counts.values.astype(int),
            textposition='outside',
        )
    ])
    fig.update_layout(
        **PLOTLY_LAYOUT,
        height=320,
        xaxis_title='',
        yaxis_title='Number of Respondents',
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('**Key Themes**')
    st.markdown('<p class="subtitle">Topics identified from open text responses.</p>', unsafe_allow_html=True)

    themes = [
        ('Topic 1 \u2014 Perceived Expensiveness', 'Medical aid is seen as costly without exploring actual pricing.'),
        ('Topic 2 \u2014 Cost and Benefit Awareness', 'Respondents are unsure what they would get for the cost.'),
        ('Topic 3 \u2014 Structural Unemployment Barrier', 'Unemployment directly prevents uptake regardless of intention.'),
        ('Topic 4 \u2014 General Avoidance Perception', 'Avoidance is framed as a shared experience among young Namibians.'),
    ]
    for title, desc in themes:
        st.markdown(f"""
        <div style="margin-bottom: 0.9rem;">
            <div style="font-weight: 600; color: #FFFFFF; font-size: 0.95rem;">{title}</div>
            <div style="color: #9CA3AF; font-size: 0.85rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------
# SECTION 7 - MESSAGING RECOMMENDATIONS
# ----------------------------------------------------------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('### Messaging Recommendations for NMC')
st.markdown('<p class="subtitle">Segment-level recommendations based on model and NLP findings.</p>', unsafe_allow_html=True)

rec_df = pd.DataFrame({
    'Segment': [
        'Employed, aware of NMC, no medical aid',
        'Neutral sentiment, on the fence',
        'Employer does not offer medical aid',
        'Unemployed or under N$5,000 income',
        'Young and healthy mindset',
    ],
    'Primary Barrier': [
        "Thinks it's too expensive without researching",
        'No reason to act yet',
        'No access to group scheme',
        'Genuinely cannot afford it',
        'Feels irrelevant right now',
    ],
    'Recommended Messaging Approach': [
        'Lead with entry-level pricing and what it covers',
        'Urgency messaging \u2014 accidents happen at any age',
        'Target HR departments and small businesses',
        'Acknowledge honestly; highlight most affordable option',
        'Lead with emergency cover and accident benefits',
    ],
})

st.dataframe(rec_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.8rem; margin-top: 2rem;">
    MSc Data Science Capstone Project &nbsp;|&nbsp; University of Europe for Applied Sciences &nbsp;|&nbsp; Rauna Nghidipaa &nbsp;|&nbsp; 2026
</div>
""", unsafe_allow_html=True)
