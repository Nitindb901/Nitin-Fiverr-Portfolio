# Technical Documentation - Multi-Category Retail KPI Dashboard

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Data Model](#data-model)
3. [Data Generation Pipeline](#data-generation-pipeline)
4. [KPI Processing Logic](#kpi-processing-logic)
5. [Machine Learning Models](#machine-learning-models)
6. [Visualization System](#visualization-system)
7. [Dashboard Architecture](#dashboard-architecture)
8. [API Reference](#api-reference)

---

## Architecture Overview

### System Design
```
┌─────────────────────────────────────────────────────────────┐
│                   Data Generation Layer                      │
│  (Faker, pandas, numpy - 200K transactions synthetic)       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Processing Layer                      │
│  (ETL, KPI Calculation, Time Series Aggregation)            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Machine Learning Layer                     │
│  (Forecasting, Anomaly Detection, Classification)           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Visualization Layer                        │
│  (matplotlib, seaborn - 12 charts @ 300 DPI)                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Presentation Layer                         │
│  (HTML5, CSS3, JavaScript, Chart.js - Interactive)          │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack
- **Backend**: Python 3.14
- **Data Processing**: pandas 2.3.3, NumPy 2.3.5
- **Data Generation**: Faker 38.2.0
- **Machine Learning**: scikit-learn (LinearRegression, IsolationForest, RandomForestClassifier)
- **Visualization**: matplotlib 3.10.7, seaborn 0.13.2
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Charting**: Chart.js 4.4.0

---

## Data Model

### Entity Relationship

```
┌─────────────────┐
│   PRODUCTS      │
│─────────────────│
│ product_id (PK) │──┐
│ category        │  │
│ subcategory     │  │
│ brand           │  │
│ price           │  │
│ cost            │  │
└─────────────────┘  │
                     │
                     │    ┌─────────────────┐
                     ├───>│ TRANSACTIONS    │
                     │    │─────────────────│
┌─────────────────┐ │    │ transaction_id  │
│   CUSTOMERS     │ │    │ customer_id (FK)│
│─────────────────│ │    │ product_id (FK) │
│ customer_id (PK)│─┘    │ store_id        │
│ name            │       │ date            │
│ email           │       │ channel         │
│ city            │       │ quantity        │
│ segment         │       │ revenue         │
│ join_date       │       │ profit          │
└─────────────────┘       │ discount        │
                          └─────────────────┘
```

### Schema Definitions

#### Products Table
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| product_id | String | Unique identifier (P001-P1000) | P001 |
| category | String | Main category | Electronics |
| subcategory | String | Product subcategory | Mobile Phones |
| brand | String | Brand name | Samsung |
| name | String | Product display name | Samsung Galaxy S23 |
| price | Float | Retail price (₹) | 79999.0 |
| cost | Float | Cost price (₹) | 64000.0 |
| margin_pct | Float | Profit margin % | 19.99 |

#### Customers Table
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| customer_id | String | Unique identifier (C00001-C20000) | C00001 |
| name | String | Customer full name | Rajesh Kumar |
| email | String | Email address | rajesh.kumar@email.com |
| phone | String | Phone number | +91-9876543210 |
| city | String | Customer city | Delhi |
| segment | String | Customer segment | VIP |
| join_date | Date | Registration date | 2023-01-15 |

#### Transactions Table
| Column | Type | Description | Example |
|--------|------|-------------|---------|
| transaction_id | String | Unique identifier (T000001-T200000) | T000001 |
| customer_id | String | FK to customers | C00001 |
| product_id | String | FK to products | P001 |
| date | Date | Transaction date | 2023-01-15 |
| store_id | String | Store identifier (S01-S15) | S01 |
| store_name | String | Store display name | Delhi Connaught Place |
| store_type | String | Store category | Flagship |
| channel | String | Purchase channel | In-Store |
| quantity | Integer | Items purchased | 1 |
| unit_price | Float | Price per unit (₹) | 79999.0 |
| revenue | Float | Total revenue (₹) | 79999.0 |
| cost | Float | Total cost (₹) | 64000.0 |
| profit | Float | Total profit (₹) | 15999.0 |
| profit_margin_pct | Float | Margin percentage | 19.99 |
| discount_pct | Float | Discount applied % | 0-30 |

### Data Volumes
- **Products**: 1,000 records
- **Customers**: 20,000 records
- **Transactions**: 200,000 records
- **Time Period**: 36 months (Jan 2023 - Dec 2025)
- **Total Revenue**: ₹700.65 Crore
- **Total Profit**: ₹148.96 Crore

---

## Data Generation Pipeline

### 01_generate_data.py

#### Category Configuration
```python
CATEGORIES = {
    'Electronics': {
        'share': 0.20,
        'subcategories': ['Mobile Phones', 'Laptops', 'Tablets', 'Accessories', 'Audio', 'Cameras'],
        'brands': ['Samsung', 'Apple', 'OnePlus', 'Xiaomi', 'Dell', 'HP', 'Lenovo', 'Boat'],
        'price_range': (5000, 150000),
        'margin_range': (15, 25)
    },
    'Fashion': {
        'share': 0.25,
        'subcategories': ['Mens Wear', 'Womens Wear', 'Kids Wear', 'Footwear', 'Accessories'],
        'brands': ['Zara', 'H&M', 'Nike', 'Adidas', 'Puma', 'Levis', 'UCB', 'Biba'],
        'price_range': (500, 8000),
        'margin_range': (35, 50)
    },
    # ... other categories
}
```

#### Customer Segmentation
```python
SEGMENTS = {
    'VIP': {
        'share': 0.05,
        'avg_transactions': 15,
        'avg_order_value_multiplier': 2.5
    },
    'Premium': {
        'share': 0.15,
        'avg_transactions': 12,
        'avg_order_value_multiplier': 2.0
    },
    'Regular': {
        'share': 0.35,
        'avg_transactions': 10,
        'avg_order_value_multiplier': 1.5
    },
    'Occasional': {
        'share': 0.30,
        'avg_transactions': 6,
        'avg_order_value_multiplier': 1.2
    },
    'New': {
        'share': 0.15,
        'avg_transactions': 3,
        'avg_order_value_multiplier': 1.0
    }
}
```

#### Seasonal Patterns
```python
def apply_seasonal_factor(month):
    """Apply realistic seasonal multipliers"""
    if month in [10, 11]:  # Diwali season
        return 1.5
    elif month in [12, 1]:  # Year-end sales
        return 1.3
    elif month in [6, 7]:  # Mid-year sale
        return 1.2
    elif month in [2, 8]:  # Off-season
        return 0.9
    else:
        return 1.0
```

#### Store Configuration
```python
STORES = [
    {'id': 'S01', 'name': 'Delhi Connaught Place', 'city': 'Delhi', 'type': 'Flagship'},
    {'id': 'S02', 'name': 'Mumbai Bandra', 'city': 'Mumbai', 'type': 'Flagship'},
    {'id': 'S03', 'name': 'Bangalore Koramangala', 'city': 'Bangalore', 'type': 'Premium'},
    # ... 12 more stores
]
```

---

## KPI Processing Logic

### 02_process_data.py

#### Overall KPIs (19 Metrics)
```python
def calculate_overall_kpis(df):
    """
    Calculates comprehensive business KPIs
    
    Returns:
    - Total Revenue
    - Total Profit
    - Total Transactions
    - Unique Customers
    - Avg Transaction Value
    - Avg Profit Margin %
    - Total Quantity Sold
    - Avg Items per Transaction
    - Revenue per Customer
    - Transactions per Customer
    - Total Stores
    - Total Products
    - Total Categories
    - Date Range (Start/End)
    - Active Months
    - Avg Daily Revenue
    - Avg Monthly Revenue
    - Growth Rate %
    """
```

#### Category Performance Analysis
```python
def analyze_category_performance(df):
    """
    Category-level aggregation
    
    Metrics per Category:
    - Total Revenue
    - Total Profit
    - Revenue Share %
    - Profit Share %
    - Transaction Count
    - Avg Transaction Value
    - Avg Profit Margin %
    - Total Customers
    - Total Quantity
    """
```

#### Time Series Generation
```python
def create_time_series_data(df):
    """
    Generates daily, monthly, and quarterly aggregations
    
    Daily Time Series (1,095 records):
    - Date, Revenue, Transactions, Profit, Avg Margin, Customers, Quantity
    
    Monthly Time Series (37 records):
    - Month, Revenue, Transactions, Profit, Growth %, Cumulative Revenue
    
    Quarterly Time Series (13 records):
    - Quarter, Revenue, Transactions, Profit, QoQ Growth %
    """
```

#### Store Performance Analysis
```python
def analyze_store_performance(df):
    """
    Store-level KPIs (15 stores)
    
    Metrics per Store:
    - Total Revenue
    - Total Profit
    - Transaction Count
    - Avg Transaction Value
    - Total Customers
    - Revenue Rank
    - Store Type
    - City
    """
```

#### Customer Segment Analysis
```python
def analyze_customer_segments(df, customers):
    """
    Segment-level insights (5 segments)
    
    Metrics per Segment:
    - Customer Count
    - Revenue per Customer
    - Transactions per Customer
    - Avg Order Value
    - Total Revenue
    - Revenue Share %
    """
```

---

## Machine Learning Models

### 03_ml_models.py

### Model 1: Sales Forecasting

#### Architecture
```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Polynomial feature expansion (degree 3)
poly = PolynomialFeatures(degree=3, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Linear regression on polynomial features
model = LinearRegression()
model.fit(X_train_poly, y_train)
```

#### Training Configuration
- **Training Period**: 31 months (Jan 2023 - Jul 2025)
- **Test Period**: 6 months (Aug 2025 - Dec 2025)
- **Features**: Month index with polynomial expansion (x, x², x³)
- **Target**: Monthly revenue (₹ Cr)

#### Performance Metrics
```python
{
    'r2_score': -0.4445,  # Training R²
    'mae': 3.47,          # Mean Absolute Error (₹ Cr)
    'mape': 19.90,        # Mean Absolute Percentage Error
    'accuracy': 80.10     # Forecast Accuracy %
}
```

#### Forecasting Output
```python
# 12-month forecast
forecast = {
    'total_projected': 305.82,  # ₹ Cr
    'next_quarter': 66.09,      # ₹ Cr
    'next_6_months': 137.67,    # ₹ Cr
    'avg_monthly': 25.49,       # ₹ Cr
    'growth_rate': 82.71        # % vs last month
}
```

### Model 2: Anomaly Detection

#### Architecture
```python
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Feature scaling
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Isolation Forest
model = IsolationForest(
    contamination=0.05,
    n_estimators=100,
    max_samples='auto',
    random_state=42
)
```

#### Features Used (6 KPIs)
1. Daily Revenue (₹)
2. Transaction Count
3. Total Profit (₹)
4. Avg Margin %
5. Customer Count
6. Total Quantity

#### Detection Results
```python
{
    'total_days': 1095,
    'normal_days': 1040,      # 95.0%
    'anomalous_days': 55,     # 5.0%
    'avg_normal_revenue': 63.74,   # ₹ Lakhs
    'avg_anomaly_revenue': 68.66,  # ₹ Lakhs
    'top_anomaly_score': -0.711,
    'top_anomaly_date': '2023-11-15',
    'top_anomaly_revenue': 119.65  # ₹ Lakhs
}
```

### Model 3: Category Performance Classification

#### Architecture
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Random Forest configuration
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=42
)
```

#### Feature Engineering
```python
# 11 features
features = [
    'transactions',          # Transaction count
    'profit',                # Total profit
    'avg_margin_pct',        # Profit margin %
    'customers',             # Customer count
    'month_num',             # Month index
    'category_Electronics',  # One-hot encoded
    'category_Fashion',
    'category_Grocery',
    'category_Home & Living',
    'category_Beauty',
    'category_Sports'
]
```

#### Classification Logic
```python
def classify_performance(profit):
    """
    Classify category-month into performance tiers
    
    Rules:
    - High: Profit >= 66th percentile
    - Medium: 33rd percentile <= Profit < 66th percentile
    - Low: Profit < 33rd percentile
    """
    percentile_33 = df['profit'].quantile(0.33)
    percentile_66 = df['profit'].quantile(0.66)
    
    if profit >= percentile_66:
        return 'High'
    elif profit >= percentile_33:
        return 'Medium'
    else:
        return 'Low'
```

#### Performance Metrics
```python
{
    'accuracy': 0.9643,        # 96.43%
    'precision': {
        'High': 0.947,
        'Medium': 0.947,
        'Low': 1.000
    },
    'recall': {
        'High': 0.947,
        'Medium': 0.947,
        'Low': 1.000
    },
    'f1_score': {
        'High': 0.947,
        'Medium': 0.947,
        'Low': 1.000
    }
}
```

#### Feature Importance
```python
feature_importance = {
    'profit': 34.80,              # %
    'avg_margin_pct': 12.37,
    'customers': 8.05,
    'category_Fashion': 7.67,
    'transactions': 7.35,
    'category_Electronics': 6.89,
    # ... others
}
```

---

## Visualization System

### 04_generate_visualizations.py

#### Configuration
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Global settings
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14
```

#### Color Palette
```python
COLORS = {
    'primary': '#6B73FF',
    'secondary': '#000DFF',
    'accent1': '#4361EE',
    'accent2': '#7209B7',
    'accent3': '#F72585',
    'accent4': '#4CC9F0',
    'categories': ['#6B73FF', '#000DFF', '#4361EE', '#7209B7', '#F72585', '#4CC9F0']
}
```

#### Chart Specifications

##### 1. Category Revenue Comparison
```python
chart_type: 'barh' (horizontal bar)
data_source: 'category_kpis.csv'
x_axis: Revenue (₹ Cr)
y_axis: Category names
annotations: Revenue value + Share %
sorting: Descending by revenue
```

##### 2. Monthly Revenue Trend
```python
chart_type: 'line' with fill
data_source: 'monthly_time_series.csv'
x_axis: Month index (1-37)
y_axis: Revenue (₹ Cr)
features: Growth annotation, filled area
```

##### 3. Channel Distribution
```python
chart_type: 'pie'
data_source: 'channel_kpis.csv'
explosion: [0.05, 0, 0]  # Highlight top channel
autopct: '%1.1f%%'
colors: Blue gradient
```

##### 4. Top 10 Store Performance
```python
chart_type: 'barh'
data_source: 'store_kpis.csv' (top 10)
x_axis: Revenue (₹ Cr)
y_axis: Store name
color_coding: By store type
annotations: Store type labels
```

##### 5. Customer Segment Analysis
```python
chart_type: 'grouped bar'
data_source: 'segment_kpis.csv'
x_axis: Segment names
y_axis: Dual (Revenue per customer, Transactions per customer)
bar_width: 0.35
```

##### 6. Category Margin Comparison
```python
chart_type: 'bar'
data_source: 'category_kpis.csv'
x_axis: Category names
y_axis: Margin %
annotations: Percentage values on bars
sorting: Descending by margin
```

##### 7. Revenue Forecast
```python
chart_type: 'line' (dual)
data_source: 'monthly_time_series.csv' + 'revenue_forecast.csv'
x_axis: Month index (1-49)
y_axis: Revenue (₹ Cr)
features:
  - Historical data (solid line, blue)
  - Forecast data (dashed line, red)
  - Vertical separator line at month 37
  - Legend distinguishing actual vs predicted
```

##### 8. Anomaly Detection
```python
chart_type: 'scatter'
data_source: 'anomaly_detection.csv'
x_axis: Day index (1-1095)
y_axis: Revenue (₹ Lakhs)
markers:
  - Normal days: Blue dots (small)
  - Anomalies: Red X markers (large)
alpha: 0.6 for normal, 1.0 for anomalies
```

##### 9. Performance Classification
```python
chart_type: 'stacked bar'
data_source: 'category_classification.csv'
x_axis: Category names
y_axis: Count of months
stacks: High, Medium, Low performance
colors: Green, Yellow, Red
```

##### 10. Store Type Analysis
```python
chart_type: 'grouped bar'
data_source: 'store_kpis.csv' (aggregated by type)
x_axis: Store type (Flagship, Premium, Standard, Budget)
y_axis: Multiple metrics
groups: Revenue, Transactions, Customers
bar_width: 0.25
```

##### 11. Revenue-Profit Scatter
```python
chart_type: 'scatter'
data_source: 'category_kpis.csv'
x_axis: Revenue (₹ Cr)
y_axis: Profit (₹ Cr)
markers: Category names as labels
sizes: Proportional to margin %
colors: Category-specific
```

##### 12. KPI Dashboard Summary
```python
chart_type: 'subplot grid' (2x2)
data_sources: Multiple
subplots:
  - [0,0]: Category pie chart
  - [0,1]: Monthly trend line
  - [1,0]: Channel bar chart
  - [1,1]: Segment bar chart
layout: Compact, shared colorscheme
```

---

## Dashboard Architecture

### retail_kpi_dashboard.html

#### Component Structure
```
Dashboard Container
│
├── Header Section
│   ├── Title
│   ├── Subtitle
│   └── ML Badge (96.43% accuracy)
│
├── KPI Grid (5 cards)
│   ├── Total Revenue
│   ├── Total Transactions
│   ├── Total Customers
│   ├── Avg Profit Margin
│   └── Avg Order Value
│
├── ML Insights Section
│   ├── Revenue Forecast Card
│   ├── Anomaly Detection Card
│   ├── Classification Card
│   └── VIP Customer Value Card
│
├── Filters Section
│   ├── Category Dropdown
│   └── Reset Button
│
├── Charts Grid (8 visualizations)
│   ├── Category Revenue Chart
│   ├── Monthly Trend Chart
│   ├── Channel Distribution Chart
│   ├── Segment Analysis Chart
│   ├── Top Stores Chart
│   ├── Margin Comparison Chart
│   ├── Forecast Chart
│   └── Anomaly Detection Chart
│
└── Modal Component
    ├── KPI Detail View
    └── Close Handler
```

#### CSS Architecture

##### Color System
```css
:root {
    --primary-gradient: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
    --primary-color: #6B73FF;
    --secondary-color: #000DFF;
    --text-primary: #2C3E50;
    --text-secondary: #666;
    --background: white;
    --shadow: rgba(0,0,0,0.1);
}
```

##### Grid System
```css
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 20px;
}

.charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    gap: 30px;
}

.ml-insights {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
}
```

##### Animation System
```css
.kpi-card {
    transition: transform 0.3s, box-shadow 0.3s;
}

.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(107, 115, 255, 0.5);
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideUp {
    from {
        transform: translateY(50px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}
```

#### JavaScript Functions

##### Chart Initialization
```javascript
function initDashboard() {
    createCategoryChart();
    createTrendChart();
    createChannelChart();
    createSegmentChart();
    createStoreChart();
    createMarginChart();
    createForecastChart();
    createAnomalyChart();
}
```

##### Chart.js Configuration
```javascript
function createCategoryChart() {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dashboardData.categories.map(c => c.name),
            datasets: [{
                label: 'Revenue (₹ Cr)',
                data: dashboardData.categories.map(c => c.revenue),
                backgroundColor: COLORS.categories,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });
}
```

##### Modal System
```javascript
function showKPIDetail(kpi) {
    const modal = document.getElementById('kpiModal');
    const title = document.getElementById('modal-title');
    const body = document.getElementById('modal-body');
    
    // Populate modal content based on KPI
    // ...
    
    modal.style.display = 'block';
}

function closeModal(event) {
    const modal = document.getElementById('kpiModal');
    if (event.target === modal || event.target.className === 'close') {
        modal.style.display = 'none';
    }
}
```

##### Filter System
```javascript
function filterDashboard() {
    const category = document.getElementById('category-filter').value;
    
    if (category === 'All') {
        // Show all data
    } else {
        // Filter charts by category
        updateCharts(category);
    }
}

function resetFilters() {
    document.getElementById('category-filter').value = 'All';
    filterDashboard();
}
```

---

## API Reference

### Data Files

#### Input Data (Raw)
```
data/raw/products.csv
  Columns: product_id, category, subcategory, brand, name, price, cost, margin_pct
  Records: 1,000

data/raw/customers.csv
  Columns: customer_id, name, email, phone, city, segment, join_date
  Records: 20,000

data/raw/transactions.csv
  Columns: transaction_id, customer_id, product_id, date, store_id, store_name, 
           store_type, channel, quantity, unit_price, revenue, cost, profit, 
           profit_margin_pct, discount_pct
  Records: 200,000
```

#### Processed Data (KPIs)
```
data/processed/overall_kpis.csv
  Single row with 19 overall metrics

data/processed/category_kpis.csv
  6 rows (one per category) with category-level metrics

data/processed/daily_time_series.csv
  1,095 rows (daily data for 36 months)

data/processed/monthly_time_series.csv
  37 rows (monthly aggregations)

data/processed/quarterly_time_series.csv
  13 rows (quarterly aggregations)

data/processed/store_kpis.csv
  15 rows (one per store)

data/processed/segment_kpis.csv
  5 rows (one per customer segment)

data/processed/channel_kpis.csv
  3 rows (one per sales channel)

data/processed/product_kpis.csv
  1,000 rows (one per product)

data/processed/category_month_matrix.csv
  222 rows (6 categories × 37 months)
```

#### Model Outputs
```
models/revenue_forecast.csv
  Columns: month, forecasted_revenue_cr
  Records: 12 (next 12 months)

models/forecasting_metrics.csv
  Single row with R², MAE, MAPE, Accuracy

models/anomaly_detection.csv
  Columns: date, revenue, transactions, profit, margin, customers, quantity, 
           anomaly_score, is_anomaly
  Records: 1,095

models/anomaly_summary.csv
  Summary statistics for normal and anomalous days

models/category_classification.csv
  Columns: category, month, transactions, profit, margin, customers, 
           actual_performance, predicted_performance, prediction_probability
  Records: 222

models/feature_importance.csv
  Columns: feature, importance
  Records: 11

models/classification_metrics.csv
  Precision, recall, F1-score for each class
```

#### Visualizations
```
visualizations/01_category_revenue.png (300 DPI)
visualizations/02_monthly_trend.png (300 DPI)
visualizations/03_channel_distribution.png (300 DPI)
visualizations/04_top_stores.png (300 DPI)
visualizations/05_segment_analysis.png (300 DPI)
visualizations/06_category_margins.png (300 DPI)
visualizations/07_revenue_forecast.png (300 DPI)
visualizations/08_anomaly_detection.png (300 DPI)
visualizations/09_performance_classification.png (300 DPI)
visualizations/10_store_type_analysis.png (300 DPI)
visualizations/11_revenue_profit_scatter.png (300 DPI)
visualizations/12_kpi_dashboard_summary.png (300 DPI)

visualizations/insights.txt
  Text summary of key business insights
```

---

## Performance Benchmarks

### Script Execution Times
```
01_generate_data.py:         ~45 seconds
02_process_data.py:          ~30 seconds
03_ml_models.py:             ~25 seconds
04_generate_visualizations.py: ~40 seconds

Total Pipeline Execution:    ~2.5 minutes
```

### Data Processing Throughput
- **Transactions per second**: 4,444 (200K in 45s)
- **KPI calculations**: 10 datasets in 30s
- **ML model training**: 3 models in 25s
- **Chart generation**: 12 charts in 40s

### Dashboard Performance
- **Initial Load Time**: < 2 seconds
- **Chart Rendering**: < 500ms per chart
- **Filter Response**: < 100ms
- **Modal Animation**: 300ms

---

## Deployment Guide

### Prerequisites
```bash
Python 3.10+
pip install pandas numpy faker matplotlib seaborn scikit-learn
```

### Local Deployment
```bash
# Clone repository
git clone https://github.com/yourusername/Nitin-Fiverr-Portfolio.git
cd 05_Retail_KPI_MultiCategory

# Run pipeline
cd scripts
python 01_generate_data.py
python 02_process_data.py
python 03_ml_models.py
python 04_generate_visualizations.py

# Open dashboard
cd ..
open retail_kpi_dashboard.html  # macOS
start retail_kpi_dashboard.html  # Windows
```

### GitHub Pages Deployment
```bash
# Push to GitHub
git add .
git commit -m "Add Project 5: Multi-Category Retail KPI Dashboard"
git push origin main

# Enable GitHub Pages
# Settings > Pages > Source: main branch > Save

# Access at:
# https://yourusername.github.io/Nitin-Fiverr-Portfolio/05_Retail_KPI_MultiCategory/retail_kpi_dashboard.html
```

---

## Troubleshooting

### Common Issues

#### Issue: Faker Module Not Found
```bash
Solution: pip install faker
```

#### Issue: Unicode Encoding Error (₹ symbol)
```python
Solution: Add encoding='utf-8' to file operations
with open('file.txt', 'w', encoding='utf-8') as f:
    f.write('₹')
```

#### Issue: Charts Not Rendering
```
Solution: Ensure Chart.js CDN is loaded
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

#### Issue: Modal Not Closing
```javascript
Solution: Check event propagation
modal.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}
```

---

## Version History

### v1.0 (Jan 2025)
- Initial release with 6 categories
- 3 ML models (forecasting, anomaly, classification)
- 12 professional visualizations
- Interactive dashboard with Chart.js
- 96.43% classification accuracy achieved

---

## Future Enhancements

1. **Real-time Data Integration**: Connect to live retail APIs
2. **Advanced Filtering**: Multi-select filters, date range picker
3. **Export Functionality**: PDF reports, Excel downloads
4. **Predictive Alerts**: Automated anomaly notifications
5. **Mobile App**: React Native dashboard app
6. **Database Integration**: PostgreSQL/MongoDB backend
7. **User Authentication**: Multi-user dashboard access
8. **A/B Testing Module**: Campaign performance tracking

---

## Contact & Support

For technical questions or contributions:
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Email**: your.email@example.com

---

*Documentation last updated: Jan 2025*
