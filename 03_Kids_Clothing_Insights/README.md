# 👶 Kids Clothing Insights - Enterprise Analytics Hub

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Tableau](https://img.shields.io/badge/Tableau-2024-orange)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green)
![Status](https://img.shields.io/badge/Status-Complete-success)

**Complete Business Intelligence Platform for Kids Fashion Retail**

A comprehensive analytics solution combining **Sales Performance**, **Customer Segmentation**, **Inventory Management**, **Executive KPIs**, and **E-commerce Analytics** into a unified Tableau dashboard suite.

---

## 📊 Project Overview

This project delivers end-to-end business intelligence for a kids clothing retail business with 10 stores across 4 US regions, managing 900+ SKUs and serving 10,000+ customers through both physical stores and online channels.

**Industry**: Kids Fashion Retail  
**Data Period**: January 2023 - December 2024 (2 years)  
**Total Records**: 456,000+ data points  
**Analysis Modules**: 5 integrated dashboards

---

## 🎯 Key Business Metrics

| Metric | Value | Insight |
|--------|-------|---------|
| 💰 **Total Revenue** | $1,956,784 | Girls clothing leads with 45.2% share |
| 📈 **Gross Margin** | 45.23% | Above industry average (40-42%) |
| 💵 **Net Profit** | $223,574 | 11.43% net margin |
| 🛍️ **Transactions** | 50,000 | Avg order value: $39.14 |
| 👥 **Active Customers** | 9,823 | 92.5% repeat purchase rate |
| 📦 **Inventory Value** | $152,386 | 7.03x turnover ratio |
| 🌐 **Web Sessions** | 200,000 | 1.76% conversion rate |
| 🔄 **Cart Abandonment** | 84.35% | Primary reason: shipping costs (32%) |

---

## 🗂️ Project Structure

```
03_Kids_Clothing_Insights/
│
├── data/
│   ├── raw/                              # Original datasets (456K+ records)
│   │   ├── sales_transactions.csv        # 50,000 transactions
│   │   ├── customers.csv                 # 10,000 customer profiles
│   │   ├── products.csv                  # 900 SKUs
│   │   ├── inventory.csv                 # Stock levels & reorder data
│   │   ├── stores.csv                    # 10 store locations
│   │   ├── suppliers.csv                 # 15 supplier partners
│   │   └── web_analytics.csv             # 395,312 web events
│   │
│   └── processed/                        # Analysis outputs (50+ files)
│       ├── sales_summary.csv
│       ├── customer_rfm.csv              # RFM segmentation
│       ├── inventory_turnover.csv
│       ├── executive_scorecard.csv
│       └── conversion_funnel.csv
│
├── scripts/                              # Python analysis scripts
│   ├── 01_generate_data.py               # Data generation engine
│   ├── 02_sales_analysis.py              # Sales & performance metrics
│   ├── 03_customer_segmentation.py       # RFM & CLV analysis
│   ├── 04_inventory_management.py        # Stock & supply chain
│   ├── 05_executive_summary.py           # Financial KPIs
│   └── 06_ecommerce_analysis.py          # Web analytics & funnel
│
├── tableau/                              # Tableau workbooks & screenshots
│   ├── Kids_Clothing_Analytics.twbx      # Complete packaged workbook
│   └── dashboard_screenshots/            # Preview images
│
├── documentation/
│   ├── Data_Dictionary.md                # Complete data schema
│   ├── Business_Requirements.md          # Project requirements
│   └── Tableau_Usage_Guide.md            # Dashboard navigation
│
├── README.md                             # This file
└── MASTER_PROMPT.md                      # Project blueprint
```

---

## 📈 Analytics Modules

### 1️⃣ Sales Performance Dashboard

**Purpose**: Multi-dimensional sales analysis across stores, categories, and time periods

**Key Features**:
- 📍 **Geographic Sales Map**: Store performance by location with revenue bubbles
- 📊 **Category Breakdown**: Girls (45%), Boys (28%), Infants (17%), Accessories (9%)
- 📅 **Seasonal Trends**: Summer peak ($427K), Back-to-school surge in Aug-Sep
- 🏪 **Store Rankings**: LA Fashion Kids leads with $122K revenue
- 🌐 **Channel Split**: Online (42%) vs Offline (58%)
- 💳 **Payment Methods**: Credit cards dominate (45.4%)

**Top Insights**:
- West region generates highest revenue per store ($115K)
- Girls clothing has best margins and highest AOV ($47.49 online)
- Q4 holiday season drives 35% of annual sales
- Weekend sales 30% higher than weekdays

---

### 2️⃣ Customer Analytics Dashboard

**Purpose**: Customer behavior, segmentation, and lifetime value analysis

**Key Features**:
- 🎯 **RFM Segmentation**: 10 customer segments (Champions, Loyal, At-Risk, etc.)
- 💰 **Customer Lifetime Value**: Avg CLV $429.80 (Champions: $717.86)
- 🔄 **Cohort Analysis**: Retention rates by signup month
- 🗺️ **Geographic Distribution**: Customer density heatmap
- 👤 **Demographics**: Age groups and gender-based insights
- 📊 **Purchase Frequency**: Avg 4.07 purchases per customer

**Customer Segments**:
| Segment | Count | Avg CLV | Strategy |
|---------|-------|---------|----------|
| 🏆 **Champions** | 1,677 (17.1%) | $717.86 | VIP rewards program |
| ❤️ **Loyal Customers** | 1,171 (11.9%) | $558.91 | Exclusive previews |
| 🌟 **Potential Loyalists** | 1,360 (13.8%) | $143.99 | Upsell campaigns |
| ⚠️ **Need Attention** | 1,702 (17.3%) | $446.73 | Re-engagement emails |
| ⛔ **At Risk** | 563 (5.7%) | $469.78 | Win-back offers |

**Key Insights**:
- 92.5% repeat purchase rate (industry avg: 25-30%)
- CLV/CAC ratio of 22.6:1 (excellent: >3:1)
- 26-35 age group has highest CLV ($435.83)
- New York City leads in customer revenue ($85K)

---

### 3️⃣ Inventory & Supply Chain Dashboard

**Purpose**: Stock optimization, reorder alerts, and supplier performance

**Key Features**:
- 🚨 **Stock Alerts**: 44 critical items (need immediate reorder)
- 📦 **Inventory Health**: 93% normal stock, 7% critical/low
- 🔄 **Turnover Analysis**: 7.03x average (healthy for retail)
- 🏭 **Supplier Scorecard**: Performance by delivery, quality, lead time
- ⏰ **Stock Age**: 37.5% inventory ageing (90+ days)
- 💸 **Slow-Moving Items**: $23K locked in slow inventory

**Supplier Performance**:
| Rank | Supplier | Score | Lead Time | On-Time % |
|------|----------|-------|-----------|-----------|
| 🥇 | Baby Boutique Supplies | 0.899 | 12 days | 96% |
| 🥈 | Fashion Kids Suppliers | 0.892 | 14 days | 95% |
| 🥉 | ABC Textiles Ltd | 0.890 | 15 days | 96% |

**Actionable Insights**:
- $5,876 immediate reorder cost for critical items
- Girls clothing has most critical stock items (17)
- Fast-moving items (240 SKUs) drive 13.5% of inventory value
- WH002 has highest utilization (52% of stock value)

---

### 4️⃣ Executive Summary Dashboard

**Purpose**: High-level KPIs and financial performance for leadership

**Key Features**:
- 💵 **Financial Summary**: Revenue, margins, EBITDA, profitability
- 📊 **KPI Scorecards**: Traffic light indicators (Green/Yellow/Red)
- 📈 **YoY Comparison**: Growth trends vs previous year
- 📅 **Quarterly Performance**: Q4 2024 strongest ($249K)
- 🔮 **6-Month Forecast**: $489K projected revenue
- 🎯 **Market Position**: Estimated 10% market share

**Financial Snapshot**:
```
Revenue:            $1,956,784
COGS:              ($1,071,650)
─────────────────────────────
Gross Profit:         $885,134   (45.23%)
Operating Expenses:  ($587,035)
─────────────────────────────
Operating Profit:     $298,099   (15.23%)
Net Profit:           $223,574   (11.43%)

EBITDA:               $337,235
```

**Executive Scorecard**:
| KPI | Actual | Target | Status |
|-----|--------|--------|--------|
| Gross Margin | 45.23% | 45.0% | 🟢 Green |
| Net Margin | 11.43% | 15.0% | 🔴 Red |
| Inventory Turnover | 7.03x | 5.0x | 🟢 Green |
| CLV/CAC Ratio | 22.62x | 5.0x | 🟢 Green |
| Avg Transaction | $39.14 | $45.0 | 🔴 Red |

---

### 5️⃣ E-commerce Analytics Dashboard

**Purpose**: Online channel performance, conversion funnel, and user behavior

**Key Features**:
- 🎯 **Conversion Funnel**: Homepage → Purchase journey analysis
- 📱 **Device Breakdown**: Mobile (57.7%), Desktop (35.3%), Tablet (7%)
- 🚀 **Traffic Sources**: Organic search leads (42.1%)
- 🛒 **Cart Abandonment**: 84.35% rate with reason breakdown
- ⏰ **Peak Hours**: 2-6 PM highest traffic
- 📄 **Product Performance**: Top viewed & converting products

**Conversion Funnel**:
```
Homepage:     200,000 sessions (100%)
    ↓ 60% drop-off
Category:      80,014 sessions (40%)
    ↓ 30% drop-off
Product:       56,085 sessions (28%)
    ↓ 60% drop-off
Cart:          22,456 sessions (11%)
    ↓ 68% drop-off
Checkout:       7,271 sessions (4%)
    ↓ 52% drop-off
Purchase:       3,515 sessions (1.76%)
```

**Cart Abandonment Reasons**:
- 🚚 High Shipping Costs: 32%
- 💰 Better Price Elsewhere: 18%
- 💳 Payment Issues: 15%
- 👀 Just Browsing: 20%
- 🐛 Website Errors: 8%
- ❓ Other: 7%

**Traffic Source Performance**:
| Source | Sessions | Share | Conversion |
|--------|----------|-------|------------|
| Organic Search | 84,125 | 42.1% | 1.69% |
| Paid Search | 35,832 | 17.9% | 1.84% |
| Social Media | 29,981 | 15.0% | 1.76% |
| Direct | 24,095 | 12.1% | 1.89% |

---

## 🛠️ Technologies Used

- **Python 3.14**: Data processing and analysis
- **Pandas 2.0+**: Data manipulation and aggregation
- **NumPy**: Statistical calculations
- **Tableau 2024**: Interactive dashboard visualization
- **CSV**: Data storage format

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.10+
Tableau Desktop 2023.1+
Pandas, NumPy libraries
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Nitindb901/Nitin-Fiverr-Portfolio.git
cd 03_Kids_Clothing_Insights
```

2. **Install dependencies**
```bash
pip install pandas numpy
```

3. **Generate data (if needed)**
```bash
python scripts/01_generate_data.py
```

4. **Run analysis scripts**
```bash
python scripts/02_sales_analysis.py
python scripts/03_customer_segmentation.py
python scripts/04_inventory_management.py
python scripts/05_executive_summary.py
python scripts/06_ecommerce_analysis.py
```

5. **Open Tableau workbook**
- Navigate to `tableau/` folder
- Open `Kids_Clothing_Analytics.twbx` in Tableau Desktop
- Explore 5 interactive dashboards

---

## 📊 Data Dictionary

### Sales Transactions (50,000 rows)
| Column | Type | Description |
|--------|------|-------------|
| TransactionID | String | Unique transaction identifier (TXN000001) |
| Date | Date | Transaction date (2023-01-01 to 2024-12-31) |
| StoreID | String | Store identifier or 'ONLINE' |
| ProductID | String | Product identifier (P0001-P0900) |
| CustomerID | String | Customer identifier or GUEST#### |
| Quantity | Integer | Units purchased (1-3) |
| UnitPrice | Float | Price per unit after discounts |
| TotalAmount | Float | Total transaction value |
| PaymentMethod | String | Credit Card, Debit Card, PayPal, Cash |
| Channel | String | Online or Offline |

### Customer RFM (9,823 rows)
| Column | Type | Description |
|--------|------|-------------|
| CustomerID | String | Unique customer identifier |
| Recency | Integer | Days since last purchase |
| Frequency | Integer | Total number of purchases |
| Monetary | Float | Total spend across all purchases |
| R_Score | Integer | Recency score (1-5) |
| F_Score | Integer | Frequency score (1-5) |
| M_Score | Integer | Monetary score (1-5) |
| Segment | String | Customer segment (10 categories) |
| CLV | Float | Customer Lifetime Value |

### Inventory (900 rows)
| Column | Type | Description |
|--------|------|-------------|
| ProductID | String | Product identifier |
| WarehouseID | String | Warehouse location (WH001-WH003) |
| StockLevel | Integer | Current units in stock |
| ReorderPoint | Integer | Threshold for reorder alert |
| LeadTime | Integer | Supplier delivery time (days) |
| StockStatus | String | Critical, Low, or Normal |
| TurnoverRatio | Float | Annual sales / avg inventory |

*Full data dictionary available in `/documentation/Data_Dictionary.md`*

---

## 📚 Business Insights & Recommendations

### 🎯 Sales Optimization
1. **Focus on Girls Clothing**: 45% revenue share, highest margins
2. **Expand Online Presence**: 42% revenue with better AOV ($39.42 vs $38.93)
3. **Regional Strategy**: West region shows best performance ($115K/store)
4. **Seasonal Planning**: Increase inventory before Q4 (35% annual sales)

### 👥 Customer Engagement
1. **Champions Program**: VIP benefits for top 17% customers (CLV: $717)
2. **Win-Back Campaigns**: Target 563 "At Risk" customers (high CLV)
3. **New Customer Onboarding**: Convert one-time buyers (7.5%) to repeat
4. **Geographic Expansion**: Focus on top cities (NYC, Columbus, Denver)

### 📦 Inventory Management
1. **Immediate Action**: Reorder 44 critical items ($5,876 investment)
2. **Slow Inventory Clearance**: Discount 119 slow-moving items ($23K locked)
3. **Supplier Optimization**: Increase orders from top 3 suppliers (96% OTD)
4. **Category Balance**: Reduce Girls Clothing stock age (highest ageing)

### 🌐 E-commerce Enhancements
1. **Reduce Cart Abandonment**: Free shipping threshold to address #1 reason
2. **Mobile Optimization**: 57.7% traffic but same conversion as desktop
3. **Checkout Simplification**: 52% drop-off at final step
4. **Product Page UX**: Highlight top converters (63% add-to-cart rate)

### 💰 Financial Improvements
1. **Increase Net Margin**: Target 15% through operational efficiency
2. **Boost AOV**: Bundle deals to reach $45 target (current $39.14)
3. **Marketing ROI**: Excellent CLV/CAC (22.6x) - scale acquisition
4. **Forecast Confidence**: 6-month projection: $489K revenue

---

## 📸 Dashboard Previews

> **Note**: Tableau workbook contains 5 interactive dashboards with drill-down capabilities, filters, and real-time calculations.

### Sales Performance
- Geographic heatmap with store performance
- Category and seasonal trend analysis
- Top products and payment method breakdown

### Customer Analytics
- RFM segmentation scatter plot
- Cohort retention heatmap
- Geographic customer distribution

### Inventory Management
- Stock level gauges by category
- Critical reorder alerts table
- Supplier performance scorecard

### Executive Summary
- Financial KPI cards with sparklines
- YoY comparison charts
- Revenue forecast with confidence bands

### E-commerce Analytics
- Conversion funnel visualization
- Traffic source pie charts
- Device performance comparison

---

## 🎓 Skills Demonstrated

- ✅ **Business Intelligence**: Multi-source data integration and analysis
- ✅ **Data Visualization**: Tableau dashboard design with best practices
- ✅ **Python Programming**: Advanced Pandas, NumPy data processing
- ✅ **Analytics**: Sales, Customer, Inventory, Financial, Web analytics
- ✅ **Data Engineering**: ETL pipeline from raw to processed data
- ✅ **Business Acumen**: Retail industry knowledge and KPI understanding
- ✅ **Statistical Analysis**: RFM segmentation, CLV calculation, forecasting
- ✅ **Documentation**: Comprehensive technical and business documentation

---

## 📁 Related Projects

- [**Project 1**: Retail Analytics Dashboard](../01_Retail_Analytics_Dashboard/)
- [**Project 2**: Grocery + Fashion Dashboard](../02_Grocery_Fashion_Dashboard/)
- [**Project 7**: Sales Forecasting with ML](../07_Sales_Forecasting_ML/)
- [**Project 8**: Customer Segmentation (K-Means)](../08_Customer_Segmentation_KMeans/)

---

## 🤝 Contact

**Nitin DB**  
📧 Email: nitindb901@gmail.com  
💼 LinkedIn: [linkedin.com/in/nitindb](https://linkedin.com/in/nitindb)  
🐙 GitHub: [github.com/Nitindb901](https://github.com/Nitindb901)  

---

## 📄 License

This project is part of a professional portfolio. All data is synthetic and generated for demonstration purposes.

---

## 🙏 Acknowledgments

- **Data Generation**: Realistic patterns based on retail industry research
- **Tableau Best Practices**: Following Tableau's design guidelines
- **Business Metrics**: Industry-standard KPIs for retail analytics

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by Nitin DB | © 2024

</div>
