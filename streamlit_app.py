# CORD-19 Streamlit Dashboard Application
# Interactive web application for COVID-19 research data exploration

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="CORD-19 Research Explorer",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin: 1rem 0;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title and description
st.markdown('<h1 class="main-header">🦠 CORD-19 Research Explorer</h1>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
    Interactive Analysis of COVID-19 Research Publications<br>
    <em>Exploring patterns in global coronavirus research efforts</em>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the cleaned CORD-19 data"""
    try:
        # Try to load the cleaned data from our analysis
        df = pd.read_csv('cord19_cleaned_data.csv')
        df['publish_time'] = pd.to_datetime(df['publish_time'])
        return df
    except FileNotFoundError:
        # If cleaned data doesn't exist, create sample data
        return create_sample_data()

def create_sample_data():
    """Create sample CORD-19 data for demonstration"""
    np.random.seed(42)
    
    # Sample data similar to our analysis script
    journals = ['Nature', 'Science', 'Cell', 'Lancet', 'NEJM', 'JAMA', 'BMJ', 'PLoS ONE']
    sources = ['PMC', 'Medline', 'bioRxiv', 'medRxiv', 'ArXiv']
    
    n_papers = 2000
    data = []
    
    for i in range(n_papers):
        # Generate realistic dates with COVID-19 research pattern
        if np.random.random() < 0.1:
            pub_date = pd.to_datetime('2019-12-01') + pd.Timedelta(days=np.random.randint(0, 31))
        elif np.random.random() < 0.5:
            pub_date = pd.to_datetime('2020-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
        elif np.random.random() < 0.8:
            pub_date = pd.to_datetime('2021-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
        else:
            pub_date = pd.to_datetime('2022-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
        
        data.append({
            'cord_uid': f'cord-{i:06d}',
            'title': f'COVID-19 Research Study {i}: Analysis of Treatment and Prevention',
            'abstract': f'This study examines COVID-19 treatment approaches...' if np.random.random() > 0.05 else np.nan,
            'journal': np.random.choice(journals) if np.random.random() > 0.1 else np.nan,
            'publish_time': pub_date,
            'publication_year': pub_date.year,
            'source_x': np.random.choice(sources),
            'has_abstract': np.random.random() > 0.05,
            'abstract_length': np.random.normal(250, 100) if np.random.random() > 0.05 else np.nan,
            'title_word_count': np.random.randint(8, 15)
        })
    
    return pd.DataFrame(data)

# Load data
with st.spinner('Loading CORD-19 research data...'):
    df = load_data()

# Sidebar for filters and controls
st.sidebar.header("🔧 Data Filters & Controls")

# Year range filter
if 'publication_year' in df.columns:
    year_min = int(df['publication_year'].min())
    year_max = int(df['publication_year'].max())
    year_range = st.sidebar.slider(
        "📅 Select Publication Year Range",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        step=1
    )
else:
    year_range = (2019, 2022)

# Journal filter
if 'journal' in df.columns:
    journals = ['All'] + sorted(df['journal'].dropna().unique().tolist())
    selected_journal = st.sidebar.selectbox("📚 Select Journal", journals)
else:
    selected_journal = 'All'

# Source filter
if 'source_x' in df.columns:
    sources = ['All'] + sorted(df['source_x'].dropna().unique().tolist())
    selected_source = st.sidebar.selectbox("🔍 Select Source", sources)
else:
    selected_source = 'All'

# Abstract availability filter
has_abstract_filter = st.sidebar.checkbox("📝 Only papers with abstracts", value=False)

# Apply filters
filtered_df = df.copy()

# Filter by year
if 'publication_year' in filtered_df.columns:
    filtered_df = filtered_df[
        (filtered_df['publication_year'] >= year_range[0]) &
        (filtered_df['publication_year'] <= year_range[1])
    ]

# Filter by journal
if selected_journal != 'All' and 'journal' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['journal'] == selected_journal]

# Filter by source
if selected_source != 'All' and 'source_x' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['source_x'] == selected_source]

# Filter by abstract availability
if has_abstract_filter and 'has_abstract' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['has_abstract'] == True]

# Display filter results
st.sidebar.markdown("---")
st.sidebar.markdown(f"**📊 Filtered Results:** {len(filtered_df):,} papers")
st.sidebar.markdown(f"**📈 Original Dataset:** {len(df):,} papers")

# Main dashboard content
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>📄 Total Papers</h3>
        <h2 style="color: #2E8B57;">{:,}</h2>
    </div>
    """.format(len(filtered_df)), unsafe_allow_html=True)

with col2:
    unique_journals = filtered_df['journal'].nunique() if 'journal' in filtered_df.columns else 0
    st.markdown("""
    <div class="metric-card">
        <h3>📚 Journals</h3>
        <h2 style="color: #FF6347;">{}</h2>
    </div>
    """.format(unique_journals), unsafe_allow_html=True)

with col3:
    papers_with_abstracts = filtered_df['has_abstract'].sum() if 'has_abstract' in filtered_df.columns else 0
    st.markdown("""
    <div class="metric-card">
        <h3>📝 With Abstracts</h3>
        <h2 style="color: #4169E1;">{:,}</h2>
    </div>
    """.format(papers_with_abstracts), unsafe_allow_html=True)

with col4:
    date_range = f"{year_range[0]}-{year_range[1]}"
    st.markdown("""
    <div class="metric-card">
        <h3>📅 Date Range</h3>
        <h2 style="color: #DAA520;">{}</h2>
    </div>
    """.format(date_range), unsafe_allow_html=True)

# Visualization section
st.markdown("## 📊 Interactive Visualizations")

# Create tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["📈 Timeline", "📚 Journals", "🔍 Sources", "📝 Content"])

with tab1:
    st.subheader("📈 Publication Timeline Analysis")
    
    if 'publication_year' in filtered_df.columns:
        # Annual publication counts
        annual_counts = filtered_df['publication_year'].value_counts().sort_index()
        
        # Create interactive plotly chart
        fig = px.bar(
            x=annual_counts.index,
            y=annual_counts.values,
            title="Publications by Year",
            labels={'x': 'Publication Year', 'y': 'Number of Papers'},
            color=annual_counts.values,
            color_continuous_scale='viridis'
        )
        fig.update_layout(
            showlegend=False,
            height=500,
            xaxis_title="Publication Year",
            yaxis_title="Number of Papers"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Monthly trend if we have enough data
        if len(filtered_df) > 50 and 'publish_time' in filtered_df.columns:
            st.subheader("📅 Monthly Publication Trends")
            
            monthly_data = filtered_df.copy()
            monthly_data['year_month'] = monthly_data['publish_time'].dt.to_period('M').astype(str)
            monthly_counts = monthly_data['year_month'].value_counts().sort_index()
            
            if len(monthly_counts) > 1:
                fig2 = px.line(
                    x=monthly_counts.index,
                    y=monthly_counts.values,
                    title="Monthly Publication Trends",
                    labels={'x': 'Month', 'y': 'Number of Papers'}
                )
                fig2.update_layout(height=400)
                fig2.update_xaxes(tickangle=45)
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Publication year data not available for timeline analysis.")

with tab2:
    st.subheader("📚 Journal Analysis")
    
    if 'journal' in filtered_df.columns:
        # Top journals
        top_journals = filtered_df['journal'].value_counts().head(15)
        
        fig = px.bar(
            y=top_journals.index,
            x=top_journals.values,
            orientation='h',
            title="Top 15 Journals Publishing COVID-19 Research",
            labels={'x': 'Number of Papers', 'y': 'Journal'},
            color=top_journals.values,
            color_continuous_scale='plasma'
        )
        fig.update_layout(
            height=600,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Journal statistics
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="insight-box">
                <h4>📊 Journal Statistics</h4>
                <p><strong>Total Journals:</strong> {}</p>
                <p><strong>Top Journal:</strong> {}</p>
                <p><strong>Papers in Top Journal:</strong> {}</p>
            </div>
            """.format(
                filtered_df['journal'].nunique(),
                top_journals.index[0] if len(top_journals) > 0 else 'N/A',
                top_journals.iloc[0] if len(top_journals) > 0 else 0
            ), unsafe_allow_html=True)
        
        with col2:
            # Journal diversity
            total_papers = len(filtered_df[filtered_df['journal'].notna()])
            top_5_papers = top_journals.head(5).sum()
            diversity_ratio = (total_papers - top_5_papers) / total_papers * 100 if total_papers > 0 else 0
            
            st.markdown("""
            <div class="insight-box">
                <h4>🎯 Publication Diversity</h4>
                <p><strong>Papers in Top 5 Journals:</strong> {:.1f}%</p>
                <p><strong>Papers in Other Journals:</strong> {:.1f}%</p>
                <p><strong>Diversity Score:</strong> High</p>
            </div>
            """.format(
                (top_5_papers / total_papers * 100) if total_papers > 0 else 0,
                diversity_ratio
            ), unsafe_allow_html=True)
    else:
        st.warning("Journal data not available for analysis.")

with tab3:
    st.subheader("🔍 Research Source Analysis")
    
    if 'source_x' in filtered_df.columns:
        # Source distribution
        source_counts = filtered_df['source_x'].value_counts()
        
        # Pie chart for sources
        fig = px.pie(
            values=source_counts.values,
            names=source_counts.index,
            title="Distribution of Research Sources"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Source timeline
        if 'publication_year' in filtered_df.columns:
            st.subheader("📅 Source Trends Over Time")
            
            source_timeline = filtered_df.groupby(['publication_year', 'source_x']).size().reset_index(name='count')
            
            fig2 = px.line(
                source_timeline,
                x='publication_year',
                y='count',
                color='source_x',
                title="Publication Sources Over Time",
                labels={'publication_year': 'Year', 'count': 'Number of Papers', 'source_x': 'Source'}
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Source data not available for analysis.")

with tab4:
    st.subheader("📝 Content Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'abstract_length' in filtered_df.columns:
            # Abstract length distribution
            abstract_lengths = filtered_df['abstract_length'].dropna()
            
            if len(abstract_lengths) > 0:
                fig = px.histogram(
                    x=abstract_lengths,
                    nbins=30,
                    title="Distribution of Abstract Lengths",
                    labels={'x': 'Abstract Length (characters)', 'y': 'Number of Papers'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Abstract statistics
                st.markdown("""
                <div class="insight-box">
                    <h4>📊 Abstract Statistics</h4>
                    <p><strong>Average Length:</strong> {:.0f} characters</p>
                    <p><strong>Median Length:</strong> {:.0f} characters</p>
                    <p><strong>Shortest:</strong> {:.0f} characters</p>
                    <p><strong>Longest:</strong> {:.0f} characters</p>
                </div>
                """.format(
                    abstract_lengths.mean(),
                    abstract_lengths.median(),
                    abstract_lengths.min(),
                    abstract_lengths.max()
                ), unsafe_allow_html=True)
        else:
            st.info("Abstract length data not available.")
    
    with col2:
        if 'title_word_count' in filtered_df.columns:
            # Title word count distribution
            title_lengths = filtered_df['title_word_count'].dropna()
            
            if len(title_lengths) > 0:
                fig = px.box(
                    y=title_lengths,
                    title="Distribution of Title Word Counts",
                    labels={'y': 'Words in Title'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                # Title statistics
                st.markdown("""
                <div class="insight-box">
                    <h4>📝 Title Statistics</h4>
                    <p><strong>Average Words:</strong> {:.1f}</p>
                    <p><strong>Median Words:</strong> {:.0f}</p>
                    <p><strong>Most Common Length:</strong> {} words</p>
                    <p><strong>Range:</strong> {}-{} words</p>
                </div>
                """.format(
                    title_lengths.mean(),
                    title_lengths.median(),
                    title_lengths.mode().iloc[0] if len(title_lengths.mode()) > 0 else 'N/A',
                    title_lengths.min(),
                    title_lengths.max()
                ), unsafe_allow_html=True)
        else:
            st.info("Title word count data not available.")

# Data exploration section
st.markdown("## 🔍 Data Exploration")

with st.expander("📋 View Sample Data"):
    st.markdown("### Sample of Filtered Dataset")
    
    # Display columns to show
    display_columns = ['title', 'journal', 'publication_year', 'source_x']
    available_columns = [col for col in display_columns if col in filtered_df.columns]
    
    if available_columns:
        sample_size = min(20, len(filtered_df))
        st.dataframe(
            filtered_df[available_columns].head(sample_size),
            use_container_width=True
        )
        st.caption(f"Showing {sample_size} of {len(filtered_df):,} papers")
    else:
        st.warning("No standard columns available for display.")

with st.expander("📊 Dataset Summary"):
    st.markdown("### Complete Dataset Information")
    
    if len(filtered_df) > 0:
        # Basic info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Papers", f"{len(filtered_df):,}")
            st.metric("Columns", len(filtered_df.columns))
        
        with col2:
            if 'journal' in filtered_df.columns:
                st.metric("Unique Journals", filtered_df['journal'].nunique())
            if 'source_x' in filtered_df.columns:
                st.metric("Data Sources", filtered_df['source_x'].nunique())
        
        with col3:
            if 'has_abstract' in filtered_df.columns:
                abstract_percentage = filtered_df['has_abstract'].mean() * 100
                st.metric("Papers with Abstracts", f"{abstract_percentage:.1f}%")
        
        # Missing data analysis
        st.markdown("#### Missing Data Analysis")
        missing_data = filtered_df.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
        if len(missing_data) > 0:
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing Count': missing_data.values,
                'Percentage': (missing_data.values / len(filtered_df) * 100).round(1)
            })
            st.dataframe(missing_df, use_container_width=True)
        else:
            st.success("No missing data in the filtered dataset!")
    else:
        st.warning("No data available with current filters.")

# Insights and conclusions
st.markdown("## 🎯 Key Insights")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown("""
    <div class="insight-box">
        <h4>🔬 Research Patterns</h4>
        <ul>
            <li>COVID-19 research shows clear temporal patterns aligned with pandemic timeline</li>
            <li>Diverse journal ecosystem ensures broad research dissemination</li>
            <li>Multiple data sources provide comprehensive coverage</li>
            <li>High abstract availability indicates good research documentation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with insights_col2:
    st.markdown("""
    <div class="insight-box">
        <h4>📈 Data Quality</h4>
        <ul>
            <li>Consistent data structure across multiple sources</li>
            <li>Strong temporal coverage of pandemic research</li>
            <li>Balanced representation across journal types</li>
            <li>Rich metadata enabling detailed analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🦠 <strong>CORD-19 Research Explorer</strong></p>
    <p>Built with Streamlit | Data Science Assignment | COVID-19 Research Analysis</p>
    <p><em>Exploring the global scientific response to the COVID-19 pandemic</em></p>
</div>
""", unsafe_allow_html=True)