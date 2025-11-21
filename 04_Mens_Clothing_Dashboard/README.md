# 🎯 Men's Clothing Analytics Dashboard with Machine Learning

![Dashboard Preview](visualizations/dashboard_preview.png)

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![ML](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-success.svg)](https://nitindb901.github.io/Nitin-Fiverr-Portfolio/04_Mens_Clothing_Dashboard/mens_clothing_dashboard.html)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
- [Data Overview](#data-overview)
- [ML Models](#ml-models)
- [Dashboard Features](#dashboard-features)
- [Key Insights](#key-insights)
- [Results](#results)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## 🎬 Overview

A comprehensive end-to-end data science project analyzing men's clothing retail business with advanced **Machine Learning** capabilities. This project demonstrates the complete analytics pipeline from data generation to interactive dashboard deployment, featuring:

- 📊 **100,000 synthetic transactions** across 4 product categories
- 🤖 **Machine Learning models** for sales forecasting and customer segmentation
- 📈 **93.18% accuracy** on revenue predictions
- 💎 **Interactive web dashboard** with real-time filtering and beautiful visualizations
- 🎯 **Business intelligence** with actionable insights

**Live Dashboard:** [View Here](https://nitindb901.github.io/Nitin-Fiverr-Portfolio/04_Mens_Clothing_Dashboard/mens_clothing_dashboard.html)

## ✨ Key Features

### 🤖 Machine Learning Models
- **Sales Forecasting**: 6-month revenue prediction with 93.18% accuracy
- **Customer Segmentation**: K-means clustering identifying 5 distinct customer groups
- **Predictive Analytics**: Confidence intervals and trend analysis

### 📊 Advanced Analytics
- **RFM Analysis**: Recency, Frequency, Monetary segmentation
- **Customer Lifetime Value (CLV)** calculation
- **Cohort Analysis** and retention metrics
- **Profit Margin** optimization insights

### 💻 Interactive Dashboard
- **Real-time filtering** by category, channel, and period
- **7 interactive charts** built with Chart.js
- **Beautiful modal popups** with detailed breakdowns
- **Responsive design** for all devices
- **ML insights section** with forecast visualization

### 📈 Business Intelligence
- **Category performance** analysis (Formal, Casual, Sports, Accessories)
- **Channel optimization** (In-Store, Online, Mobile App)
- **Store benchmarking** across 10 locations
- **Brand performance** tracking
- **Discount impact** analysis

## 📁 Project Structure

```
04_Mens_Clothing_Dashboard/
│
├── 📂 data/
│   ├── raw/                          # Original generated datasets
│   │   ├── transactions.csv          # 100K transactions
│   │   ├── products.csv              # 500 products
│   │   └── customers.csv             # 12K customers
│   │
│   ├── processed/                    # Cleaned and transformed data
│   │   ├── transactions_processed.csv
│   │   ├── customers_rfm.csv         # RFM analysis results
│   │   ├── monthly_totals.csv        # Time series aggregations
│   │   ├── category_performance.csv
│   │   ├── brand_performance.csv
│   │   ├── store_performance.csv
│   │   ├── channel_performance.csv
│   │   └── customer_lifetime_value.csv
│   │
│   └── ml_results/                   # ML model outputs
│       ├── revenue_forecast.csv      # 6-month predictions
│       ├── customer_clusters.csv     # K-means results
│       ├── cluster_summary.csv
│       ├── sales_forecast.png
│       ├── customer_segmentation.png
│       └── cluster_distribution.png
│
├── 📂 scripts/
│   ├── 01_generate_data.py          # Synthetic data generation
│   ├── 02_process_data.py           # Data cleaning & RFM analysis
│   ├── 03_ml_models.py              # ML forecasting & clustering
│   └── 04_generate_visualizations.py # Business charts
│
├── 📂 visualizations/               # Professional charts (300 DPI)
│   ├── 01_category_performance.png
│   ├── 02_monthly_trend.png
│   ├── 03_channel_distribution.png
│   ├── 04_top_stores.png
│   ├── 05_brand_performance.png
│   ├── 06_rfm_segments.png
│   ├── 07_transaction_distribution.png
│   ├── 08_weekday_weekend.png
│   ├── 09_clv_by_segment.png
│   ├── 10_discount_analysis.png
│   └── insights.txt                 # Key findings summary
│
├── 📄 mens_clothing_dashboard.html  # Interactive web dashboard
├── 📄 README.md                     # This file
└── 📄 DOCUMENTATION.md              # Detailed technical docs

```

## 🛠️ Technologies Used

### Programming & Data Science
- **Python 3.14** - Core programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning (K-means, preprocessing)

### Visualization
- **Matplotlib** - Static chart generation
- **Seaborn** - Statistical visualizations
- **Chart.js 4.4.0** - Interactive web charts

### Web Technologies
- **HTML5** - Dashboard structure
- **CSS3** - Styling and animations
- **JavaScript ES6+** - Interactivity and data handling

### Tools
- **Git & GitHub** - Version control and deployment
- **VS Code** - Development environment
- **GitHub Pages** - Dashboard hosting

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/Nitindb901/Nitin-Fiverr-Portfolio.git
cd Nitin-Fiverr-Portfolio/04_Mens_Clothing_Dashboard
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Step 4: Run the Analysis Pipeline
```bash
# Generate synthetic data
python scripts/01_generate_data.py

# Process and clean data
python scripts/02_process_data.py

# Build ML models
python scripts/03_ml_models.py

# Generate visualizations
python scripts/04_generate_visualizations.py
```

### Step 5: View Dashboard
Open `mens_clothing_dashboard.html` in your web browser.

## 📊 Data Overview

### Dataset Statistics
- **Total Transactions**: 100,000
- **Date Range**: January 2023 - December 2024 (24 months)
- **Total Revenue**: ₹20.43 Crores
- **Unique Customers**: 11,998
- **Products**: 500 (across 4 categories)
- **Stores**: 10 major cities in India

### Product Categories
1. **Casual Wear** (31.0%) - T-shirts, Jeans, Casual Shirts, Chinos, Shorts
2. **Sports & Activewear** (27.5%) - Gym Wear, Track Pants, Sports Shoes, Jackets
3. **Formal Wear** (25.3%) - Suits, Dress Shirts, Blazers, Trousers, Waistcoats
4. **Accessories** (16.2%) - Belts, Wallets, Ties, Watches, Sunglasses, Bags

### Brand Tiers
- **Premium**: Armani, Hugo Boss, Ralph Lauren, Calvin Klein
- **Mid-Range**: Levi's, Tommy Hilfiger, Nike, Adidas, Puma
- **Budget**: H&M, Zara, Uniqlo, GAP

## 🤖 ML Models

### 1. Sales Forecasting Model
**Objective**: Predict next 6 months revenue

**Approach**: Weighted Moving Average with Trend & Seasonality
- Analyzes last 12 months of data
- Applies seasonal patterns based on historical months
- Incorporates growth trends with diminishing factor

**Performance**:
- **Accuracy**: 93.18% (MAPE: 6.82%)
- **Validation**: Backtesting on last 3 months
- **Forecast Period**: January - June 2025

**Predictions**:
| Month | Predicted Revenue | Confidence Interval |
|-------|------------------|---------------------|
| Jan 2025 | ₹6.67 Cr | ₹5.67 - ₹7.67 Cr |
| Feb 2025 | ₹8.43 Cr | ₹7.17 - ₹9.70 Cr |
| Mar 2025 | ₹9.23 Cr | ₹7.85 - ₹10.62 Cr |
| Apr 2025 | ₹9.26 Cr | ₹7.87 - ₹10.65 Cr |
| May 2025 | ₹9.39 Cr | ₹7.98 - ₹10.80 Cr |
| Jun 2025 | ₹9.19 Cr | ₹7.81 - ₹10.57 Cr |

**Total 6-Month Projection**: ₹5.22 Crores (+2.1% vs historical average)

### 2. Customer Segmentation (K-Means)
**Objective**: Identify distinct customer groups for targeted marketing

**Features**:
- Recency (days since last purchase)
- Frequency (number of purchases)
- Monetary (total spend)
- Log-transformed and standardized

**Model Configuration**:
- **Algorithm**: K-means clustering
- **Optimal K**: 5 clusters
- **Silhouette Score**: 0.256
- **Iterations**: 17

**Segments Identified**:

| Segment | Size | Avg Spend | Frequency | Revenue Share |
|---------|------|-----------|-----------|---------------|
| **VIP Customers** | 3,367 (28.1%) | ₹26,344 | 10.8 | 43.4% |
| **Loyal Actives** | 1,620 (13.5%) | ₹22,091 | 10.4 | 17.5% |
| **Regular Shoppers** | 7,011 (58.4%) | ₹11,426 | 7.4 | 39.1% |

**Business Impact**:
- VIP segment contributes **43.4% of revenue** with only 28% of customers
- Identified **1,139 "At Risk" customers** for re-engagement campaigns
- Potential revenue recovery: ₹25+ Lakhs from dormant customers

## 📈 Dashboard Features

### Interactive Elements
1. **KPI Cards** (5 cards)
   - Total Revenue with YoY growth
   - Total Transactions with avg order value
   - Unique Customers with purchase frequency
   - Profit Margin with total profit
   - Customer Lifetime Value with tenure

2. **ML Insights Section**
   - Next month forecast
   - 6-month revenue projection
   - VIP customer count
   - Growth projection vs historical

3. **Dynamic Charts** (7 charts)
   - Category Revenue Performance (Bar)
   - Monthly Revenue Trend (Line)
   - Sales Channel Distribution (Doughnut)
   - Customer Segmentation RFM (Pie)
   - Top 10 Stores Performance (Horizontal Bar)
   - ML Customer Clusters (Combo: Bar + Line)
   - 6-Month Revenue Forecast (Line with Confidence Interval)

4. **Category Performance Table**
   - Sortable columns
   - Clickable rows for detailed view
   - Real-time filtering

5. **Advanced Filtering**
   - Category filter (All, Formal, Casual, Sports, Accessories)
   - Real-time chart updates
   - Smooth animations

### Modal Popups
Each KPI card and table row opens detailed modal with:
- Large icon and title
- 4 stat cards in grid layout
- 3-4 business insights with icons
- Smooth animations (fadeIn, slideUp, bounce)
- Close on ESC key or overlay click

## 🎯 Key Insights

### Revenue Performance
1. **Casual Wear dominates** with ₹6.33 Cr (31% of revenue)
2. **+22.3% revenue growth** from Jan 2023 to Dec 2024
3. **₹2,043 average transaction value** across all categories
4. **26.63% profit margin** generating ₹5.44 Cr total profit

### Customer Behavior
5. **Champions segment** has **1.7x higher CLV** (₹29,239 vs ₹17,031 avg)
6. **8.3 orders per customer** indicating strong loyalty
7. **30.6% customers** are Potential Loyalists (3,666 customers)
8. **60% repeat purchase rate** showing customer retention

### Channel & Store Performance
9. **Balanced channel distribution**: In-Store 33.4%, Online 33.3%, Mobile App 33.2%
10. **Delhi Connaught Place** is top store with ₹2.09 Cr revenue
11. **Weekend sales contribute 28.5%** of total revenue
12. **Online channels growing** at 15% year-over-year

### Brand & Product Insights
13. **Calvin Klein** is top brand with ₹2.88 Cr revenue
14. **Premium brands** contribute 28% of revenue with 5% higher margins
15. **Formal Wear** has highest margin (27.1%)
16. **Sports & Activewear** shows fastest growth trajectory

## 📊 Results

### Data Generation
✅ Successfully generated 100,000 realistic transactions  
✅ Created 500 diverse product catalog  
✅ Synthesized 12,000 customer profiles with realistic behavior  
✅ Implemented seasonal patterns and promotional cycles  

### Data Processing
✅ Zero missing values after quality checks  
✅ Calculated RFM scores for all 11,998 active customers  
✅ Generated 11 processed datasets for analysis  
✅ Computed CLV with 556 days average tenure  

### ML Models
✅ Achieved **93.18% forecast accuracy** (6.82% MAPE)  
✅ Identified **5 distinct customer segments** with K-means  
✅ Generated 6-month revenue predictions with confidence intervals  
✅ Created 3 ML visualization outputs (forecast, segmentation, distribution)  

### Visualizations
✅ Produced **10 professional charts** at 300 DPI resolution  
✅ Generated comprehensive business insights summary  
✅ Created color-coded visualizations for easy interpretation  
✅ Built responsive, interactive web dashboard  

### Dashboard Deployment
✅ Developed fully functional HTML dashboard with Chart.js  
✅ Implemented beautiful modal system with animations  
✅ Added real-time filtering and dynamic updates  
✅ Deployed to GitHub Pages for public access  

## 💼 Usage

### For Business Analysts
1. Review the **Key Insights** section for strategic recommendations
2. Use the **interactive dashboard** to explore category performance
3. Analyze **customer segments** for targeted marketing campaigns
4. Monitor **ML forecasts** for inventory planning

### For Data Scientists
1. Study the **ML models** implementation in `scripts/03_ml_models.py`
2. Examine **feature engineering** techniques in `scripts/02_process_data.py`
3. Review **data generation** logic in `scripts/01_generate_data.py`
4. Explore **visualization** best practices in `scripts/04_generate_visualizations.py`

### For Developers
1. Clone the repository and follow **Installation** steps
2. Modify `mens_clothing_dashboard.html` for custom dashboard features
3. Extend ML models with new algorithms (LSTM, Prophet, etc.)
4. Add new visualizations or metrics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Nitin**
- GitHub: [@Nitindb901](https://github.com/Nitindb901)
- Portfolio: [Nitin-Fiverr-Portfolio](https://github.com/Nitindb901/Nitin-Fiverr-Portfolio)

## 🙏 Acknowledgments

- Inspired by real-world retail analytics challenges
- Built with modern data science best practices
- Designed for portfolio demonstration and learning

## 📞 Contact

For questions, suggestions, or collaboration opportunities, please open an issue on GitHub.

---

⭐ **Star this repository** if you find it helpful!

📌 **Live Dashboard**: [View Here](https://nitindb901.github.io/Nitin-Fiverr-Portfolio/04_Mens_Clothing_Dashboard/mens_clothing_dashboard.html)
