# 📚 Technical Documentation - Men's Clothing Analytics Dashboard

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Data Pipeline](#data-pipeline)
3. [Machine Learning Models](#machine-learning-models)
4. [Dashboard Implementation](#dashboard-implementation)
5. [API Reference](#api-reference)
6. [Performance Optimization](#performance-optimization)
7. [Troubleshooting](#troubleshooting)

---

## 🏗️ Architecture Overview

### System Design
```
┌─────────────────────────────────────────────────────────────┐
│                    Data Generation Layer                     │
│  (01_generate_data.py - Synthetic Transaction Generator)     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Processing Layer                      │
│  (02_process_data.py - ETL, RFM Analysis, Aggregations)     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                 Machine Learning Layer                       │
│  (03_ml_models.py - Forecasting & Clustering)               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                  Visualization Layer                         │
│  (04_generate_visualizations.py - Charts & Insights)        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Presentation Layer                         │
│  (mens_clothing_dashboard.html - Interactive Dashboard)     │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technologies | Purpose |
|-------|--------------|---------|
| **Data Generation** | Python, NumPy, Pandas, Random | Create realistic synthetic data |
| **Data Processing** | Pandas, NumPy | ETL, feature engineering, aggregations |
| **Machine Learning** | Scikit-learn, NumPy | Forecasting, clustering, predictions |
| **Visualization** | Matplotlib, Seaborn | Static chart generation |
| **Web Dashboard** | HTML5, CSS3, JavaScript, Chart.js | Interactive analytics interface |
| **Deployment** | Git, GitHub Pages | Version control & hosting |

---

## 📊 Data Pipeline

### 1. Data Generation (01_generate_data.py)

#### Purpose
Generate synthetic but realistic men's clothing retail transaction data for analysis.

#### Process Flow
```python
# Configuration
NUM_TRANSACTIONS = 100,000
NUM_CUSTOMERS = 12,000
NUM_PRODUCTS = 500
DATE_RANGE = Jan 2023 - Dec 2024

# Step 1: Generate Product Catalog
for each category in [Formal, Casual, Sports, Accessories]:
    - Select subcategories (e.g., Suits, T-Shirts, Gym Wear, Belts)
    - Assign brand tier (Premium, Mid-Range, Budget)
    - Calculate price based on tier
    - Compute cost for margin calculation (55-70% of price)
    
# Step 2: Generate Customer Base
for each customer:
    - Assign segment (Premium, Value-Conscious, Trendy, Casual, Fitness)
    - Determine age (18-65, normal distribution around 35)
    - Set income level based on segment
    - Record join date

# Step 3: Generate Transactions
for each transaction:
    - Select random date with seasonal bias
    - Choose customer (60% repeat, 40% new)
    - Match product to customer segment
    - Calculate quantity (weighted: 70% buy 1, 25% buy 2, 5% buy 3)
    - Apply discount based on season
    - Assign store and channel
    - Record payment method
```

#### Seasonal Patterns Implemented
- **Festive Season** (Oct-Dec): 1.5x boost
- **Sale Months** (Jan, Jul): 1.3x boost, 20-50% discounts
- **Regular Months**: Standard patterns

#### Output Files
- `data/raw/transactions.csv` - 100K rows, 19 columns
- `data/raw/products.csv` - 500 rows, 11 columns
- `data/raw/customers.csv` - 12K rows, 5 columns

---

### 2. Data Processing (02_process_data.py)

#### Purpose
Clean, transform, and prepare data for analysis and ML modeling.

#### Data Quality Checks
```python
# Validation Steps
1. Check for missing values (should be 0)
2. Identify duplicate transactions
3. Validate date ranges
4. Verify data types
```

#### Feature Engineering
```python
# Time-based Features
- DayOfWeek: Monday-Sunday
- WeekOfYear: 1-52
- IsWeekend: 0 or 1
- MonthName: January-December

# Financial Features
- CostAmount = Cost × Quantity
- MarginAmount = TotalAmount - CostAmount
- MarginPercent = (MarginAmount / TotalAmount) × 100
```

#### RFM Analysis
```python
# Calculate RFM Metrics
analysis_date = max(transaction_date) + 1 day

for each customer:
    Recency = days since last purchase
    Frequency = count of transactions
    Monetary = sum of total amount

# Score RFM on 1-5 scale
R_Score = quantile(Recency, 5) [inverted: 5 is best]
F_Score = quantile(Frequency, 5) [5 is best]
M_Score = quantile(Monetary, 5) [5 is best]

RFM_Total = R_Score + F_Score + M_Score

# Segment Customers
if RFM_Total >= 13: Champions
elif RFM_Total >= 10: Loyal Customers
elif RFM_Total >= 7: Potential Loyalists
elif RFM_Total >= 5 and R_Score >= 3: Recent Customers
elif RFM_Total >= 5: At Risk
else: Lost Customers
```

#### Aggregations Created
1. **Monthly Sales by Category** - 24 months × 4 categories = 96 rows
2. **Monthly Totals** - Revenue, transactions, customers, margin (24 rows)
3. **Category Performance** - Revenue, share, AOV, margin (4 rows)
4. **Brand Performance** - 13 brands with metrics
5. **Store Performance** - 10 stores with KPIs
6. **Channel Performance** - 3 channels with distribution
7. **Customer Lifetime Value** - 11,998 customers with CLV metrics

#### Output Files (11 processed datasets)
```
data/processed/
├── transactions_processed.csv       # Enhanced with features
├── customers_rfm.csv                # Customers with RFM scores
├── rfm_analysis.csv                 # RFM summary
├── monthly_sales_by_category.csv
├── monthly_totals.csv
├── category_performance.csv
├── brand_performance.csv
├── store_performance.csv
├── channel_performance.csv
├── customer_lifetime_value.csv
└── product_performance.csv
```

---

## 🤖 Machine Learning Models

### Model 1: Sales Forecasting

#### Algorithm: Weighted Moving Average with Trend & Seasonality

**Mathematical Formulation**:
```
# Base Forecast
weights = [0.5, 0.3, 0.2]  # Last 3 months
base_forecast = Σ(revenue[t-i] × weights[i]) for i in [1,2,3]

# Trend Calculation
recent_6_avg = avg(revenue[t-5:t])
earlier_6_avg = avg(revenue[t-11:t-6])
trend = (recent_6_avg - earlier_6_avg) / earlier_6_avg

# Forecast with Trend
for month i in [1, 2, ..., 6]:
    trend_factor = 1 + (trend × (1 - i × 0.1))  # Diminishing trend
    forecast[i] = base_forecast × trend_factor
    
    # Apply Seasonality
    historical_month_avg = avg(revenue for same month in history)
    seasonal_factor = historical_month_avg / overall_avg
    forecast[i] *= seasonal_factor

# Confidence Interval
lower_bound = forecast × 0.85  # 15% below
upper_bound = forecast × 1.15  # 15% above
```

**Model Validation**:
```python
# Backtesting (Last 3 months)
actual = [month_n-2, month_n-1, month_n]
predicted = []

for i in range(3):
    train_data = all_data[:-(3-i)]
    pred = forecast_next_months(train_data, n_months=1)
    predicted.append(pred)

# Calculate Error
MAPE = mean(abs((actual - predicted) / actual)) × 100
Accuracy = 100 - MAPE
```

**Performance Metrics**:
- **MAPE**: 6.82%
- **Accuracy**: 93.18%
- **Forecast Horizon**: 6 months
- **Update Frequency**: Monthly (retrain with new data)

**Predictions Output**:
```csv
Month,Predicted_Revenue,Lower_Bound,Upper_Bound
2025-01,6665516,5665689,7665343
2025-02,8430767,7166152,9695382
...
```

---

### Model 2: Customer Segmentation (K-Means)

#### Algorithm Configuration
```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Feature Preparation
features = ['Recency', 'Frequency', 'Monetary']

# Log Transformation (handle skewness)
features_log = log1p(features)

# Standardization (mean=0, std=1)
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features_log)

# Model Training
kmeans = KMeans(
    n_clusters=5,
    init='k-means++',
    n_init=10,
    max_iter=300,
    random_state=42
)
clusters = kmeans.fit_predict(features_scaled)
```

#### Optimal K Selection
```python
# Elbow Method
for k in range(3, 9):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(features_scaled)
    inertias.append(kmeans.inertia_)
    
# Silhouette Score
for k in range(3, 9):
    kmeans = KMeans(n_clusters=k)
    labels = kmeans.fit_predict(features_scaled)
    silhouette_scores.append(silhouette_score(features_scaled, labels))

# Select k=5 for balance between inertia and interpretability
```

#### Cluster Interpretation
```python
# Analyze Cluster Characteristics
for cluster_id in [0, 1, 2, 3, 4]:
    avg_recency = mean(recency[cluster == cluster_id])
    avg_frequency = mean(frequency[cluster == cluster_id])
    avg_monetary = mean(monetary[cluster == cluster_id])
    
    # Name based on characteristics
    if avg_monetary > 25000 and avg_frequency > 10:
        name = "VIP Customers"
    elif avg_recency < 100 and avg_frequency > 8:
        name = "Loyal Actives"
    # ... more rules
```

**Cluster Profiles**:

| Cluster ID | Name | Size | Avg Recency | Avg Frequency | Avg Monetary | Business Action |
|------------|------|------|-------------|---------------|--------------|-----------------|
| 0 | Loyal Actives | 1,620 | 80 days | 10.4 | ₹22,091 | Reward loyalty |
| 1 | Regular Shoppers | 3,286 | 145 days | 7.4 | ₹14,142 | Upsell campaigns |
| 2 | Regular Shoppers | 1,535 | 180 days | 4.3 | ₹6,317 | Engagement emails |
| 3 | VIP Customers | 3,367 | 65 days | 10.8 | ₹26,344 | Premium service |
| 4 | Regular Shoppers | 2,190 | 160 days | 7.2 | ₹10,815 | Retention offers |

**Model Metrics**:
- **Silhouette Score**: 0.256 (acceptable clustering quality)
- **Inertia**: 12,578.30
- **Iterations to Converge**: 17

---

## 💻 Dashboard Implementation

### HTML Structure
```html
<body>
    <div class="dashboard-container">
        <!-- Header with title and ML badge -->
        <div class="header">...</div>
        
        <!-- KPI Cards (5 cards) -->
        <div class="kpi-grid">
            <div class="kpi-card" onclick="showKPIDetail()">...</div>
        </div>
        
        <!-- ML Insights Section -->
        <div class="ml-section">
            <div class="ml-insights">
                <div class="ml-card">...</div>
            </div>
        </div>
        
        <!-- Filters -->
        <div class="filters">
            <button class="filter-btn">...</button>
        </div>
        
        <!-- Key Insights Box -->
        <div class="insights-box">...</div>
        
        <!-- Charts Grid (7 charts) -->
        <div class="charts-grid">
            <div class="chart-container">
                <canvas id="categoryChart"></canvas>
            </div>
        </div>
        
        <!-- Category Table -->
        <table class="data-table">...</table>
        
        <!-- ML Forecast Chart -->
        <canvas id="forecastChart"></canvas>
    </div>
    
    <!-- Modal Overlay -->
    <div class="modal-overlay">
        <div class="modal-content">...</div>
    </div>
</body>
```

### CSS Architecture
```css
/* Design System */
:root {
    --primary-color: #2E86AB;
    --secondary-color: #2C3E50;
    --accent-color: #F18F01;
    --success-color: #06A77D;
    --danger-color: #C73E1D;
    
    --spacing-sm: 10px;
    --spacing-md: 20px;
    --spacing-lg: 30px;
    
    --border-radius: 15px;
    --transition-speed: 0.3s;
}

/* Layout */
.dashboard-container { max-width: 1500px; }
.kpi-grid { grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); }
.charts-grid { grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); }

/* Animations */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { transform: translateY(50px); opacity: 0; } }
@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
```

### JavaScript Data Management
```javascript
// Dashboard Data Structure
const dashboardData = {
    categories: [...],      // 4 categories with revenue, share, transactions
    channels: [...],        // 3 channels with distribution
    monthlyData: [...],     // 24 months of time series
    segments: [...],        // 6 RFM segments
    stores: [...],          // 10 stores
    mlClusters: [...],      // 5 ML clusters
    forecast: [...]         // 6 months predictions
};

// State Management
let currentFilter = 'all';

// Event Handlers
function setupFilters() {
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            currentFilter = btn.dataset.value;
            updateDashboard();
        });
    });
}

function updateDashboard() {
    // Add animation
    container.classList.add('update-animation');
    
    // Update charts and table
    setTimeout(() => {
        updateCategoryChart();
        populateCategoryTable();
        container.classList.remove('update-animation');
    }, 300);
}
```

### Chart.js Implementation
```javascript
// Example: Category Chart
function createCategoryChart() {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    const filteredData = getFilteredData();
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: filteredData.map(c => c.name),
            datasets: [{
                label: 'Revenue (₹)',
                data: filteredData.map(c => c.revenue),
                backgroundColor: ['#2E86AB', '#3498DB', '#E74C3C', '#9B59B6'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            return '₹' + (context.raw / 10000000).toFixed(2) + ' Cr';
                        }
                    }
                }
            },
            onClick: (event, elements) => {
                if (elements.length > 0) {
                    showCategoryDetail(filteredData[elements[0].index]);
                }
            }
        }
    });
}
```

### Modal System
```javascript
// Show KPI Detail
function showKPIDetail(kpi) {
    const modal = document.getElementById('modalOverlay');
    const kpiData = {
        revenue: {
            icon: '💰',
            title: 'Total Revenue',
            subtitle: '₹20.43 Crores',
            stats: [
                { label: 'Casual Wear', value: '₹6.33 Cr' },
                // ... more stats
            ],
            insights: [
                { icon: '📈', text: '+22.3% growth' },
                // ... more insights
            ]
        }
        // ... more KPIs
    };
    
    // Populate modal content
    populateModal(kpiData[kpi]);
    modal.style.display = 'flex';
}

// Close Modal
function closeModal(event) {
    if (event.target === modal || event.target.classList.contains('modal-close')) {
        modal.style.display = 'none';
    }
}

// ESC key support
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeModal();
    }
});
```

---

## 🔧 API Reference

### Data Generation Functions

```python
def forecast_next_months(data: pd.DataFrame, n_months: int) -> np.array
    """
    Forecast revenue for next n months using weighted moving average.
    
    Args:
        data: DataFrame with 'Revenue' column and monthly data
        n_months: Number of months to forecast (default: 6)
    
    Returns:
        numpy array of forecasted values
    """
```

```python
def segment_customers(row: pd.Series) -> str
    """
    Segment customer based on RFM total score.
    
    Args:
        row: Pandas Series with RFM_Total and R_Score
    
    Returns:
        str: Segment name (Champions, Loyal Customers, etc.)
    """
```

### Chart Functions

```javascript
function createCategoryChart()
    // Creates bar chart for category revenue performance
    // Uses Chart.js library
    // Handles click events to show detailed modal

function updateCategoryChart()
    // Destroys existing chart and recreates with filtered data
    // Called when filters are applied

function showKPIDetail(kpi: string)
    // Displays modal with detailed KPI breakdown
    // Args: kpi - one of ['revenue', 'transactions', 'customers', 'margin', 'clv']

function closeModal(event: Event)
    // Closes modal on overlay click, close button, or ESC key
```

---

## ⚡ Performance Optimization

### Data Processing
1. **Vectorized Operations**: Use Pandas/NumPy instead of loops
2. **Chunking**: Process large files in chunks if memory constrained
3. **Data Types**: Use appropriate dtypes (int32 vs int64, category for strings)
4. **Indexing**: Set proper indexes for fast lookups

### Dashboard
1. **Chart Destroy/Recreate**: Properly destroy Chart.js instances before recreation
2. **Debouncing**: Delay filter updates by 300ms for smooth animations
3. **Lazy Loading**: Load charts only when visible
4. **Image Optimization**: Use compressed PNGs for visualizations

### ML Models
1. **Feature Scaling**: Always scale features before K-means
2. **Random State**: Set seed for reproducibility
3. **n_init Parameter**: Use 10 initializations for stable results
4. **Early Stopping**: Monitor convergence for iterative algorithms

---

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: Charts Not Rendering
**Symptoms**: Blank chart containers  
**Solution**:
```javascript
// Ensure Chart.js is loaded
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

// Check canvas exists
const canvas = document.getElementById('categoryChart');
if (!canvas) {
    console.error('Canvas element not found');
}

// Verify data format
console.log(dashboardData.categories);  // Should be array of objects
```

#### Issue 2: Filter Not Working
**Symptoms**: Charts don't update on filter click  
**Solution**:
```javascript
// Check event listeners
document.querySelectorAll('.filter-btn').forEach(btn => {
    console.log('Button:', btn, 'Filter:', btn.dataset.filter);
});

// Verify currentFilter value
console.log('Current filter:', currentFilter);

// Check if updateDashboard is called
function updateDashboard() {
    console.log('Updating dashboard with filter:', currentFilter);
    // ... rest of code
}
```

#### Issue 3: Modal Not Closing
**Symptoms**: Modal stays open on overlay click  
**Solution**:
```javascript
// Add stopPropagation to modal content
<div class="modal-content" onclick="event.stopPropagation()">

// Check event handler
document.getElementById('modalOverlay').onclick = function(event) {
    console.log('Click target:', event.target);
    closeModal(event);
};
```

#### Issue 4: ML Model Poor Performance
**Symptoms**: High MAPE (>10%) or strange forecasts  
**Solution**:
```python
# Check for outliers
print(monthly_totals['Revenue'].describe())

# Verify trend calculation
recent_6 = monthly_totals['Revenue'].tail(6).values
print('Recent 6 months:', recent_6)

# Test seasonal factor
month_avg = monthly_totals[monthly_totals['Month'].dt.month == 1]['Revenue'].mean()
overall_avg = monthly_totals['Revenue'].mean()
seasonal_factor = month_avg / overall_avg
print('January seasonal factor:', seasonal_factor)
```

#### Issue 5: Large File Size
**Symptoms**: Dashboard HTML >5MB  
**Solution**:
```javascript
// Minimize data embedded in HTML
// Store only essential data, calculate derived metrics on-the-fly

// Compress JSON
const compressedData = JSON.stringify(dashboardData, null, 0);  // No indentation

// Use CDN for Chart.js (already done)
```

---

## 📝 Best Practices

### Data Science
1. Always validate data quality before analysis
2. Document assumptions and business rules
3. Use version control for scripts
4. Save intermediate results for debugging
5. Create reproducible pipelines with clear dependencies

### Dashboard Development
1. Mobile-first responsive design
2. Accessibility (ARIA labels, keyboard navigation)
3. Consistent color scheme and branding
4. Loading states for async operations
5. Error handling and user feedback

### Machine Learning
1. Split data chronologically for time series
2. Validate on recent unseen data
3. Monitor model performance over time
4. Document model limitations and assumptions
5. Plan for model retraining schedule

---

## 🔄 Maintenance & Updates

### Monthly Tasks
- [ ] Add new transaction data
- [ ] Retrain ML models
- [ ] Update dashboard with latest KPIs
- [ ] Review model accuracy

### Quarterly Tasks
- [ ] Analyze new customer segments
- [ ] Optimize discount strategies
- [ ] Review store performance
- [ ] Update forecasts

### Annual Tasks
- [ ] Full model reevaluation
- [ ] Dashboard redesign if needed
- [ ] Technology stack updates
- [ ] Comprehensive business review

---

## 📚 References

### Libraries Documentation
- [Pandas](https://pandas.pydata.org/docs/)
- [NumPy](https://numpy.org/doc/)
- [Scikit-learn](https://scikit-learn.org/stable/documentation.html)
- [Matplotlib](https://matplotlib.org/stable/contents.html)
- [Chart.js](https://www.chartjs.org/docs/latest/)

### Learning Resources
- [K-means Clustering Explained](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [Time Series Forecasting](https://otexts.com/fpp2/)
- [RFM Analysis Guide](https://www.optimove.com/resources/learning-center/rfm-segmentation)

---

**Last Updated**: November 22, 2025  
**Version**: 1.0.0  
**Author**: Nitin
