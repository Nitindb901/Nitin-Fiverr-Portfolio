# 📊 Retail Analytics Dashboard

A comprehensive, production-ready retail analytics project featuring synthetic data generation, ETL pipeline, exploratory data analysis, and dashboard-ready datasets for business intelligence tools.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Latest-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Business Problem](#business-problem)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Key Insights](#key-insights)
- [Visualizations](#visualizations)
- [Dashboard Integration](#dashboard-integration)
- [Technical Details](#technical-details)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Project Overview

This project demonstrates end-to-end retail analytics capabilities, from synthetic data generation to actionable business insights. It includes:

- **Synthetic Dataset**: 12 months of realistic retail transaction data
- **ETL Pipeline**: Robust data cleaning and feature engineering
- **EDA Notebook**: Comprehensive exploratory data analysis
- **Dashboard Exports**: Power BI/Excel-ready datasets
- **Visualizations**: 10+ professional charts and graphs
- **KPI Tracking**: Executive-level performance metrics

### Dataset Characteristics

- **Time Period**: January 2024 - December 2024 (365 days)
- **Stores**: 5 retail locations
- **Categories**: 4 main categories (Electronics, Apparel, Home, Grocery)
- **SubCategories**: 16 subcategories
- **Brands**: 20+ brands
- **Transactions**: 100,000+ transaction records
- **Revenue**: $15M+ total revenue

---

## 💼 Business Problem

**Challenge**: Retail businesses need comprehensive analytics to:
- Understand sales trends and patterns
- Optimize inventory and pricing strategies
- Improve conversion rates and customer engagement
- Identify top-performing products and stores
- Make data-driven decisions for promotions and discounts

**Solution**: This project provides a complete analytics framework that:
1. Generates realistic retail data with business logic
2. Cleans and enriches data with derived features
3. Performs deep exploratory analysis
4. Delivers actionable insights through visualizations
5. Exports dashboard-ready datasets for BI tools

---

## ✨ Features

### 🔧 Data Generation
- Realistic business logic with weekly seasonality
- Festival/promotional spikes (Republic Day, Diwali, Black Friday, etc.)
- Store-level footfall variations
- Discount impact on quantity sold
- Price band segmentation

### 🧹 Data Cleaning & ETL
- Missing value handling
- Duplicate removal
- Data type validation
- Business logic verification
- Outlier detection and removal (IQR method)
- Feature engineering (20+ derived features)

### 📈 Analysis Features
- Time series analysis (daily, weekly, monthly trends)
- Category and subcategory performance
- Store performance benchmarking
- Discount effectiveness analysis
- Price segment analysis
- Day-of-week patterns
- Correlation analysis
- Top performers identification

### 📊 Dashboard Outputs
- Main fact table (all transactions with enriched features)
- Daily aggregation by store
- Category and subcategory summaries
- Store performance metrics
- Monthly trend analysis
- KPI summary for executives
- Top SKUs and brands

---

## 📁 Project Structure

```
01_Retail_Analytics_Dashboard/
│
├── data/                                    # Dataset storage
│   ├── retail_transactions_raw.csv         # Generated synthetic data
│   └── retail_transactions_clean.csv       # Cleaned & enriched data
│
├── scripts/                                 # Python automation scripts
│   ├── generate_data.py                    # Synthetic data generation
│   ├── etl_clean.py                        # Data cleaning & feature engineering
│   └── export_for_dashboard.py             # Dashboard export preparation
│
├── notebooks/                               # Jupyter notebooks
│   └── retail_eda_analysis.ipynb           # Exploratory Data Analysis
│
├── dashboard/                               # Dashboard-ready files
│   ├── powerbi_ready.csv                   # Main fact table
│   ├── daily_aggregation.csv               # Daily metrics by store
│   ├── category_aggregation.csv            # Category performance
│   ├── store_performance.csv               # Store metrics
│   ├── monthly_trend.csv                   # Monthly trends
│   └── DATA_DICTIONARY.md                  # Complete data dictionary
│
├── results/                                 # Analysis outputs
│   ├── kpi_summary.csv                     # Executive KPIs
│   ├── category_summary.csv                # Category breakdown
│   ├── top_skus.csv                        # Top 10 products
│   ├── top_brands.csv                      # Top 10 brands
│   ├── executive_summary.csv               # Executive summary report
│   │
│   └── [Visualizations - PNG files]
│       ├── univariate_distributions.png
│       ├── category_revenue_analysis.png
│       ├── top_subcategories.png
│       ├── time_series_analysis.png
│       ├── day_of_week_analysis.png
│       ├── store_performance_analysis.png
│       ├── discount_impact_analysis.png
│       ├── correlation_matrix.png
│       └── price_segment_analysis.png
│
├── README.md                                # This file
├── MASTER_PROMPT.md                         # Project specifications
└── requirements.txt                         # Python dependencies

```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Jupyter Notebook (optional, for running analysis notebook)

### Setup Steps

1. **Clone or download this project**
   ```powershell
   cd c:\Users\nitin\OneDrive\Desktop\Nitin-Fiverr-Portfolio\01_Retail_Analytics_Dashboard
   ```

2. **Create a virtual environment (recommended)**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install required packages**
   ```powershell
   pip install -r requirements.txt
   ```

---

## 💻 Usage

### Step 1: Generate Synthetic Data

```powershell
python scripts\generate_data.py
```

**Output**: Creates `data/retail_transactions_raw.csv` with 100,000+ transactions

**What it does**:
- Generates 12 months of daily transactions
- Applies realistic business logic (seasonality, promotions)
- Creates transactions for 5 stores across 4 categories
- Includes footfall, conversion rates, and discount data

### Step 2: Clean and Enrich Data

```powershell
python scripts\etl_clean.py
```

**Output**: Creates `data/retail_transactions_clean.csv` with cleaned and enriched data

**What it does**:
- Validates data quality and removes anomalies
- Adds 20+ derived features (Month, Week, DayOfWeek, PriceSegment, etc.)
- Handles outliers using IQR method
- Generates category summary in `results/category_summary.csv`

### Step 3: Export Dashboard-Ready Files

```powershell
python scripts\export_for_dashboard.py
```

**Output**: Creates multiple files in `dashboard/` and `results/` folders

**What it does**:
- Creates fact table for Power BI/Excel
- Generates aggregated views (daily, category, store, monthly)
- Calculates KPIs and performance metrics
- Exports top performers (SKUs and brands)

### Step 4: Run Exploratory Data Analysis

```powershell
jupyter notebook notebooks\retail_eda_analysis.ipynb
```

**What it does**:
- Performs comprehensive statistical analysis
- Generates 10+ professional visualizations
- Provides actionable business insights
- Creates executive summary report

**Alternative (if Jupyter is not installed)**:
Open the notebook in VS Code with the Jupyter extension.

---

## 📊 Key Insights

Based on the analysis, here are typical insights you'll discover:

### 🏆 Performance Highlights

1. **Top Revenue Category**: Electronics typically generates 30-35% of total revenue
2. **Best Performing Store**: Store performance varies with Store_D often leading
3. **Peak Sales Day**: Weekends show 30-40% higher revenue than weekdays
4. **Best Month**: November (Diwali/Black Friday) typically shows highest revenue
5. **Discount Effectiveness**: Discounts >20% increase quantity sold by 40-50%

### 📈 Trends & Patterns

- **Weekend Premium**: 35% higher average daily revenue on weekends
- **Festival Impact**: Revenue spikes 80% during festival periods (±3 days)
- **Month-End Effect**: 20% increase in sales during last week of month
- **Conversion Rates**: Average 20-30% with top stores reaching 35%

### 💡 Strategic Recommendations

1. **Inventory Planning**: Stock up on high-demand categories before festivals
2. **Promotional Strategy**: Focus weekend promotions for maximum impact
3. **Staffing Optimization**: Increase staffing on weekends and festival periods
4. **Discount Optimization**: Use targeted discounts >20% for clearance items
5. **Store Best Practices**: Replicate top-performing store strategies across network
6. **Premium Segment**: Develop premium offerings for higher margins
7. **Conversion Improvement**: Target underperforming stores for conversion training
8. **Category Mix**: Optimize category mix based on revenue contribution

---

## 📸 Visualizations

The project generates multiple professional visualizations:

### Available Charts

1. **Univariate Distributions** - Revenue, Quantity, Discount, Conversion distributions
2. **Category Revenue Analysis** - Bar chart and pie chart of category performance
3. **Top SubCategories** - Horizontal bar chart of top 10 subcategories
4. **Time Series Analysis** - Daily revenue trend with moving average + monthly bars
5. **Day of Week Analysis** - Revenue and transaction patterns by weekday
6. **Store Performance** - Multi-metric store comparison
7. **Discount Impact** - Revenue and quantity by discount segment
8. **Correlation Matrix** - Heatmap of key metric correlations
9. **Price Segment Analysis** - Revenue, transactions, and discounts by price tier

All visualizations are saved as high-resolution PNG files (300 DPI) in the `results/` folder.

---

## 🎨 Dashboard Integration

### Power BI

1. **Import Main Data**:
   - Open Power BI Desktop
   - Get Data → Text/CSV → Select `dashboard/powerbi_ready.csv`

2. **Create Relationships**:
   - Use Date, Store, Category as relationship keys
   - Import aggregation files as separate tables if needed

3. **Key Visualizations to Create**:
   - Revenue trend line chart (Date vs NETAMT)
   - Category revenue pie chart
   - Store performance comparison (bar chart)
   - KPI cards (Total Revenue, Transactions, Avg Transaction Value)
   - Discount vs Revenue scatter plot
   - Monthly trend column chart

4. **Recommended Filters**:
   - Date slicer (range)
   - Store dropdown
   - Category dropdown
   - Price Segment

### Excel

1. **Import Data**:
   - Data → From Text/CSV → Select `dashboard/daily_aggregation.csv`

2. **Create Pivot Tables**:
   - Revenue by Category
   - Store performance comparison
   - Monthly trends
   - Day-of-week analysis

3. **Create Charts**:
   - Use Insert → Charts for quick visualizations
   - Apply consistent formatting and colors

4. **Executive Dashboard**:
   - Import `results/kpi_summary.csv` for key metrics
   - Use conditional formatting for performance indicators

### Tableau

1. **Connect to Data**:
   - Connect → Text File → `dashboard/powerbi_ready.csv`

2. **Create Calculated Fields**:
   - Revenue Growth: `(SUM([NETAMT]) - LOOKUP(SUM([NETAMT]), -1)) / LOOKUP(SUM([NETAMT]), -1)`
   - Discount Impact: `AVG([Qty])` by `[DiscountSegment]`

3. **Build Dashboards**:
   - Create individual worksheets for each analysis
   - Combine into interactive dashboard with filters

---

## 🔧 Technical Details

### Data Generation Logic

**Seasonality Factors**:
- Weekend Multiplier: 1.4x (Saturdays & Sundays)
- Festival Multiplier: 1.8x (within ±3 days of festival dates)
- Month-End Multiplier: 1.2x (days 26-31)

**Store Characteristics**:
- Avg daily footfall ranges from 1,000 to 1,800 customers
- Conversion rates: 15-35% of footfall
- Each store serves all categories

**Pricing Strategy**:
- Electronics: $5,000 - $80,000 MRP
- Apparel: $500 - $5,000 MRP
- Home: $1,000 - $15,000 MRP
- Grocery: $50 - $1,000 MRP

**Discount Logic**:
- Regular days: 0-20% discount
- Festival periods: 10-40% discount
- Higher discounts drive higher quantity (1-5 units vs 1-3 units)

### Feature Engineering

**Time Features** (9):
- Year, Month, MonthName, Week, Quarter
- DayOfWeek, DayName, IsWeekend

**Price Features** (3):
- DiscountAmount, ProfitMargin, PriceSegment

**Transaction Features** (3):
- DiscountSegment, TransactionSize, AvgUnitPrice

**Total**: 30+ features in cleaned dataset

### Data Quality Measures

- **Validation Checks**: 7 automated checks in ETL
- **Outlier Removal**: IQR method with 3× threshold
- **Business Logic Validation**: MRP ≥ SellingPrice, NETAMT = SellingPrice × Qty
- **No Missing Values**: Complete data integrity
- **Duplicate Removal**: Automatic deduplication

---

## 📦 Requirements

```txt
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
scipy>=1.9.0
jupyter>=1.0.0
openpyxl>=3.0.0
```

All dependencies are listed in `requirements.txt` and can be installed with:
```powershell
pip install -r requirements.txt
```

---

## 🤝 Contributing

This is a portfolio project, but suggestions and improvements are welcome!

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Enhancement

- Add machine learning models (sales forecasting, customer segmentation)
- Implement real-time dashboard updates
- Add geographic analysis with store locations
- Include customer demographics data
- Build interactive web dashboard using Dash or Streamlit
- Add A/B testing framework for promotions

---

## 📄 License

This project is created for portfolio demonstration purposes. Feel free to use and modify for your own learning and portfolio projects.

---

## 👤 Author

**Nitin Dubey**  
Data Analyst | Data Scientist | Business Intelligence Specialist

- 🌐 Portfolio: [https://nitindb901.github.io/Nitindb901-nitin-official-website/](https://nitindb901.github.io/Nitindb901-nitin-official-website/)
- 💼 GitHub: [@nitindb901](https://github.com/nitindb901)
- 📊 Project Repository: [Nitin-Fiverr-Portfolio](https://github.com/nitindb901/Nitin-Fiverr-Portfolio)
- 🔗 LinkedIn: [Connect with me](https://www.linkedin.com/in/nitindb901/)
- 📧 Email: nitindb901@gmail.com

---

## 🙏 Acknowledgments

- Inspired by real-world retail analytics challenges
- Built with best practices from industry-leading data science projects
- Designed for educational and portfolio demonstration purposes

---

## 📞 Support

For questions or issues:

1. Check the [Data Dictionary](dashboard/DATA_DICTIONARY.md) for field descriptions
2. Review the Jupyter notebook for analysis examples
3. Examine script comments for implementation details
4. Open an issue in the repository

---

## 📝 Version History

- **v1.0** (November 2024)
  - Initial release
  - Complete ETL pipeline
  - Comprehensive EDA notebook
  - Dashboard-ready exports
  - Professional visualizations
  - Full documentation

---

## 🎯 Project Status

✅ **Production Ready** - All features implemented and tested

**Completed**:
- [x] Synthetic data generation with realistic business logic
- [x] Robust ETL pipeline with data validation
- [x] Comprehensive exploratory data analysis
- [x] Professional visualizations (10+ charts)
- [x] Dashboard-ready datasets for Power BI/Excel
- [x] Complete documentation and data dictionary
- [x] Executive summary and KPI reports

**Future Enhancements** (Optional):
- [ ] Machine learning models (forecasting, segmentation)
- [ ] Interactive web dashboard
- [ ] Real-time data processing
- [ ] Advanced statistical testing
- [ ] Customer behavior analysis

---

## 💡 Quick Start Summary

```powershell
# 1. Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Run Pipeline
python scripts\generate_data.py
python scripts\etl_clean.py
python scripts\export_for_dashboard.py

# 3. Analyze
jupyter notebook notebooks\retail_eda_analysis.ipynb

# 4. Use dashboard files in dashboard/ folder with Power BI/Excel
```

---

**Happy Analyzing! 📊✨**
