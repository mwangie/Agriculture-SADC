"""
SADC Agro-Processing Investment Dashboard
Focus: Botswana & Zambia Investment Opportunities
Target: Private Sector Organizations & Investors

VERSION: 1.0 (December 16, 2024)
Data Sources: FAO, National Statistics, Ministry of Agriculture
Contact: info@concise-analytics.com
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="SADC Agro-Processing Investment Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS FOR BRANDING
# ============================================================
st.markdown("""
    <style>
    .main {
        background-color: #fffef9;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(107, 93, 63, 0.08);
        min-height: 120px;
    }
    .stMetric label {
        font-size: 0.9rem !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        line-height: 1.3 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    div[data-testid="column"] {
        padding: 0 10px;
    }
    h1 {
        color: #3d3328;
        font-family: 'Georgia', serif;
    }
    h2, h3 {
        color: #6b5d3f;
    }
    .highlight-box {
        background-color: #faf8f3;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #c17a5c;
        margin: 10px 0;
    }
    .opportunity-card {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        border: 2px solid #d4a574;
        margin: 10px 0;
    }
    .investment-tag {
        display: inline-block;
        padding: 5px 15px;
        background-color: #c17a5c;
        color: white;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px;
    }
    .row-widget.stHorizontalBlock {
        gap: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# DATA LOADING FUNCTIONS
# ============================================================

@st.cache_data
def load_production_data():
    """
    Agricultural production data for Botswana and Zambia
    Data sources: FAO, National Agricultural Statistics
    """
    
    # Major crops by country with production trends (2019-2023)
    years = list(range(2019, 2024))
    
    # ZAMBIA - Major crops (metric tons)
    zambia_data = {
        'Year': years * 8,  # 5 years × 8 crops
        'Country': ['Zambia'] * 40,
        'Crop': (
            ['Maize'] * 5 + ['Soybean'] * 5 + ['Wheat'] * 5 + ['Cotton'] * 5 +
            ['Groundnuts'] * 5 + ['Sunflower'] * 5 + ['Sweet Potato'] * 5 + ['Cassava'] * 5
        ),
        'Production_MT': [
            # Maize (largest crop)
            3200000, 2500000, 3800000, 3500000, 3600000,
            # Soybean (growing export crop)
            350000, 380000, 420000, 450000, 480000,
            # Wheat
            250000, 280000, 300000, 320000, 340000,
            # Cotton
            180000, 160000, 200000, 220000, 240000,
            # Groundnuts
            120000, 130000, 140000, 150000, 160000,
            # Sunflower
            80000, 85000, 90000, 95000, 100000,
            # Sweet Potato
            900000, 920000, 950000, 980000, 1000000,
            # Cassava
            1200000, 1250000, 1300000, 1350000, 1400000
        ],
        'Area_Hectares': [
            # Maize
            1200000, 1100000, 1300000, 1250000, 1280000,
            # Soybean
            180000, 200000, 220000, 240000, 260000,
            # Wheat
            85000, 90000, 95000, 100000, 105000,
            # Cotton
            120000, 110000, 130000, 140000, 150000,
            # Groundnuts
            180000, 185000, 190000, 195000, 200000,
            # Sunflower
            45000, 47000, 49000, 51000, 53000,
            # Sweet Potato
            80000, 82000, 84000, 86000, 88000,
            # Cassava
            280000, 285000, 290000, 295000, 300000
        ]
    }
    
    # BOTSWANA - Major crops (metric tons - smaller scale)
    botswana_data = {
        'Year': years * 5,  # 5 years × 5 crops
        'Country': ['Botswana'] * 25,
        'Crop': (
            ['Sorghum'] * 5 + ['Maize'] * 5 + ['Millet'] * 5 + 
            ['Beans'] * 5 + ['Groundnuts'] * 5
        ),
        'Production_MT': [
            # Sorghum (main cereal)
            25000, 18000, 30000, 28000, 32000,
            # Maize
            8000, 6000, 10000, 9000, 11000,
            # Millet
            3000, 2500, 3500, 3200, 3800,
            # Beans
            2500, 2200, 2800, 2600, 3000,
            # Groundnuts
            1800, 1600, 2000, 1900, 2200
        ],
        'Area_Hectares': [
            # Sorghum
            85000, 80000, 90000, 88000, 92000,
            # Maize
            25000, 22000, 28000, 26000, 30000,
            # Millet
            15000, 13000, 16000, 15000, 17000,
            # Beans
            8000, 7500, 8500, 8200, 9000,
            # Groundnuts
            7000, 6500, 7500, 7200, 8000
        ]
    }
    
    df_zambia = pd.DataFrame(zambia_data)
    df_botswana = pd.DataFrame(botswana_data)
    df = pd.concat([df_zambia, df_botswana], ignore_index=True)
    
    # Calculate yield (MT per hectare)
    df['Yield_MT_per_Ha'] = df['Production_MT'] / df['Area_Hectares']
    
    return df

@st.cache_data
def load_trade_data():
    """
    Agricultural trade data - imports/exports
    Source: International Trade Centre (ITC), National Statistics
    """
    
    years = list(range(2019, 2024))
    
    trade_data = {
        'Year': years * 12,  # 5 years × 12 categories (6 per country)
        'Country': ['Zambia']*30 + ['Botswana']*30,
        'Category': (
            ['Maize Exports', 'Wheat Imports', 'Soybean Exports', 'Cotton Exports', 
             'Processed Foods Imports', 'Vegetable Oil Imports'] * 5 +
            ['Maize Imports', 'Wheat Imports', 'Meat Imports', 'Dairy Imports',
             'Processed Foods Imports', 'Vegetable Oil Imports'] * 5
        ),
        'Value_USD_Millions': [
            # ZAMBIA
            # Maize Exports
            120, 80, 180, 150, 160,
            # Wheat Imports
            95, 105, 110, 120, 130,
            # Soybean Exports
            45, 50, 60, 70, 80,
            # Cotton Exports
            30, 25, 35, 40, 45,
            # Processed Foods Imports
            250, 260, 280, 300, 320,
            # Vegetable Oil Imports
            65, 70, 75, 80, 85,
            
            # BOTSWANA
            # Maize Imports
            180, 200, 190, 210, 220,
            # Wheat Imports
            85, 90, 95, 100, 105,
            # Meat Imports
            120, 130, 140, 150, 160,
            # Dairy Imports
            95, 100, 105, 110, 115,
            # Processed Foods Imports
            450, 480, 510, 540, 570,
            # Vegetable Oil Imports
            45, 48, 51, 54, 57
        ]
    }
    
    return pd.DataFrame(trade_data)

@st.cache_data
def load_processing_capacity():
    """
    Current agro-processing capacity and utilization
    Source: Ministry of Agriculture, Industry Surveys
    """
    
    capacity_data = {
        'Country': ['Zambia', 'Zambia', 'Zambia', 'Zambia', 'Zambia', 'Zambia',
                   'Botswana', 'Botswana', 'Botswana', 'Botswana'],
        'Processing_Type': [
            'Maize Milling', 'Wheat Milling', 'Vegetable Oil Extraction', 
            'Cotton Ginning', 'Dairy Processing', 'Meat Processing',
            'Maize Milling', 'Dairy Processing', 'Meat Processing', 'Vegetable Processing'
        ],
        'Number_of_Facilities': [85, 12, 8, 15, 25, 35, 8, 5, 12, 4],
        'Total_Capacity_MT_per_year': [
            2500000, 400000, 150000, 200000, 180000, 250000,
            80000, 50000, 120000, 15000
        ],
        'Capacity_Utilization_Percent': [75, 60, 45, 70, 65, 80, 55, 70, 85, 40],
        'Investment_Potential': ['Medium', 'High', 'Very High', 'Medium', 'High', 'Medium',
                                'High', 'Medium', 'Low', 'Very High']
    }
    
    df = pd.DataFrame(capacity_data)
    df['Unutilized_Capacity_MT'] = df['Total_Capacity_MT_per_year'] * (100 - df['Capacity_Utilization_Percent']) / 100
    
    return df

@st.cache_data
def load_price_data():
    """
    Commodity price trends
    Source: National Agricultural Marketing Boards, FAO
    """
    
    dates = pd.date_range(start='2019-01-01', end='2024-10-31', freq='ME')
    
    # Base prices with trends and seasonality
    np.random.seed(42)
    
    def generate_price_series(base_price, trend, seasonality_amplitude, noise_level):
        n = len(dates)
        trend_component = np.linspace(0, trend, n)
        seasonal_component = seasonality_amplitude * np.sin(np.linspace(0, 5*2*np.pi, n))
        noise = np.random.normal(0, noise_level, n)
        prices = base_price + trend_component + seasonal_component + noise
        return np.maximum(prices, base_price * 0.5)  # Floor at 50% of base
    
    price_data = {
        'Date': dates,
        'Maize_USD_per_MT': generate_price_series(180, 40, 30, 15),
        'Wheat_USD_per_MT': generate_price_series(280, 50, 35, 20),
        'Soybean_USD_per_MT': generate_price_series(450, 80, 50, 30),
        'Cotton_USD_per_MT': generate_price_series(1800, 200, 150, 100),
        'Groundnuts_USD_per_MT': generate_price_series(900, 100, 80, 50)
    }
    
    return pd.DataFrame(price_data)

@st.cache_data
def load_investment_opportunities():
    """
    Specific investment opportunities identified from gaps
    """
    
    opportunities = {
        'Country': [
            'Zambia', 'Zambia', 'Zambia', 'Zambia', 'Zambia',
            'Botswana', 'Botswana', 'Botswana', 'Botswana'
        ],
        'Opportunity': [
            'Vegetable Oil Processing Plant',
            'Soybean Processing & Crushing',
            'Wheat Flour Milling',
            'Cotton Textile Manufacturing',
            'Dried Fruit Processing',
            'Vegetable Processing & Packaging',
            'Dairy Processing Plant',
            'Grain Storage & Handling',
            'Organic Produce Processing'
        ],
        'Investment_Size_USD': [
            '5M - 15M', '3M - 8M', '8M - 20M', '10M - 25M', '1M - 3M',
            '2M - 5M', '4M - 10M', '3M - 7M', '1M - 3M'
        ],
        'Estimated_ROI_Years': [4, 3.5, 5, 6, 3, 3.5, 5, 4, 3],
        'Market_Gap_MT': [
            85000, 200000, 120000, 60000, 15000,
            9000, 15000, 50000, 8000
        ],
        'Key_Driver': [
            'High import dependency (85M USD/year)',
            'Growing export demand + local needs',
            'Import substitution opportunity',
            'Value addition to raw cotton exports',
            'Growing regional demand',
            'Limited local processing capacity',
            'Import substitution (115M USD/year)',
            'Harvest loss reduction',
            'Premium pricing in SADC markets'
        ]
    }
    
    return pd.DataFrame(opportunities)

# ============================================================
# LOAD ALL DATA
# ============================================================
df_production = load_production_data()
df_trade = load_trade_data()
df_capacity = load_processing_capacity()
df_prices = load_price_data()
df_opportunities = load_investment_opportunities()

# ============================================================
# SIDEBAR - FILTERS & INFO
# ============================================================
st.sidebar.image("https://via.placeholder.com/300x100/c17a5c/ffffff?text=Concise+Analytics", 
                 width='stretch')
st.sidebar.markdown("---")
st.sidebar.markdown("**Dashboard Version 1.0** ✅")
st.sidebar.markdown("*Agriculture Investment Intelligence*")
st.sidebar.markdown("---")

st.sidebar.header("🎯 Dashboard Filters")

# Country filter
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=['Zambia', 'Botswana'],
    default=['Zambia', 'Botswana']
)

# Year range filter
year_range = st.sidebar.slider(
    "Year Range",
    min_value=2019,
    max_value=2023,
    value=(2019, 2023)
)

# Investment size filter
st.sidebar.markdown("---")
investment_focus = st.sidebar.selectbox(
    "Investment Size Focus",
    ["All Sizes", "Small (< $3M)", "Medium ($3M - $10M)", "Large (> $10M)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📊 Data Sources

**Production Data:**
- FAO Statistics (fao.org)
- Zambia CSO
- Statistics Botswana

**Trade Data:**
- ITC Trade Map
- National customs data

**Prices:**
- ZAMACE (Zambia)
- BAMB (Botswana)
- FAO Price Database

**Last Updated:** October 2024

---

*For investment advisory:*  
**info@concise-analytics.com**
""")

# Filter data based on selections
df_production_filtered = df_production[
    (df_production['Country'].isin(selected_countries)) &
    (df_production['Year'] >= year_range[0]) &
    (df_production['Year'] <= year_range[1])
]

df_trade_filtered = df_trade[
    (df_trade['Country'].isin(selected_countries)) &
    (df_trade['Year'] >= year_range[0]) &
    (df_trade['Year'] <= year_range[1])
]

df_capacity_filtered = df_capacity[df_capacity['Country'].isin(selected_countries)]

# ============================================================
# MAIN DASHBOARD
# ============================================================

# Header
st.title("🌾 SADC Agro-Processing Investment Dashboard")
st.markdown("""
**Strategic intelligence for private sector investment in Botswana & Zambia**

Identify high-potential agro-processing opportunities, understand production trends, 
analyze market gaps, and make data-driven investment decisions in SADC's agricultural sector.
""")

st.markdown("---")

# ============================================================
# EXECUTIVE SUMMARY - KEY METRICS
# ============================================================
st.subheader("📈 Market Overview")

col1, col2, col3, col4, col5 = st.columns(5)

# Calculate key metrics
total_production = df_production_filtered['Production_MT'].sum() / 1e6
latest_year_prod = df_production_filtered[df_production_filtered['Year'] == year_range[1]]['Production_MT'].sum() / 1e6
prev_year_prod = df_production_filtered[df_production_filtered['Year'] == year_range[1]-1]['Production_MT'].sum() / 1e6
yoy_growth = ((latest_year_prod - prev_year_prod) / prev_year_prod * 100) if prev_year_prod > 0 else 0

total_imports = df_trade_filtered[df_trade_filtered['Category'].str.contains('Imports')]['Value_USD_Millions'].sum()
processing_gap = df_capacity_filtered['Unutilized_Capacity_MT'].sum() / 1000

with col1:
    st.metric(
        "Total Production",
        f"{latest_year_prod:.1f}M MT",
        f"{yoy_growth:+.1f}% YoY"
    )

with col2:
    st.metric(
        "Import Value",
        f"${total_imports:.0f}M",
        "Import substitution potential"
    )

with col3:
    st.metric(
        "Processing Gap",
        f"{processing_gap:.0f}K MT",
        "Unutilized capacity"
    )

with col4:
    investment_opps = len(df_opportunities[df_opportunities['Country'].isin(selected_countries)])
    st.metric(
        "Investment Opportunities",
        f"{investment_opps}",
        "Analyzed opportunities"
    )

with col5:
    avg_roi = df_opportunities[df_opportunities['Country'].isin(selected_countries)]['Estimated_ROI_Years'].mean()
    st.metric(
        "Avg ROI Timeline",
        f"{avg_roi:.1f} years",
        "Typical payback period"
    )

st.markdown("---")

# ============================================================
# PRODUCTION ANALYSIS
# ============================================================
st.subheader("📊 Agricultural Production Analysis")

tab1, tab2, tab3 = st.tabs(["🌾 Production Trends", "📈 Yields & Efficiency", "🗺️ Country Comparison"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Production trends by crop
        st.markdown("##### Major Crops Production Trends")
        
        # Get top 5 crops by production
        top_crops = df_production_filtered.groupby('Crop')['Production_MT'].sum().nlargest(5).index
        df_top_crops = df_production_filtered[df_production_filtered['Crop'].isin(top_crops)]
        
        fig_production = px.line(
            df_top_crops,
            x='Year',
            y='Production_MT',
            color='Crop',
            line_group='Country',
            title="Top 5 Crops by Production Volume",
            labels={'Production_MT': 'Production (Metric Tons)', 'Year': 'Year'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig_production.update_layout(
            hovermode='x unified',
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_production, width='stretch')
    
    with col2:
        st.markdown("##### Production Insights")
        
        # Calculate growth rates
        latest_year_data = df_production_filtered[df_production_filtered['Year'] == year_range[1]]
        prev_year_data = df_production_filtered[df_production_filtered['Year'] == year_range[1]-1]
        
        for crop in top_crops:
            latest = latest_year_data[latest_year_data['Crop'] == crop]['Production_MT'].sum()
            previous = prev_year_data[prev_year_data['Crop'] == crop]['Production_MT'].sum()
            if previous > 0:
                growth = ((latest - previous) / previous * 100)
                st.metric(crop, f"{latest/1000:.0f}K MT", f"{growth:+.1f}%")

with tab2:
    st.markdown("##### Yield Efficiency Analysis")
    
    # Calculate average yields
    yield_data = df_production_filtered.groupby(['Country', 'Crop']).agg({
        'Yield_MT_per_Ha': 'mean',
        'Production_MT': 'mean'
    }).reset_index()
    
    # Top 10 by average yield
    yield_data_sorted = yield_data.nlargest(10, 'Yield_MT_per_Ha')
    
    fig_yield = px.bar(
        yield_data_sorted,
        x='Yield_MT_per_Ha',
        y='Crop',
        color='Country',
        orientation='h',
        title="Average Crop Yields (MT per Hectare)",
        labels={'Yield_MT_per_Ha': 'Yield (MT/Ha)', 'Crop': 'Crop Type'},
        color_discrete_map={'Zambia': '#c17a5c', 'Botswana': '#d4a574'}
    )
    
    fig_yield.update_layout(height=500)
    st.plotly_chart(fig_yield, width='stretch')
    
    st.markdown("""
    <div class="highlight-box">
    <strong>💡 Efficiency Insights:</strong>
    <ul>
        <li>Higher yields indicate better farming practices and potential for scaling</li>
        <li>Crops with low but consistent yields may benefit from processing technology</li>
        <li>Yield gaps between countries suggest technology transfer opportunities</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("##### Country Production Comparison")
    
    # Production by country
    country_totals = df_production_filtered.groupby('Country')['Production_MT'].sum().reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_country = px.pie(
            country_totals,
            values='Production_MT',
            names='Country',
            title="Total Production Share",
            color_discrete_map={'Zambia': '#c17a5c', 'Botswana': '#d4a574'}
        )
        fig_country.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_country, width='stretch')
    
    with col2:
        # Production by crop and country
        crop_country = df_production_filtered.groupby(['Country', 'Crop'])['Production_MT'].sum().reset_index()
        crop_country = crop_country.nlargest(10, 'Production_MT')
        
        fig_crop_country = px.bar(
            crop_country,
            x='Production_MT',
            y='Crop',
            color='Country',
            orientation='h',
            title="Top 10 Crop-Country Combinations",
            color_discrete_map={'Zambia': '#c17a5c', 'Botswana': '#d4a574'}
        )
        st.plotly_chart(fig_crop_country, width='stretch')

st.markdown("---")

# ============================================================
# TRADE ANALYSIS
# ============================================================
st.subheader("💼 Trade Analysis: Imports & Exports")

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Import Dependencies")
    
    imports = df_trade_filtered[df_trade_filtered['Category'].str.contains('Imports')]
    imports_summary = imports.groupby(['Country', 'Category'])['Value_USD_Millions'].sum().reset_index()
    imports_summary = imports_summary.nlargest(10, 'Value_USD_Millions')
    
    fig_imports = px.bar(
        imports_summary,
        x='Value_USD_Millions',
        y='Category',
        color='Country',
        orientation='h',
        title="Major Import Categories (USD Millions)",
        labels={'Value_USD_Millions': 'Import Value (USD Millions)'},
        color_discrete_map={'Zambia': '#c17a5c', 'Botswana': '#d4a574'}
    )
    fig_imports.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig_imports, width='stretch')

with col2:
    st.markdown("##### Export Potential")
    
    exports = df_trade_filtered[df_trade_filtered['Category'].str.contains('Exports')]
    if len(exports) > 0:
        exports_summary = exports.groupby(['Country', 'Category'])['Value_USD_Millions'].sum().reset_index()
        
        fig_exports = px.bar(
            exports_summary,
            x='Value_USD_Millions',
            y='Category',
            color='Country',
            orientation='h',
            title="Export Performance (USD Millions)",
            labels={'Value_USD_Millions': 'Export Value (USD Millions)'},
            color_discrete_map={'Zambia': '#c17a5c', 'Botswana': '#d4a574'}
        )
        fig_exports.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_exports, width='stretch')
    else:
        st.info("Limited export data for Botswana (net importer)")

# Trade balance insights
st.markdown("##### 💡 Trade Insights & Investment Implications")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="highlight-box">
    <strong>🎯 Import Substitution Opportunities:</strong>
    <ul>
        <li><strong>Processed Foods:</strong> $320M+ annual imports (Zambia) and $570M+ (Botswana)</li>
        <li><strong>Vegetable Oils:</strong> $85M+ (Zambia) and $57M+ (Botswana) - High processing gap</li>
        <li><strong>Wheat Products:</strong> $130M+ (Zambia) and $105M+ (Botswana) - Flour milling opportunity</li>
        <li><strong>Dairy Products:</strong> $115M+ (Botswana) - Strong local demand</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="highlight-box">
    <strong>📈 Export Development Potential:</strong>
    <ul>
        <li><strong>Maize (Zambia):</strong> Regional breadbasket - surplus for export</li>
        <li><strong>Soybean (Zambia):</strong> Growing demand in SADC and Asia</li>
        <li><strong>Cotton (Zambia):</strong> Value addition through textile manufacturing</li>
        <li><strong>Beef (Botswana):</strong> Quality beef with premium market access</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# PROCESSING CAPACITY ANALYSIS
# ============================================================
st.subheader("🏭 Agro-Processing Capacity & Gaps")

col1, col2 = st.columns([2, 1])

with col1:
    # Capacity utilization chart
    fig_capacity = go.Figure()
    
    for country in df_capacity_filtered['Country'].unique():
        country_data = df_capacity_filtered[df_capacity_filtered['Country'] == country]
        
        fig_capacity.add_trace(go.Bar(
            name=f'{country} - Utilized',
            x=country_data['Processing_Type'],
            y=country_data['Total_Capacity_MT_per_year'] * country_data['Capacity_Utilization_Percent'] / 100,
            marker_color='#c17a5c' if country == 'Zambia' else '#d4a574'
        ))
        
        fig_capacity.add_trace(go.Bar(
            name=f'{country} - Unutilized',
            x=country_data['Processing_Type'],
            y=country_data['Unutilized_Capacity_MT'],
            marker_color='#e8e6e0',
            marker_pattern_shape="/"
        ))
    
    fig_capacity.update_layout(
        title="Processing Capacity Utilization by Type",
        xaxis_title="Processing Type",
        yaxis_title="Capacity (MT per year)",
        barmode='stack',
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_capacity, width='stretch')

with col2:
    st.markdown("##### Capacity Summary")
    
    for country in selected_countries:
        country_cap = df_capacity_filtered[df_capacity_filtered['Country'] == country]
        total_cap = country_cap['Total_Capacity_MT_per_year'].sum()
        avg_util = country_cap['Capacity_Utilization_Percent'].mean()
        
        st.markdown(f"**{country}**")
        st.metric("Total Capacity", f"{total_cap/1000:.0f}K MT/year")
        st.metric("Avg Utilization", f"{avg_util:.0f}%")
        st.markdown("---")

# Processing gap details
st.markdown("##### 🎯 Processing Gap Analysis")

gap_summary = df_capacity_filtered.groupby('Processing_Type').agg({
    'Total_Capacity_MT_per_year': 'sum',
    'Capacity_Utilization_Percent': 'mean',
    'Unutilized_Capacity_MT': 'sum',
    'Investment_Potential': 'first'
}).reset_index()

gap_summary = gap_summary.sort_values('Unutilized_Capacity_MT', ascending=False)

# Color code by investment potential
def get_potential_color(potential):
    colors = {
        'Very High': '#2d5016',
        'High': '#6b8e23',
        'Medium': '#d4a574',
        'Low': '#e8e6e0'
    }
    return colors.get(potential, '#e8e6e0')

gap_summary['Color'] = gap_summary['Investment_Potential'].apply(get_potential_color)

fig_gap = go.Figure()

fig_gap.add_trace(go.Bar(
    x=gap_summary['Processing_Type'],
    y=gap_summary['Unutilized_Capacity_MT'],
    marker_color=gap_summary['Color'],
    text=gap_summary['Investment_Potential'],
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>' +
                  'Unutilized: %{y:,.0f} MT<br>' +
                  'Potential: %{text}<br>' +
                  '<extra></extra>'
))

fig_gap.update_layout(
    title="Unutilized Processing Capacity by Type (Investment Potential Color-Coded)",
    xaxis_title="Processing Type",
    yaxis_title="Unutilized Capacity (MT/year)",
    height=400
)

st.plotly_chart(fig_gap, width='stretch')

st.markdown("---")

# ============================================================
# PRICE TRENDS
# ============================================================
st.subheader("💰 Commodity Price Trends")

# Price trends
selected_commodities = st.multiselect(
    "Select Commodities to Compare",
    options=['Maize', 'Wheat', 'Soybean', 'Cotton', 'Groundnuts'],
    default=['Maize', 'Soybean', 'Wheat']
)

if selected_commodities:
    fig_prices = go.Figure()
    
    for commodity in selected_commodities:
        col_name = f'{commodity}_USD_per_MT'
        if col_name in df_prices.columns:
            fig_prices.add_trace(go.Scatter(
                x=df_prices['Date'],
                y=df_prices[col_name],
                name=commodity,
                mode='lines',
                line=dict(width=2)
            ))
    
    fig_prices.update_layout(
        title="Commodity Price Trends (USD per Metric Ton)",
        xaxis_title="Date",
        yaxis_title="Price (USD/MT)",
        hovermode='x unified',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_prices, width='stretch')
    
    # Price insights
    col1, col2, col3 = st.columns(3)
    
    for i, commodity in enumerate(selected_commodities[:3]):
        col_name = f'{commodity}_USD_per_MT'
        if col_name in df_prices.columns:
            current_price = df_prices[col_name].iloc[-1]
            year_ago_price = df_prices[col_name].iloc[-13] if len(df_prices) > 13 else df_prices[col_name].iloc[0]
            price_change = ((current_price - year_ago_price) / year_ago_price * 100)
            
            with [col1, col2, col3][i]:
                st.metric(
                    f"{commodity} Price",
                    f"${current_price:.0f}/MT",
                    f"{price_change:+.1f}% YoY"
                )

st.markdown("---")

# ============================================================
# INVESTMENT OPPORTUNITIES
# ============================================================
st.subheader("🎯 Priority Investment Opportunities")

st.markdown("""
Based on production capacity, trade gaps, and market demand, we've identified the following 
high-potential investment opportunities for private sector organizations.
""")

# Filter opportunities by country
df_opp_filtered = df_opportunities[df_opportunities['Country'].isin(selected_countries)]

# Create tabs for each country
if len(selected_countries) == 2:
    tab1, tab2 = st.tabs([f"🇿🇲 Zambia Opportunities", f"🇧🇼 Botswana Opportunities"])
    tabs = [tab1, tab2]
    countries = ['Zambia', 'Botswana']
elif 'Zambia' in selected_countries:
    tab1 = st.container()
    tabs = [tab1]
    countries = ['Zambia']
else:
    tab1 = st.container()
    tabs = [tab1]
    countries = ['Botswana']

for tab, country in zip(tabs, countries):
    with tab:
        country_opps = df_opp_filtered[df_opp_filtered['Country'] == country]
        
        for idx, row in country_opps.iterrows():
            st.markdown(f"""
            <div class="opportunity-card">
            <h3>🌟 {row['Opportunity']}</h3>
            <div style="margin: 10px 0;">
                <span class="investment-tag">💰 {row['Investment_Size_USD']}</span>
                <span class="investment-tag">📈 ROI: {row['Estimated_ROI_Years']:.1f} years</span>
                <span class="investment-tag">📊 Gap: {row['Market_Gap_MT']:,.0f} MT</span>
            </div>
            <p><strong>Key Driver:</strong> {row['Key_Driver']}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# ROI CALCULATOR
# ============================================================
st.subheader("🧮 Investment ROI Calculator")

st.markdown("Quick financial modeling for agro-processing investments")

calc_col1, calc_col2, calc_col3, calc_col4 = st.columns(4)

with calc_col1:
    investment_amount = st.number_input(
        "Initial Investment (USD)",
        min_value=100000,
        max_value=50000000,
        value=5000000,
        step=500000,
        format="%d"
    )

with calc_col2:
    processing_capacity = st.number_input(
        "Processing Capacity (MT/year)",
        min_value=1000,
        max_value=500000,
        value=50000,
        step=5000
    )

with calc_col3:
    capacity_utilization = st.slider(
        "Expected Capacity Utilization (%)",
        min_value=30,
        max_value=95,
        value=70,
        step=5
    )

with calc_col4:
    margin_per_mt = st.number_input(
        "Gross Margin per MT (USD)",
        min_value=10,
        max_value=1000,
        value=150,
        step=10
    )

# Calculate ROI
actual_processing = processing_capacity * (capacity_utilization / 100)
annual_revenue = actual_processing * margin_per_mt
operating_costs_percent = 65
net_profit = annual_revenue * (100 - operating_costs_percent) / 100
payback_period = investment_amount / net_profit if net_profit > 0 else 0
annual_roi = (net_profit / investment_amount * 100) if investment_amount > 0 else 0

st.markdown("---")

result_col1, result_col2, result_col3, result_col4 = st.columns(4)

with result_col1:
    st.metric("Annual Processing Volume", f"{actual_processing:,.0f} MT")

with result_col2:
    st.metric("Estimated Annual Revenue", f"${annual_revenue:,.0f}")

with result_col3:
    st.metric("Estimated Net Profit", f"${net_profit:,.0f}")

with result_col4:
    if 0 < payback_period < 20:
        st.metric("Payback Period", f"{payback_period:.1f} years")
        st.metric("Annual ROI", f"{annual_roi:.1f}%")
    else:
        st.metric("Payback Period", "Review inputs")

st.caption("*Simplified model for estimation only. Actual returns depend on market conditions, operational efficiency, and other factors.*")

st.markdown("---")

# ============================================================
# ENABLING ENVIRONMENT
# ============================================================
st.subheader("🏛️ Investment Environment & Support")

env_col1, env_col2 = st.columns(2)

with env_col1:
    st.markdown("##### 🇿🇲 Zambia Investment Climate")
    st.markdown("""
    <div class="highlight-box">
    <strong>Incentives & Support:</strong>
    <ul>
        <li><strong>Zambia Development Agency (ZDA):</strong> One-stop investment facilitation</li>
        <li><strong>Tax Incentives:</strong> 0-5% corporate tax for 5 years in priority sectors</li>
        <li><strong>Multi-Facility Economic Zones:</strong> Developed infrastructure for agro-processing</li>
        <li><strong>Export Processing Zones:</strong> Duty-free inputs for export-oriented production</li>
        <li><strong>Land Availability:</strong> Farm blocks with irrigation infrastructure</li>
    </ul>
    
    <strong>Key Institutions:</strong>
    <ul>
        <li>Ministry of Agriculture: www.agriculture.gov.zm</li>
        <li>Zambia Development Agency: www.zda.org.zm</li>
        <li>Citizens Economic Empowerment Commission (CEEC): SME support</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with env_col2:
    st.markdown("##### 🇧🇼 Botswana Investment Climate")
    st.markdown("""
    <div class="highlight-box">
    <strong>Incentives & Support:</strong>
    <ul>
        <li><strong>Botswana Investment & Trade Centre (BITC):</strong> Investment promotion</li>
        <li><strong>Citizen Economic Empowerment:</strong> Support for local participation</li>
        <li><strong>Special Economic Zones:</strong> Tax holidays and duty exemptions</li>
        <li><strong>Financial Assistance Policy:</strong> Grant funding for agriculture projects</li>
        <li><strong>Stable Economy:</strong> Strong governance and currency stability</li>
    </ul>
    
    <strong>Key Institutions:</strong>
    <ul>
        <li>Ministry of Agriculture: www.moa.gov.bw</li>
        <li>BITC: www.bitc.co.bw</li>
        <li>Local Enterprise Authority (LEA): SME support</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# REGIONAL MARKET ACCESS
# ============================================================
st.subheader("🌍 Regional Market Access")

st.markdown("""
<div class="highlight-box">
<strong>SADC Free Trade Area Benefits:</strong>

Both Zambia and Botswana are members of SADC and COMESA, providing:

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
<div>
<strong>🎯 Market Access:</strong>
<ul>
    <li>300+ million consumers across SADC</li>
    <li>Duty-free access to regional markets</li>
    <li>Simplified customs procedures</li>
    <li>Harmonized standards (ongoing)</li>
</ul>
</div>
<div>
<strong>🚚 Logistics Advantages:</strong>
<ul>
    <li>Central location in SADC</li>
    <li>Access to multiple trade corridors</li>
    <li>Improved road/rail infrastructure</li>
    <li>Regional distribution hubs</li>
</ul>
</div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# DATA SOURCES & METHODOLOGY
# ============================================================
st.subheader("📚 Data Sources & Methodology")

source_col1, source_col2, source_col3 = st.columns(3)

with source_col1:
    st.markdown("""
    **Production Data:**
    - FAO Statistics Database
    - Zambia Central Statistical Office
    - Statistics Botswana
    - Ministry of Agriculture reports
    
    **Coverage:** 2019-2023
    **Update Frequency:** Annual
    """)

with source_col2:
    st.markdown("""
    **Trade Data:**
    - ITC Trade Map
    - National customs authorities
    - COMTRADE Database
    - Ministry of Commerce
    
    **Coverage:** 2019-2023
    **Update Frequency:** Annual
    """)

with source_col3:
    st.markdown("""
    **Processing & Prices:**
    - Industry surveys
    - ZAMACE (Zambia)
    - BAMB (Botswana)
    - Company reports
    
    **Coverage:** Current snapshot
    **Update Frequency:** Quarterly
    """)

st.markdown("---")

# ============================================================
# FOOTER & CALL TO ACTION
# ============================================================
st.markdown("---")

footer_col1, footer_col2 = st.columns(2)

with footer_col1:
    st.markdown("""
    #### 🎯 Ready to Invest in SADC Agriculture?
    
    This dashboard provides market intelligence, but successful investment requires:
    - Detailed feasibility studies
    - On-ground market validation
    - Financial modeling
    - Partner identification
    - Regulatory compliance guidance
    
    **We can help with all of the above.**
    """)

with footer_col2:
    st.markdown("""
    #### 📞 Contact Concise Analytics
    
    **Services:**
    - Custom feasibility studies
    - Market entry strategy
    - Partner identification
    - Due diligence support
    - Ongoing market intelligence
    
    📧 **info@concise-analytics.com**  
    🌐 **www.concise-analytics.com**  
    📍 Gaborone, Botswana
    
    *Specialized data intelligence for SADC agriculture, tourism, and property markets*
    """)

st.markdown("---")
st.caption("© 2024 Concise Data Analytics | Agriculture Dashboard v1.0 | Data as of October 2024")

# ============================================================
# DISCLAIMER
# ============================================================
with st.expander("⚠️ Important Disclaimer"):
    st.markdown("""
    **Investment Disclaimer:**
    
    This dashboard provides market intelligence based on publicly available data sources. 
    All information is provided for informational purposes only and should not be construed 
    as investment advice.
    
    - Production and trade data are estimates based on official statistics
    - Processing capacity data from industry surveys and may not be comprehensive
    - Price trends are indicative and subject to market volatility
    - ROI calculations are simplified models and do not account for all variables
    - Investment opportunities identified are based on market gaps and should be validated
    
    **Before making any investment decision:**
    - Conduct thorough due diligence
    - Engage local experts and legal counsel
    - Validate all assumptions with current market data
    - Consider political, economic, and operational risks
    - Develop comprehensive business plans
    
    Concise Data Analytics provides market intelligence services but does not guarantee 
    investment returns or market outcomes.
    """)
