# Data Dictionary - Retail Analytics Dashboard

## Overview
This document describes all fields available in the dashboard datasets for the Retail Analytics project.

---

## Main Fact Table: `powerbi_ready.csv`

### Date & Time Dimensions

| Field Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| Date | Date | Transaction date | 2024-01-15 |
| Year | Integer | Year of transaction | 2024 |
| Month | Integer | Month number (1-12) | 1 |
| MonthName | Text | Full month name | January |
| Week | Integer | ISO week number (1-53) | 3 |
| Quarter | Integer | Quarter (1-4) | 1 |
| DayOfWeek | Integer | Day of week (0=Monday, 6=Sunday) | 0 |
| DayName | Text | Full day name | Monday |
| IsWeekend | Boolean | 1 if Saturday/Sunday, 0 otherwise | 0 |

### Location Dimension

| Field Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| Store | Text | Store identifier | Store_A |

### Product Dimensions

| Field Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| Category | Text | Main product category | Electronics |
| SubCategory | Text | Product subcategory | Mobile |
| Brand | Text | Product brand name | Samsung |
| SKU | Text | Stock Keeping Unit identifier | ELE-MOB-1234 |

### Transaction Metrics

| Field Name | Data Type | Description | Example | Unit |
|------------|-----------|-------------|---------|------|
| MRP | Decimal | Maximum Retail Price | 25000.00 | $ |
| SellingPrice | Decimal | Actual selling price after discount | 20000.00 | $ |
| Qty | Integer | Quantity of items sold | 2 | units |
| NETAMT | Decimal | Net transaction amount (SellingPrice × Qty) | 40000.00 | $ |
| DiscountPct | Decimal | Discount percentage applied | 20.00 | % |
| DiscountAmount | Decimal | Discount amount in dollars | 5000.00 | $ |
| AvgUnitPrice | Decimal | Average price per unit in transaction | 20000.00 | $ |

### Customer Behavior Metrics

| Field Name | Data Type | Description | Example | Unit |
|------------|-----------|-------------|---------|------|
| Footfall | Integer | Daily store footfall count | 1250 | customers |
| ConversionPct | Decimal | Conversion rate (transactions/footfall) | 25.50 | % |

### Derived Segments

| Field Name | Data Type | Description | Possible Values |
|------------|-----------|-------------|----------------|
| PriceSegment | Text | Price category based on MRP | Budget (<$500)<br>Economy ($500-$2,000)<br>Mid-Range ($2,000-$10,000)<br>Premium (>$10,000) |
| DiscountSegment | Text | Discount category | No Discount (0%)<br>Low Discount (<10%)<br>Medium Discount (10-25%)<br>High Discount (>25%) |
| TransactionSize | Text | Transaction value category | Small (<$500)<br>Medium ($500-$2,000)<br>Large ($2,000-$10,000)<br>Extra Large (>$10,000) |

---

## Daily Aggregation: `daily_aggregation.csv`

| Field Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| Date | Date | Transaction date | 2024-01-15 |
| Store | Text | Store identifier | Store_A |
| Revenue | Decimal | Total daily revenue | 125000.50 |
| Units_Sold | Integer | Total units sold | 450 |
| Footfall | Integer | Average daily footfall | 1250 |
| Conversion_Rate | Decimal | Average conversion rate | 25.50 |
| Avg_Discount | Decimal | Average discount percentage | 18.75 |
| Transactions | Integer | Number of transactions | 120 |
| Avg_Transaction_Value | Decimal | Average transaction value | 1041.67 |
| Year | Integer | Year | 2024 |
| Month | Integer | Month number | 1 |
| Week | Integer | Week number | 3 |
| DayName | Text | Day of week | Monday |

---

## Category Aggregation: `category_aggregation.csv`

| Field Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| Category | Text | Main product category | Electronics |
| SubCategory | Text | Product subcategory | Mobile |
| Total_Revenue | Decimal | Total revenue for subcategory | 2500000.00 |
| Avg_Transaction | Decimal | Average transaction value | 1250.50 |
| Transaction_Count | Integer | Number of transactions | 2000 |
| Total_Units | Integer | Total units sold | 3500 |
| Avg_Discount | Decimal | Average discount percentage | 19.25 |
| Unique_SKUs | Integer | Number of unique products | 450 |
| Revenue_Percent | Decimal | Percentage of total revenue | 15.75 |

---

## Store Performance: `store_performance.csv`

| Field Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| Store | Text | Store identifier | Store_A |
| Total_Revenue | Decimal | Total revenue | 3500000.00 |
| Avg_Transaction | Decimal | Average transaction value | 1150.25 |
| Total_Units | Integer | Total units sold | 12500 |
| Avg_Footfall | Integer | Average daily footfall | 1250 |
| Avg_Conversion | Decimal | Average conversion rate | 26.50 |
| Avg_Discount | Decimal | Average discount percentage | 17.80 |
| Unique_SKUs | Integer | Number of unique products | 2800 |
| Transactions | Integer | Total transactions | 3040 |
| Performance_Score | Decimal | Overall performance score (0-100) | 85.50 |

---

## Monthly Trend: `monthly_trend.csv`

| Field Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| Year | Integer | Year | 2024 |
| Month | Integer | Month number | 1 |
| MonthName | Text | Month name | January |
| Revenue | Decimal | Monthly revenue | 1250000.00 |
| Units_Sold | Integer | Units sold in month | 5600 |
| Avg_Discount | Decimal | Average discount percentage | 18.50 |
| Avg_Conversion | Decimal | Average conversion rate | 25.75 |
| Transactions | Integer | Number of transactions | 1850 |
| Avg_Transaction_Value | Decimal | Average transaction value | 675.68 |
| Revenue_Growth_% | Decimal | Month-over-month revenue growth | 5.25 |

---

## KPI Summary: `kpi_summary.csv`

Contains high-level business metrics for executive dashboards.

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| Total_Revenue | Decimal | Total revenue across all stores and periods |
| Total_Transactions | Integer | Total number of transactions |
| Total_Units_Sold | Integer | Total units sold |
| Avg_Transaction_Value | Decimal | Average transaction value |
| Avg_Discount_Percent | Decimal | Average discount percentage |
| Avg_Conversion_Rate | Decimal | Average conversion rate |
| Unique_SKUs | Integer | Total unique products |
| Unique_Brands | Integer | Total unique brands |
| Number_of_Stores | Integer | Total number of stores |
| Number_of_Categories | Integer | Total number of categories |
| Date_Range | Text | Analysis period |
| Total_Days | Integer | Number of days in analysis |
| Avg_Daily_Revenue | Decimal | Average daily revenue |
| Peak_Revenue_Day | Date | Date with highest revenue |
| Peak_Revenue_Amount | Decimal | Highest single-day revenue |

---

## Top Performers: `top_skus.csv` & `top_brands.csv`

### top_skus.csv

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| SKU | Text | Stock Keeping Unit identifier |
| Category | Text | Product category |
| Brand | Text | Brand name |
| Revenue | Decimal | Total revenue for SKU |

### top_brands.csv

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| Brand | Text | Brand name |
| Category | Text | Main category |
| Revenue | Decimal | Total revenue for brand |

---

## Business Logic & Calculations

### Revenue Calculation
```
NETAMT = SellingPrice × Qty
```

### Discount Calculation
```
DiscountPct = ((MRP - SellingPrice) / MRP) × 100
DiscountAmount = MRP - SellingPrice
```

### Conversion Rate
```
ConversionPct = (Transactions / Footfall) × 100
```

### Performance Score (Store)
```
Performance_Score = (Revenue_Score × 0.4) + (Conversion_Score × 0.3) + (Transaction_Score × 0.3)
where each score is normalized to 0-100 scale
```

---

## Data Quality Notes

1. **No Missing Values**: All datasets have been cleaned and validated
2. **Date Range**: January 1, 2024 - December 31, 2024 (12 months)
3. **Currency**: All monetary values in US Dollars ($)
4. **Precision**: Financial values rounded to 2 decimal places
5. **Outliers**: Extreme outliers removed using IQR method (3× IQR threshold)

---

## Usage Recommendations

### For Power BI:
- Use `powerbi_ready.csv` as main fact table
- Create relationships using Date, Store, Category fields
- Use aggregation files for quick summary visuals

### For Excel:
- Import `daily_aggregation.csv` for pivot table analysis
- Use `category_aggregation.csv` for category comparisons
- Reference `kpi_summary.csv` for executive dashboards

### For Tableau:
- Connect to `powerbi_ready.csv` for detailed analysis
- Use extracts for better performance with large datasets
- Create calculated fields for custom metrics

---

## Contact & Support

For questions about this data dictionary or dataset:
- Review the README.md in the project root
- Check Python scripts in `/scripts` folder for data generation logic
- Examine Jupyter notebook in `/notebooks` for analysis examples

---

**Last Updated**: November 2024  
**Version**: 1.0  
**Data Owner**: Retail Analytics Team
