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
    /* Light theme */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1a1a1a;
        margin-bottom: 0.3rem;
        text-align: center;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    .sub-header {
        font-size: 0.95rem;
        color: #4a4a4a;
        margin-bottom: 0;
        text-align: center;
    }
    
    .header-container {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1rem 2rem;
        border-radius: 8px;
        border: 1px solid #90caf9;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* KPI cards */
    .kpi-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #90caf9;
        height: 100%;
    }
    
    .kpi-title {
        font-size: 0.9rem;
        color: #6c757d;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a1a1a;
        margin-bottom: 0.3rem;
    }
    
    .kpi-delta {
        font-size: 0.85rem;
        color: #dc3545;
    }
    
    .kpi-delta.positive {
        color: #28a745;
    }
    
    /* Chart containers */
    .chart-container {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #64b5f6;
        margin-bottom: 1rem;
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1a1a1a;
        margin-bottom: 0.3rem;
    }
    
    .chart-subtitle {
        font-size: 0.9rem;
        color: #6c757d;
        margin-bottom: 1rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #e3f2fd;
        border-right: 1px solid #90caf9;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #1a1a1a;
    }
    
    /* Filter section headers */
    .filter-header {
        font-size: 0.85rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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
        font_color='#1a1a1a',
        xaxis=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            tickvals=list(range(2014, 2025)),
            tickfont=dict(color='#1a1a1a')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            title="",
            tickfont=dict(color='#1a1a1a')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#1a1a1a')
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
        font_color='#1a1a1a',
        barmode='stack',
        xaxis=dict(
            showgrid=False,
            title="",
            categoryorder='array',
            categoryarray=['Pre-COVID', 'COVID Peak', 'Recovery', 'Post-COVID'],
            tickfont=dict(color='#1a1a1a')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            title=dict(text="Unemployment Rate (%)", font=dict(color='#1a1a1a')),
            side='left',
            tickfont=dict(color='#1a1a1a')
        ),
        yaxis2=dict(
            showgrid=False,
            title="",
            overlaying='y',
            side='right',
            tickfont=dict(color='#1a1a1a')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#1a1a1a')
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
    font_color='#1a1a1a',
    geo=dict(
        bgcolor='#ffffff',
        showframe=True,
        showcoastlines=True,
        coastlinecolor='#90caf9',
        showcountries=True,
        countrycolor='#90caf9',
        countrywidth=0.5,
        showland=True,
        landcolor='#e3f2fd',
        projection_type='natural earth'
    ),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.05,
        xanchor="center",
        x=0.5,
        font=dict(color='#1a1a1a')
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
        font_color='#1a1a1a',
        xaxis=dict(
            showgrid=False,
            title="",
            tickfont=dict(color='#1a1a1a')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            title=dict(text="Unemployment Rate (%)", font=dict(color='#1a1a1a')),
            tickfont=dict(color='#1a1a1a')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='#1a1a1a')
        ),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    fig_gender.update_traces(textposition='outside')
    
    st.plotly_chart(fig_gender, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right2:
    # Donut chart - COVID recovery analysis
    st.markdown("""
    <div class="chart-container">
        <div class="chart-title">Unemployment rate across COVID timeline</div>
        <div class="chart-subtitle">Donut chart · Period-wise average distribution</div>
    """, unsafe_allow_html=True)
    
    df_donut = df_filtered.groupby('covid_period')['unemployment_rate'].mean().reset_index()
    df_donut = df_donut.sort_values('covid_period', 
                                     key=lambda x: x.map({'Pre-COVID': 0, 'COVID Peak': 1, 
                                                          'Recovery': 2, 'Post-COVID': 3}))
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=df_donut['covid_period'],
        values=df_donut['unemployment_rate'],
        hole=0.5,
        marker=dict(
            colors=['#51cf66', '#ff6b6b', '#ffa94d', '#5b9bd5'],
            line=dict(color='#e3f2fd', width=2)
        ),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(color='#1a1a1a', size=12),
        hovertemplate='<b>%{label}</b><br>Avg Rate: %{value:.1f}%<br>Share: %{percent}<extra></extra>'
    )])
    
    fig_donut.add_annotation(
        text=f"<b>{df_donut['unemployment_rate'].mean():.1f}%</b><br>Overall Avg",
        x=0.5, y=0.5,
        font=dict(size=16, color='#1a1a1a'),
        showarrow=False,
        align='center'
    )
    
    fig_donut.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font_color='#1a1a1a',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color='#1a1a1a')
        ),
        height=400,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig_donut, use_container_width=True)
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
        font_color='#1a1a1a',
        xaxis=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            title="",
            tickfont=dict(color='#1a1a1a')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#e0e0e0',
            title="",
            tickfont=dict(color='#1a1a1a')
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color='#1a1a1a')
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
        font_color='#1a1a1a',
        xaxis=dict(
            title=dict(text="Year", font=dict(color='#1a1a1a')),
            tickmode='linear',
            tick0=2014,
            dtick=2,
            side='bottom',
            showgrid=False,
            tickfont=dict(color='#1a1a1a')
        ),
        yaxis=dict(
            title=dict(text="Country", font=dict(color='#1a1a1a')),
            showgrid=False,
            tickfont=dict(color='#1a1a1a')
        ),
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SDG 8 Dashboard — ITS68404 Group Assignment
