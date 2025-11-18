# Data Dictionary - Grocery + Fashion Dashboard

## Overview
This document describes all fields in the merged POS dataset and dashboard exports.

---

## 📊 Main Dataset: `merged_pos_data.csv`

### Transaction Information

| Field Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| **TransactionID** | String | Unique transaction identifier | `POS1_Store_A_00000001` |
| **POS_System** | String | Point of Sale system identifier | `POS1`, `POS2` |
| **Store** | String | Store identifier | `Store_A`, `Store_B`, etc. |
| **Date** | Date | Transaction date | `2024-01-15` |

### Product Information

| Field Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| **Category** | String | Main product category | `Grocery`, `Fashion` |
| **SubCategory** | String | Product subcategory | `FMCG`, `Men`, `Women`, etc. |
| **SKU_ID** | String | Stock Keeping Unit ID | `GROFMC15234` |
| **Brand** | String | Product brand | `BrandG1`, `BrandF3`, etc. |

### Pricing Information

| Field Name | Data Type | Description | Example | Range |
|------------|-----------|-------------|---------|-------|
| **MRP** | Float | Maximum Retail Price (INR) | `1250.00` | 50 - 15000 |
| **SellingPrice** | Float | Actual selling price (INR) | `1000.00` | 50 - 15000 |
| **DiscountPercent** | Integer | Discount applied (%) | `20` | 0 - 30 |
| **CostPrice** | Float | Cost price per unit (INR) | `800.00` | 40 - 12000 |

### Transaction Metrics

| Field Name | Data Type | Description | Example | Range |
|------------|-----------|-------------|---------|-------|
| **Quantity** | Integer | Number of units sold | `2` | 1 - 5 |
| **NetAmount** | Float | Total transaction amount (INR) | `2000.00` | 50 - 75000 |
| **Profit** | Float | Profit amount (INR) | `400.00` | -500 - 30000 |
| **MarginPercent** | Float | Profit margin (%) | `25.00` | 5 - 60 |

### Stock Information

| Field Name | Data Type | Description | Example | Range |
|------------|-----------|-------------|---------|-------|
| **ManufacturingDate** | Date | Product manufacturing date | `2024-01-01` | Jan-Dec 2024 |
| **ExpiryDate** | Date | Product expiry date | `2025-01-01` | Jan-Dec 2025 |
| **StockAgeDays** | Integer | Age of stock in days | `45` | 0 - 180 |
| **DaysToExpiry** | Integer | Days until expiry | `320` | 30 - 730 |
| **StockAgeCategory** | String | Stock age classification | `Fresh`, `Normal`, `Ageing` | - |
| **StockHealth** | String | Stock health indicator | `Excellent`, `Good`, `Warning`, `Critical` | - |

### Temporal Features (Generated)

| Field Name | Data Type | Description | Example | Range |
|------------|-----------|-------------|---------|-------|
| **Year** | Integer | Transaction year | `2024` | 2024 |
| **Month** | Integer | Transaction month | `6` | 1 - 12 |
| **MonthName** | String | Month abbreviation | `Jun` | Jan - Dec |
| **Quarter** | Integer | Fiscal quarter | `2` | 1 - 4 |
| **DayOfWeek** | String | Day name | `Monday` | Mon - Sun |
| **WeekNumber** | Integer | ISO week number | `24` | 1 - 52 |
| **IsWeekend** | Integer | Weekend flag | `0` (No), `1` (Yes) | 0, 1 |

### Derived Categories

| Field Name | Data Type | Description | Example | Range |
|------------|-----------|-------------|---------|-------|
| **MarginCategory** | String | Margin classification | `Low`, `Medium`, `High`, `Very High` | - |
| **RevenueCategory** | String | Revenue classification | `Low`, `Medium`, `High`, `Very High` | - |

---

## 📈 Dashboard Exports

### 1. `category_performance.csv`

| Field | Description |
|-------|-------------|
| Category | Grocery or Fashion |
| Transactions | Total transaction count |
| TotalRevenue | Sum of revenue (INR) |
| AvgRevenue | Average revenue per transaction (INR) |
| TotalProfit | Sum of profit (INR) |
| AvgProfit | Average profit per transaction (INR) |
| AvgMargin | Average margin % |
| TotalQuantity | Total units sold |
| UniqueSKUs | Number of unique products |

### 2. `subcategory_performance.csv`

| Field | Description |
|-------|-------------|
| Category | Parent category |
| SubCategory | Subcategory name |
| Transactions | Transaction count |
| TotalRevenue | Revenue (INR) |
| AvgRevenue | Average revenue per transaction |
| TotalProfit | Profit (INR) |
| AvgMargin | Average margin % |
| TotalQuantity | Units sold |

### 3. `pos_comparison.csv`

| Field | Description |
|-------|-------------|
| POS_System | POS1 or POS2 |
| Store | Store name |
| Transactions | Transaction count |
| TotalRevenue | Revenue (INR) |
| TotalProfit | Profit (INR) |
| AvgMargin | Average margin % |
| TotalQuantity | Units sold |
| UniqueSKUs | Unique products |

### 4. `stock_ageing_overall.csv`

| Field | Description |
|-------|-------------|
| StockAgeCategory | Fresh, Normal, Ageing, Old |
| Transactions | Transaction count |
| TotalRevenue | Revenue (INR) |
| TotalQuantity | Units sold |
| AvgStockAge | Average stock age in days |

### 5. `stock_ageing_by_category.csv`

| Field | Description |
|-------|-------------|
| Category | Grocery or Fashion |
| StockAgeCategory | Stock age group |
| Transactions | Transaction count |
| TotalRevenue | Revenue (INR) |
| TotalQuantity | Units sold |
| AvgStockAge | Average age in days |

### 6. `margin_analysis.csv`

| Field | Description |
|-------|-------------|
| Category | Parent category |
| SubCategory | Subcategory name |
| AvgMargin | Average margin % |
| MinMargin | Minimum margin % |
| MaxMargin | Maximum margin % |
| TotalProfit | Total profit (INR) |
| TotalRevenue | Total revenue (INR) |
| ProfitMargin% | Profit as % of revenue |

### 7. `monthly_trends.csv`

| Field | Description |
|-------|-------------|
| YearMonth | Period (YYYY-MM) |
| Category | Grocery or Fashion |
| Transactions | Transaction count |
| Revenue | Revenue (INR) |
| Profit | Profit (INR) |
| Quantity | Units sold |

### 8. `brand_performance.csv`

| Field | Description |
|-------|-------------|
| Category | Parent category |
| Brand | Brand name |
| Transactions | Transaction count |
| TotalRevenue | Revenue (INR) |
| TotalProfit | Profit (INR) |
| AvgMargin | Average margin % |
| UniqueSKUs | Unique products |

### 9. `weekend_analysis.csv`

| Field | Description |
|-------|-------------|
| Category | Grocery or Fashion |
| Day_Type | Weekday or Weekend |
| Transactions | Transaction count |
| TotalRevenue | Revenue (INR) |
| AvgRevenue | Average revenue per transaction |
| TotalQuantity | Units sold |

### 10. `top_100_skus.csv`

| Field | Description |
|-------|-------------|
| SKU_ID | Product SKU identifier |
| Category | Parent category |
| SubCategory | Subcategory |
| Brand | Brand name |
| Transactions | Transaction count |
| TotalRevenue | Revenue (INR) |
| TotalProfit | Profit (INR) |
| TotalQuantity | Units sold |

### 11. `summary_kpis.csv`

| Field | Description |
|-------|-------------|
| Metric | KPI name |
| Value | Formatted value with units |

**Included Metrics:**
- Total Transactions
- Total Revenue (INR)
- Total Profit (INR)
- Average Margin (%)
- Total Quantity Sold
- Unique SKUs
- Unique Stores
- Fresh Stock (%)
- Ageing Stock (%)
- Average Transaction Value (INR)
- Grocery Revenue (INR)
- Fashion Revenue (INR)
- POS1 Revenue (INR)
- POS2 Revenue (INR)

---

## 📋 Category Definitions

### Grocery SubCategories

| SubCategory | Description | Examples |
|-------------|-------------|----------|
| **FMCG** | Fast Moving Consumer Goods | Packaged foods, beverages, personal care |
| **Staples** | Basic food items | Rice, wheat, pulses, cooking oil |
| **Dairy** | Dairy products | Milk, cheese, yogurt, butter |
| **Snacks** | Snack items | Chips, biscuits, chocolates |

### Fashion SubCategories

| SubCategory | Description | Examples |
|-------------|-------------|----------|
| **Men** | Men's clothing | Shirts, trousers, jackets |
| **Women** | Women's clothing | Dresses, tops, ethnic wear |
| **Kids** | Children's clothing | School wear, casual wear |
| **Accessories** | Fashion accessories | Bags, belts, watches, jewelry |

---

## 📊 Metric Calculations

### Margin Percent
```
MarginPercent = ((SellingPrice - CostPrice) / CostPrice) * 100
```

### Profit
```
Profit = (SellingPrice - CostPrice) * Quantity
```

### Net Amount
```
NetAmount = SellingPrice * Quantity
```

### Stock Age Days
```
StockAgeDays = TransactionDate - ManufacturingDate (in days)
```

### Days to Expiry
```
DaysToExpiry = ExpiryDate - TransactionDate (in days)
```

---

## 🏷️ Classification Ranges

### Stock Age Categories

| Category | Days Range | Health Status |
|----------|------------|---------------|
| **Fresh** | 0 - 30 days | Excellent |
| **Normal** | 31 - 90 days | Good |
| **Ageing** | 91 - 180 days | Warning |
| **Old** | 180+ days | Critical |

### Margin Categories

| Category | Margin % Range |
|----------|----------------|
| **Low** | 0 - 15% |
| **Medium** | 16 - 30% |
| **High** | 31 - 45% |
| **Very High** | 46%+ |

### Revenue Categories

| Category | Amount Range (INR) |
|----------|-------------------|
| **Low** | 0 - 500 |
| **Medium** | 501 - 2000 |
| **High** | 2001 - 5000 |
| **Very High** | 5000+ |

---

## 🔍 Data Quality Notes

### Validation Rules Applied

1. **Pricing Validation**
   - SellingPrice ≤ MRP
   - CostPrice < SellingPrice
   - DiscountPercent: 0-30%

2. **Date Validation**
   - ManufacturingDate ≤ TransactionDate
   - ExpiryDate > ManufacturingDate
   - All dates within 2024

3. **Numerical Validation**
   - All amounts > 0
   - Quantity: 1-5 units
   - Margins within realistic ranges

4. **Stock Validation**
   - StockAgeDays ≥ 0
   - DaysToExpiry > 0
   - No negative values

---

## 📞 Support

For questions about data definitions or field usage:
- See main [README.md](README.md)
- Review [notebooks/grocery_fashion_eda.ipynb](notebooks/grocery_fashion_eda.ipynb)

---

**Last Updated**: December 2024  
**Version**: 1.0
