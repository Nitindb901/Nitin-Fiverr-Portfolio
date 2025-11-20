# Excel Dashboard Setup Guide

## 📊 Complete Excel Dashboard Creation

### Step 1: Import Data

1. **Open Microsoft Excel** (2016 or later recommended)

2. **Import Main Data**
   - Go to: **Data** → **Get Data** → **From File** → **From Text/CSV**
   - Select: `dashboard/powerbi_ready.csv`
   - Click **Load**
   - Data will appear in a new sheet named "powerbi_ready"

3. **Import Additional Tables** (for separate analysis)
   - Repeat for: `daily_aggregation.csv`, `category_aggregation.csv`, `store_performance.csv`, `monthly_trend.csv`
   - Each will create a separate sheet

4. **Convert to Tables**
   - Select data range → **Insert** → **Table**
   - Check "My table has headers"
   - Name each table appropriately (Table Tools → Design → Table Name)

---

## 📋 Dashboard Sheet Setup

### Create New Sheet: "Dashboard"

1. **Right-click** on sheet tabs → **Insert** → **Worksheet**
2. **Rename** to "Dashboard"
3. **Format background**: Light gray or white
4. **Add title**: "Retail Analytics Dashboard" (Font: Arial, Size: 24, Bold)

---

## 📊 Section 1: KPI Cards (Top Row)

### Create 6 KPI Cards Using Formulas

**Position**: Cells B2:G5 (merge cells for each KPI)

#### KPI 1: Total Revenue (B2:B5)
```excel
=TEXT(SUM(powerbi_ready[NETAMT]), "$#,##0,,.00""B""")
```
- **Format**: Merge B2:B5
- **Font**: Size 28, Bold, Blue
- **Border**: Thick outline
- **Label** (below): "Total Revenue"

#### KPI 2: Total Transactions (C2:C5)
```excel
=TEXT(COUNTA(powerbi_ready[NETAMT]), "#,##0")
```
- **Format**: Merge C2:C5
- **Font**: Size 28, Bold, Green
- **Label**: "Total Transactions"

#### KPI 3: Avg Transaction Value (D2:D5)
```excel
=TEXT(AVERAGE(powerbi_ready[NETAMT]), "$#,##0")
```
- **Format**: Merge D2:D5
- **Font**: Size 28, Bold, Orange
- **Label**: "Avg Transaction"

#### KPI 4: Total Units Sold (E2:E5)
```excel
=TEXT(SUM(powerbi_ready[Qty]), "#,##0")
```
- **Format**: Merge E2:E5
- **Font**: Size 28, Bold, Red
- **Label**: "Units Sold"

#### KPI 5: Avg Discount % (F2:F5)
```excel
=TEXT(AVERAGE(powerbi_ready[DiscountPct]), "0.0") & "%"
```
- **Format**: Merge F2:F5
- **Font**: Size 28, Bold, Purple
- **Label**: "Avg Discount"

#### KPI 6: Avg Conversion Rate (G2:G5)
```excel
=TEXT(AVERAGE(powerbi_ready[ConversionPct]), "0.0") & "%"
```
- **Format**: Merge G2:G5
- **Font**: Size 28, Bold, Teal
- **Label**: "Conversion Rate"

---

## 📊 Section 2: Pivot Tables & Charts

### Chart 1: Revenue by Category (B7:D25)

1. **Insert Pivot Table**
   - Select `powerbi_ready` table
   - **Insert** → **PivotTable**
   - Place in: Dashboard!B7

2. **Configure Pivot Table**
   - **Rows**: Category
   - **Values**: Sum of NETAMT
   - **Sort**: Descending by Sum of NETAMT

3. **Create Pie Chart**
   - Select Pivot Table
   - **Insert** → **Pie Chart** → **Pie**
   - **Chart Title**: "Revenue by Category"
   - **Position**: Next to pivot table
   - **Size**: 300x300 pixels
   - **Colors**: Assign distinct colors (Blue, Red, Green, Orange)

### Chart 2: Monthly Revenue Trend (E7:G25)

1. **Insert Pivot Table**
   - **Rows**: MonthName (sort by Month number)
   - **Values**: Sum of NETAMT
   - Position: E7

2. **Create Column Chart**
   - **Insert** → **Column Chart** → **Clustered Column**
   - **Chart Title**: "Monthly Revenue Performance"
   - **Format**: 
     - Data labels: Show on top
     - Colors: Gradient blue

### Chart 3: Store Performance (B27:D45)

1. **Insert Pivot Table**
   - **Rows**: Store
   - **Values**: Sum of NETAMT
   - **Sort**: Descending
   - Position: B27

2. **Create Bar Chart**
   - **Insert** → **Bar Chart** → **Clustered Bar**
   - **Chart Title**: "Revenue by Store"
   - **Format**: Horizontal bars, blue color

### Chart 4: Day of Week Analysis (E27:G45)

1. **Insert Pivot Table**
   - **Rows**: DayName (order: Mon-Sun)
   - **Values**: Sum of NETAMT, Count of NETAMT
   - Position: E27

2. **Create Column Chart**
   - **Insert** → **Column Chart** → **Clustered Column**
   - **Chart Title**: "Day of Week Performance"
   - **Format**: Weekend days in different color

### Chart 5: Top 10 SubCategories (B47:D65)

1. **Insert Pivot Table**
   - **Rows**: Category, SubCategory
   - **Values**: Sum of NETAMT
   - **Filter**: Top 10 by Sum of NETAMT
   - Position: B47

2. **Create Bar Chart**
   - **Insert** → **Bar Chart** → **Clustered Bar**
   - **Chart Title**: "Top 10 SubCategories"
   - **Format**: Horizontal bars, gradient colors

### Chart 6: Discount Impact (E47:G65)

1. **Insert Pivot Table**
   - **Rows**: DiscountSegment
   - **Values**: Sum of NETAMT, Average of Qty
   - Position: E47

2. **Create Column Chart**
   - **Insert** → **Column Chart** → **Clustered Column**
   - **Chart Title**: "Discount Impact on Revenue & Quantity"

---

## 🎛️ Section 3: Slicers (Interactive Filters)

### Add Slicers for Interactivity

1. **Date Range Slicer**
   - **Insert** → **Slicer**
   - Field: Date
   - **Type**: Timeline (Insert → Timeline)
   - **Position**: Top right (H2:I5)
   - **Format**: Blue theme

2. **Store Slicer**
   - Field: Store
   - **Position**: H7:H15
   - **Format**: Tile style, multiple selection enabled

3. **Category Slicer**
   - Field: Category
   - **Position**: H17:H25
   - **Format**: Tile style, multiple selection enabled

4. **Price Segment Slicer**
   - Field: PriceSegment
   - **Position**: H27:H35
   - **Format**: Horizontal tiles

### Connect Slicers to All Pivot Tables

1. Right-click on slicer → **Report Connections**
2. Check all pivot tables
3. Click OK

---

## 📊 Section 4: Additional Analysis Sheets

### Sheet 2: "Detailed Analysis"

**Table 1: Store Performance Summary**
- Source: `store_performance.csv`
- **Columns**: Store, Total_Revenue, Avg_Transaction, Avg_Conversion, Performance_Score
- **Formatting**:
  - Conditional formatting: Data bars on revenue
  - Color scale on performance score (red-yellow-green)

**Table 2: Monthly Trend**
- Source: `monthly_trend.csv`
- **Columns**: MonthName, Revenue, Units_Sold, Avg_Discount, Revenue_Growth_%
- **Formatting**:
  - Line chart for revenue trend
  - Sparklines for growth %

### Sheet 3: "Category Deep Dive"

**Pivot Table 1: Category × SubCategory Matrix**
- **Rows**: Category
- **Columns**: SubCategory
- **Values**: Sum of NETAMT
- **Format**: Heat map conditional formatting

**Pivot Table 2: Category Performance Metrics**
- **Rows**: Category
- **Values**: 
  - Sum of NETAMT
  - Count of transactions
  - Average of NETAMT
  - Average of DiscountPct
- **Format**: Table with data bars

### Sheet 4: "Time Analysis"

**Chart 1: Daily Revenue Trend**
- Line chart with date on X-axis
- Add 7-day moving average trendline
- Format: Smooth line

**Chart 2: Quarter Comparison**
- Pivot table: Quarter vs Revenue
- Column chart showing quarterly performance

**Chart 3: Weekend vs Weekday**
- Pivot table: IsWeekend (grouped) vs Revenue
- Pie chart showing split

---

## 🎨 Formatting & Design

### Color Scheme
```
Primary Blue:    RGB(52, 152, 219)   #3498db
Success Green:   RGB(46, 204, 113)   #2ecc71
Warning Orange:  RGB(243, 156, 18)   #f39c12
Danger Red:      RGB(231, 76, 60)    #e74c3c
Neutral Gray:    RGB(149, 165, 166)  #95a5a6
```

### Apply Consistent Formatting

1. **Headers**: Arial, 14pt, Bold, Blue
2. **KPIs**: Arial, 28pt, Bold, Color-coded
3. **Charts**: 
   - Title: 14pt, Bold
   - Data labels: 10pt
   - Gridlines: Light gray
   - Border: Thin gray

4. **Tables**:
   - Header row: Blue background, white text
   - Alternating rows: White and light gray
   - Borders: Thin gray lines

---

## 📐 Layout Tips

### Grid System (Based on A1:Z100)

**Top Section (Rows 1-5)**: Dashboard title + KPI cards
**Middle Section (Rows 7-45)**: Main charts (3 columns × 2 rows)
**Bottom Section (Rows 47-65)**: Additional charts
**Right Section (Columns H-I)**: Slicers and filters

### Alignment
- Use **Align** tools (Drawing Tools → Align)
- **Distribute Horizontally** for even spacing
- **Snap to Grid** for precision

---

## 📊 Advanced Features

### 1. Dynamic Date Filter

Create named range for date criteria:
```excel
=DATE(YEAR(TODAY()),MONTH(TODAY()),1)  'First day of current month
```

Use in formulas:
```excel
=SUMIFS(powerbi_ready[NETAMT], powerbi_ready[Date], ">="&StartDate)
```

### 2. Top N Analysis

Formula for Top 5 categories:
```excel
=LARGE(CategoryRevenue, ROW()-1)
```

### 3. Sparklines

Add mini charts in cells:
- Select cell range
- **Insert** → **Sparklines** → **Line**
- Configure data range

### 4. Conditional Formatting Rules

**Revenue Performance**:
- Green: >$500K
- Yellow: $200K-$500K
- Red: <$200K

**Growth Indicators**:
- ↑ for positive growth
- ↓ for negative growth

### 5. Data Validation (Dropdowns)

Create dropdown for quick filters:
- **Data** → **Data Validation**
- **List**: Store names or categories
- Use in formulas with IF statements

---

## 🔢 Useful Formulas

### Growth Calculation
```excel
=(CurrentMonth - PreviousMonth) / PreviousMonth
```

### Moving Average (7-day)
```excel
=AVERAGE(OFFSET(A1,-6,0,7,1))
```

### Rank Stores by Revenue
```excel
=RANK(B2, $B$2:$B$6, 0)
```

### Percentage of Total
```excel
=B2/SUM($B$2:$B$6)
```

### Weekend Revenue
```excel
=SUMIF(powerbi_ready[IsWeekend], 1, powerbi_ready[NETAMT])
```

---

## 📱 Dashboard Interactivity

### Add Buttons for Navigation

1. **Insert** → **Shapes** → **Rectangle**
2. **Format**: Blue fill, white text, rounded corners
3. **Right-click** → **Assign Macro** or **Link**
4. Create buttons:
   - "Refresh Data"
   - "Export PDF"
   - "Reset Filters"
   - "Go to Details"

### Hyperlinks Between Sheets

```excel
=HYPERLINK("#'Detailed Analysis'!A1", "View Details")
```

---

## 💾 Save & Share

### Save as Excel Dashboard
- **File** → **Save As**
- **File Type**: Excel Workbook (*.xlsx)
- Name: "Retail_Analytics_Dashboard.xlsx"

### Protect Dashboard
- **Review** → **Protect Sheet**
- Allow: Use PivotTables, Use Slicers
- Prevent: Deleting columns, rows

### Share Options

**Option 1: Email**
- **File** → **Share** → **Email**
- Attach workbook

**Option 2: OneDrive/SharePoint**
- **File** → **Share** → **Save to Cloud**
- Share link with permissions

**Option 3: Export PDF**
- **File** → **Export** → **Create PDF/XPS**
- Select "Dashboard" sheet only

---

## 🔧 Troubleshooting

### Issue: Pivot Table Not Refreshing
- **Solution**: Right-click → Refresh or **Data** → **Refresh All**

### Issue: Charts Showing Errors
- **Solution**: Check source data range, update if needed

### Issue: Slicers Not Working
- **Solution**: Reconnect to pivot tables (Report Connections)

### Issue: Slow Performance
- **Solution**: 
  - Reduce data rows (use aggregated tables)
  - Turn off automatic calculations: **Formulas** → **Calculation Options** → **Manual**

---

## 📚 Excel Shortcuts

- **Ctrl + R**: Refresh all pivot tables
- **Alt + F1**: Create chart from selected data
- **Ctrl + T**: Create table from range
- **Alt + N + V**: Insert PivotTable
- **F9**: Recalculate formulas

---

## ✅ Dashboard Checklist

- [ ] All data imported and formatted as tables
- [ ] KPI cards created with formulas
- [ ] 6 main charts created and formatted
- [ ] Slicers added and connected
- [ ] Conditional formatting applied
- [ ] Color scheme consistent
- [ ] Additional analysis sheets completed
- [ ] Navigation buttons added
- [ ] Dashboard protected
- [ ] File saved and backed up
- [ ] Shared with stakeholders

---

## 🎯 Final Tips

1. **Keep it Simple**: Don't overcrowd the dashboard
2. **Use White Space**: Makes it easier to read
3. **Test Interactivity**: Click all slicers to ensure they work
4. **Print Preview**: Check how it looks on paper
5. **Document Formulas**: Add comments for complex calculations
6. **Regular Updates**: Refresh data weekly/monthly
7. **Backup**: Save versions with dates

---

**Your Excel Dashboard is ready for business insights! 📊✨**
