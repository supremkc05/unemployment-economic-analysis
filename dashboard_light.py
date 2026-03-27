import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="SDG 8 — Global Unemployment Dashboard",
)

# Custom CSS for light theme
st.markdown("""
    <style>
    /* Light theme with gradient background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling with modern gradient */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1rem;
        color: #5a6c7d;
        margin-bottom: 0;
        text-align: center;
        font-weight: 500;
    }
    
    .header-container {
        background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
        padding: 1.8rem 2rem;
        border-radius: 16px;
        border: 2px solid #90caf9;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        backdrop-filter: blur(4px);
    }
    
    /* KPI cards with glassmorphism effect */
    .kpi-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        padding: 1.8rem 1.5rem;
        border-radius: 16px;
        border: 2px solid rgba(144, 202, 249, 0.5);
        height: 100%;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(31, 38, 135, 0.2);
        border-color: #64b5f6;
    }
    
    .kpi-title {
        font-size: 0.85rem;
        color: #5a6c7d;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    
    .kpi-delta {
        font-size: 0.85rem;
        color: #e53e3e;
        font-weight: 500;
    }
    
    .kpi-delta.positive {
        color: #38a169;
    }
    
    /* Chart containers with modern design */
    .chart-container {
        background: #ffffff;
        padding: 2rem 1.8rem;
        border-radius: 20px;
        border: none;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 40px rgba(31, 38, 135, 0.12);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        box-shadow: 0 15px 50px rgba(31, 38, 135, 0.18);
    }
    
    .chart-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.4rem;
        letter-spacing: -0.3px;
    }
    
    .chart-subtitle {
        font-size: 0.9rem;
        color: #1565C0;
        margin-bottom: 1.2rem;
        font-weight: 500;
    }
    
    /* Sidebar styling with ocean blue gradient */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #006994 0%, #004d6d 100%);
        border-right: 3px solid #0891b2;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #ffffff;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    section[data-testid="stSidebar"] p {
        color: #cffafe;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Filter section headers */
    .filter-header {
        font-size: 0.8rem;
        color: #e2e8f0;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 1.8rem;
        margin-bottom: 0.8rem;
        font-weight: 700;
    }
    
    /* Streamlit widget styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #1565C0 0%, #0D47A1 100%);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #e3f2fd;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #1565C0 0%, #0D47A1 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #0D47A1 0%, #1565C0 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/outputs/merged_data_features.csv')
    
    # Apply categorical ordering
    tier_order = ['Low Income', 'Lower-Middle', 'Upper-Middle', 'High Income']
    df['dev_tier'] = pd.Categorical(df['dev_tier'], categories=tier_order, ordered=True)
    
    covid_order = ['Pre-COVID', 'COVID Peak', 'Recovery', 'Post-COVID']
    df['covid_period'] = pd.Categorical(df['covid_period'], categories=covid_order, ordered=True)
    
    df['year'] = df['year'].astype(int)
    
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.markdown("### SDG 8 Dashboard")
    st.markdown("**Decent Work & Economic Growth**")
    st.markdown("---")
    
    st.markdown('<p class="filter-header">Global Filters</p>', unsafe_allow_html=True)
    
    st.markdown("**Year range**")
    year_range = st.slider(
        "Years",
        min_value=2014,
        max_value=2024,
        value=(2014, 2024),
        label_visibility="collapsed"
    )
    
    st.markdown("**COVID period**")
    covid_filter = st.selectbox(
        "COVID",
        options=['All periods', 'Pre-COVID', 'COVID Peak', 'Recovery', 'Post-COVID'],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("**Age group**")
    age_filter = st.selectbox(
        "Age",
        options=['Both', 'Youth', 'Adults'],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("Data: ILO + World Bank | 185 countries | 2014–2024")

# Apply filters
if age_filter == 'Both':
    age_list = ['Youth', 'Adults']
else:
    age_list = [age_filter]

if covid_filter == 'All periods':
    covid_list = ['Pre-COVID', 'COVID Peak', 'Recovery', 'Post-COVID']
else:
    covid_list = [covid_filter]

sex_list = ['Male', 'Female']
dev_tier_list = ['Low Income', 'Lower-Middle', 'Upper-Middle', 'High Income']

df_filtered = df[
    df['sex'].isin(sex_list) & 
    df['age_categories'].isin(age_list) &
    (df['year'] >= year_range[0]) &
    (df['year'] <= year_range[1]) &
    df['dev_tier'].isin(dev_tier_list) &
    df['covid_period'].isin(covid_list)
]

if df_filtered.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# Header
st.markdown("""
<div class="header-container">
    <p class="main-header">Global Youth Unemployment Analysis</p>
    <p class="sub-header">SDG 8: Decent Work and Economic Growth | 2014-2024</p>
</div>
""", unsafe_allow_html=True)

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

# KPI 1: Youth unemployment
youth_2024 = df_filtered[
    (df_filtered['age_categories'] == 'Youth') &
    (df_filtered['year'] == 2024)
]['unemployment_rate'].mean()

youth_pre = df_filtered[
    (df_filtered['age_categories'] == 'Youth') &
    (df_filtered['year'] < 2020)
]['unemployment_rate'].mean()

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Youth unemployment (2024)</div>
        <div class="kpi-value">{youth_2024:.1f}%</div>
        <div class="kpi-delta">▲ vs {youth_pre:.1f}% pre-COVID</div>
    </div>
    """, unsafe_allow_html=True)

# KPI 2: Youth-adult gap
adult_2024 = df_filtered[
    (df_filtered['age_categories'] == 'Adults') &
    (df_filtered['year'] == 2024)
]['unemployment_rate'].mean()
gap = youth_2024 / adult_2024 if adult_2024 > 0 else 0

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Youth-adult gap</div>
        <div class="kpi-value">{gap:.1f}×</div>
        <div class="kpi-delta">youth vs adults</div>
    </div>
    """, unsafe_allow_html=True)

# KPI 3: COVID recovery
youth_2020 = df_filtered[
    (df_filtered['age_categories'] == 'Youth') &
    (df_filtered['year'] == 2020)
]['unemployment_rate'].mean()
recovery = youth_2024 - youth_2020
recovery_class = "positive" if recovery < 0 else ""

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">COVID recovery</div>
        <div class="kpi-value">{recovery:+.1f} pp</div>
        <div class="kpi-delta {recovery_class}">{'improved' if recovery < 0 else 'worsened'} since 2020</div>
    </div>
    """, unsafe_allow_html=True)

# KPI 4: Crisis countries
country_avg = df_filtered[
    (df_filtered['age_categories'] == 'Youth') &
    (df_filtered['year'] == 2024)
].groupby('country_name')['unemployment_rate'].mean()
crisis_pct = (country_avg > 20).sum() / len(country_avg) * 100 if len(country_avg) > 0 else 0

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Crisis countries</div>
        <div class="kpi-value">{crisis_pct:.0f}%</div>
        <div class="kpi-delta">youth unemp. > 20%</div>
    </div>
    """, unsafe_allow_html=True)

# KPI 5: GDP correlation
df_2024 = df_filtered[df_filtered['year'] == 2024].dropna(
    subset=['gdp_per_capita_current_usd', 'unemployment_rate']
)
corr = df_2024['gdp_per_capita_current_usd'].corr(df_2024['unemployment_rate']) if len(df_2024) > 0 else 0

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">GDP-unemp. correlation</div>
        <div class="kpi-value">{corr:.3f}</div>
        <div class="kpi-delta">weak / jobless growth</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main content - 2 columns
col_left, col_right = st.columns([1.5, 1])

with col_left:
    # Trend chart
    st.markdown("""
    <div class="chart-container">
        <div class="chart-title">Global unemployment trend 2014–2024</div>
        <div class="chart-subtitle">Youth vs adults · COVID period shaded</div>
    """, unsafe_allow_html=True)
    
    trend = df_filtered.groupby(['year', 'age_categories'])['unemployment_rate'].mean().reset_index()
    
    fig_trend = go.Figure()
    
    for age_cat in ['Youth', 'Adults']:
        age_data = trend[trend['age_categories'] == age_cat]
        color = '#5b9bd5' if age_cat == 'Youth' else '#ed7d31'
        
        fig_trend.add_trace(go.Scatter(
            x=age_data['year'],
            y=age_data['unemployment_rate'],
            mode='lines+markers+text',
            name=age_cat,
            line=dict(color=color, width=3),
            marker=dict(size=8),
            text=[f'{val:.1f}%' for val in age_data['unemployment_rate']],
            textposition='top center',
            textfont=dict(size=10, color=color)
        ))
    
    fig_trend.add_vrect(
        x0=2020, x1=2022,
        fillcolor="red", opacity=0.1,
        line_width=0,
        annotation_text="COVID",
        annotation_position="top left",
        annotation=dict(font_color="#1a1a1a")
    )
    
    fig_trend.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font_color='#2d3748',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(203, 213, 224, 0.5)',
            tickvals=list(range(2014, 2025)),
            tickfont=dict(color='#4a5568', size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(203, 213, 224, 0.5)',
            title="",
            tickfont=dict(color='#4a5568', size=11)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#2d3748', size=11),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#cbd5e0',
            borderwidth=1
        ),
        hovermode='x unified',
        margin=dict(l=20, r=20, t=40, b=20),
        height=350
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # COVID scenario
    st.markdown("""
    <div class="chart-container">
        <div class="chart-title">COVID scenario comparison</div>
        <div class="chart-subtitle">Youth vs Adults · by COVID period</div>
    """, unsafe_allow_html=True)
    
    df_covid = df_filtered.groupby(['covid_period', 'age_categories'])['unemployment_rate'].mean().reset_index()
    
    fig_covid = go.Figure()
    
    for age_cat in ['Adults', 'Youth']:
        age_data = df_covid[df_covid['age_categories'] == age_cat]
        color = '#5b9bd5' if age_cat == 'Adults' else '#ff6b6b'
        
        fig_covid.add_trace(go.Bar(
            x=age_data['covid_period'],
            y=age_data['unemployment_rate'],
            name=age_cat,
            marker_color=color,
            text=[f'{val:.1f}%' for val in age_data['unemployment_rate']],
            textposition='inside',
            textfont=dict(color='black', size=11)
        ))
    
    df_total = df_covid.groupby('covid_period')['unemployment_rate'].sum().reset_index()
    
    fig_covid.add_trace(go.Scatter(
        x=df_total['covid_period'],
        y=df_total['unemployment_rate'],
        name='Total',
        mode='lines+markers+text',
        line=dict(color='#ffa94d', width=3),
        marker=dict(size=10),
        text=[f'{val:.1f}%' for val in df_total['unemployment_rate']],
        textposition='top center',
        textfont=dict(color='#ffa94d', size=11),
        yaxis='y2'
    ))
    
    fig_covid.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font_color='#2d3748',
        barmode='stack',
        xaxis=dict(
            showgrid=False,
            title="",
            categoryorder='array',
            categoryarray=['Pre-COVID', 'COVID Peak', 'Recovery', 'Post-COVID'],
            tickfont=dict(color='#4a5568', size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(203, 213, 224, 0.5)',
            title=dict(text="Unemployment Rate (%)", font=dict(color='#2d3748', size=12)),
            side='left',
            tickfont=dict(color='#4a5568', size=11)
        ),
        yaxis2=dict(
            showgrid=False,
            title="",
            overlaying='y',
            side='right',
            tickfont=dict(color='#4a5568', size=11)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#2d3748', size=11),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#cbd5e0',
            borderwidth=1
        ),
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig_covid, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Map - Full width below
st.markdown("""
<div class="chart-container">
    <div class="chart-title">Unemployment severity map</div>
    <div class="chart-subtitle">Country-level · Filtered by global settings</div>
""", unsafe_allow_html=True)

df_map = df_filtered.groupby('country_name').agg(
    unemployment_rate=('unemployment_rate', 'mean')
).reset_index()

def categorize_severity(rate):
    if pd.isna(rate):
        return 'Unknown'
    elif rate < 5:
        return 'Low'
    elif rate < 10:
        return 'Moderate'
    elif rate < 20:
        return 'High'
    else:
        return 'Severe'

df_map['severity'] = df_map['unemployment_rate'].apply(categorize_severity)

severity_colors = {
    "Low": "#51cf66",
    "Moderate": "#ffa94d",
    "High": "#ff8787",
    "Severe": "#ff6b6b"
}

fig_map = px.choropleth(
    df_map,
    locations='country_name',
    locationmode='country names',
    color='severity',
    hover_name='country_name',
    hover_data={
        'unemployment_rate': ':.1f',
        'severity': True
    },
    color_discrete_map=severity_colors,
    category_orders={'severity': ['Low', 'Moderate', 'High', 'Severe']}
)

fig_map.update_layout(
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font_color='#2d3748',
    geo=dict(
        bgcolor='#ffffff',
        showframe=True,
        framecolor='#1565C0',
        framewidth=2,
        showcoastlines=True,
        coastlinecolor='#cbd5e0',
        showcountries=True,
        countrycolor='#cbd5e0',
        countrywidth=0.5,
        showland=True,
        landcolor='#f8f9fa',
        showocean=True,
        oceancolor='#ffffff',
        projection_type='natural earth'
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0.5,
        font=dict(color='#2d3748', size=11),
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='#cbd5e0',
        borderwidth=1
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=450
)

major_countries = {
    'United States': (37.0902, -95.7129),
    'China': (35.8617, 104.1954),
    'India': (20.5937, 78.9629),
    'Brazil': (-14.2350, -51.9253),
    'Russia': (61.5240, 105.3188),
    'Australia': (-25.2744, 133.7751),
    'Canada': (56.1304, -106.3468),
    'Germany': (51.1657, 10.4515),
    'France': (46.2276, 2.2137),
    'United Kingdom': (55.3781, -3.4360),
    'Japan': (36.2048, 138.2529),
    'South Africa': (-30.5595, 22.9375),
    'Mexico': (23.6345, -102.5528),
    'Argentina': (-38.4161, -63.6167),
    'Egypt': (26.8206, 30.8025),
    'Nigeria': (9.0820, 8.6753),
    'Saudi Arabia': (23.8859, 45.0792),
    'Turkey': (38.9637, 35.2433),
    'Indonesia': (-0.7893, 113.9213),
    'South Korea': (35.9078, 127.7669),
    'Spain': (40.4637, -3.7492),
    'Italy': (41.8719, 12.5674),
    'Poland': (51.9194, 19.1451),
    'Thailand': (15.8700, 100.9925),
    'Vietnam': (14.0583, 108.2772)
}

for country, (lat, lon) in major_countries.items():
    if country in df_map['country_name'].values:
        fig_map.add_trace(go.Scattergeo(
            lon=[lon],
            lat=[lat],
            text=country,
            mode='text',
            textfont=dict(size=7, color='#1a1a1a', family='Arial'),
            showlegend=False,
            hoverinfo='skip'
        ))

st.plotly_chart(fig_map, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Second row - 2 columns
col_left2, col_right2 = st.columns(2)

with col_left2:
    # Gender gap bar chart
    st.markdown("""
    <div class="chart-container">
        <div class="chart-title">Gender gap by development tier</div>
        <div class="chart-subtitle">Male vs Female · Average unemployment rate</div>
    """, unsafe_allow_html=True)
    
    df_gender = df_filtered.groupby(['dev_tier', 'sex'])['unemployment_rate'].mean().reset_index()
    
    fig_gender = px.bar(
        df_gender,
        x='dev_tier',
        y='unemployment_rate',
        color='sex',
        barmode='group',
        color_discrete_map={"Male": "#5b9bd5", "Female": "#ff6b6b"},
        text_auto='.1f'
    )
    
    fig_gender.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font_color='#2d3748',
        xaxis=dict(
            showgrid=False,
            title="",
            tickfont=dict(color='#4a5568', size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(203, 213, 224, 0.5)',
            title=dict(text="Unemployment Rate (%)", font=dict(color='#2d3748', size=12)),
            tickfont=dict(color='#4a5568', size=11)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#2d3748', size=11),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#cbd5e0',
            borderwidth=1
        ),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    fig_gender.update_traces(textposition='outside')
    
    st.plotly_chart(fig_gender, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right2:
    # Slope chart - COVID impact by development tier
    st.markdown("""
    <div class="chart-container">
        <div class="chart-title">Youth unemployment trajectory by development tier</div>
        <div class="chart-subtitle">Slope chart · COVID phase progression</div>
    """, unsafe_allow_html=True)
    
    # Prepare data for slope chart - youth unemployment by dev tier and COVID period
    df_slope = df_filtered[df_filtered['age_categories'] == 'Youth'].groupby(
        ['covid_period', 'dev_tier']
    )['unemployment_rate'].mean().reset_index()
    
    # Create slope chart
    fig_slope = go.Figure()
    
    # Color mapping for development tiers
    tier_colors = {
        'Low Income': '#ff6b6b',
        'Lower-Middle': '#ffa94d',
        'Upper-Middle': '#5b9bd5',
        'High Income': '#51cf66'
    }
    
    # Add a line for each development tier
    for tier in ['Low Income', 'Lower-Middle', 'Upper-Middle', 'High Income']:
        tier_data = df_slope[df_slope['dev_tier'] == tier].sort_values(
            'covid_period',
            key=lambda x: x.map({'Pre-COVID': 0, 'COVID Peak': 1, 'Recovery': 2, 'Post-COVID': 3})
        )
        
        if not tier_data.empty:
            fig_slope.add_trace(go.Scatter(
                x=tier_data['covid_period'],
                y=tier_data['unemployment_rate'],
                mode='lines+markers+text',
                name=tier,
                line=dict(color=tier_colors[tier], width=3),
                marker=dict(size=10, symbol='circle'),
                text=[f'{val:.1f}%' for val in tier_data['unemployment_rate']],
                textposition='top center',
                textfont=dict(size=9, color=tier_colors[tier]),
                hovertemplate='<b>%{fullData.name}</b><br>Period: %{x}<br>Rate: %{y:.1f}%<extra></extra>'
            ))
    
    fig_slope.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font_color='#2d3748',
        xaxis=dict(
            showgrid=False,
            title="",
            categoryorder='array',
            categoryarray=['Pre-COVID', 'COVID Peak', 'Recovery', 'Post-COVID'],
            tickfont=dict(size=10, color='#4a5568')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(203, 213, 224, 0.5)',
            title=dict(text="Youth Unemployment Rate (%)", font=dict(size=11, color='#2d3748')),
            tickfont=dict(size=10, color='#4a5568')
        ),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="right",
            x=1.15,
            font=dict(size=10, color='#2d3748'),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#cbd5e0',
            borderwidth=1
        ),
        height=400,
        margin=dict(l=20, r=80, t=20, b=20),
        hovermode='closest'
    )
    
    st.plotly_chart(fig_slope, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Third row - 2 columns
col1, col2 = st.columns(2)

with col1:
    # Bubble chart
    # Use the latest year available in filtered data
    latest_year = df_filtered['year'].max()
    
    st.markdown(f"""
    <div class="chart-container">
        <div class="chart-title">Bubble chart — GDP vs unemployment</div>
        <div class="chart-subtitle">Bubble size = inflation · {latest_year}</div>
    """, unsafe_allow_html=True)
    
    df_bubble = df_filtered[df_filtered['year'] == latest_year].groupby('country_name').agg(
        unemployment_rate=('unemployment_rate', 'mean'),
        gdp_growth_pct_annual=('gdp_growth_pct_annual', 'mean'),
        inflation_cpi_pct=('inflation_cpi_pct', 'mean'),
        dev_tier=('dev_tier', 'first')
    ).reset_index().dropna()
    
    df_bubble = df_bubble[
        (df_bubble['inflation_cpi_pct'] < 50) &
        (df_bubble['gdp_growth_pct_annual'] > -10) &
        (df_bubble['gdp_growth_pct_annual'] < 15)
    ]
    
    df_bubble['inflation_size'] = df_bubble['inflation_cpi_pct'].clip(lower=1)
    
    fig_bubble = px.scatter(
        df_bubble,
        x='gdp_growth_pct_annual',
        y='unemployment_rate',
        size='inflation_size',
        color='dev_tier',
        hover_name='country_name',
        size_max=30,
        color_discrete_map={
            'Low Income': '#ff6b6b',
            'Lower-Middle': '#ffa94d',
            'Upper-Middle': '#5b9bd5',
            'High Income': '#51cf66'
        }
    )
    
    fig_bubble.add_hline(y=10, line_dash="dash", line_color="gray", opacity=0.5)
    fig_bubble.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig_bubble.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font_color='#2d3748',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(203, 213, 224, 0.5)',
            title="",
            tickfont=dict(color='#4a5568', size=11)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(203, 213, 224, 0.5)',
            title="",
            tickfont=dict(color='#4a5568', size=11)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color='#2d3748', size=11),
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='#cbd5e0',
            borderwidth=1
        ),
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig_bubble, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Youth-adult ratio heatmap
    st.markdown("""
    <div class="chart-container">
        <div class="chart-title">Youth-adult unemployment ratio heatmap</div>
        <div class="chart-subtitle">Top 10 countries · Ratio by year (Higher = Worse for youth)</div>
    """, unsafe_allow_html=True)
    
    youth = df_filtered[df_filtered['age_categories'] == 'Youth'][
        ['country_name', 'year', 'sex', 'unemployment_rate']
    ]
    
    adult = df_filtered[df_filtered['age_categories'] == 'Adults'][
        ['country_name', 'year', 'sex', 'unemployment_rate']
    ]
    
    ratio_df = youth.merge(
        adult,
        on=['country_name', 'year', 'sex'],
        suffixes=('_youth', '_adult')
    )
    
    ratio_df['ratio'] = np.where(
        ratio_df['unemployment_rate_adult'] == 0,
        np.nan,
        ratio_df['unemployment_rate_youth'] / ratio_df['unemployment_rate_adult']
    )
    
    ratio_country = ratio_df.groupby(['country_name', 'year'])['ratio'].mean().reset_index()
    top10 = ratio_country.groupby('country_name')['ratio'].mean().nlargest(10).index.tolist()
    
    df_heat = ratio_country[ratio_country['country_name'].isin(top10)]
    df_pivot = df_heat.pivot(index='country_name', columns='year', values='ratio')
    df_pivot = df_pivot.reindex(df_pivot.mean(axis=1).sort_values(ascending=False).index)
    
    fig_heat = go.Figure(data=go.Heatmap(
        z=df_pivot.values,
        x=df_pivot.columns,
        y=df_pivot.index,
        colorscale=[[0, '#51cf66'], [1, '#ff6b6b']],
        text=np.round(df_pivot.values, 1),
        texttemplate='%{text}x',
        textfont={"size": 10, "color": "black"},
        colorbar=dict(
            title=dict(text="Ratio", side="right"),
            tickmode="linear",
            tick0=0,
            dtick=1,
            thickness=15,
            len=0.7
        ),
        hovertemplate='<b>%{y}</b><br>Year: %{x}<br>Ratio: %{z:.2f}x<extra></extra>'
    ))
    
    fig_heat.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font_color='#2d3748',
        xaxis=dict(
            title=dict(text="Year", font=dict(color='#2d3748', size=12)),
            tickmode='linear',
            tick0=2014,
            dtick=2,
            side='bottom',
            showgrid=False,
            tickfont=dict(color='#4a5568', size=11)
        ),
        yaxis=dict(
            title=dict(text="Country", font=dict(color='#2d3748', size=12)),
            showgrid=False,
            tickfont=dict(color='#4a5568', size=11)
        ),
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Gender Equity Progress Chart - Full width at the end
st.markdown("""
<div class="chart-container">
    <div class="chart-title">Gender equity progress tracker</div>
    <div class="chart-subtitle">Tracking unemployment gap between women and men · SDG 8.5: Equal pay for work of equal value</div>
""", unsafe_allow_html=True)

# Calculate gender gap (Female - Male unemployment rate)
df_equity = df_filtered.groupby(['year', 'sex'])['unemployment_rate'].mean().reset_index()
df_equity_pivot = df_equity.pivot(index='year', columns='sex', values='unemployment_rate').reset_index()
df_equity_pivot['gender_gap'] = df_equity_pivot['Female'] - df_equity_pivot['Male']

# Create line chart
fig_equity = go.Figure()

# Add gender gap line with gradient effect
fig_equity.add_trace(go.Scatter(
    x=df_equity_pivot['year'],
    y=df_equity_pivot['gender_gap'],
    mode='lines+markers',
    name='Gender Gap',
    line=dict(color='#7C3AED', width=4, shape='spline'),
    marker=dict(size=12, symbol='circle', color='#7C3AED', 
                line=dict(color='#ffffff', width=2)),
    fill='tozeroy',
    fillcolor='rgba(124, 58, 237, 0.2)',
    hovertemplate='<b>Year: %{x}</b><br>Gender Gap: %{y:.2f}pp<br>(Female - Male unemployment)<extra></extra>'
))

# Add zero reference line (equity target)
fig_equity.add_hline(
    y=0, 
    line_dash="dash", 
    line_color="#2d3748", 
    line_width=3,
    annotation_text="⚖ Equity Target",
    annotation_position="right",
    annotation=dict(font=dict(size=12, color='#2d3748', weight='bold'))
)

# Add COVID period shading with better visibility
fig_equity.add_vrect(
    x0=2020, x1=2022,
    fillcolor="#ff6b6b", opacity=0.12,
    line_width=0,
    annotation_text="COVID-19 Period",
    annotation_position="top left",
    annotation=dict(font_color="#c92a2a", font_size=11, font_weight='bold')
)

# Add zone labels for interpretation
max_gap = df_equity_pivot['gender_gap'].max()
min_gap = df_equity_pivot['gender_gap'].min()

if max_gap > 0:
    fig_equity.add_annotation(
        x=2024,
        y=max_gap * 0.7,
        text="↑ Female Disadvantage",
        showarrow=False,
        font=dict(size=11, color='#718096', weight='bold'),
        xanchor='right',
        bgcolor='rgba(255, 107, 107, 0.1)',
        borderpad=6
    )

if min_gap < 0:
    fig_equity.add_annotation(
        x=2024,
        y=min_gap * 0.7,
        text="↓ Male Disadvantage",
        showarrow=False,
        font=dict(size=11, color='#718096', weight='bold'),
        xanchor='right',
        bgcolor='rgba(81, 207, 102, 0.1)',
        borderpad=6
    )

fig_equity.update_layout(
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font_color='#2d3748',
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(203, 213, 224, 0.5)',
        title="Year",
        tickfont=dict(color='#4a5568', size=11),
        tickmode='linear',
        tick0=2014,
        dtick=1
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(203, 213, 224, 0.5)',
        title=dict(text="Gender Gap (percentage points)", font=dict(color='#2d3748', size=12)),
        tickfont=dict(color='#4a5568', size=11),
        zeroline=True,
        zerolinecolor='#2d3748',
        zerolinewidth=3
    ),
    showlegend=False,
    hovermode='x unified',
    height=400,
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig_equity, use_container_width=True)

# Add insights summary below the chart
col_insight1, col_insight2, col_insight3 = st.columns(3)

# Calculate key metrics
overall_2024 = df_equity_pivot[df_equity_pivot['year'] == 2024]['gender_gap'].iloc[0]
overall_2014 = df_equity_pivot[df_equity_pivot['year'] == 2014]['gender_gap'].iloc[0]
change = overall_2024 - overall_2014
progress_status = "Improving" if abs(overall_2024) < abs(overall_2014) else "Worsening"

with col_insight1:
    st.markdown(f"""
    <div style="background: rgba(124, 58, 237, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #7C3AED;">
        <div style="font-size: 0.85rem; color: #718096; margin-bottom: 0.3rem;">Current Gap (2024)</div>
        <div style="font-size: 1.8rem; font-weight: bold; color: #2d3748;">{overall_2024:+.2f}pp</div>
        <div style="font-size: 0.8rem; color: #718096;">{'Women face higher unemployment' if overall_2024 > 0 else 'Men face higher unemployment'}</div>
    </div>
    """, unsafe_allow_html=True)

with col_insight2:
    st.markdown(f"""
    <div style="background: rgba(21, 101, 192, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #1565C0;">
        <div style="font-size: 0.85rem; color: #718096; margin-bottom: 0.3rem;">10-Year Trend</div>
        <div style="font-size: 1.8rem; font-weight: bold; color: #2d3748;">{progress_status}</div>
        <div style="font-size: 0.8rem; color: #718096;">Change: {change:+.2f}pp since 2014</div>
    </div>
    """, unsafe_allow_html=True)

with col_insight3:
    # Calculate distance from equity
    distance_from_equity = abs(overall_2024)
    
    st.markdown(f"""
    <div style="background: rgba(81, 207, 102, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #51cf66;">
        <div style="font-size: 0.85rem; color: #718096; margin-bottom: 0.3rem;">Distance from Equity</div>
        <div style="font-size: 1.8rem; font-weight: bold; color: #2d3748;">{distance_from_equity:.2f}pp</div>
        <div style="font-size: 0.8rem; color: #718096;">{'Close to equity' if distance_from_equity < 1 else 'Needs improvement'}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# SDG 8 Dashboard — ITS68404 Group Assignment
