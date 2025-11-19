# 📊 Tableau Dashboards - Kids Clothing Insights

## Dashboard Files

This folder contains Tableau dashboard files and related resources for the Kids Clothing Insights project.

---

## 📂 Folder Structure

```
tableau/
├── Kids_Clothing_Analytics.twbx          ⏳ (To be created)
├── TABLEAU_DEVELOPMENT_GUIDE.md          ✅ Complete step-by-step guide
├── README_TABLEAU.md                     ✅ This file
└── dashboard_screenshots/                📸 Dashboard images
    ├── 01_sales_performance.png          ⏳ (Create after dashboard)
    ├── 02_customer_analytics.png         ⏳ (Create after dashboard)
    ├── 03_inventory_management.png       ⏳ (Create after dashboard)
    ├── 04_executive_summary.png          ⏳ (Create after dashboard)
    └── 05_ecommerce_analytics.png        ⏳ (Create after dashboard)
```

---

## 🎯 Quick Start

### Option 1: Build Dashboards Yourself

1. **Install Tableau Desktop** (version 2023.1 or later)
2. **Follow the guide**: Open `TABLEAU_DEVELOPMENT_GUIDE.md`
3. **Connect data**: Use CSV files from `../data/processed/`
4. **Build dashboards**: Follow step-by-step instructions (10 hours total)
5. **Export**: Save as `.twbx` and capture screenshots

### Option 2: Use Pre-Built Dashboards (When Available)

1. **Download**: `Kids_Clothing_Analytics.twbx`
2. **Open**: Double-click file (opens in Tableau Desktop)
3. **Explore**: Navigate between 5 dashboards
4. **Customize**: Modify as needed for your use case

---

## 📊 Dashboard Overview

### Dashboard 1: Sales Performance
**Purpose**: Track revenue, products, stores, and sales trends

**Key Visualizations**:
- 📍 Geographic sales map with store bubbles
- 📊 Category performance bar chart (Girls, Boys, Infants, Accessories)
- 📅 Monthly trend line with seasonality
- 🏪 Store ranking table (top 10)
- 🌐 Channel split pie chart (Online vs Offline)
- 💳 Payment method distribution

**Key Metrics**:
- Total Revenue: $1,956,784
- Transactions: 50,000
- Average Order Value: $39.14
- Top Category: Girls Clothing (45.2%)

**File**: `dashboard_screenshots/01_sales_performance.png` ⏳

---

### Dashboard 2: Customer Analytics
**Purpose**: Customer segmentation, RFM analysis, lifetime value

**Key Visualizations**:
- 🎯 RFM scatter plot (Recency vs Frequency, sized by Monetary)
- 📊 Customer segment pie chart (10 segments)
- 💰 CLV by segment bar chart
- 🗺️ Geographic customer heatmap
- 🔄 Cohort retention matrix
- 👤 Demographics breakdown (age, gender)

**Key Metrics**:
- Total Customers: 9,823
- Average CLV: $429.80
- Champions CLV: $717.86 (highest)
- Repeat Purchase Rate: 92.5%
- Top Segment: Need Attention (17.3%)

**File**: `dashboard_screenshots/02_customer_analytics.png` ⏳

---

### Dashboard 3: Inventory Management
**Purpose**: Stock optimization, reorder alerts, supplier performance

**Key Visualizations**:
- 🚨 Stock status gauges (Critical, Low, Normal)
- 📋 Reorder alerts table (priority sorted)
- 🏭 Supplier scorecard (performance ranking)
- 🔄 Inventory turnover chart (Fast/Regular/Slow/Dead)
- 🏢 Warehouse utilization bars
- ⏰ Stock age analysis

**Key Metrics**:
- Total Stock Value: $152,386
- Critical Items: 44 (need reorder)
- Reorder Cost: $5,876 (immediate)
- Slow-Moving Inventory: $23,120
- Best Supplier: Baby Boutique Supplies (0.899 score)
- Inventory Turnover: 7.03x

**File**: `dashboard_screenshots/03_inventory_management.png` ⏳

---

### Dashboard 4: Executive Summary
**Purpose**: High-level financial KPIs for leadership

**Key Visualizations**:
- 💵 KPI cards (Revenue, Margins, EBITDA, Ratios)
- 📊 P&L waterfall chart (Revenue to Net Profit)
- 📅 YoY comparison bars (2023 vs 2024)
- 📈 Quarterly performance trend
- 🔮 Revenue forecast (6 months with confidence bands)
- 🎯 Executive scorecard (traffic light indicators)

**Key Metrics**:
- Total Revenue: $1,956,784
- Gross Margin: 45.23% 🟢
- Net Margin: 11.43% 🔴 (target: 15%)
- EBITDA: $337,235
- Inventory Turnover: 7.03x 🟢
- CLV/CAC Ratio: 22.62x 🟢

**File**: `dashboard_screenshots/04_executive_summary.png` ⏳

---

### Dashboard 5: E-commerce Analytics
**Purpose**: Online channel performance, conversion optimization

**Key Visualizations**:
- 🎯 Conversion funnel (6 stages: Homepage → Purchase)
- 🚀 Traffic source pie chart (with conversion rates)
- 📱 Device comparison bars (Mobile, Desktop, Tablet)
- 🛒 Cart abandonment reasons bar chart
- ⏰ Hourly traffic heatmap
- 📅 Day-of-week performance chart
- 🛍️ Product page performance table

**Key Metrics**:
- Total Sessions: 200,000
- Conversion Rate: 1.76%
- Cart Abandonment: 84.35% ⚠️
- Top Traffic Source: Organic Search (42.1%)
- Mobile Sessions: 57.7% (dominant)
- #1 Abandonment Reason: High Shipping Costs (32%)

**File**: `dashboard_screenshots/05_ecommerce_analytics.png` ⏳

---

## 🎨 Design Specifications

### Color Palette

**Primary (Kids Clothing Theme)**:
- Pink: `#FF6B9D` (Girls Clothing)
- Blue: `#4A90E2` (Boys Clothing)
- Yellow: `#FFC845` (Infants)
- Purple: `#9B59B6` (Accessories)

**Secondary**:
- Light Gray: `#F8F9FA` (backgrounds)
- Dark Gray: `#2C3E50` (text)
- Success Green: `#27AE60`
- Warning Orange: `#F39C12`
- Danger Red: `#E74C3C`

### Typography

- **Dashboard Titles**: Arial Black, 24px
- **Chart Titles**: Arial Bold, 14px
- **Labels**: Arial, 11px
- **Numbers**: Arial, 12px

### Layout

- **Dashboard Size**: 1920x1080 (Fixed) or Automatic (Responsive)
- **Padding**: 10px between objects
- **Margins**: 20px from edges
- **Background**: White (#FFFFFF) or Light Gray (#F8F9FA)

---

## 🔗 Data Sources

All dashboards connect to CSV files in: `../data/processed/`

**Required Files** (47 total):
- Sales: 10 CSV files
- Customer: 8 CSV files
- Inventory: 9 CSV files
- Executive: 9 CSV files
- E-commerce: 9 CSV files

**Connection Type**: Text File (CSV)  
**Refresh**: Daily batch (automated via Python scripts)

---

## 🚀 Usage Instructions

### For Viewers (Tableau Reader/Server)

1. **Open dashboard** in Tableau Reader or Server
2. **Apply filters** at top of each dashboard
3. **Click visualizations** to drill-down
4. **Hover** for detailed tooltips
5. **Export** to PDF/Excel as needed

**Full usage guide**: See `../documentation/Tableau_Usage_Guide.md`

### For Developers (Tableau Desktop)

1. **Open** `.twbx` file in Tableau Desktop
2. **Refresh data**: Data → Refresh All Extracts
3. **Modify layouts**: Dashboard → Edit
4. **Add calculations**: Analysis → Create Calculated Field
5. **Publish**: Server → Publish Workbook

**Development guide**: See `TABLEAU_DEVELOPMENT_GUIDE.md`

---

## 📸 Taking Screenshots

After building dashboards, capture high-quality screenshots:

### Method 1: Built-in Export
1. Navigate to dashboard
2. **Dashboard → Export Image**
3. Resolution: **High (2x)**
4. Format: **PNG**
5. Save to: `dashboard_screenshots/`
6. Naming: `01_sales_performance.png`, etc.

### Method 2: Tableau Server
1. Open dashboard in browser
2. Click **Download → Image**
3. Select **PNG** format
4. High resolution

### Method 3: Manual Screenshot
1. Set dashboard to full screen (F11)
2. Use Windows Snipping Tool (Win + Shift + S)
3. Capture entire dashboard
4. Save as PNG

**Recommended Size**: 1920x1080 for README display

---

## 📦 Packaging for Distribution

### Create Packaged Workbook

1. **File → Export Packaged Workbook (.twbx)**
2. Includes:
   - ✅ All data sources (embedded)
   - ✅ All worksheets and dashboards
   - ✅ Custom calculations
   - ✅ Images/logos
3. **Save as**: `Kids_Clothing_Analytics.twbx`
4. **Location**: This folder (`tableau/`)

**File Size**: ~10-15 MB (with embedded data)

### Share Workbook

**Option 1: GitHub**
- Upload `.twbx` file to this folder
- Users download and open in Tableau Desktop/Reader

**Option 2: Tableau Public**
- File → Save to Tableau Public
- Get shareable link
- Add link to main README.md

**Option 3: Tableau Server**
- Server → Publish Workbook
- Set permissions
- Share server URL with team

---

## 🔧 Troubleshooting

### Common Issues

**Issue**: Data not loading
- **Solution**: Refresh data connections (Data → Refresh All)
- Check CSV files exist in `../data/processed/`

**Issue**: Broken visualizations
- **Solution**: Verify field names match CSV column names
- Re-establish calculated fields if needed

**Issue**: Slow performance
- **Solution**: Create data extracts instead of live connections
- Optimize dashboard (fewer sheets per dashboard)

**Issue**: Can't open .twbx file
- **Solution**: Install Tableau Desktop or Tableau Reader (free)
- Download from: https://www.tableau.com/products/reader

---

## 📊 Dashboard Metrics Summary

| Dashboard | Charts | Filters | Data Files | Complexity |
|-----------|--------|---------|------------|------------|
| Sales Performance | 7 | 4 | 10 | Medium |
| Customer Analytics | 8 | 4 | 8 | High |
| Inventory Management | 6 | 4 | 9 | Medium |
| Executive Summary | 6 | 2 | 9 | Medium |
| E-commerce Analytics | 8 | 4 | 9 | High |
| **Total** | **35** | **18** | **47** | - |

**Estimated Build Time**: 10-12 hours for all 5 dashboards

---

## 🎓 Learning Resources

**Tableau Training**:
- Tableau Desktop Fundamentals: https://www.tableau.com/learn/training
- Tableau Public Gallery: https://public.tableau.com/gallery
- YouTube Tutorials: Search "Tableau dashboard design"

**Specific Techniques**:
- RFM Scatter Plot: https://www.tableau.com/learn/tutorials/rfm-analysis
- Waterfall Charts: https://www.tableau.com/learn/tutorials/waterfall-charts
- Conversion Funnels: https://www.tableau.com/blog/funnel-charts
- Heatmaps: https://help.tableau.com/current/pro/desktop/en-us/buildexamples_highlight.htm

---

## 📞 Support

**Questions about Tableau dashboards?**
- Development Guide: `TABLEAU_DEVELOPMENT_GUIDE.md`
- Usage Guide: `../documentation/Tableau_Usage_Guide.md`
- Project Owner: nitindb901@gmail.com

**Tableau Community**:
- Forums: https://community.tableau.com
- Support: https://www.tableau.com/support

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 2024 | Initial structure and documentation |

---

## ✅ Next Steps

1. ⏳ **Build dashboards** using `TABLEAU_DEVELOPMENT_GUIDE.md`
2. ⏳ **Capture screenshots** of all 5 dashboards
3. ⏳ **Export .twbx** packaged workbook
4. ⏳ **Update main README** with screenshot links
5. ⏳ **Upload to GitHub** (all files in this folder)
6. ⏳ **Publish to Tableau Public** (optional)

---

<div align="center">

**Kids Clothing Insights - Enterprise Analytics Hub**  
*5 Interactive Tableau Dashboards for Complete Business Intelligence*

© 2024 Nitin DB | All Rights Reserved

</div>
