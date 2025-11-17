# -*- coding: utf-8 -*-
# CORD-19 Data Analysis Assignment
# COVID-19 Research Papers Analysis with Streamlit Dashboard
#
# This script performs comprehensive analysis of the CORD-19 dataset
# and includes all required components for the assignment.

"""
CORD-19 RESEARCH DATASET ANALYSIS
=================================

Assignment Components:
1. Data Loading and Basic Exploration
2. Data Cleaning and Preparation
3. Data Analysis and Visualization
4. Streamlit Application (see separate file)
5. Documentation and Findings

Dataset: CORD-19 metadata.csv
Focus: COVID-19 research papers analysis
"""

import sys
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
from collections import Counter
import re
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go

# Set UTF-8 encoding for console output (Windows compatibility)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configure settings
warnings.filterwarnings('ignore')
plt.style.use('default')
sns.set_palette("husl")

print("=" * 80)
print("CORD-19 COVID-19 RESEARCH DATASET ANALYSIS")
print("Assignment: Frameworks and Libraries")
print("=" * 80)

# ============================================================================
# PART 1: DATA LOADING AND BASIC EXPLORATION
# ============================================================================

print("\n📊 PART 1: DATA LOADING AND BASIC EXPLORATION")
print("=" * 60)

def load_cord19_data():
    """
    Load CORD-19 metadata with error handling
    Returns a pandas DataFrame
    """
    try:
        # Try to load the actual CORD-19 metadata file
        print("🔍 Attempting to load metadata.csv...")
        df = pd.read_csv('metadata.csv')
        print("✅ Successfully loaded CORD-19 metadata.csv!")
        return df
        
    except FileNotFoundError:
        print("⚠️ metadata.csv not found. Creating sample CORD-19 dataset for demonstration...")
        return create_sample_cord19_data()
    
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        print("Creating sample dataset...")
        return create_sample_cord19_data()

def create_sample_cord19_data():
    """
    Create a realistic sample CORD-19 dataset for demonstration
    """
    np.random.seed(42)
    
    # Sample journal names
    journals = [
        'Nature', 'Science', 'Cell', 'Lancet', 'New England Journal of Medicine',
        'JAMA', 'BMJ', 'PLoS ONE', 'Nature Medicine', 'Science Translational Medicine',
        'Journal of Virology', 'Virology', 'Clinical Infectious Diseases',
        'Emerging Infectious Diseases', 'Journal of Medical Virology'
    ]
    
    # Sample sources
    sources = ['PMC', 'Medline', 'bioRxiv', 'medRxiv', 'ArXiv', 'WHO']
    
    # Sample title keywords for COVID-19 research
    title_keywords = [
        'COVID-19', 'SARS-CoV-2', 'coronavirus', 'pandemic', 'vaccination',
        'treatment', 'diagnosis', 'epidemiology', 'transmission', 'symptoms',
        'clinical', 'therapeutic', 'antiviral', 'antibody', 'immunity',
        'respiratory', 'pneumonia', 'outbreak', 'public health', 'lockdown'
    ]
    
    # Generate sample data
    n_papers = 5000  # Reasonable sample size
    data = []
    
    # Generate dates with realistic COVID-19 research timeline
    start_date = pd.to_datetime('2019-12-01')
    end_date = pd.to_datetime('2022-12-31')
    
    for i in range(n_papers):
        # Create realistic publication date distribution (peak in 2020-2021)
        if np.random.random() < 0.1:  # 10% from 2019
            pub_date = start_date + pd.Timedelta(days=np.random.randint(0, 31))
        elif np.random.random() < 0.5:  # 40% from 2020
            pub_date = pd.to_datetime('2020-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
        elif np.random.random() < 0.8:  # 30% from 2021
            pub_date = pd.to_datetime('2021-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
        else:  # 20% from 2022
            pub_date = pd.to_datetime('2022-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
        
        # Generate realistic title
        num_keywords = np.random.randint(2, 5)
        selected_keywords = np.random.choice(title_keywords, num_keywords, replace=False)
        title = f"Analysis of {' and '.join(selected_keywords)} in clinical settings"
        
        # Generate abstract (some missing)
        if np.random.random() > 0.05:  # 95% have abstracts
            abstract_length = np.random.randint(100, 500)
            abstract = f"This study examines {selected_keywords[0]} with {abstract_length} word abstract..."
        else:
            abstract = np.nan
            
        # Generate authors (some missing)
        if np.random.random() > 0.02:  # 98% have authors
            num_authors = np.random.randint(1, 8)
            authors = f"Author{i}_1, Author{i}_2" if num_authors > 1 else f"Author{i}_1"
        else:
            authors = np.nan
        
        data.append({
            'cord_uid': f'cord-{i:06d}',
            'title': title,
            'abstract': abstract,
            'authors': authors,
            'journal': np.random.choice(journals) if np.random.random() > 0.1 else np.nan,
            'publish_time': pub_date.strftime('%Y-%m-%d') if np.random.random() > 0.05 else np.nan,
            'source_x': np.random.choice(sources),
            'doi': f'10.1000/sample.{i}' if np.random.random() > 0.1 else np.nan,
            'pmcid': f'PMC{1000000 + i}' if np.random.random() > 0.3 else np.nan,
            'url': f'https://example.com/paper_{i}' if np.random.random() > 0.2 else np.nan
        })
    
    df = pd.DataFrame(data)
    print(f"✅ Created sample CORD-19 dataset with {len(df)} papers")
    return df

# Load the data
df = load_cord19_data()

print(f"\n📋 DATASET OVERVIEW")
print("-" * 30)
print(f"Dataset dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

print(f"\n🔍 FIRST 5 ROWS:")
print(df.head())

print(f"\n🔍 LAST 5 ROWS:")
print(df.tail())

print(f"\n📊 COLUMN INFORMATION:")
print(df.info())

print(f"\n🏷️ DATA TYPES:")
print(df.dtypes)

print(f"\n📈 DATASET STRUCTURE:")
print(f"Columns: {list(df.columns)}")

# ============================================================================
# PART 2: DATA CLEANING AND PREPARATION
# ============================================================================

print(f"\n\n🧹 PART 2: DATA CLEANING AND PREPARATION")
print("=" * 60)

print(f"\n❓ MISSING VALUES ANALYSIS:")
print("-" * 35)

missing_analysis = pd.DataFrame({
    'Column': df.columns,
    'Missing_Count': df.isnull().sum().values,
    'Missing_Percentage': (df.isnull().sum() / len(df) * 100).values
})
missing_analysis = missing_analysis[missing_analysis['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)

if len(missing_analysis) > 0:
    print(missing_analysis.to_string(index=False))
    
    print(f"\n🎯 Missing Value Summary:")
    for _, row in missing_analysis.iterrows():
        print(f"  • {row['Column']}: {row['Missing_Count']} ({row['Missing_Percentage']:.1f}%)")
else:
    print("✅ No missing values found!")

print(f"\n🔄 DATA CLEANING PROCESS:")
print("-" * 30)

# Create a copy for cleaning
df_clean = df.copy()
original_shape = df_clean.shape

# 1. Handle publication dates
print("📅 Processing publication dates...")
if 'publish_time' in df_clean.columns:
    # Convert to datetime
    df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')
    
    # Extract year, month for analysis
    df_clean['publication_year'] = df_clean['publish_time'].dt.year
    df_clean['publication_month'] = df_clean['publish_time'].dt.month
    
    # Filter reasonable date range for COVID-19 research
    valid_years = (df_clean['publication_year'] >= 2019) & (df_clean['publication_year'] <= 2023)
    print(f"  ✅ Dates processed. Valid years: {df_clean[valid_years]['publication_year'].nunique()}")
else:
    print("  ⚠️ No publish_time column found")

# 2. Clean text fields
print("📝 Processing text fields...")

# Clean titles
if 'title' in df_clean.columns:
    df_clean['title_length'] = df_clean['title'].str.len()
    df_clean['title_word_count'] = df_clean['title'].str.split().str.len()
    print(f"  ✅ Title processing complete")

# Clean abstracts
if 'abstract' in df_clean.columns:
    df_clean['has_abstract'] = df_clean['abstract'].notna()
    df_clean['abstract_length'] = df_clean['abstract'].str.len()
    df_clean['abstract_word_count'] = df_clean['abstract'].str.split().str.len()
    print(f"  ✅ Abstract processing complete")

# 3. Clean categorical fields
print("🏷️ Processing categorical fields...")

# Clean journal names
if 'journal' in df_clean.columns:
    df_clean['journal'] = df_clean['journal'].str.strip()
    df_clean['has_journal'] = df_clean['journal'].notna()
    print(f"  ✅ Journal processing complete")

# Clean source information
if 'source_x' in df_clean.columns:
    df_clean['source_x'] = df_clean['source_x'].str.strip()
    print(f"  ✅ Source processing complete")

# 4. Remove duplicates
print("🔄 Checking for duplicates...")
if 'title' in df_clean.columns:
    initial_count = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=['title'], keep='first')
    removed_count = initial_count - len(df_clean)
    print(f"  ✅ Removed {removed_count} duplicate titles")

print(f"\n✅ DATA CLEANING SUMMARY:")
print(f"  • Original shape: {original_shape}")
print(f"  • Cleaned shape: {df_clean.shape}")
print(f"  • Rows removed: {original_shape[0] - df_clean.shape[0]}")

# ============================================================================
# PART 3: DATA ANALYSIS AND VISUALIZATION
# ============================================================================

print(f"\n\n📊 PART 3: DATA ANALYSIS AND VISUALIZATION")
print("=" * 60)

# Create figure for multiple subplots
fig = plt.figure(figsize=(20, 16))

# Analysis 1: Publications by Year
print("📈 Analysis 1: Publications by Year")
if 'publication_year' in df_clean.columns:
    year_counts = df_clean['publication_year'].value_counts().sort_index()
    
    plt.subplot(2, 3, 1)
    bars = plt.bar(year_counts.index, year_counts.values, 
                   color='steelblue', alpha=0.8, edgecolor='black')
    plt.title('📈 COVID-19 Research Publications by Year', fontsize=14, fontweight='bold')
    plt.xlabel('Publication Year')
    plt.ylabel('Number of Papers')
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, year_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(year_counts)*0.01, 
                f'{value}', ha='center', va='bottom', fontweight='bold')
    
    print(f"  • Peak year: {year_counts.idxmax()} ({year_counts.max()} papers)")
    print(f"  • Total years covered: {len(year_counts)}")

# Analysis 2: Top Journals
print("\n📚 Analysis 2: Top Publishing Journals")
if 'journal' in df_clean.columns:
    top_journals = df_clean['journal'].value_counts().head(10)
    
    plt.subplot(2, 3, 2)
    bars = plt.barh(range(len(top_journals)), top_journals.values, 
                    color='lightcoral', alpha=0.8, edgecolor='black')
    plt.title('📚 Top 10 Journals Publishing COVID-19 Research', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Papers')
    plt.yticks(range(len(top_journals)), top_journals.index)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_journals.values)):
        plt.text(value + max(top_journals)*0.01, i, f'{value}', 
                va='center', ha='left', fontweight='bold')
    
    print(f"  • Top journal: {top_journals.index[0]} ({top_journals.iloc[0]} papers)")
    print(f"  • Unique journals: {df_clean['journal'].nunique()}")

# Analysis 3: Research Sources
print("\n🔍 Analysis 3: Research Sources")
if 'source_x' in df_clean.columns:
    source_counts = df_clean['source_x'].value_counts()
    
    plt.subplot(2, 3, 3)
    colors = plt.cm.Set3(np.linspace(0, 1, len(source_counts)))
    wedges, texts, autotexts = plt.pie(source_counts.values, labels=source_counts.index, 
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('🔍 Distribution of Research Sources', fontsize=14, fontweight='bold')
    
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
    
    print(f"  • Primary source: {source_counts.index[0]} ({source_counts.iloc[0]} papers)")
    print(f"  • Total sources: {len(source_counts)}")

# Analysis 4: Abstract Length Distribution
print("\n📝 Analysis 4: Abstract Length Analysis")
if 'abstract_length' in df_clean.columns:
    abstract_lengths = df_clean['abstract_length'].dropna()
    
    plt.subplot(2, 3, 4)
    plt.hist(abstract_lengths, bins=30, alpha=0.7, color='lightgreen', 
             edgecolor='black', density=True)
    plt.axvline(abstract_lengths.mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {abstract_lengths.mean():.0f}')
    plt.axvline(abstract_lengths.median(), color='blue', linestyle='--', 
                linewidth=2, label=f'Median: {abstract_lengths.median():.0f}')
    plt.title('📝 Distribution of Abstract Lengths', fontsize=14, fontweight='bold')
    plt.xlabel('Abstract Length (characters)')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    print(f"  • Average abstract length: {abstract_lengths.mean():.0f} characters")
    print(f"  • Papers with abstracts: {df_clean['has_abstract'].sum()}")

# Analysis 5: Monthly Publication Trends
print("\n📅 Analysis 5: Monthly Publication Trends")
if 'publication_year' in df_clean.columns and 'publication_month' in df_clean.columns:
    # Focus on 2020-2021 for detailed monthly analysis
    monthly_data = df_clean[(df_clean['publication_year'].isin([2020, 2021]))].copy()
    monthly_data['year_month'] = monthly_data['publish_time'].dt.to_period('M')
    monthly_counts = monthly_data['year_month'].value_counts().sort_index()
    
    plt.subplot(2, 3, 5)
    plt.plot(range(len(monthly_counts)), monthly_counts.values, 
             marker='o', linewidth=2, markersize=6, color='purple')
    plt.title('📅 Monthly Publications (2020-2021)', fontsize=14, fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Number of Papers')
    plt.xticks(range(0, len(monthly_counts), 3), 
               [str(monthly_counts.index[i]) for i in range(0, len(monthly_counts), 3)], 
               rotation=45)
    plt.grid(True, alpha=0.3)
    
    print(f"  • Peak month: {monthly_counts.idxmax()} ({monthly_counts.max()} papers)")

# Analysis 6: Title Word Cloud (Simple word frequency)
print("\n☁️ Analysis 6: Title Word Analysis")
if 'title' in df_clean.columns:
    plt.subplot(2, 3, 6)
    
    # Simple word frequency analysis
    all_titles = ' '.join(df_clean['title'].dropna().str.lower())
    # Remove common stop words and clean
    stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had']
    words = re.findall(r'\b\w+\b', all_titles)
    words = [word for word in words if len(word) > 2 and word not in stop_words]
    
    word_freq = Counter(words)
    top_words = dict(word_freq.most_common(20))
    
    # Create a simple bar chart instead of word cloud for compatibility
    words_list = list(top_words.keys())[:10]
    freq_list = list(top_words.values())[:10]
    
    bars = plt.barh(range(len(words_list)), freq_list, color='orange', alpha=0.7, edgecolor='black')
    plt.title('☁️ Most Frequent Words in Titles', fontsize=14, fontweight='bold')
    plt.xlabel('Frequency')
    plt.yticks(range(len(words_list)), words_list)
    plt.gca().invert_yaxis()
    
    for i, (bar, value) in enumerate(zip(bars, freq_list)):
        plt.text(value + max(freq_list)*0.01, i, f'{value}', 
                va='center', ha='left', fontweight='bold')
    
    print(f"  • Most common word: '{words_list[0]}' ({freq_list[0]} occurrences)")
    print(f"  • Unique words in titles: {len(word_freq)}")

plt.tight_layout(pad=3.0)

# Save the figure to a file
output_figure = 'cord19_visualizations.png'
plt.savefig(output_figure, dpi=300, bbox_inches='tight')
print(f"\n📊 Visualizations saved as '{output_figure}'")

# Display the figure
plt.show()

# ============================================================================
# ADDITIONAL STATISTICAL ANALYSIS
# ============================================================================

print(f"\n📈 DETAILED STATISTICAL ANALYSIS")
print("-" * 40)

# Time-based analysis
if 'publication_year' in df_clean.columns:
    print("📅 Temporal Analysis:")
    yearly_stats = df_clean.groupby('publication_year').agg({
        'title': 'count',
        'has_abstract': 'sum',
        'abstract_length': 'mean'
    }).round(2)
    yearly_stats.columns = ['Papers_Count', 'Papers_with_Abstract', 'Avg_Abstract_Length']
    print(yearly_stats)

# Journal analysis
if 'journal' in df_clean.columns:
    print(f"\n📚 Journal Analysis:")
    journal_stats = df_clean['journal'].describe()
    print(f"  • Unique journals: {journal_stats['unique']}")
    print(f"  • Most frequent journal: {journal_stats['top']} ({journal_stats['freq']} papers)")

# Content analysis
print(f"\n📝 Content Analysis:")
if 'title_word_count' in df_clean.columns:
    print(f"  • Average title length: {df_clean['title_word_count'].mean():.1f} words")
    print(f"  • Title length range: {df_clean['title_word_count'].min()}-{df_clean['title_word_count'].max()} words")

if 'abstract_word_count' in df_clean.columns:
    print(f"  • Average abstract length: {df_clean['abstract_word_count'].mean():.1f} words")
    print(f"  • Papers with abstracts: {df_clean['has_abstract'].sum()}/{len(df_clean)} ({df_clean['has_abstract'].mean()*100:.1f}%)")

# ============================================================================
# EXPORT CLEANED DATA
# ============================================================================

print(f"\n💾 EXPORTING CLEANED DATA")
print("-" * 30)

# Save cleaned dataset
output_filename = 'cord19_cleaned_data.csv'
df_clean.to_csv(output_filename, index=False)
print(f"✅ Cleaned dataset saved as '{output_filename}'")

# Save summary statistics
summary_stats = {
    'total_papers': len(df_clean),
    'date_range': f"{df_clean['publication_year'].min()}-{df_clean['publication_year'].max()}" if 'publication_year' in df_clean.columns else 'Unknown',
    'unique_journals': df_clean['journal'].nunique() if 'journal' in df_clean.columns else 0,
    'papers_with_abstracts': df_clean['has_abstract'].sum() if 'has_abstract' in df_clean.columns else 0,
    'avg_abstract_length': df_clean['abstract_length'].mean() if 'abstract_length' in df_clean.columns else 0
}

print(f"\n📊 FINAL DATASET SUMMARY:")
for key, value in summary_stats.items():
    print(f"  • {key.replace('_', ' ').title()}: {value}")

# ============================================================================
# KEY FINDINGS AND INSIGHTS
# ============================================================================

print(f"\n\n🎯 KEY FINDINGS AND INSIGHTS")
print("=" * 60)

findings = [
    "📈 Publication Timeline: COVID-19 research shows expected peak during 2020-2021",
    "📚 Journal Diversity: Research published across multiple high-impact journals",
    "🔍 Source Distribution: Multiple databases contribute to comprehensive coverage",
    "📝 Content Quality: Majority of papers include detailed abstracts",
    "☁️ Research Focus: Title analysis reveals key themes in COVID-19 research",
    "📅 Research Response: Clear temporal pattern showing rapid scientific response"
]

for i, finding in enumerate(findings, 1):
    print(f"{i}. {finding}")

print(f"\n🔬 RESEARCH IMPLICATIONS:")
implications = [
    "Scientific community responded rapidly to COVID-19 pandemic",
    "Diverse publication venues ensured broad dissemination of research",
    "High abstract availability indicates good research documentation",
    "Temporal patterns reflect real-world pandemic timeline"
]

for i, implication in enumerate(implications, 1):
    print(f"  • {implication}")

print(f"\n" + "="*60)
print("🎉 CORD-19 ANALYSIS COMPLETED SUCCESSFULLY!")
print("Ready for Streamlit application development.")
print("="*60)