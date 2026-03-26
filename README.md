# Global Youth Unemployment Dashboard

**SDG 8: Decent Work and Economic Growth**

An interactive Streamlit dashboard analyzing global youth unemployment trends from 2014-2024 across 185 countries.

---

## Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd data_vis_group
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install streamlit pandas numpy plotly
```

### Run the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open automatically at `http://localhost:8501`

---

## Features

### **5 Key Performance Indicators**
- Youth Unemployment Rate (2024)
- Youth-Adult Gap (multiplier)
- COVID Recovery Status
- Crisis Countries (>20% unemployment)
- GDP-Unemployment Correlation

### **Interactive Visualizations**
1. **Global Trend Line Chart** - Youth vs Adults unemployment over time
2. **COVID Scenario Comparison** - Stacked bar chart with trend line
3. **Unemployment Severity Map** - Choropleth map with country labels
4. **Gender Gap Analysis** - Bar chart by development tier
5. **COVID Timeline Donut** - Period-wise distribution
6. **Bubble Chart** - GDP vs Unemployment (bubble size = inflation)
7. **Youth-Adult Ratio Heatmap** - Top 10 countries over time

### **Global Filters**
- Year Range (2014-2024)
- COVID Period (Pre-COVID, COVID Peak, Recovery, Post-COVID)
- Age Group (Youth, Adults, Both)

---

## Project Structure

```
data_vis_group/
├── dashboard.py              # Main dashboard application
├── data/
│   └── outputs/
│       └── merged_data_features.csv  # Dataset
├── analysis/
│   ├── data_cleaning.ipynb   # Data preprocessing
│   ├── eda.ipynb            # Exploratory data analysis
│   └── feature.ipynb        # Feature engineering
├── README.md                # This file
└── .venv/                   # Virtual environment
```

---

## Data Source

- **ILO (International Labour Organization)** - Unemployment statistics
- **World Bank** - Economic indicators (GDP, inflation)
- **Coverage**: 185 countries, 2014-2024
- **Variables**: Unemployment rate, GDP, inflation, development tier, COVID period

---

## Key Insights

- Youth unemployment is **2.8× higher** than adults globally
- **30%** of countries face crisis-level youth unemployment (>20%)
- Weak GDP-unemployment correlation (**-0.134**) reveals "jobless growth"
- COVID-19 impact shows incomplete recovery by 2024

---

## Customization

### Change Color Scheme
Edit the color maps in `dashboard.py`:
```python
color_discrete_map={"Youth": "#ff6b6b", "Adults": "#5b9bd5"}
```

### Modify Filters
Update sidebar filters in the `with st.sidebar:` section

### Add New Charts
Follow the existing chart structure:
```python
st.markdown('<div class="chart-container">...</div>', unsafe_allow_html=True)
fig = px.chart_type(...)
st.plotly_chart(fig, use_container_width=True)
```

---

## Requirements

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
```

---

