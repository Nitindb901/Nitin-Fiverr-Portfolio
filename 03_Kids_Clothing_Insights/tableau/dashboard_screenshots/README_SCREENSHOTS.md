# 📸 Dashboard Screenshots

This folder will contain high-quality screenshots of all 5 Tableau dashboards.

---

## 📂 Expected Files

After building Tableau dashboards, capture and save screenshots here:

### Dashboard Screenshots (PNG format, 1920x1080)

1. **01_sales_performance.png** ⏳
   - Sales Performance Dashboard
   - Shows: Revenue map, category bars, monthly trends, store rankings

2. **02_customer_analytics.png** ⏳
   - Customer Analytics Dashboard
   - Shows: RFM scatter plot, segment pie chart, cohort heatmap, CLV bars

3. **03_inventory_management.png** ⏳
   - Inventory Management Dashboard
   - Shows: Stock gauges, reorder alerts, supplier scorecard, turnover chart

4. **04_executive_summary.png** ⏳
   - Executive Summary Dashboard
   - Shows: KPI cards, P&L waterfall, YoY comparison, forecast, scorecard

5. **05_ecommerce_analytics.png** ⏳
   - E-commerce Analytics Dashboard
   - Shows: Conversion funnel, traffic sources, device comparison, abandonment reasons

---

## 📸 How to Capture Screenshots

### Method 1: Tableau Built-in Export (Recommended)

```
1. Open dashboard in Tableau Desktop
2. Dashboard → Export Image
3. Resolution: High (2x)
4. Format: PNG
5. Save to this folder
6. Naming: 01_sales_performance.png, 02_customer_analytics.png, etc.
```

**Settings**:
- Resolution: 1920x1080 or higher
- DPI: 300 for print quality
- Background: White

### Method 2: Tableau Server Download

```
1. Publish dashboard to Tableau Server
2. Open in web browser
3. Click Download → Image
4. Select PNG format
5. Save to this folder
```

### Method 3: Manual Screenshot

```
1. Set browser/Tableau to fullscreen (F11)
2. Use Windows Snipping Tool (Win + Shift + S)
3. Select entire dashboard
4. Save as PNG to this folder
```

---

## 🎨 Screenshot Guidelines

### Quality Standards

✅ **DO**:
- Capture at **1920x1080** resolution minimum
- Use **PNG format** (lossless quality)
- Include **all dashboard elements** (filters, titles, charts)
- Ensure **data is loaded** (no loading spinners)
- Use **representative data** (not empty/test data)
- Apply **default filters** (show typical use case)
- Ensure **text is readable** at full size

❌ **DON'T**:
- Use JPEG (lossy compression, artifacts)
- Crop important elements
- Include personal/sensitive data
- Capture with browser UI visible (address bar, bookmarks)
- Use low resolution (<1280x720)
- Include loading states or errors

### Naming Convention

Format: `##_dashboard_name.png`

- Use leading zeros (01, 02, not 1, 2)
- Lowercase with underscores
- Descriptive but concise
- Match dashboard order

Examples:
- ✅ `01_sales_performance.png`
- ✅ `02_customer_analytics.png`
- ❌ `Sales Dashboard Screenshot.png`
- ❌ `dashboard1.jpg`

---

## 🔗 Usage in Documentation

### Update Main README.md

After capturing screenshots, update main README with:

```markdown
## 📸 Dashboard Previews

### 1. Sales Performance Dashboard
![Sales Performance](tableau/dashboard_screenshots/01_sales_performance.png)

### 2. Customer Analytics Dashboard
![Customer Analytics](tableau/dashboard_screenshots/02_customer_analytics.png)

### 3. Inventory Management Dashboard
![Inventory Management](tableau/dashboard_screenshots/03_inventory_management.png)

### 4. Executive Summary Dashboard
![Executive Summary](tableau/dashboard_screenshots/04_executive_summary.png)

### 5. E-commerce Analytics Dashboard
![E-commerce Analytics](tableau/dashboard_screenshots/05_ecommerce_analytics.png)
```

### GitHub Display

GitHub will automatically render PNG images in README files when using relative paths.

**Image Size Recommendations**:
- Original: 1920x1080 (full quality)
- Display width in README: 100% or 800px
- GitHub auto-scales for mobile

---

## 📊 Screenshot Checklist

Before considering screenshots complete:

**Pre-Capture**:
- [ ] All 5 dashboards built in Tableau
- [ ] Data connections working
- [ ] Filters set to default/typical values
- [ ] No errors or warnings visible
- [ ] Charts displaying correctly

**Capture Process**:
- [ ] Dashboard 1 (Sales) screenshot captured
- [ ] Dashboard 2 (Customer) screenshot captured
- [ ] Dashboard 3 (Inventory) screenshot captured
- [ ] Dashboard 4 (Executive) screenshot captured
- [ ] Dashboard 5 (E-commerce) screenshot captured

**Post-Capture**:
- [ ] All files named correctly
- [ ] All files are PNG format
- [ ] Resolution is 1920x1080 or higher
- [ ] File sizes reasonable (500KB - 5MB each)
- [ ] Images display correctly when opened
- [ ] README.md updated with image links
- [ ] Images pushed to GitHub
- [ ] Images render correctly on GitHub

---

## 📏 File Size Expectations

| Screenshot | Expected Size | Notes |
|------------|---------------|-------|
| Sales Performance | 1-3 MB | Map + multiple charts |
| Customer Analytics | 2-4 MB | Scatter plot + heatmap (complex) |
| Inventory Management | 1-2 MB | Tables + gauges |
| Executive Summary | 1-2 MB | KPI cards + charts |
| E-commerce Analytics | 2-3 MB | Funnel + multiple charts |
| **Total** | **7-14 MB** | All 5 screenshots |

**Optimization**:
- PNG compression tools: TinyPNG, ImageOptim
- Balance: Quality vs. file size
- GitHub limit: 100 MB per file (plenty of headroom)

---

## 🎨 Alternative: Animated GIFs

For interactive demonstrations:

### Create Dashboard GIF

1. **Use screen recording tool** (OBS Studio, ScreenToGif)
2. **Record dashboard interaction**:
   - Apply filters
   - Drill-down
   - Hover tooltips
   - Navigate between sheets
3. **Save as GIF** (max 10MB for GitHub)
4. **Name**: `01_sales_performance_demo.gif`

**GIF Guidelines**:
- Duration: 10-30 seconds
- Frame rate: 10-15 fps
- Resolution: 1280x720 (smaller than screenshots)
- Loop: Infinite
- Size: <10 MB (optimize if needed)

---

## 📞 Support

**Need help with screenshots?**
- See: `../TABLEAU_DEVELOPMENT_GUIDE.md` for dashboard build
- See: `../../documentation/Tableau_Usage_Guide.md` for usage
- Contact: nitindb901@gmail.com

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 2024 | Initial screenshot guide created |

---

<div align="center">

**Ready for Screenshots!**

Build your Tableau dashboards first, then return here to capture professional-quality screenshots for your portfolio.

</div>
