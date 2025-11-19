# PROJECT 3: KIDS CLOTHING INSIGHTS - ENTERPRISE ANALYTICS HUB

## 🎯 PROJECT OVERVIEW
**Industry**: Kids Fashion Retail  
**Type**: Comprehensive Business Intelligence Dashboard (Tableau)  
**Scope**: End-to-end analytics covering Sales, Customers, Inventory, Executive KPIs, and E-commerce  
**Goal**: Create unified analytics platform for kids clothing business decision-making

---

## 📊 INTEGRATED MODULES

### Module 1: Sales Performance Dashboard
**Purpose**: Multi-dimensional sales analysis and store performance tracking

**Key Metrics**:
- Total Revenue: $2.5M - $3M
- Units Sold: 45K - 50K items
- Average Order Value (AOV): $55 - $65
- Growth Rate: 15-25% YoY
- Store Count: 8-10 locations across regions

**Visualizations**:
1. **Geographic Sales Map** - Revenue by store location with bubble size
2. **Category Performance Bar Chart** - Boys/Girls/Infants/Accessories revenue comparison
3. **Seasonal Trends Line Chart** - Monthly sales patterns with forecasting
4. **Store Comparison Matrix** - Top/bottom performers with drill-down
5. **Product Performance Heatmap** - Size × Season × Category analysis
6. **KPI Dashboard Cards** - Real-time metrics with sparklines

**Filters**: Date Range, Region, Store, Category, Season

---

### Module 2: Customer Analytics Dashboard
**Purpose**: Customer behavior analysis and segmentation insights

**Key Metrics**:
- Total Customers: 8K - 10K
- Repeat Purchase Rate: 35-45%
- Customer Lifetime Value (CLV): $180 - $220
- Churn Rate: 18-25%
- Average Purchase Frequency: 2.8 - 3.5 times/year

**Visualizations**:
1. **RFM Segmentation Scatter Plot** - Recency vs Frequency vs Monetary value
2. **Customer Cohort Analysis** - Retention heatmap by signup month
3. **Geographic Distribution Map** - Customer density by city/region
4. **Age Group Donut Chart** - Parent demographics (18-25, 26-35, 36-45, 46+)
5. **Purchase Behavior Timeline** - Average days between purchases
6. **Customer Segments Table** - Champions, Loyal, At-Risk, Lost categories

**Segments**:
- Champions (20%): High RFM scores
- Loyal Customers (25%): Regular purchasers
- Potential Loyalists (18%): Recent high-value buyers
- At Risk (15%): Decreasing frequency
- Lost Customers (12%): No purchase in 6+ months
- Others (10%)

---

### Module 3: Inventory & Supply Chain Dashboard
**Purpose**: Stock management and supplier performance optimization

**Key Metrics**:
- Total SKUs: 850 - 950
- Stock Value: $1.2M - $1.5M
- Stockout Rate: 3-5%
- Inventory Turnover: 4.5 - 5.5x per year
- Average Lead Time: 15-25 days

**Visualizations**:
1. **Stock Level Gauge Charts** - Current vs optimal by category
2. **Reorder Alert Table** - Items below reorder point (highlighted red)
3. **Supplier Performance Scorecard** - On-time delivery, defect rate, cost
4. **Warehouse Capacity Bar Chart** - Utilization by location
5. **Lead Time Analysis Box Plot** - Supplier comparison
6. **Slow-Moving Inventory List** - Items with <1x turnover

**Alerts**:
- Critical Stock (<10 units): Red
- Low Stock (10-30 units): Orange
- Optimal Stock: Green

---

### Module 4: Executive Summary Dashboard
**Purpose**: High-level KPIs and strategic insights for leadership

**Key Metrics**:
- Gross Margin: 42-48%
- Net Profit Margin: 12-18%
- Operating Expenses: 30-35% of revenue
- EBITDA: $450K - $550K
- Market Share: 8-12% (regional)

**Visualizations**:
1. **Financial Summary Cards** - Revenue, Profit, Margin, Expenses
2. **Trend Analysis Dual-Axis Chart** - Revenue vs Profit over time
3. **Category Contribution Treemap** - Revenue by category with hierarchy
4. **YoY Comparison Bar Chart** - Current vs previous year metrics
5. **Forecast Line Chart** - 6-month revenue prediction with confidence bands
6. **KPI Scorecards** - Traffic light indicators (Green/Yellow/Red)

**Time Periods**: Daily, Weekly, Monthly, Quarterly, Yearly

---

### Module 5: E-commerce Analytics Dashboard
**Purpose**: Online sales funnel and digital performance tracking

**Key Metrics**:
- Website Traffic: 120K - 150K visitors/month
- Conversion Rate: 2.8-3.5%
- Cart Abandonment Rate: 65-72%
- Online Revenue Share: 40-45% of total
- Average Session Duration: 4.5 - 6 minutes

**Visualizations**:
1. **Conversion Funnel Chart** - Homepage → Product → Cart → Checkout → Purchase
2. **Traffic Source Pie Chart** - Organic, Paid, Social, Direct, Referral
3. **Product Page Performance Table** - Views, Add-to-Cart rate, Purchase rate
4. **Cart Abandonment Analysis** - Reasons breakdown (shipping cost, payment issues, etc.)
5. **Customer Journey Sankey Diagram** - Path from entry to conversion
6. **Device Performance Comparison** - Desktop vs Mobile vs Tablet

**Key Insights**:
- Mobile traffic: 55-60%
- Peak hours: 8-10 PM
- Highest converting category: Accessories
- Average cart value: $75-85

---

## 📁 PROJECT STRUCTURE

```
03_Kids_Clothing_Insights/
│
├── data/
│   ├── raw/
│   │   ├── sales_transactions.csv           (50K+ rows)
│   │   ├── customers.csv                    (10K rows)
│   │   ├── products.csv                     (900 rows)
│   │   ├── inventory.csv                    (900 rows)
│   │   ├── stores.csv                       (10 rows)
│   │   ├── suppliers.csv                    (15 rows)
│   │   └── web_analytics.csv               (200K+ rows)
│   │
│   └── processed/
│       ├── sales_summary.csv
│       ├── customer_rfm.csv
│       ├── inventory_alerts.csv
│       ├── executive_kpis.csv
│       └── ecommerce_funnel.csv
│
├── scripts/
│   ├── 01_generate_data.py                  (Data generation)
│   ├── 02_sales_analysis.py                 (Sales metrics)
│   ├── 03_customer_segmentation.py          (RFM analysis)
│   ├── 04_inventory_management.py           (Stock calculations)
│   ├── 05_executive_summary.py              (KPI aggregation)
│   └── 06_ecommerce_analysis.py            (Funnel analysis)
│
├── tableau/
│   ├── Kids_Clothing_Analytics.twbx         (Packaged workbook)
│   ├── dashboard_screenshots/
│   │   ├── 01_sales_performance.png
│   │   ├── 02_customer_analytics.png
│   │   ├── 03_inventory_supply.png
│   │   ├── 04_executive_summary.png
│   │   └── 05_ecommerce_analytics.png
│   └── story_presentation.png
│
├── notebooks/
│   └── Exploratory_Analysis.ipynb           (Data exploration)
│
├── documentation/
│   ├── Data_Dictionary.md
│   ├── Business_Requirements.md
│   ├── Tableau_Usage_Guide.md
│   └── Insights_Report.pdf
│
├── README.md
└── MASTER_PROMPT.md (this file)
```

---

## 🎨 TABLEAU DESIGN SPECIFICATIONS

### Color Palette (Kids Clothing Theme)
- **Primary**: #FF6B9D (Pink) - Girls category
- **Secondary**: #4A90E2 (Blue) - Boys category
- **Accent 1**: #FFC845 (Yellow) - Infants category
- **Accent 2**: #9B59B6 (Purple) - Accessories
- **Neutral**: #34495E (Dark Gray) - Text
- **Background**: #F7F9FB (Light Gray)
- **Success**: #2ECC71 (Green) - Positive metrics
- **Warning**: #F39C12 (Orange) - Alerts
- **Danger**: #E74C3C (Red) - Critical alerts

### Dashboard Layout
- **Navigation**: Top horizontal tab bar with icons
- **Filters**: Left sidebar (consistent across all dashboards)
- **Main Content**: Center area (1200px × 800px optimal)
- **KPI Cards**: Top row (4-6 cards)
- **Charts**: Grid layout (2×2 or 3×2)
- **Footer**: Data source info and last updated timestamp

### Interactive Features
1. **Cross-filtering**: Click any chart to filter others
2. **Drill-down**: Category → Subcategory → Product
3. **Tooltips**: Rich tooltips with mini-charts
4. **Parameters**: Dynamic date ranges, targets, thresholds
5. **Actions**: Filter, Highlight, URL actions to details
6. **Story Points**: 8-10 guided narrative slides

---

## 📈 DATA GENERATION REQUIREMENTS

### Sales Transactions (50K rows)
- **Date Range**: Jan 2023 - Dec 2024 (2 years)
- **Columns**: TransactionID, Date, StoreID, ProductID, CustomerID, Quantity, UnitPrice, TotalAmount, PaymentMethod, Channel (Online/Offline)
- **Patterns**: 
  - Seasonal peaks: Back-to-school (Aug-Sep), Holidays (Nov-Dec)
  - Weekend spikes: 30% higher than weekdays
  - Clearance periods: End of season discounts (20-40% off)

### Customers (10K rows)
- **Columns**: CustomerID, Name, Email, City, State, ZipCode, SignupDate, Age, Gender, TotalSpend, PurchaseCount, LastPurchaseDate
- **Segments**: Generate realistic RFM distributions
- **Geography**: Focus on US major cities (NY, LA, Chicago, Houston, Miami)

### Products (900 rows)
- **Categories**: 
  - Boys Clothing (250 items): Shirts, Pants, Shorts, Jackets
  - Girls Clothing (300 items): Dresses, Tops, Skirts, Leggings
  - Infants (200 items): Onesies, Sleepwear, Rompers
  - Accessories (150 items): Shoes, Hats, Bags, Socks
- **Attributes**: ProductID, Name, Category, Subcategory, Size (0-3M, 3-6M, 6-12M, 1T-6T, 7-14), Season, Color, Cost, Price, Brand
- **Price Range**: $8-$65

### Inventory (900 rows)
- **Columns**: ProductID, WarehouseID, StockLevel, ReorderPoint, LeadTime, SupplierID, LastRestocked
- **Logic**: Calculate based on sales velocity and safety stock

### Web Analytics (200K rows)
- **Columns**: SessionID, Date, Time, Page, Action (View/AddCart/Purchase), ProductID, CustomerID, DeviceType, TrafficSource, Duration
- **Funnel**: Homepage (100K) → Product Page (60K) → Cart (20K) → Checkout (8K) → Purchase (3.5K)

---

## 🎯 KEY INSIGHTS TO HIGHLIGHT

### Sales Performance
1. Girls clothing generates 38% of revenue (highest category)
2. Store #3 (New York) is top performer: $520K annual revenue
3. Q4 accounts for 35% of annual sales (holiday season)
4. Average basket size increased 12% YoY

### Customer Analytics
1. 23% of customers are Champions (top 20% revenue)
2. Repeat customers have 3.2x higher CLV than one-time buyers
3. Customer acquisition cost: $28, Average CLV: $198 (7:1 ratio)
4. Email marketing has 18% conversion rate (highest channel)

### Inventory Management
1. Inventory turnover: 5.2x (healthy for fashion retail)
2. 15 SKUs critically low stock (need immediate reorder)
3. Supplier "ABC Textiles" has 96% on-time delivery (best performer)
4. $180K in slow-moving inventory (>120 days old)

### Executive Summary
1. Gross margin improved from 44% to 47% YoY
2. Operating expenses decreased 3% through efficiency gains
3. Projected Q1 2025 revenue: $680K (+18% growth)
4. Market share increased from 9.2% to 11.5%

### E-commerce Analytics
1. 68% cart abandonment due to shipping costs
2. Mobile drives 58% of traffic but only 42% of revenue
3. Product pages with videos have 25% higher conversion
4. Organic search is #1 traffic source (42%)

---

## 🚀 TABLEAU DASHBOARD FEATURES

### Dashboard 1: Sales Performance
- **Size**: 1200×800px
- **Layout**: KPI cards (top) + Map (left) + Charts (right)
- **Interactions**: Click store on map to filter all charts
- **Parameters**: Date range, Category filter, Store type
- **Highlight**: Top 3 stores with green border

### Dashboard 2: Customer Analytics
- **Size**: 1200×800px
- **Layout**: Segmentation scatter (center) + Supporting charts (sides)
- **Interactions**: Hover on segment to show details, click to drill-down
- **Calculated Fields**: RFM_Score, Customer_Segment, CLV
- **Color Coding**: Segments by value (Champions = Gold, Lost = Gray)

### Dashboard 3: Inventory & Supply Chain
- **Size**: 1200×800px
- **Layout**: Stock gauges (top) + Alerts table (left) + Supplier chart (right)
- **Interactions**: Red alerts clickable for reorder workflow
- **Conditional Formatting**: Stock levels (Red/Orange/Green)
- **Parameters**: Reorder threshold adjustment

### Dashboard 4: Executive Summary
- **Size**: 1200×800px
- **Layout**: Financial cards (top) + Trend chart (center) + Comparisons (bottom)
- **Interactions**: Click time period to update all metrics
- **Forecast**: 6-month prediction with 95% confidence interval
- **Export**: Formatted for executive reports

### Dashboard 5: E-commerce Analytics
- **Size**: 1200×800px
- **Layout**: Funnel (center) + Traffic sources (left) + Device stats (right)
- **Interactions**: Click funnel stage to see drop-off reasons
- **Tooltips**: Show sample product page URLs
- **Parameters**: Date comparison (This week vs Last week)

---

## 📝 DOCUMENTATION REQUIREMENTS

### README.md
- Project overview with business context
- Dataset description and statistics
- Tableau dashboard walkthrough (with screenshots)
- Key findings and recommendations
- Technologies used
- How to open and use the Tableau workbook
- Contact information

### Data_Dictionary.md
- Complete schema for all 7 datasets
- Column names, data types, descriptions
- Sample values and constraints
- Relationships between tables

### Business_Requirements.md
- Problem statement
- Stakeholder needs (Sales team, Marketing, Operations, Executives)
- Success criteria
- Assumptions and limitations

### Tableau_Usage_Guide.md
- How to navigate dashboards
- Filter usage instructions
- Interactive features explanation
- Exporting reports
- Troubleshooting common issues

---

## ✅ COMPLETION CHECKLIST

### Phase 1: Data Generation ✅
- [ ] Generate sales transactions (50K rows)
- [ ] Generate customer data (10K rows)
- [ ] Generate product catalog (900 rows)
- [ ] Generate inventory data
- [ ] Generate supplier data
- [ ] Generate web analytics (200K rows)
- [ ] Validate data quality and relationships

### Phase 2: Python Analysis ✅
- [ ] Sales performance analysis script
- [ ] Customer RFM segmentation script
- [ ] Inventory management calculations
- [ ] Executive KPI aggregation
- [ ] E-commerce funnel analysis
- [ ] Export processed CSV files

### Phase 3: Tableau Development ✅
- [ ] Create data connections
- [ ] Build Sales Performance dashboard
- [ ] Build Customer Analytics dashboard
- [ ] Build Inventory & Supply Chain dashboard
- [ ] Build Executive Summary dashboard
- [ ] Build E-commerce Analytics dashboard
- [ ] Add navigation and filters
- [ ] Create Story presentation
- [ ] Package workbook (.twbx)
- [ ] Export dashboard screenshots

### Phase 4: Documentation ✅
- [ ] Write comprehensive README.md
- [ ] Create Data Dictionary
- [ ] Document business requirements
- [ ] Write Tableau usage guide
- [ ] Generate insights report PDF

### Phase 5: GitHub Upload ✅
- [ ] Initialize git repository
- [ ] Commit all files
- [ ] Push to GitHub
- [ ] Verify file structure
- [ ] Test links and images

---

## 🎓 SKILLS DEMONSTRATED

1. **Data Engineering**: Multi-source data generation with realistic patterns
2. **Business Intelligence**: Tableau dashboard design and development
3. **Analytics**: Sales, Customer, Inventory, Financial analysis
4. **Data Visualization**: 30+ chart types with best practices
5. **Storytelling**: Narrative-driven insights presentation
6. **Domain Knowledge**: Retail fashion industry expertise
7. **Python Programming**: Pandas, NumPy for data processing
8. **Documentation**: Comprehensive technical and business docs

---

## 📞 PROJECT METADATA

**Client**: Portfolio Project  
**Developer**: Nitin DB  
**Timeline**: 1-2 days  
**Complexity**: Advanced (Multiple integrated modules)  
**Audience**: Hiring managers, clients looking for BI expertise  
**Deliverables**: Tableau workbook + Python scripts + Documentation + GitHub repo

---

*This master prompt serves as the complete blueprint for Project 3. Follow all specifications to ensure consistency and professionalism.*
