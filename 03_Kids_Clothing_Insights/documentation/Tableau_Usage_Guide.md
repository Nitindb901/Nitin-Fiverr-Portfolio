# 📊 Tableau Usage Guide

## Kids Clothing Insights - Enterprise Analytics Hub

**Version**: 1.0  
**Last Updated**: December 2024  
**For**: All Dashboard Users

---

## 📑 Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Navigation Guide](#navigation-guide)
4. [Dashboard Details](#dashboard-details)
   - [Sales Performance Dashboard](#1-sales-performance-dashboard)
   - [Customer Analytics Dashboard](#2-customer-analytics-dashboard)
   - [Inventory Management Dashboard](#3-inventory-management-dashboard)
   - [Executive Summary Dashboard](#4-executive-summary-dashboard)
   - [E-commerce Analytics Dashboard](#5-e-commerce-analytics-dashboard)
5. [Interactive Features](#interactive-features)
6. [Exporting & Sharing](#exporting--sharing)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)
9. [Glossary](#glossary)
10. [Support](#support)

---

## 🚀 Getting Started

### Accessing the Dashboards

#### Option 1: Tableau Desktop (Local)
1. Download the packaged workbook: `Kids_Clothing_Analytics.twbx`
2. Double-click to open in Tableau Desktop
3. Navigate between dashboards using tabs at bottom of screen

#### Option 2: Tableau Server (Recommended)
1. Open web browser (Chrome, Firefox, Edge, Safari)
2. Navigate to: `https://your-tableau-server.com/views/KidsClothingInsights`
3. Log in with your credentials
4. Select dashboard from left navigation menu

#### Option 3: Tableau Public (Portfolio Demo)
1. Visit: `https://public.tableau.com/profile/nitindb`
2. Find "Kids Clothing Insights" project
3. Click to view interactive dashboards

### System Requirements

**Minimum Specifications**:
- **Browser**: Chrome 90+, Firefox 88+, Edge 90+, Safari 14+
- **Screen Resolution**: 1366x768 (1920x1080 recommended)
- **Internet**: Stable connection (2 Mbps+)
- **Tableau Desktop**: Version 2023.1 or later (if using local)

**Optimal Experience**:
- Large monitor (24" or larger)
- Desktop/laptop (mobile responsive but best on desktop)
- Modern browser with JavaScript enabled

### First-Time Setup

1. **Request Access**: Contact IT to request dashboard access
2. **Complete Training**: Attend 2-hour user training workshop
3. **Bookmark Dashboards**: Save frequently used dashboards to browser favorites
4. **Set Default View**: Configure your landing page (ask admin)

---

## 📊 Dashboard Overview

The Enterprise Analytics Hub consists of **5 integrated dashboards**:

| Dashboard | Purpose | Primary Users | Refresh |
|-----------|---------|---------------|---------|
| 🛍️ **Sales Performance** | Track revenue, products, stores | Sales team, Store managers | Daily |
| 👥 **Customer Analytics** | Segment customers, CLV analysis | Marketing team | Daily |
| 📦 **Inventory Management** | Stock levels, reorder alerts | Operations team | Daily |
| 💼 **Executive Summary** | Financial KPIs, high-level metrics | Executive leadership | Daily |
| 🌐 **E-commerce Analytics** | Website funnel, conversions | E-commerce team | Daily |

**Navigation Flow**:
```
Homepage (Dashboard List)
    ↓
Select Dashboard
    ↓
Apply Filters (Date, Category, etc.)
    ↓
Interact (Click charts, drill-down)
    ↓
Export/Share Results
```

---

## 🧭 Navigation Guide

### Dashboard Menu

**Location**: Top navigation bar or left sidebar

**Menu Structure**:
```
📂 Kids Clothing Insights
   ├── 📊 Sales Performance
   ├── 👥 Customer Analytics
   ├── 📦 Inventory Management
   ├── 💼 Executive Summary
   └── 🌐 E-commerce Analytics
```

### Quick Navigation Tips

1. **Dashboard Tabs**: Click tabs at bottom to switch dashboards (Desktop)
2. **Breadcrumbs**: Use breadcrumb trail to navigate back
3. **Home Button**: Click logo to return to dashboard list
4. **Search**: Use Cmd/Ctrl+F to search for specific metrics
5. **Keyboard Shortcuts**:
   - `Ctrl + G`: Show/hide filters
   - `Ctrl + H`: Show/hide legends
   - `Ctrl + R`: Refresh data
   - `Ctrl + E`: Export view

---

## 📈 Dashboard Details

### 1. Sales Performance Dashboard

**Purpose**: Analyze sales trends across stores, categories, and time periods

#### Key Visualizations

##### 📍 Geographic Sales Map
- **What**: Store locations with revenue-sized bubbles
- **How to Use**:
  - Hover over bubble to see store details
  - Click bubble to filter entire dashboard to that store
  - Zoom in/out using mouse scroll or +/- buttons
- **Insights**: Identify top-performing regions and underperforming locations

##### 📊 Category Performance Bar Chart
- **What**: Revenue breakdown by product category (Girls, Boys, Infants, Accessories)
- **How to Use**:
  - Click bar to drill-down into specific category
  - Hover for exact revenue and percentage
- **Insights**: Girls Clothing leads with 45.2% share

##### 📅 Monthly Trend Line Chart
- **What**: Revenue trends over time with seasonal patterns
- **How to Use**:
  - Click and drag to zoom into specific date range
  - Right-click on line to see trend analysis
- **Insights**: Summer peak (June-Aug), Q4 holiday surge

##### 🏪 Store Ranking Table
- **What**: Top 10 stores ranked by revenue
- **How to Use**:
  - Click column header to sort by different metric
  - Click store name to filter dashboard
- **Insights**: LA Fashion Kids ($122K) leads all stores

##### 🌐 Channel Split Pie Chart
- **What**: Online vs. Offline revenue distribution
- **How to Use**:
  - Click slice to filter to that channel
- **Insights**: 42% online, 58% offline (growing online trend)

##### 💳 Payment Method Distribution
- **What**: Breakdown of payment types used
- **How to Use**:
  - Hover for transaction count and AOV by payment method
- **Insights**: Credit cards dominate (45.4%)

#### Filters Available

| Filter | Options | Default |
|--------|---------|---------|
| **Date Range** | Custom, Last 30 days, Last quarter, Last year | Last year |
| **Category** | All, Girls, Boys, Infants, Accessories | All |
| **Store** | All stores, S001-S010, Online | All |
| **Region** | All, West, East, Central, South | All |
| **Channel** | All, Online, Offline | All |

#### Example Use Cases

**Use Case 1: Analyze Summer Performance**
1. Set Date Range filter to June-August 2024
2. Observe revenue spike in monthly trend chart
3. Click category bar to see which categories drove summer sales
4. Result: Girls Clothing had biggest summer surge (+$50K)

**Use Case 2: Compare Store Performance**
1. View Store Ranking Table
2. Click top store (LA Fashion Kids)
3. Review category breakdown for top store
4. Compare with bottom store to identify improvement opportunities
5. Result: Top stores have balanced category mix; bottom stores over-rely on one category

**Use Case 3: Identify Declining Trends**
1. Zoom into last 3 months on trend chart
2. Notice any downward patterns
3. Filter by category to isolate underperforming products
4. Result: Accessories showing -12% decline → Action: Investigate and adjust

---

### 2. Customer Analytics Dashboard

**Purpose**: Understand customer segments, lifetime value, and behavior patterns

#### Key Visualizations

##### 🎯 RFM Segmentation Scatter Plot
- **What**: Customers plotted by Recency (X) vs. Frequency (Y), sized by Monetary value
- **Color Coding**:
  - 🟢 Green: Champions, Loyal (high value)
  - 🟡 Yellow: Potential Loyalists, Need Attention
  - 🔴 Red: At Risk, Can't Lose Them, Lost
- **How to Use**:
  - Click cluster to filter dashboard to that segment
  - Hover over dot to see individual customer details
- **Insights**: 1,677 Champions (17.1%) drive highest CLV ($717.86)

##### 📊 Customer Segment Pie Chart
- **What**: Distribution of 10 customer segments
- **Segments**:
  1. Champions (17.1%)
  2. Loyal Customers (11.9%)
  3. Potential Loyalists (13.8%)
  4. New Customers (10.0%)
  5. Promising (9.0%)
  6. Need Attention (17.3% - largest)
  7. About to Sleep (10.0%)
  8. At Risk (5.7%)
  9. Can't Lose Them (4.6%)
  10. Lost (0.5%)
- **How to Use**:
  - Click slice to view details for that segment
  - Export segment list for marketing campaigns

##### 💰 CLV by Segment Bar Chart
- **What**: Average Customer Lifetime Value for each segment
- **How to Use**:
  - Sort by CLV to prioritize high-value segments
  - Compare against acquisition cost (CAC)
- **Insights**: Champions CLV ($717) is 17x higher than Lost customers ($36)

##### 🗺️ Geographic Heatmap
- **What**: Customer density by city/state
- **Color Intensity**: Darker = more customers
- **How to Use**:
  - Click region to filter dashboard
  - Identify expansion opportunities (low density areas)
- **Insights**: NYC, Columbus, Denver are top 3 cities

##### 🔄 Cohort Retention Matrix
- **What**: Retention rates by signup month (rows) and months since signup (columns)
- **Color Scale**: Green (high retention) to Red (low retention)
- **How to Use**:
  - Read horizontally to see cohort lifecycle
  - Read vertically to compare same month across cohorts
- **Insights**: 78% retain after month 1, 32% after year 1

##### 👤 Demographics Breakdown
- **Age Groups**: 22-25, 26-35, 36-45
- **Gender**: Female (65%), Male (30%), Other (5%)
- **How to Use**:
  - Click demographic to filter
  - Cross-reference with CLV to find high-value demographics
- **Insights**: 26-35 age group has highest CLV ($435.83)

#### Filters Available

| Filter | Options | Default |
|--------|---------|---------|
| **Segment** | All, Champions, Loyal, At Risk, etc. | All |
| **Region** | All, West, East, Central, South | All |
| **CLV Range** | <$100, $100-$300, $300-$500, $500+ | All |
| **Signup Date** | Custom, Last 6 months, Last year, All time | All time |
| **Age Group** | All, 22-25, 26-35, 36-45 | All |

#### Example Use Cases

**Use Case 1: Create Champions VIP Program**
1. Click "Champions" segment in pie chart
2. Review CLV ($717.86 avg) and purchase behavior
3. Export customer list (see Exporting section)
4. Create VIP program with exclusive perks
5. Result: 1,677 customers identified for VIP program

**Use Case 2: Win-Back At-Risk Customers**
1. Filter to "At Risk" segment (563 customers)
2. Note high CLV ($469.78) despite low recency
3. Review last purchase date and frequency
4. Design win-back email campaign with 20% discount
5. Result: Prevent churn of high-value customers

**Use Case 3: Geographic Expansion Analysis**
1. View geographic heatmap
2. Identify cities with low customer density but high spending
3. Cross-reference with store locations
4. Recommend new store locations or targeted digital ads
5. Result: Identified 3 underserved cities for expansion

---

### 3. Inventory Management Dashboard

**Purpose**: Optimize stock levels, prevent stockouts, and manage suppliers

#### Key Visualizations

##### 🚨 Stock Status Gauges
- **What**: Real-time stock health across categories
- **Color Coding**:
  - 🔴 Red (Critical): <50% of reorder point
  - 🟡 Yellow (Low): 50-100% of reorder point
  - 🟢 Green (Normal): >100% of reorder point
- **How to Use**:
  - Click gauge to view products in that status
- **Insights**: 44 critical items, 19 low, 837 normal

##### 📋 Reorder Alerts Table
- **Columns**: Product, Category, Current Stock, Reorder Point, Qty Needed, Cost
- **Sorting**: Default sorted by priority (critical first)
- **How to Use**:
  - Click row to view product details
  - Export table to create purchase order
  - Check "Cost" column for budget planning
- **Insights**: $5,876 immediate reorder cost for 44 critical items

##### 🏭 Supplier Scorecard
- **Metrics**: Performance score (0-1), On-time delivery %, Defect rate %, Avg lead time
- **Ranking**: #1 Baby Boutique Supplies (0.899 score)
- **How to Use**:
  - Sort by score to identify best/worst suppliers
  - Click supplier to see products they supply
  - Use for contract renegotiation leverage
- **Insights**: Top 3 suppliers have 95%+ on-time delivery

##### 🔄 Inventory Turnover Chart
- **Categories**: Fast-moving (>6x), Regular (3-6x), Slow (<3x), Dead (0x)
- **How to Use**:
  - Click category to view products
  - Focus on slow/dead stock for clearance sales
- **Insights**: 240 fast-moving items, 119 slow/dead ($23K locked)

##### 🏢 Warehouse Utilization
- **What**: Stock value by warehouse (WH001-WH003)
- **How to Use**:
  - Identify imbalances in warehouse distribution
  - Plan inventory transfers
- **Insights**: WH002 (East) has 52% of total stock value

##### ⏰ Stock Age Analysis
- **What**: Inventory grouped by days in stock (0-30, 31-60, 61-90, 90+ days)
- **How to Use**:
  - Focus on 90+ day category for clearance
- **Insights**: 37.5% of inventory ageing (90+ days)

#### Filters Available

| Filter | Options | Default |
|--------|---------|---------|
| **Category** | All, Girls, Boys, Infants, Accessories | All |
| **Warehouse** | All, WH001, WH002, WH003 | All |
| **Stock Status** | All, Critical, Low, Normal | All |
| **Supplier** | All 15 suppliers | All |
| **Turnover** | All, Fast, Regular, Slow, Dead | All |

#### Example Use Cases

**Use Case 1: Process Reorder Alerts**
1. View Reorder Alerts Table
2. Filter to "Critical" status
3. Export table (44 items, $5,876 cost)
4. Forward to procurement team for PO creation
5. Result: Prevent stockouts of critical items

**Use Case 2: Clearance Sale Planning**
1. Filter Inventory Turnover to "Slow" and "Dead"
2. View 119 items worth $23K
3. Export product list
4. Create clearance sale (30-50% discount)
5. Result: Free up $23K cash and warehouse space

**Use Case 3: Supplier Performance Review**
1. View Supplier Scorecard
2. Identify bottom 3 suppliers (score <0.80)
3. Compare with top 3 suppliers
4. Negotiate better terms or switch suppliers
5. Result: Improve delivery reliability and reduce defects

---

### 4. Executive Summary Dashboard

**Purpose**: High-level financial KPIs and strategic insights for leadership

#### Key Visualizations

##### 💵 KPI Cards (Top Row)
- **Revenue**: $1,956,784 (🟢 +7.5% YoY)
- **Gross Margin**: 45.23% (🟢 Target: 45%)
- **Net Margin**: 11.43% (🔴 Target: 15%)
- **Transactions**: 50,000
- **AOV**: $39.14 (🔴 Target: $45)
- **Active Customers**: 9,823
- **Inventory Turnover**: 7.03x (🟢 Target: 5x)
- **CLV/CAC**: 22.62x (🟢 Target: 5x)

##### 📊 P&L Waterfall Chart
- **What**: Visual profit & loss statement
- **Flow**: Revenue → COGS → Gross Profit → OpEx → Net Profit
- **How to Use**:
  - Hover over each bar to see exact values
  - Identify largest cost drivers (COGS: 54.77%, OpEx: 30%)
- **Insights**: Strong gross margin (45%) but high operating expenses

##### 📅 YoY Comparison Bars
- **What**: Current year vs. prior year performance
- **Metrics**: Revenue, transactions, AOV, margin
- **How to Use**:
  - Identify growth or decline trends
  - Click bar to drill into monthly details
- **Insights**: Flat growth (+0.07%) - mature market, need new strategies

##### 📈 Quarterly Performance Trend
- **What**: Revenue by quarter (Q1-Q4) for both years
- **Pattern**: Q4 strongest ($249K) due to holidays
- **How to Use**:
  - Plan seasonal inventory and marketing
- **Insights**: 35% of annual revenue in Q4

##### 🔮 Revenue Forecast
- **What**: 6-month revenue projection with confidence bands
- **Method**: Linear regression on historical trends
- **Forecast**: $489,980 next 6 months
- **How to Use**:
  - Budget planning for next fiscal half
  - Adjust growth strategies if trending below forecast
- **Insights**: Expects continued flat growth without intervention

##### 🎯 Executive Scorecard (Traffic Lights)
- **Green** (Exceeding Target):
  - ✅ Gross Margin: 45.23% (target: 45%)
  - ✅ Inventory Turnover: 7.03x (target: 5x)
  - ✅ CLV/CAC: 22.62x (target: 5x)
- **Red** (Below Target):
  - ❌ Net Margin: 11.43% (target: 15%)
  - ❌ AOV: $39.14 (target: $45)
- **How to Use**:
  - Focus improvement efforts on red indicators
  - Maintain green indicators

#### Filters Available

| Filter | Options | Default |
|--------|---------|---------|
| **Date Range** | Current year, Prior year, Last 6 months | Current year |
| **Comparison Period** | YoY, QoQ, MoM | YoY |
| **Category** | All, Girls, Boys, Infants, Accessories | All |

#### Example Use Cases

**Use Case 1: Quarterly Board Presentation**
1. Set Date Range to current year
2. Review all KPI cards for headline numbers
3. Highlight P&L waterfall to show profitability
4. Point to YoY comparison for growth story
5. Show forecast for next 6 months
6. Result: Comprehensive 5-minute board update

**Use Case 2: Identify Improvement Priorities**
1. Review Executive Scorecard
2. Note 2 red indicators (Net Margin, AOV)
3. Drill into Net Margin: High OpEx driving low net profit
4. Drill into AOV: Need bundling/upsell strategies
5. Result: Create action plan for margin improvement

**Use Case 3: Budget Planning**
1. View Revenue Forecast chart
2. Note $489K forecast for next 6 months
3. Apply cost ratios: COGS 54.77%, OpEx 30%
4. Calculate budget allocation by department
5. Result: Data-driven budget plan for next fiscal half

---

### 5. E-commerce Analytics Dashboard

**Purpose**: Optimize online channel performance and user experience

#### Key Visualizations

##### 🎯 Conversion Funnel
- **Stages**: Homepage → Category → Product → Cart → Checkout → Purchase
- **Numbers**:
  - Homepage: 200,000 (100%)
  - Category: 80,014 (40%) → 60% drop
  - Product: 56,085 (28%) → 30% drop
  - Cart: 22,456 (11%) → 60% drop ⚠️
  - Checkout: 7,271 (4%) → 68% drop ⚠️
  - Purchase: 3,515 (1.76%)
- **How to Use**:
  - Identify largest drop-off points
  - Click stage to see detailed metrics
- **Insights**: Critical drop-offs at Cart (60%) and Checkout (68%)

##### 🚀 Traffic Source Pie Chart
- **Sources**: Organic (42%), Paid (18%), Social (15%), Direct (12%), Referral (8%), Email (5%)
- **How to Use**:
  - Click slice to filter entire dashboard to that source
  - Compare conversion rates across sources
- **Insights**: Organic best volume, Direct best conversion (1.89%)

##### 📱 Device Comparison Bars
- **Devices**: Mobile (57.7%), Desktop (35.3%), Tablet (7%)
- **Metrics**: Sessions, conversion rate, revenue, AOV
- **How to Use**:
  - Identify device-specific issues
  - Prioritize mobile optimization (majority traffic)
- **Insights**: Tablet has best conversion (1.81%) despite lowest traffic

##### 🛍️ Product Page Performance Table
- **Columns**: Product, Views, Add-to-Cart rate, Purchases, View-to-Purchase %
- **Sorting**: Default sorted by views (most popular first)
- **How to Use**:
  - Identify best/worst converting product pages
  - Apply learnings from top performers to underperformers
- **Insights**: Best add-to-cart rate: 63.2% (PetitMode Leggings)

##### 🛒 Cart Abandonment Reasons
- **Top 5 Reasons**:
  1. High Shipping Costs (32%)
  2. Just Browsing (20%)
  3. Better Price Elsewhere (18%)
  4. Payment Issues (15%)
  5. Website Errors (8%)
- **How to Use**:
  - Prioritize fixes based on impact (% affected)
- **Action Items**: Offer free shipping threshold, simplify checkout

##### ⏰ Hourly & Day-of-Week Heatmaps
- **Hourly**: Peak traffic 2-6 PM, peak conversion 6-11 PM
- **Day-of-Week**: Saturday best (1.87% conv), Monday lowest (1.65%)
- **How to Use**:
  - Schedule marketing campaigns during peak hours
  - Plan site maintenance during low-traffic hours
- **Insights**: Evening shoppers convert better (more deliberate)

#### Filters Available

| Filter | Options | Default |
|--------|---------|---------|
| **Date Range** | Custom, Last 30 days, Last quarter | Last quarter |
| **Traffic Source** | All, Organic, Paid, Social, Direct, Referral, Email | All |
| **Device** | All, Mobile, Desktop, Tablet | All |
| **Category** | All, Girls, Boys, Infants, Accessories | All |

#### Example Use Cases

**Use Case 1: Reduce Cart Abandonment**
1. View Cart Abandonment Reasons
2. Note #1 reason: High Shipping Costs (32%)
3. Calculate break-even for free shipping: $50 order minimum
4. Implement free shipping over $50 promo
5. Result: 10-15% reduction in cart abandonment expected

**Use Case 2: Optimize Mobile Experience**
1. Filter to "Mobile" device
2. Compare conversion rate with desktop (equal: 1.75%)
3. Note: Mobile has 57.7% traffic but same conversion
4. Investigate: Are mobile users browsing and converting on desktop later?
5. Action: Improve mobile UX (larger buttons, faster load)
6. Result: Increase mobile conversion from 1.75% to 2.0%

**Use Case 3: Traffic Source Optimization**
1. View Traffic Source pie chart
2. Note: Direct has best conversion (1.89%) but only 12% share
3. Compare with Paid (1.84% conv, 18% share)
4. Strategy: Increase direct traffic via brand awareness, reduce paid spend
5. Result: Improve marketing ROI by shifting budget

---

## 🎛️ Interactive Features

### Filtering

**Types of Filters**:
1. **Global Filters** (top of dashboard): Apply to all visualizations
2. **Chart-Specific Filters**: Apply to single chart only
3. **Date Range Filters**: Custom date selection or presets

**How to Apply Filters**:
1. Click filter dropdown (top right of dashboard)
2. Select desired values (multi-select allowed)
3. Click "Apply" or press Enter
4. Click "Clear" to reset filters

**Filter Tips**:
- Use Ctrl+Click to select multiple values
- Use "Exclude" option to show everything except selected
- Use "Wildcard Match" for partial text searches

### Drill-Down

**What is Drill-Down?**: Click on a data point to see more detailed information

**Examples**:
- Click a store on map → Filter to that store's data
- Click a category bar → See products in that category
- Click a customer segment → View customers in that segment

**How to Drill-Down**:
1. Hover over data point (chart changes to hand cursor)
2. Click once to drill-down
3. Use breadcrumb trail to navigate back
4. Click "Reset" to return to top level

### Highlighting

**What is Highlighting?**: Temporarily emphasize related data without filtering

**How to Highlight**:
1. Hover over data point (no click needed)
2. Related data across all charts highlights
3. Unrelated data dims but remains visible
4. Move mouse away to remove highlight

**Example**: Hover over "Girls Clothing" category → See girls-related data highlighted in all charts

### Sorting

**How to Sort Tables**:
1. Click column header once: Ascending sort (A→Z, 0→9)
2. Click again: Descending sort (Z→A, 9→0)
3. Click third time: Return to default sort

**How to Sort Charts**:
1. Right-click on chart
2. Select "Sort"
3. Choose sort field and direction

### Tooltips

**What are Tooltips?**: Pop-up boxes with detailed information

**How to View Tooltips**:
1. Hover mouse over any data point
2. Tooltip appears after 1 second
3. Move mouse away to hide tooltip

**Tooltip Content**:
- Exact values (e.g., Revenue: $122,803.43)
- Percentages (e.g., 6.3% of total)
- Related metrics (e.g., Transactions: 3,138)
- Additional context (e.g., "Top store in West region")

### Cross-Dashboard Navigation

**Method 1: Dashboard Tabs**
- Click tabs at bottom of screen (Tableau Desktop)
- Click dashboard name in left menu (Tableau Server)

**Method 2: Click-Through Actions**
1. Click data point with link icon (underlined)
2. Automatically navigate to related dashboard
3. Context (filters) preserved in new dashboard

**Example**: Click store name in Sales dashboard → Opens filtered view in Inventory dashboard showing that store's stock

---

## 📤 Exporting & Sharing

### Export Options

#### Export to PDF
**Use When**: Creating reports for meetings, archival

**Steps**:
1. Navigate to desired dashboard
2. Click "File" → "Print to PDF" (Desktop) or "Download" → "PDF" (Server)
3. Select options:
   - Include only visible data (filters applied)
   - Specific sheet or entire workbook
   - Page size (A4, Letter)
4. Click "Save"

**Tips**:
- Use landscape orientation for wide dashboards
- Apply filters before exporting to reduce PDF size
- "Scaling" option: "Fit to Page" vs. "Actual Size"

#### Export to Excel/CSV
**Use When**: Further analysis in Excel, data sharing

**Steps**:
1. Right-click on chart or table
2. Select "View Data" → "Export All" (or "Export Crosstab" for tables)
3. Choose format: Excel (.xlsx) or CSV (.csv)
4. Click "Save"

**What's Exported**:
- Underlying data (not just visible data)
- All rows (not limited to dashboard view)
- Column headers included

**Tips**:
- Use "Crosstab" export for pivot-table-ready format
- Use "Data" export for raw data

#### Export to PowerPoint
**Use When**: Building presentations

**Steps** (Tableau Server only):
1. Click "Download" → "PowerPoint"
2. Select dashboards to include
3. Click "Download"

**Result**: One slide per dashboard with interactive links

#### Export to Image (PNG/JPEG)
**Use When**: Embedding in documents, websites, emails

**Steps**:
1. Click "Worksheet" → "Export" → "Image" (Desktop)
2. Or right-click dashboard → "Copy" → "Image" (Server)
3. Select format: PNG (transparent background) or JPEG (smaller file)
4. Choose resolution: Normal, High, Extra High

**Tips**:
- Use PNG for presentations (better quality)
- Use JPEG for emails (smaller file size)

### Sharing Dashboards

#### Share Link (Tableau Server)
**Steps**:
1. Navigate to dashboard
2. Copy URL from browser address bar
3. OR click "Share" button → Copy link
4. Paste link in email or chat

**Link Options**:
- Include current filters: Add `?:filters=...` to URL
- Auto-refresh: Add `?:refresh=yes` to URL

**Permissions**: Recipient must have dashboard access rights

#### Email Subscription
**Steps**:
1. Click "Subscribe" button (Server only)
2. Choose frequency: Daily, Weekly, Monthly
3. Select format: PDF, PNG
4. Add recipients
5. Click "Subscribe"

**Result**: Automated email with dashboard snapshot at specified time

#### Embedding (Website/Intranet)
**For IT/Web Developers**:
```html
<iframe src="https://your-tableau-server.com/views/Dashboard/Sales"
        width="1200" height="800" frameborder="0"></iframe>
```

**Options**:
- Toolbar: `?:toolbar=no` to hide
- Tabs: `?:tabs=no` to hide
- Auto-size: `?:embed=yes` for responsive

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Issue: Dashboard Not Loading
**Symptoms**: Blank screen, "Loading..." message stuck

**Solutions**:
1. **Check Internet**: Ensure stable connection (2+ Mbps)
2. **Refresh Page**: Press Ctrl+R or click browser refresh
3. **Clear Cache**: Clear browser cache and cookies
4. **Try Different Browser**: Test in Chrome, Firefox, Edge
5. **Contact IT**: If issue persists, IT may need to restart Tableau Server

#### Issue: Slow Performance
**Symptoms**: Dashboard takes >10 seconds to load

**Solutions**:
1. **Reduce Date Range**: Filter to last 30 days instead of all-time
2. **Close Other Tabs**: Close unused browser tabs (memory)
3. **Simplify Filters**: Apply fewer filters simultaneously
4. **Use Extract**: Ask admin to optimize data extract (backend)
5. **Check Network**: Test internet speed (speedtest.net)

#### Issue: Data Looks Outdated
**Symptoms**: Numbers don't match expectations, old dates

**Solutions**:
1. **Check Refresh Time**: Look for "Data last refreshed: [timestamp]" note
2. **Force Refresh**: Click Ctrl+R or "Refresh Data" button
3. **Verify Date Filter**: Ensure date filter set to current period
4. **Contact IT**: Data may need manual refresh if scheduled refresh failed

#### Issue: Can't Find Specific Metric
**Symptoms**: Looking for metric but can't locate it

**Solutions**:
1. **Use Search**: Press Ctrl+F, type metric name (e.g., "CLV")
2. **Check Tooltips**: Hover over charts - metric may be in tooltip
3. **Try Different Dashboard**: Metric may be on different dashboard
4. **Check Glossary**: Metric may be labeled differently (e.g., "LTV" vs. "CLV")
5. **Ask Analyst**: Contact BI team if metric truly missing

#### Issue: Export Fails
**Symptoms**: Error message when trying to export

**Solutions**:
1. **Reduce Data**: Apply filters to reduce export size (<50K rows)
2. **Check Format**: Try different format (PDF vs. Excel)
3. **Browser Permissions**: Allow pop-ups and downloads
4. **Disk Space**: Ensure sufficient disk space on local machine
5. **Admin Rights**: Some exports require admin approval

#### Issue: Filters Not Working
**Symptoms**: Applying filter has no effect on dashboard

**Solutions**:
1. **Clear All Filters**: Click "Reset" to clear conflicting filters
2. **Check Filter Hierarchy**: Some filters depend on others (e.g., must select region before store)
3. **Refresh Dashboard**: Press F5 to reload
4. **Check Data**: Filtered data may genuinely not exist
5. **Report Bug**: If consistent, report to BI team

### Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "Unable to connect to data source" | Connection lost | Check internet, refresh page |
| "Timeout error" | Query took too long | Reduce date range, simplify filters |
| "Insufficient permissions" | Access denied | Contact IT for dashboard access |
| "Data source not found" | Backend issue | Contact BI team |
| "Invalid filter selection" | Filter conflict | Clear all filters, reapply |

---

## ✅ Best Practices

### For Daily Users

1. **Start with Filters**: Apply date range and relevant filters before exploring
2. **Use Tooltips**: Hover for quick insights without cluttering screen
3. **Bookmark Views**: Save frequently used filter combinations as bookmarks
4. **Export Regularly**: Export key metrics for offline reference
5. **Check Refresh Time**: Verify data freshness before making decisions

### For Managers

1. **Weekly Reviews**: Schedule recurring time to review dashboards
2. **Compare Periods**: Always compare current vs. prior period (YoY, MoM)
3. **Drill Into Anomalies**: Investigate unusual spikes or drops
4. **Share Insights**: Share dashboard findings with team in meetings
5. **Act on Data**: Create action items from insights (don't just observe)

### For Executives

1. **Start with Executive Dashboard**: High-level overview first
2. **Focus on Red Indicators**: Prioritize areas below target
3. **Trend Over Point**: Look at trends, not single data points
4. **Combine Dashboards**: Cross-reference (e.g., Sales + Inventory)
5. **Ask "Why"**: Use dashboards to identify problems, then dig deeper

### For Analysts

1. **Validate Data**: Cross-check with source systems periodically
2. **Document Insights**: Keep log of findings and actions taken
3. **Educate Users**: Help colleagues interpret data correctly
4. **Suggest Improvements**: Provide feedback to BI team for enhancements
5. **Stay Updated**: Attend training on new dashboard features

### Do's and Don'ts

✅ **DO**:
- Apply filters to focus analysis
- Export data for deeper analysis in Excel
- Share dashboards via links (not screenshots when possible)
- Report bugs or data quality issues promptly
- Attend training sessions to learn advanced features

❌ **DON'T**:
- Make major decisions based on single data point
- Share confidential data outside organization
- Modify dashboard design without approval
- Ignore data quality warnings
- Assume data is always correct (validate critical decisions)

---

## 📖 Glossary

| Term | Definition | Example |
|------|------------|---------|
| **Dashboard** | Collection of visualizations on single screen | Sales Performance dashboard |
| **Filter** | Control to narrow data displayed | Date range filter: Jan-Mar 2024 |
| **Drill-Down** | Click to see more detailed data | Click store → See store's products |
| **Tooltip** | Pop-up with detailed information | Hover over bar → See exact value |
| **Extract** | Snapshot of data for performance | Refreshed nightly at 2 AM |
| **Workbook** | Collection of dashboards in one file | Kids_Clothing_Analytics.twbx |
| **Worksheet** | Single visualization or chart | Category performance bar chart |
| **Parameter** | User-controlled value | "Top N" parameter: Show top 10 |
| **Calculated Field** | Derived metric | AOV = Revenue / Transactions |
| **Aggregation** | Summary of data | SUM(Revenue) by Category |
| **Dimension** | Categorical field | Category, Store, Date |
| **Measure** | Numeric field | Revenue, Quantity, CLV |
| **Granularity** | Level of detail | Transaction-level vs. Daily |

---

## 📞 Support

### Getting Help

#### Self-Service Resources
1. **This Guide**: Comprehensive usage instructions
2. **FAQ Document**: `FAQ.md` in documentation folder
3. **Video Tutorials**: Available on company intranet
4. **Tableau Help**: [https://help.tableau.com](https://help.tableau.com)

#### Human Support

**Tier 1: Dashboard Help Desk**
- **Contact**: dashboards@company.com
- **Hours**: Mon-Fri 9 AM - 5 PM
- **Response Time**: 4 business hours
- **Issues**: Login problems, basic navigation, exports

**Tier 2: BI Team**
- **Contact**: bi-team@company.com
- **Hours**: Mon-Fri 9 AM - 5 PM
- **Response Time**: 1 business day
- **Issues**: Data questions, dashboard bugs, feature requests

**Tier 3: Project Owner**
- **Contact**: nitindb901@gmail.com
- **Hours**: By appointment
- **Response Time**: 2-3 business days
- **Issues**: Complex analytics questions, custom dashboard requests

### Reporting Issues

**Bug Report Template**:
```
Subject: [BUG] Brief description

Dashboard: Sales Performance
Issue: Filter not working
Steps to Reproduce:
1. Open Sales Performance dashboard
2. Select "West" region filter
3. Chart does not update

Expected: Chart shows only West region data
Actual: Chart shows all regions

Browser: Chrome 120
Screenshot: [Attach]
```

### Feature Requests

**Request Template**:
```
Subject: [FEATURE] New metric request

Dashboard: Customer Analytics
Requested Feature: Add "Average Days Between Purchases" metric

Business Justification:
Would help identify purchase frequency patterns and optimize email campaign timing

Priority: Medium
Requested By: Marketing Team
```

### Training & Onboarding

**New User Onboarding**:
1. **Welcome Email**: Access credentials and this guide
2. **Self-Paced Learning**: 1-hour video tutorial series
3. **Live Training**: 2-hour workshop (weekly sessions)
4. **Office Hours**: Weekly drop-in Q&A sessions (Fridays 2-3 PM)

**Advanced Training**:
- **Monthly Webinars**: Deep-dives on specific dashboards
- **Quarterly Updates**: New feature training
- **Custom Sessions**: Departmental training on request

---

## 📝 Document Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 2024 | Initial guide creation |

---

## 📎 Quick Reference Card

**Print this section for desk reference!**

### Most Common Tasks

| Task | Steps |
|------|-------|
| **Apply Date Filter** | Top right → Date dropdown → Select range → Apply |
| **Export to Excel** | Right-click chart → View Data → Export All |
| **Reset Filters** | Click "Reset" button (top right) |
| **Navigate Dashboards** | Click tabs at bottom OR left menu |
| **Drill-Down** | Click on data point (bar, bubble, etc.) |
| **Print to PDF** | File → Print to PDF OR Download → PDF |
| **Share Link** | Copy browser URL OR Share button |
| **Get Help** | Email: dashboards@company.com |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + G` | Toggle filters |
| `Ctrl + H` | Toggle legends |
| `Ctrl + R` | Refresh data |
| `Ctrl + E` | Export view |
| `Ctrl + F` | Search |
| `F5` | Reload dashboard |
| `Esc` | Clear selection |

---

<div align="center">

**Questions? Contact Us!**

📧 dashboards@company.com  
💬 Internal Chat: #tableau-support  
🎓 Training Portal: intranet.company.com/training

**Kids Clothing Insights - Enterprise Analytics Hub**  
*Empowering Data-Driven Decisions*

© 2024 Nitin DB | Version 1.0

</div>
