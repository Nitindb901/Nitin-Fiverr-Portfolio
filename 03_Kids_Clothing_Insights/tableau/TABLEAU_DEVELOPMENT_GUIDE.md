# 📊 Tableau Dashboard Development Guide

## Kids Clothing Insights - Enterprise Analytics Hub

**Step-by-Step Instructions to Build All 5 Dashboards**

---

## 🎯 Quick Start

### Prerequisites
- ✅ Tableau Desktop 2023.1+ installed
- ✅ All processed CSV files (in `data/processed/` folder)
- ✅ This guide for reference

### Time Estimate
- **Dashboard 1 (Sales)**: 2 hours
- **Dashboard 2 (Customer)**: 2.5 hours
- **Dashboard 3 (Inventory)**: 2 hours
- **Dashboard 4 (Executive)**: 1.5 hours
- **Dashboard 5 (E-commerce)**: 2 hours
- **Total**: ~10 hours for all 5 dashboards

---

## 📂 Step 1: Connect Data Sources

### Connect All CSV Files

1. **Open Tableau Desktop**
2. Click **"Connect"** → **"Text file"**
3. Navigate to: `03_Kids_Clothing_Insights/data/processed/`
4. Select and connect these files:

**For Sales Dashboard:**
- `sales_summary.csv`
- `category_performance.csv`
- `store_performance.csv`
- `monthly_trends.csv`
- `seasonal_performance.csv`
- `top_products.csv`
- `channel_performance.csv`
- `payment_analysis.csv`
- `regional_performance.csv`

**For Customer Dashboard:**
- `customer_rfm.csv`
- `customer_segments.csv`
- `clv_by_segment.csv`
- `customer_geography.csv`
- `customer_demographics_age.csv`
- `customer_demographics_gender.csv`
- `cohort_analysis.csv`
- `repeat_customer_analysis.csv`

**For Inventory Dashboard:**
- `reorder_alerts.csv`
- `inventory_turnover.csv`
- `supplier_performance.csv`
- `warehouse_analysis.csv`
- `category_inventory.csv`
- `stock_status_summary.csv`
- `days_of_inventory.csv`
- `stock_age_analysis.csv`
- `slow_moving_inventory.csv`

**For Executive Dashboard:**
- `financial_summary.csv`
- `kpi_summary.csv`
- `yearly_comparison.csv`
- `quarterly_performance.csv`
- `category_financial.csv`
- `channel_financial.csv`
- `monthly_profitability.csv`
- `revenue_forecast.csv`
- `executive_scorecard.csv`

**For E-commerce Dashboard:**
- `conversion_funnel.csv`
- `traffic_source_analysis.csv`
- `device_analysis.csv`
- `product_page_performance.csv`
- `hourly_traffic.csv`
- `dow_traffic.csv`
- `online_category_performance.csv`
- `cart_abandonment_reasons.csv`
- `customer_journey_summary.csv`

4. **Create Relationships** (if needed):
   - Most files are already pre-aggregated
   - No complex joins needed for V1.0

---

## 🛍️ Dashboard 1: Sales Performance

### Layout Structure
```
+--------------------------------------------------+
|  FILTERS: Date Range | Category | Store | Region |
+--------------------------------------------------+
|  KPI CARDS: Revenue | Transactions | AOV | Units |
+--------------------------------------------------+
|                    |                              |
|   GEOGRAPHIC MAP   |   CATEGORY BAR CHART         |
|   (Store bubbles)  |   (Revenue by Category)      |
|                    |                              |
+--------------------+------------------------------+
|                                                   |
|        MONTHLY TREND LINE CHART                   |
|        (Revenue over Time with Seasonality)       |
|                                                   |
+---------------------------------------------------+
|  STORE TABLE  |  CHANNEL PIE  |  PAYMENT BARS    |
+---------------------------------------------------+
```

### Step-by-Step Build

#### 1.1 Create KPI Cards (Top Row)

**Total Revenue Card:**
1. Drag `sales_summary.csv` to canvas
2. Drag `TotalRevenue` to **Text**
3. Format: Number → Currency → $ prefix → 2 decimals
4. Customize: Font size 36px, Bold, Color #667eea
5. Add label: "Total Revenue"
6. Duplicate for: Transactions, AOV, Unique Customers

**KPI Card Colors:**
- Revenue: #667eea (Purple)
- Transactions: #4A90E2 (Blue)
- AOV: #FFC845 (Yellow)
- Customers: #FF6B9D (Pink)

#### 1.2 Geographic Sales Map

**Data Source:** `regional_performance.csv` + `store_performance.csv`

1. Create new worksheet: "Sales Map"
2. Drag `store_performance.csv` to canvas
3. Drag `City` to **Detail** (Tableau will geocode automatically)
4. Drag `TotalRevenue` to **Size** (creates bubbles)
5. Drag `TotalRevenue` to **Color**
6. **Color Scale**: Blue-Green gradient (low to high)
7. **Tooltip**: 
   ```
   <b><ATTR(StoreName)></b>
   City: <ATTR(City)>
   Revenue: $<SUM(TotalRevenue)>
   Transactions: <SUM(Transactions)>
   AOV: $<AVG(AvgOrderValue)>
   ```
8. Add filter: Region (multi-select dropdown)
9. **Map Style**: Normal (or Light for clean look)

**Interactivity:**
- Enable **Highlight**: Hover to highlight store
- Enable **Filter Action**: Click to filter entire dashboard

#### 1.3 Category Performance Bar Chart

**Data Source:** `category_performance.csv`

1. Create new worksheet: "Category Performance"
2. Drag `Category` to **Rows**
3. Drag `TotalRevenue` to **Columns**
4. **Sort**: Descending by Revenue
5. **Color**: By Category
   - Girls Clothing: #FF6B9D (Pink)
   - Boys Clothing: #4A90E2 (Blue)
   - Infants: #FFC845 (Yellow)
   - Accessories: #9B59B6 (Purple)
6. Add **Labels**: Show revenue values on bars
7. **Tooltip**:
   ```
   <b><ATTR(Category)></b>
   Revenue: $<SUM(TotalRevenue)>
   Share: <SUM(RevenueShare)>%
   Transactions: <SUM(Transactions)>
   Avg Order Value: $<AVG(AvgOrderValue)>
   ```

**Formatting:**
- Bar thickness: Adjust in Format → Worksheet → Size
- Font: Arial, 11pt
- Grid lines: Hide vertical lines

#### 1.4 Monthly Trend Line Chart

**Data Source:** `monthly_trends.csv`

1. Create new worksheet: "Monthly Trends"
2. Convert `Year` and `Month` to **Date**:
   - Create calculated field: `MAKEDATE([Year], [Month], 1)`
   - Name it: `Date`
3. Drag `Date` to **Columns**
4. Drag `TotalRevenue` to **Rows**
5. **Mark Type**: Line
6. **Color**: #667eea (Purple)
7. **Line Thickness**: 3px
8. Add **Trend Line**: Analysis → Trend Lines → Show Trend Lines
9. Add **Reference Line** for average: Analytics → Reference Line → Average
10. **Tooltip**:
    ```
    <b><MONTHYEAR(Date)></b>
    Revenue: $<SUM(TotalRevenue)>
    Transactions: <SUM(Transactions)>
    Growth: <SUM(GrowthRate)>%
    ```

**Annotations:**
- Add annotation for Summer peak: Right-click July → Annotate → Point
- Text: "Summer Peak: $427K"

#### 1.5 Store Ranking Table

**Data Source:** `store_performance.csv`

1. Create new worksheet: "Store Rankings"
2. Drag `StoreName` to **Rows**
3. Drag these to **Columns**:
   - `RevenueRank` (number format)
   - `TotalRevenue` (currency format)
   - `Transactions` (number format)
   - `AvgOrderValue` (currency format)
4. **Sort**: By Rank ascending
5. **Color**: Apply gradient to Revenue column (green = high)
6. **Top 10 Only**: Filter → RevenueRank → Top → 10

**Table Styling:**
- Header background: #f8f9fa
- Alternating row colors: #ffffff and #f8f9fa
- Borders: Light gray (#e0e0e0)

#### 1.6 Channel Split Pie Chart

**Data Source:** `channel_performance.csv`

1. Create new worksheet: "Channel Distribution"
2. Drag `Channel` to **Color**
3. Drag `TotalRevenue` to **Angle**
4. **Mark Type**: Pie
5. **Colors**:
   - Online: #4A90E2 (Blue)
   - Offline: #FF6B9D (Pink)
6. **Labels**: Show percentage (42% / 58%)
7. **Tooltip**:
   ```
   <b><ATTR(Channel)></b>
   Revenue: $<SUM(TotalRevenue)>
   Share: <SUM(RevenueShare)>%
   AOV: $<AVG(AvgOrderValue)>
   ```

#### 1.7 Payment Method Bars

**Data Source:** `payment_analysis.csv`

1. Create new worksheet: "Payment Methods"
2. Drag `PaymentMethod` to **Rows**
3. Drag `Share` (percentage) to **Columns**
4. **Sort**: Descending
5. **Color**: Single color #9B59B6 (Purple)
6. **Labels**: Show percentage

#### 1.8 Assemble Dashboard

1. **Dashboard → New Dashboard**
2. **Size**: Fixed size 1920x1080 (or Automatic for responsive)
3. **Layout**:
   - Top: Horizontal container with filters
   - Row 2: Horizontal container with 4 KPI cards
   - Row 3: Horizontal container with Map (60%) and Category chart (40%)
   - Row 4: Full-width Monthly Trend chart
   - Row 5: 3 containers (Store table, Channel pie, Payment bars) - 40/30/30 split
4. **Padding**: 10px between all objects
5. **Background**: #ffffff (white)
6. **Title**: "Sales Performance Dashboard" - Font: Arial 24px Bold

**Interactivity:**
1. Add **Filter Actions**:
   - Map → Filters entire dashboard by store
   - Category chart → Filters by category
2. Add **Highlight Actions**:
   - Hover on any chart highlights related data
3. Add **URL Actions**:
   - Click store → Opens Google Maps (optional)

**Filters (Make visible):**
- Date Range (relative date filter: Last 12 months)
- Category (multi-select dropdown)
- Store (multi-select dropdown)
- Region (multi-select dropdown)

---

## 👥 Dashboard 2: Customer Analytics

### Layout Structure
```
+--------------------------------------------------+
|  FILTERS: Segment | Region | CLV Range | Date    |
+--------------------------------------------------+
|  KPI CARDS: Total Customers | Avg CLV | Repeat % |
+--------------------------------------------------+
|                          |                        |
|  RFM SCATTER PLOT        |  SEGMENT PIE CHART     |
|  (Recency vs Frequency)  |  (10 Segments)         |
|                          |                        |
+--------------------------+------------------------+
|                                                   |
|  COHORT RETENTION HEATMAP                         |
|  (Month vs Months Since Signup)                   |
|                                                   |
+---------------------------------------------------+
|  GEOGRAPHIC  |  CLV BY SEGMENT  |  DEMOGRAPHICS   |
|  HEATMAP     |  BAR CHART       |  BREAKDOWN      |
+---------------------------------------------------+
```

### Step-by-Step Build

#### 2.1 KPI Cards

**Data Source:** `customer_segments.csv` aggregated

1. **Total Customers**: COUNT(DISTINCT [CustomerID])
2. **Average CLV**: AVG([CLV]) - Format: $429.80
3. **Repeat Rate**: 92.5% (from `repeat_customer_analysis.csv`)
4. **Active Segments**: COUNT(DISTINCT [Segment])

#### 2.2 RFM Scatter Plot

**Data Source:** `customer_rfm.csv`

1. Create worksheet: "RFM Analysis"
2. Drag `Recency` to **Columns** (reverse scale: low = right)
3. Drag `Frequency` to **Rows**
4. Drag `CustomerID` to **Detail** (one dot per customer)
5. Drag `Monetary` to **Size** (bigger = higher spend)
6. Drag `Segment` to **Color**
7. **Color Palette**:
   - Champions: #27AE60 (Green)
   - Loyal: #2ECC71 (Light Green)
   - Potential Loyalists: #F39C12 (Orange)
   - Need Attention: #E67E22 (Dark Orange)
   - At Risk: #E74C3C (Red)
   - Lost: #C0392B (Dark Red)
   - Others: #95A5A6 (Gray)
8. **Transparency**: 70% (to see overlapping points)
9. **Tooltip**:
   ```
   Customer: <ATTR(CustomerID)>
   Segment: <ATTR(Segment)>
   Recency: <SUM(Recency)> days
   Frequency: <SUM(Frequency)> purchases
   Monetary: $<SUM(Monetary)>
   CLV: $<SUM(CLV)>
   ```

**Add Quadrant Lines:**
1. Add **Reference Line** on Recency: Average
2. Add **Reference Line** on Frequency: Average
3. Creates 4 quadrants for visual segmentation

#### 2.3 Customer Segment Pie Chart

**Data Source:** `customer_segments.csv` aggregated

1. Create worksheet: "Segment Distribution"
2. Drag `Segment` to **Color**
3. Drag `CustomerCount` (calculated: COUNT(CustomerID)) to **Angle**
4. **Mark Type**: Pie
5. **Sort**: By size descending
6. **Labels**: Show segment name and percentage
7. **Colors**: Same as scatter plot
8. **Tooltip**:
   ```
   <b><ATTR(Segment)></b>
   Customers: <COUNT(CustomerID)>
   Percentage: <Calculated %>
   Avg CLV: $<AVG(CLV)>
   Total Value: $<SUM(CLV)>
   ```

#### 2.4 Cohort Retention Heatmap

**Data Source:** `cohort_analysis.csv`

1. Create worksheet: "Cohort Retention"
2. Drag `SignupMonth` to **Rows**
3. Create calculated fields for each month column:
   - `Month_0`, `Month_1`, ... `Month_12`
4. Use **Measure Values** and **Measure Names**
5. Drag measure to **Columns**
6. Drag values to **Color**
7. **Color Scale**: Red-Yellow-Green diverging
   - 100% = Dark Green
   - 50% = Yellow
   - 0% = Red
8. **Mark Type**: Square
9. **Labels**: Show percentage in each cell
10. **Tooltip**:
    ```
    Cohort: <MONTHYEAR(SignupMonth)>
    Months Since Signup: <ATTR(Measure Names)>
    Retention: <SUM(Measure Values)>%
    ```

**Formatting:**
- Cell borders: White, 2px
- Text: White for dark cells, Black for light cells

#### 2.5 Geographic Customer Heatmap

**Data Source:** `customer_geography.csv`

1. Create worksheet: "Customer Geography"
2. Drag `City` and `State` to **Detail** (geocode)
3. Drag `CustomerCount` to **Color**
4. **Map Type**: Filled Map (state-level) or Symbol Map (city-level)
5. **Color**: Blue gradient (light to dark)
6. **Tooltip**:
   ```
   <b><ATTR(City)>, <ATTR(State)></b>
   Customers: <SUM(CustomerCount)>
   Revenue: $<SUM(TotalRevenue)>
   Avg CLV: $<AVG(AvgCLV)>
   ```

#### 2.6 CLV by Segment Bar Chart

**Data Source:** `clv_by_segment.csv`

1. Create worksheet: "CLV by Segment"
2. Drag `Segment` to **Rows**
3. Drag `AvgCLV` to **Columns**
4. **Sort**: Descending by CLV
5. **Color**: By segment (same palette)
6. **Labels**: Show CLV values
7. Add **Reference Line**: Average CLV across all segments

#### 2.7 Demographics Breakdown

**Data Source:** `customer_demographics_age.csv` and `customer_demographics_gender.csv`

**Age Group Chart:**
1. Bar chart: Age Group vs Customer Count
2. Colors: Gradient blue

**Gender Chart:**
1. Pie chart: Gender distribution
2. Colors: Pink (Female), Blue (Male), Purple (Other)

#### 2.8 Assemble Dashboard

Similar to Sales dashboard, create layout with:
- Filters at top
- KPI cards row
- Main visualizations (scatter + pie)
- Cohort heatmap full width
- Bottom row: Geography, CLV bars, Demographics

---

## 📦 Dashboard 3: Inventory Management

### Layout Structure
```
+--------------------------------------------------+
|  FILTERS: Category | Warehouse | Status | Stock  |
+--------------------------------------------------+
|  GAUGES: Critical | Low | Normal (Stock Status)  |
+--------------------------------------------------+
|                          |                        |
|  REORDER ALERTS TABLE    |  SUPPLIER SCORECARD    |
|  (Priority sorted)       |  (Top 5 + Bottom 5)    |
|                          |                        |
+--------------------------+------------------------+
|  INVENTORY TURNOVER      |  WAREHOUSE UTILIZATION |
|  (Fast/Regular/Slow)     |  (Stock Value by WH)   |
+--------------------------+------------------------+
|                                                   |
|  STOCK AGE ANALYSIS (Bar Chart)                   |
|                                                   |
+---------------------------------------------------+
```

### Key Visualizations

#### 3.1 Stock Status Gauges

**Data Source:** `stock_status_summary.csv`

1. Create 3 **Bullet Graphs** (one per status: Critical, Low, Normal)
2. Show count of products in each status
3. Color coding: Red (Critical), Yellow (Low), Green (Normal)
4. Add target lines for acceptable thresholds

#### 3.2 Reorder Alerts Table

**Data Source:** `reorder_alerts.csv`

1. Columns: Product Name, Category, Current Stock, Reorder Point, Qty Needed, Cost
2. Sort by Priority (Critical first)
3. Conditional formatting:
   - Critical rows: Light red background
   - Low rows: Light yellow background
4. Add **SUM of Reorder Cost** at bottom

#### 3.3 Supplier Performance Scorecard

**Data Source:** `supplier_performance.csv`

1. Table with columns: Rank, Supplier, Score, On-Time %, Defect %, Lead Time
2. Sort by Score descending
3. Conditional formatting:
   - Score > 0.85: Green
   - Score 0.75-0.85: Yellow
   - Score < 0.75: Red
4. Show Top 5 and Bottom 5 only

#### 3.4 Inventory Turnover

**Data Source:** `inventory_turnover.csv`

1. Stacked bar chart: Category vs Product Count
2. Stack by: Fast-moving, Regular, Slow, Dead
3. Colors: Green, Blue, Orange, Red
4. Labels: Show count in each segment

#### 3.5 Warehouse Utilization

**Data Source:** `warehouse_analysis.csv`

1. Horizontal bar chart: Warehouse vs Stock Value
2. Color by value (gradient)
3. Show percentage of total

#### 3.6 Stock Age Analysis

**Data Source:** `stock_age_analysis.csv`

1. Bar chart: Age Category (0-30, 31-60, 61-90, 90+) vs Product Count
2. Color gradient: Green to Red (older = redder)
3. Add labels for percentages

---

## 💼 Dashboard 4: Executive Summary

### Layout Structure
```
+--------------------------------------------------+
|  FILTERS: Date Range | Comparison Period         |
+--------------------------------------------------+
|  KPI CARDS: Revenue | Gross Margin | Net Margin  |
|             | EBITDA | Inventory Turnover | CLV  |
+--------------------------------------------------+
|                          |                        |
|  P&L WATERFALL CHART     |  EXECUTIVE SCORECARD   |
|  (Revenue to Net Profit) |  (Traffic Lights)      |
|                          |                        |
+--------------------------+------------------------+
|  YOY COMPARISON BARS     |  QUARTERLY TREND LINE  |
+--------------------------+------------------------+
|                                                   |
|  REVENUE FORECAST (with Confidence Bands)         |
|                                                   |
+---------------------------------------------------+
```

### Key Visualizations

#### 4.1 KPI Cards (8 cards)

**Data Source:** `kpi_summary.csv` and `financial_summary.csv`

1. Total Revenue: $1,956,784
2. Gross Margin: 45.23%
3. Net Margin: 11.43%
4. EBITDA: $337,235
5. Inventory Turnover: 7.03x
6. Transactions: 50,000
7. AOV: $39.14
8. CLV/CAC: 22.62x

**Color Coding:**
- Green: Exceeds target
- Red: Below target

#### 4.2 P&L Waterfall Chart

**Data Source:** `financial_summary.csv`

1. Create calculated field for each P&L line:
   - Starting: Revenue
   - Decrease: COGS (negative)
   - Subtotal: Gross Profit
   - Decrease: Operating Expenses (negative)
   - Subtotal: Operating Profit
   - Decrease: Taxes (negative)
   - Total: Net Profit
2. **Mark Type**: Gantt Bar (creates waterfall effect)
3. Colors: Green (positive), Red (negative), Blue (subtotals)
4. Add labels on each bar

**Tableau Waterfall:**
1. Drag measure to Columns
2. Right-click → Quick Table Calculation → Running Total
3. Drag same measure to Size (creates bar)
4. Customize colors and labels

#### 4.3 Executive Scorecard

**Data Source:** `executive_scorecard.csv`

1. Create **KPI Table** with columns:
   - KPI Name
   - Current Value
   - Target Value
   - Status (shape)
2. Use **Shapes** for status:
   - Green circle: ● (Exceeds target)
   - Red circle: ● (Below target)
3. Conditional formatting on variance

**Custom Shapes:**
- Use Unicode symbols: ● (circle)
- Or custom shape files (traffic lights)

#### 4.4 YoY Comparison Bars

**Data Source:** `yearly_comparison.csv`

1. Grouped bar chart: Year (2023, 2024) vs Revenue
2. Side-by-side bars
3. Colors: Light blue (2023), Dark blue (2024)
4. Add labels showing growth percentage

#### 4.5 Quarterly Performance Trend

**Data Source:** `quarterly_performance.csv`

1. Line chart: Quarter vs Revenue
2. Two lines: 2023 (dotted), 2024 (solid)
3. Colors: Same as YoY chart
4. Add markers on data points

#### 4.6 Revenue Forecast

**Data Source:** `revenue_forecast.csv`

1. Area chart: Month vs Revenue
2. Three series:
   - Forecast (line)
   - Confidence Lower (area, light)
   - Confidence Upper (area, light)
3. Create **band** between upper and lower (shaded area)
4. Historical data: Solid line
5. Forecast data: Dashed line
6. Colors: Blue (historical), Purple (forecast), Light purple (confidence band)

**Tableau Forecast:**
1. Drag Date to Columns, Revenue to Rows
2. Analytics pane → Forecast → Show Forecast
3. Customize: 6 months ahead, 90% confidence interval

---

## 🌐 Dashboard 5: E-commerce Analytics

### Layout Structure
```
+--------------------------------------------------+
|  FILTERS: Date | Traffic Source | Device | Category|
+--------------------------------------------------+
|  KPI CARDS: Sessions | Conversion % | Cart Abandon%|
+--------------------------------------------------+
|                          |                        |
|  CONVERSION FUNNEL       |  TRAFFIC SOURCE PIE    |
|  (6 stages)              |  (with Conv Rates)     |
|                          |                        |
+--------------------------+------------------------+
|  DEVICE COMPARISON BARS  |  CART ABANDONMENT      |
|                          |  REASONS (Bar Chart)   |
+--------------------------+------------------------+
|  HOURLY HEATMAP          |  DAY-OF-WEEK HEATMAP   |
+--------------------------+------------------------+
|  PRODUCT PAGE PERFORMANCE TABLE                   |
+---------------------------------------------------+
```

### Key Visualizations

#### 5.1 KPI Cards

**Data Source:** `conversion_funnel.csv` aggregated

1. Total Sessions: 200,000
2. Conversion Rate: 1.76%
3. Cart Abandonment: 84.35%
4. Avg Pages/Session: 1.98
5. Avg Duration: 109s

#### 5.2 Conversion Funnel

**Data Source:** `conversion_funnel.csv`

**Method 1: Area Chart**
1. Create calculated field for each stage:
   - Homepage: 200,000
   - Category: 80,014
   - Product: 56,085
   - Cart: 22,456
   - Checkout: 7,271
   - Purchase: 3,515
2. Drag measure names to Columns
3. Drag measure values to Rows
4. **Mark Type**: Area
5. **Color**: Gradient (light to dark purple)
6. **Labels**: Show value and drop-off percentage

**Method 2: Funnel Chart (Extension)**
1. Download Funnel Chart extension from Tableau Exchange
2. Configure stages and values
3. Customize colors

**Annotations:**
- Add callouts for critical drop-off points (Cart: 60%, Checkout: 68%)

#### 5.3 Traffic Source Pie Chart

**Data Source:** `traffic_source_analysis.csv`

1. Pie chart: Traffic Source vs Sessions
2. Colors: Different color per source
3. **Labels**: Source name, percentage, conversion rate
4. **Tooltip**:
   ```
   <b><ATTR(TrafficSource)></b>
   Sessions: <SUM(Sessions)>
   Share: <Calculated %>
   Conversions: <SUM(Conversions)>
   Conv Rate: <SUM(ConversionRate)>%
   Revenue: $<SUM(Revenue)>
   ```

#### 5.4 Device Comparison Bars

**Data Source:** `device_analysis.csv`

1. Grouped bar chart: Metric (Sessions, Conv Rate, Revenue) vs Device
2. Side-by-side bars for Mobile, Desktop, Tablet
3. Colors: Pink (Mobile), Blue (Desktop), Purple (Tablet)
4. Dual axis: Sessions (left), Conv Rate (right)

#### 5.5 Cart Abandonment Reasons

**Data Source:** `cart_abandonment_reasons.csv`

1. Horizontal bar chart: Reason vs Percentage
2. Sort: Descending by percentage
3. Color: Single color (red/orange to indicate problem)
4. Labels: Show percentage
5. Add reference line for average

#### 5.6 Hourly Traffic Heatmap

**Data Source:** `hourly_traffic.csv`

1. Create heatmap: Hour (0-23) vs Day of Week
2. Color: Sessions (light to dark)
3. **Mark Type**: Square
4. **Labels**: Show session count
5. **Tooltip**: Add conversion rate

**Calculated Field for Day of Week:**
```
DATENAME('weekday', [Date])
```

#### 5.7 Day-of-Week Performance

**Data Source:** `dow_traffic.csv`

1. Bar chart: Day vs Conversion Rate
2. Add Sessions as secondary metric (dual axis)
3. Bars: Conv rate (blue), Line: Sessions (orange)
4. Sort: Mon-Sun (not alphabetically)

#### 5.8 Product Page Performance Table

**Data Source:** `product_page_performance.csv`

1. Table: Product Name, Page Views, Add-to-Cart Rate, Purchases, View-to-Purchase %
2. Sort by Page Views descending
3. Conditional formatting:
   - High add-to-cart rate (>50%): Green
   - Medium (30-50%): Yellow
   - Low (<30%): Red
4. Show top 20 products only

---

## 🎨 Global Design Guidelines

### Color Palette (Kids Clothing Theme)

**Primary Colors:**
- Pink: #FF6B9D (Girls)
- Blue: #4A90E2 (Boys)
- Yellow: #FFC845 (Infants)
- Purple: #9B59B6 (Accessories)

**Secondary Colors:**
- Light Gray: #F8F9FA (backgrounds)
- Dark Gray: #2C3E50 (text)
- Success Green: #27AE60
- Warning Orange: #F39C12
- Danger Red: #E74C3C

**Dashboard Background:**
- White (#FFFFFF) or Light Gray (#F8F9FA)

**Chart Backgrounds:**
- White with light gray borders

### Typography

**Fonts:**
- Titles: Arial Black, 24px
- Headers: Arial Bold, 14px
- Body: Arial, 11px
- Numbers: Arial, 12px

**Alignment:**
- Titles: Center
- Labels: Left
- Numbers: Right

### Spacing

- **Padding**: 10px between all objects
- **Margins**: 20px from dashboard edges
- **Gaps**: 5px between elements in containers

---

## 🔗 Cross-Dashboard Navigation

### Create Navigation Menu

1. **Create Text Object** with dashboard links:
   ```
   📊 Sales | 👥 Customers | 📦 Inventory | 💼 Executive | 🌐 E-commerce
   ```
2. Add **URL Actions** for each link:
   - Click "Sales" → Navigate to Sales dashboard
   - Click "Customers" → Navigate to Customer dashboard
   - etc.

### Add Home Button

1. Create **Image Object** with home icon
2. Add action: Click → Navigate to dashboard selection page

---

## 📤 Export & Package

### Create Dashboard Exports

1. **Export each dashboard to PNG**:
   - Dashboard → Export Image
   - Resolution: High (2x)
   - Save to: `tableau/dashboard_screenshots/`
   - Naming: `01_sales_performance.png`, `02_customer_analytics.png`, etc.

2. **Export to PDF**:
   - File → Print to PDF
   - Include: All dashboards
   - Scaling: Fit to Page

### Package Workbook

1. **File → Export Packaged Workbook (.twbx)**
2. Includes:
   - All data sources (embedded)
   - All worksheets and dashboards
   - Custom images/logos
3. Save as: `Kids_Clothing_Analytics.twbx`
4. Location: `tableau/` folder

---

## ✅ Final Checklist

Before considering dashboards complete:

**Data Connections:**
- [ ] All 47 CSV files connected
- [ ] No broken connections
- [ ] Data refreshes properly

**Visualizations:**
- [ ] All 5 dashboards created
- [ ] Each dashboard has 5-7 key visualizations
- [ ] Colors consistent with brand palette
- [ ] Tooltips informative and formatted

**Interactivity:**
- [ ] Filters working on all dashboards
- [ ] Click actions enable drill-down
- [ ] Highlight actions working
- [ ] Cross-dashboard navigation functional

**Performance:**
- [ ] Dashboards load in < 5 seconds
- [ ] No performance warnings
- [ ] Extracts optimized (if used)

**Documentation:**
- [ ] Screenshots captured (5 PNG files)
- [ ] Packaged workbook created (.twbx)
- [ ] README updated with screenshot links
- [ ] Usage guide reflects actual dashboards

**Quality Assurance:**
- [ ] No broken visualizations
- [ ] All numbers match source data
- [ ] Spelling/grammar checked
- [ ] Tested on different screen sizes
- [ ] Tested with sample filters

---

## 🎓 Learning Resources

**Tableau Tutorials:**
- Tableau Public Gallery: https://public.tableau.com/gallery
- Tableau Desktop Training: https://www.tableau.com/learn/training
- YouTube: Search "Tableau dashboard tutorial"

**Specific Techniques:**
- **Waterfall Charts**: https://www.tableau.com/learn/tutorials/waterfall-charts
- **Funnel Charts**: https://www.tableau.com/blog/quick-tip-funnel-charts
- **Heatmaps**: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_highlight.htm
- **Scatter Plots**: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_scatter.htm

---

## 💡 Pro Tips

1. **Use Containers**: Organize layout with horizontal/vertical containers
2. **Device Layouts**: Create separate layouts for Desktop/Tablet/Phone
3. **Tooltips**: Make them informative but not cluttered
4. **Performance**: Use extracts instead of live connections for large data
5. **Testing**: Test with edge cases (empty filters, extreme values)
6. **Accessibility**: Use colorblind-safe palettes, add text labels
7. **Version Control**: Save iterations (v1.0, v1.1) before major changes
8. **Feedback**: Share draft with stakeholders before finalizing

---

## 📞 Support

**Questions?**
- Refer to: `Tableau_Usage_Guide.md` for end-user help
- Tableau Community: https://community.tableau.com
- Project Owner: nitindb901@gmail.com

---

**Good luck building your dashboards!** 🚀

This guide provides step-by-step instructions to recreate all 5 dashboards in Tableau. Follow the sections in order for best results.

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Project**: Kids Clothing Insights - Enterprise Analytics Hub
