# Power BI Dashboard Setup Guide

## 📊 Complete Power BI Dashboard Creation

### Step 1: Import Data

1. **Open Power BI Desktop**

2. **Get Data from CSV**
   - Click "Get Data" → "Text/CSV"
   - Navigate to: `dashboard/powerbi_ready.csv`
   - Click "Load"

3. **Import Additional Tables** (Optional for detailed analysis)
   - `dashboard/daily_aggregation.csv`
   - `dashboard/category_aggregation.csv`
   - `dashboard/store_performance.csv`
   - `dashboard/monthly_trend.csv`

### Step 2: Create Relationships (if using multiple tables)

Go to "Model" view and create relationships:
- **powerbi_ready** [Date] → **daily_aggregation** [Date]
- **powerbi_ready** [Store] → **store_performance** [Store]
- **powerbi_ready** [Category] → **category_aggregation** [Category]

### Step 3: Create Measures (DAX Formulas)

Click "Modeling" → "New Measure" and add these:

```dax
Total Revenue = SUM(powerbi_ready[NETAMT])

Total Transactions = COUNTROWS(powerbi_ready)

Avg Transaction Value = AVERAGE(powerbi_ready[NETAMT])

Total Units Sold = SUM(powerbi_ready[Qty])

Avg Discount = AVERAGE(powerbi_ready[DiscountPct])

Avg Conversion Rate = AVERAGE(powerbi_ready[ConversionPct])

Revenue Growth MoM = 
VAR CurrentMonth = [Total Revenue]
VAR PreviousMonth = CALCULATE([Total Revenue], DATEADD(powerbi_ready[Date], -1, MONTH))
RETURN DIVIDE(CurrentMonth - PreviousMonth, PreviousMonth, 0)

Weekend Revenue = 
CALCULATE([Total Revenue], powerbi_ready[IsWeekend] = 1)

Weekday Revenue = 
CALCULATE([Total Revenue], powerbi_ready[IsWeekend] = 0)

High Discount Revenue = 
CALCULATE([Total Revenue], powerbi_ready[DiscountPct] > 20)

Premium Segment Revenue = 
CALCULATE([Total Revenue], powerbi_ready[PriceSegment] = "Premium")
```

---

## 📋 Dashboard Page 1: Executive Overview

### KPI Cards (Top Row)

Create 6 Card visuals with these measures:
1. **Total Revenue** - Format: Currency, Billions
2. **Total Transactions** - Format: Number with comma separator
3. **Avg Transaction Value** - Format: Currency
4. **Total Units Sold** - Format: Number
5. **Avg Discount %** - Format: Percentage
6. **Avg Conversion Rate** - Format: Percentage

**Formatting Tips:**
- Font Size: 32 (Value), 14 (Label)
- Colors: Use your brand colors
- Add icons if available

### Revenue Trend (Line Chart)

- **Visual**: Line Chart
- **X-Axis**: Date (Hierarchy: Year → Month → Day)
- **Y-Axis**: Total Revenue
- **Legend**: None
- **Analytics Line**: Add 7-day moving average
- **Formatting**:
  - Data colors: Blue gradient
  - Show data labels: No
  - X-axis title: "Date"
  - Y-axis title: "Revenue ($)"

### Category Revenue (Donut Chart)

- **Visual**: Donut Chart
- **Legend**: Category
- **Values**: Total Revenue
- **Formatting**:
  - Detail labels: Category, Value, Percentage
  - Legend position: Right
  - Colors: Assign distinct colors to each category

### Monthly Performance (Clustered Column Chart)

- **Visual**: Clustered Column Chart
- **X-Axis**: MonthName
- **Y-Axis**: Total Revenue
- **Formatting**:
  - Data colors: Gradient (light to dark)
  - Show data labels: Yes (on top)
  - X-axis title: "Month"

---

## 📋 Dashboard Page 2: Sales Analysis

### Revenue by Store (Bar Chart)

- **Visual**: Clustered Bar Chart
- **Y-Axis**: Store
- **X-Axis**: Total Revenue
- **Formatting**:
  - Sort by: Total Revenue (Descending)
  - Data labels: Show
  - Colors: Blue gradient

### Day of Week Performance (Column Chart)

- **Visual**: Clustered Column Chart
- **X-Axis**: DayName
- **Y-Axis**: Total Revenue, Total Transactions
- **Legend**: Metric Name
- **Formatting**:
  - Colors: Different for Revenue vs Transactions
  - Highlight weekends with different color

### Top 10 SubCategories (Bar Chart)

- **Visual**: Horizontal Bar Chart
- **Y-Axis**: SubCategory
- **X-Axis**: Total Revenue
- **Filters**: Top N = 10 by Total Revenue
- **Formatting**:
  - Sort: Descending
  - Data labels: Show
  - Colors: Gradient

### Discount Impact (Scatter Chart)

- **Visual**: Scatter Chart
- **X-Axis**: DiscountPct
- **Y-Axis**: NETAMT
- **Details**: Category
- **Size**: Qty
- **Formatting**:
  - Play axis: MonthName
  - Colors by Category

---

## 📋 Dashboard Page 3: Store Performance

### Store Performance Table

- **Visual**: Table
- **Columns**:
  - Store
  - Total Revenue
  - Total Transactions
  - Avg Transaction Value
  - Avg Conversion Rate
  - Avg Discount
- **Formatting**:
  - Conditional formatting on revenue (Data bars)
  - Sort by Total Revenue descending

### Store Comparison (Radar Chart)

- **Visual**: Radar Chart (if available, else use Line chart)
- **Category**: Metric (Revenue, Conversion, Transactions)
- **Values**: Normalized values by Store
- **Legend**: Store

### Store Revenue Over Time (Line Chart)

- **Visual**: Line Chart
- **X-Axis**: Date
- **Y-Axis**: Total Revenue
- **Legend**: Store
- **Formatting**:
  - Different color per store
  - Show markers

---

## 📋 Dashboard Page 4: Product Analysis

### Price Segment Analysis (Stacked Column)

- **Visual**: Stacked Column Chart
- **X-Axis**: PriceSegment
- **Y-Axis**: Total Revenue
- **Legend**: Category
- **Formatting**:
  - Order: Budget, Economy, Mid-Range, Premium
  - Colors by category

### Brand Performance (Tree Map)

- **Visual**: Tree Map
- **Group**: Brand
- **Values**: Total Revenue
- **Formatting**:
  - Show data labels
  - Colors: By value (gradient)

### Discount Segment Analysis (Clustered Bar)

- **Visual**: Clustered Bar Chart
- **Y-Axis**: DiscountSegment
- **X-Axis**: Total Revenue, Avg Qty
- **Legend**: Metric
- **Formatting**:
  - Order: No Discount → High Discount
  - Data labels: Show

---

## 📋 Dashboard Page 5: Time Intelligence

### Monthly Trend with Growth (Line + Column)

- **Visual**: Line and Clustered Column Chart
- **X-Axis**: MonthName
- **Column Y-Axis**: Total Revenue
- **Line Y-Axis**: Revenue Growth MoM
- **Formatting**:
  - Columns: Blue
  - Line: Red
  - Show both axes

### Quarter Comparison (Matrix)

- **Visual**: Matrix
- **Rows**: Quarter, MonthName
- **Values**: Total Revenue, Total Transactions, Avg Discount
- **Formatting**:
  - Conditional formatting on revenue
  - Show subtotals

### Calendar Heatmap (Custom Visual)

- **Install**: Calendar Heatmap from AppSource
- **Date**: Date
- **Value**: Total Revenue
- **Formatting**:
  - Color scale: Light to dark

---

## 🎨 Slicers (Add to All Pages)

### Date Range Slicer
- **Type**: Between
- **Field**: Date
- **Style**: Slider

### Store Slicer
- **Type**: Dropdown or Tile
- **Field**: Store
- **Allow multiple selections**: Yes

### Category Slicer
- **Type**: Dropdown
- **Field**: Category
- **Allow multiple selections**: Yes

### Price Segment Slicer
- **Type**: Tile
- **Field**: PriceSegment
- **Layout**: Horizontal

---

## 🎯 Advanced Features

### 1. Drill-Through Page (Detail View)

Create a new page "Transaction Details":
- **Drill-through filter**: Add Category, Store
- **Visuals**: 
  - Detailed table with all fields
  - Transaction trend for selected item
  - Back button to return

### 2. Bookmarks (For Story Telling)

Create bookmarks for:
- Executive View
- Weekend Analysis
- Festival Performance
- Store Comparison

### 3. Tooltips (Custom)

Create tooltip page:
- Small page with key metrics
- Apply to main visuals for hover details

### 4. Mobile Layout

- Switch to "Mobile Layout" view
- Rearrange visuals for phone screens
- Keep only essential KPIs and charts

---

## 📱 Publishing

### Publish to Power BI Service

1. Click "Publish" in toolbar
2. Sign in to Power BI account
3. Select workspace
4. Click "Publish"

### Schedule Refresh (if using database)

1. Go to Power BI Service
2. Find your dataset
3. Settings → Scheduled refresh
4. Configure refresh schedule

### Share Dashboard

1. Click "Share" button
2. Enter email addresses
3. Set permissions
4. Send invitation

---

## 🎨 Design Best Practices

### Color Scheme
- **Primary**: #3498db (Blue)
- **Secondary**: #2ecc71 (Green)
- **Alert**: #e74c3c (Red)
- **Warning**: #f39c12 (Orange)
- **Neutral**: #95a5a6 (Gray)

### Layout Tips
1. **KPIs at top**: Most important metrics visible first
2. **Grid alignment**: Use snap to grid (16x9)
3. **White space**: Don't overcrowd
4. **Consistent fonts**: Same font family throughout
5. **Logo**: Add company logo in corner

### Formatting Standards
- **Currency**: $#,##0.00
- **Percentage**: 0.00%
- **Numbers**: #,##0
- **Dates**: MMM DD, YYYY

---

## 🔧 Troubleshooting

### Issue: Slow Performance
- **Solution**: Reduce visual count, use aggregated tables

### Issue: Wrong Totals
- **Solution**: Check measure formulas, verify relationships

### Issue: Date Hierarchy Not Working
- **Solution**: Ensure Date column is Date data type

### Issue: Filters Not Working
- **Solution**: Check filter context and relationships

---

## 📚 Resources

- [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- [DAX Guide](https://dax.guide/)
- [Power BI Community](https://community.powerbi.com/)

---

## ✅ Checklist

- [ ] Data imported successfully
- [ ] Relationships created
- [ ] DAX measures added
- [ ] Page 1: Executive Overview complete
- [ ] Page 2: Sales Analysis complete
- [ ] Page 3: Store Performance complete
- [ ] Page 4: Product Analysis complete
- [ ] Page 5: Time Intelligence complete
- [ ] Slicers added and synced
- [ ] Formatting applied consistently
- [ ] Mobile layout configured
- [ ] Published to service
- [ ] Shared with stakeholders

---

**Dashboard is ready for business insights! 🚀**
