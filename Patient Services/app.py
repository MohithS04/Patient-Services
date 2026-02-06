import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from analysis import load_and_process_data

# Page Config
st.set_page_config(page_title="MediMetrics: Patient Experience", layout="wide", page_icon="🏥")

# Load Data
@st.cache_data
def get_data():
    return load_and_process_data()

df, report = get_data()

if df is None:
    st.error(report['error'])
    st.stop()

# Sidebar Filters
st.sidebar.header("Filters")
hospital_filter = st.sidebar.multiselect("Select Hospital", options=df['hospital'].unique(), default=df['hospital'].unique())
dept_filter = st.sidebar.multiselect("Select Department", options=df['department'].unique(), default=df['department'].unique())

# Apply Filters
filtered_df = df[
    (df['hospital'].isin(hospital_filter)) & 
    (df['department'].isin(dept_filter))
]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Overview", "🔍 Deep Dive Analysis", "💡 Key Drivers", "🛠️ Data Quality"])

# --- TAB 1: OVERVIEW ---
with tab1:
    st.title("Patient Satisfaction Overview")
    
    # KPIS
    col1, col2, col3, col4 = st.columns(4)
    avg_score = filtered_df['overall_satisfaction'].mean()
    prev_month_score = filtered_df[filtered_df['month_year'] == '2024-11']['overall_satisfaction'].mean() # Mock prev
    score_delta = round(avg_score - prev_month_score, 2)
    
    col1.metric("Overall Satisfaction", f"{avg_score:.1f}/10", f"{score_delta}")
    col2.metric("Avg Wait Time", f"{filtered_df['wait_time_min'].mean():.1f} min")
    col3.metric("Avg LOS", f"{filtered_df['length_of_stay_hours'].mean():.1f} hrs")
    col4.metric("Surveys Received", f"{len(filtered_df)}")

    # Trend Chart
    st.subheader("Satisfaction Trend (Last 12 Months)")
    trend_df = filtered_df.groupby('month_year')['overall_satisfaction'].mean().reset_index()
    fig_trend = px.line(trend_df, x='month_year', y='overall_satisfaction', markers=True, 
                        title="Average Satisfaction Score by Month")
    fig_trend.update_layout(yaxis_range=[0, 10])
    st.plotly_chart(fig_trend, use_container_width=True)

# --- TAB 2: DEEP DIVE ---
with tab2:
    st.title("Department & Provider Deep Dive")
    
    # Heatmap: Dept vs Time
    st.subheader("Score Heatmap: Department vs. Visit Type")
    heatmap_data = filtered_df.pivot_table(index='department', columns='visit_type', values='overall_satisfaction', aggfunc='mean')
    fig_heat = px.imshow(heatmap_data, text_auto=True, color_continuous_scale='RdBu', origin='lower',
                         title="Average Scores by Department & Visit Type")
    st.plotly_chart(fig_heat, use_container_width=True)

    # Provider Comparison
    st.subheader("Lowest Performing Providers (Bottom 10)")
    provider_perf = filtered_df.groupby('provider')[['overall_satisfaction', 'wait_time_min']].mean().sort_values('overall_satisfaction').head(10).reset_index()
    fig_prov = px.bar(provider_perf, x='overall_satisfaction', y='provider', orientation='h', 
                      color='wait_time_min', title="Bottom 10 Providers by Score (Color = Wait Time)")
    st.plotly_chart(fig_prov, use_container_width=True)

# --- TAB 3: DRIVERS ---
with tab3:
    st.title("Key Drivers of Satisfaction")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info("💡 Insight: **Wait Time** is the strongest negative driver. As wait time increases, satisfaction drops significantly.")
        st.dataframe(pd.DataFrame(list(report['correlations'].items()), columns=['Metric', 'Correlation with Sat.']))

    with col2:
        # Scatter Plot
        st.subheader("Wait Time vs. Satisfaction")
        # Sample for performance if needed, but 3k is fine
        fig_scatter = px.scatter(filtered_df, x='wait_time_min', y='overall_satisfaction', color='department',
                                 trendline='ols', opacity=0.6,
                                 title="Correlation: Wait Time vs. Satisfaction Score")
        st.plotly_chart(fig_scatter, use_container_width=True)

# --- TAB 4: DATA QUALITY ---
with tab4:
    st.title("Data Quality Report")
    st.warning(f"⚠️ Found {report['orphan_surveys_count']} ({report['orphan_surveys_pct']}%) surveys linked to non-existent encounters.")
    
    st.write("### Data Integrity Issues")
    dq_df = pd.DataFrame([
        {"Issue": "Orphan Surveys", "Count": report['orphan_surveys_count'], "Impact": "Cannot link to operational metrics for driver analysis"},
        {"Issue": "Missing Provider Info", "Count": report['missing_providers'], "Impact": "Provider-level attribution gaps"}
    ])
    st.table(dq_df)
    
    st.write("### Raw Data Sample (First 10 rows)")
    st.dataframe(filtered_df.head(10))
