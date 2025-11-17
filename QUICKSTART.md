# CORD-19 Data Analysis - Quick Start Guide

## Project Overview
This project analyzes COVID-19 research publications from the CORD-19 dataset, featuring comprehensive data analysis and an interactive Streamlit dashboard.

**Student:** Kimberly
**Course:** Python Programming - Week 8
**Repository:** https://github.com/Kimberly-ops177/week-8-python-assignment

---

## Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Analysis
```bash
python cord19_analysis.py
```
This generates:
- Console output with statistics
- `cord19_cleaned_data.csv` - cleaned dataset
- `cord19_visualizations.png` - 6 static visualizations

### 3. Launch Interactive Dashboard
```bash
python -m streamlit run streamlit_app.py
```
Or on Windows, simply double-click: `run_dashboard.bat`

The dashboard opens at: http://localhost:8501

---

## Project Highlights

### Data Analysis
- 📊 **5,000** sample papers analyzed
- 📈 **3,468** papers after cleaning (removed 1,532 duplicates)
- 📝 **94.6%** have abstracts (high quality data)
- 📚 **15** unique journals represented
- 🔍 **6** different data sources

### Visualizations Created
1. Publications by Year (Bar Chart)
2. Top 10 Journals (Horizontal Bar Chart)
3. Research Sources Distribution (Pie Chart)
4. Abstract Length Distribution (Histogram)
5. Monthly Publications 2020-2021 (Line Plot)
6. Most Frequent Title Words (Bar Chart)

### Interactive Dashboard Features
- Real-time filtering by year, journal, and source
- 4 analysis tabs (Timeline, Journals, Sources, Content)
- Interactive Plotly charts (hover, zoom, pan)
- Sample data viewer
- Missing data analysis
- Professional styling with custom CSS

---

## Key Findings

1. **Peak Research Year:** 2020 with 1,539 papers
2. **Top Journal:** BMJ with 226 papers
3. **Primary Source:** medRxiv with 595 papers
4. **Average Abstract:** 56 characters
5. **Research Timeline:** Clear peak during 2020-2021 pandemic period

---

## Technologies Used

- **Python 3.13**
- **pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Matplotlib** - Static visualizations
- **Seaborn** - Statistical plots
- **Plotly** - Interactive charts
- **Streamlit** - Web dashboard
- **WordCloud** - Text visualization

---

## File Structure

```
week-8-python-assignment/
├── cord19_analysis.py           # Main analysis script (523 lines)
├── streamlit_app.py             # Interactive dashboard (526 lines)
├── requirements.txt             # All dependencies
├── README.md                    # Detailed documentation
├── QUICKSTART.md                # This file
├── ASSIGNMENT_COMPLETION.md     # Completion report
├── .gitignore                   # Git ignore rules
├── run_dashboard.bat            # Windows launcher
├── cord19_cleaned_data.csv      # Generated cleaned data (975 KB)
└── cord19_visualizations.png    # Generated charts (715 KB)
```

---

## Assignment Requirements ✅

All requirements completed:

- [x] **Part 1:** Data loading and exploration
- [x] **Part 2:** Data cleaning and preparation
- [x] **Part 3:** Data analysis with 6 visualizations
- [x] **Part 4:** Interactive Streamlit application
- [x] **Part 5:** Complete documentation and reflection

---

## Troubleshooting

**Issue:** Import errors
**Solution:** Run `pip install -r requirements.txt`

**Issue:** Streamlit won't start
**Solution:** Use `python -m streamlit run streamlit_app.py`

**Issue:** Encoding errors on Windows
**Solution:** Already fixed with UTF-8 encoding in code

**Issue:** No data visualizations
**Solution:** Run `python cord19_analysis.py` first to generate the PNG

---

## For Detailed Information

See [README.md](README.md) for:
- Complete installation guide
- Detailed analysis breakdown
- Challenges and learnings
- Future improvements
- Full documentation

See [ASSIGNMENT_COMPLETION.md](ASSIGNMENT_COMPLETION.md) for:
- Detailed completion report
- Self-assessment (100/100)
- Testing results
- Key learnings

---

## Contact

**GitHub:** [@Kimberly-ops177](https://github.com/Kimberly-ops177)
**Repository:** [week-8-python-assignment](https://github.com/Kimberly-ops177/week-8-python-assignment)

---

**Status:** ✅ Complete and Ready for Review

*Built with Python and Streamlit | November 2024*
