# 📚 Data Dictionary - Kids Clothing Insights

**Complete schema documentation for all datasets in the Enterprise Analytics Hub**

---

## 📋 Table of Contents

- [Raw Datasets](#raw-datasets)
  - [Sales Transactions](#1-sales_transactionscsv)
  - [Customers](#2-customerscsv)
  - [Products](#3-productscsv)
  - [Inventory](#4-inventorycsv)
  - [Stores](#5-storescsv)
  - [Suppliers](#6-supplierscsv)
  - [Web Analytics](#7-web_analyticscsv)
- [Processed Datasets](#processed-datasets)
  - [Sales Analysis](#sales-analysis-outputs)
  - [Customer Segmentation](#customer-segmentation-outputs)
  - [Inventory Management](#inventory-management-outputs)
  - [Executive Summary](#executive-summary-outputs)
  - [E-commerce Analytics](#e-commerce-analytics-outputs)

---

## Raw Datasets

Located in: `data/raw/`

### 1. sales_transactions.csv

**Description**: Complete transaction history for all sales (online and offline)  
**Rows**: 50,000  
**Date Range**: January 1, 2023 - December 31, 2024  
**Grain**: One row per transaction line item

| Column | Data Type | Description | Example | Constraints |
|--------|-----------|-------------|---------|-------------|
| `TransactionID` | String | Unique transaction identifier | TXN000001 | Primary Key, Format: TXN######, Sequential |
| `Date` | Date | Transaction date | 2024-06-15 | Format: YYYY-MM-DD, Range: 2023-01-01 to 2024-12-31 |
| `StoreID` | String | Store identifier or ONLINE for web sales | S001 or ONLINE | Foreign Key → stores.csv, 10 stores + ONLINE |
| `ProductID` | String | Product SKU identifier | P0001 | Foreign Key → products.csv, Range: P0001-P0900 |
| `CustomerID` | String | Customer identifier or guest ID | C0001 or GUEST1234 | Foreign Key → customers.csv, ~80% registered, 20% guest |
| `Quantity` | Integer | Number of units purchased | 2 | Range: 1-3, Avg: 1.45 |
| `UnitPrice` | Float | Price per unit (after discounts) | 29.99 | Range: $8-$75, Includes seasonal discounts (0-30%) |
| `TotalAmount` | Float | Total transaction value (Quantity × UnitPrice) | 59.98 | Calculated field, Sum = $1,956,784.20 |
| `PaymentMethod` | String | Payment type | Credit Card | Values: Credit Card (45%), Debit Card (30%), PayPal (15%), Cash (10%) |
| `Channel` | String | Sales channel | Online | Values: Online (42%), Offline (58%) |

**Relationships**:
- `StoreID` → stores.csv (Many-to-One)
- `ProductID` → products.csv (Many-to-One)
- `CustomerID` → customers.csv (Many-to-One)

**Business Rules**:
- Online transactions have `StoreID` = 'ONLINE'
- Guest customers have `CustomerID` starting with 'GUEST'
- Discounts applied during: Summer (20%), Holiday (30%), Back-to-School (15%)

---

### 2. customers.csv

**Description**: Customer profile information and demographics  
**Rows**: 10,000  
**Grain**: One row per unique customer

| Column | Data Type | Description | Example | Constraints |
|--------|-----------|-------------|---------|-------------|
| `CustomerID` | String | Unique customer identifier | C0001 | Primary Key, Format: C####, Sequential |
| `Name` | String | Customer full name | Sarah Martinez | Generated name, Format: FirstName LastName |
| `Email` | String | Customer email address | sarah.martinez@email.com | Unique, Format: name@domain.com |
| `Phone` | String | Contact phone number | (555) 123-4567 | Format: (###) ###-#### |
| `City` | String | Customer city | Los Angeles | 50 US cities, Top: New York, Los Angeles, Columbus |
| `State` | String | Customer state | CA | 50 US states, 2-letter code |
| `Region` | String | Geographic region | West | Values: West (30%), East (25%), Central (25%), South (20%) |
| `SignupDate` | Date | Customer registration date | 2023-03-15 | Range: 2022-01-01 to 2024-12-31 |
| `Age` | Integer | Customer age | 32 | Range: 22-45 (parent demographic) |
| `Gender` | String | Customer gender | Female | Values: Female (65%), Male (30%), Other (5%) |
| `PreferredCategory` | String | Most purchased category | Girls Clothing | Values: Girls, Boys, Infants, Accessories |

**Derived Metrics**:
- Customer Lifetime Value (CLV): Calculated in segmentation analysis
- RFM Scores: Recency, Frequency, Monetary (1-5 scale)
- Customer Segment: 10 segments based on RFM

**Business Rules**:
- Age range represents typical parent demographic (22-45)
- 65% female reflects primary purchaser demographic
- Signup date precedes first purchase

---

### 3. products.csv

**Description**: Product catalog with pricing and category information  
**Rows**: 900  
**Grain**: One row per unique SKU

| Column | Data Type | Description | Example | Constraints |
|--------|-----------|-------------|---------|-------------|
| `ProductID` | String | Unique product identifier | P0001 | Primary Key, Format: P####, Sequential |
| `ProductName` | String | Product display name | Cotton T-Shirt | Format: {Brand} {Item Type} |
| `Category` | String | Product category | Girls Clothing | Values: Girls (40%), Boys (30%), Infants (20%), Accessories (10%) |
| `Brand` | String | Product brand | KidStyle | 20 unique brands (TinyTots, KidStyle, PetitMode, etc.) |
| `Price` | Float | Base retail price | 24.99 | Range: $10-$75, Avg: $32.19 |
| `Cost` | Float | Cost of goods sold (COGS) | 13.75 | Range: $5-$40, Avg 55% of price |
| `SupplierID` | String | Supplier partner | SUP001 | Foreign Key → suppliers.csv, 15 suppliers |
| `Size` | String | Size range | 4-6Y | Values: 0-3M, 3-6M, 6-12M, 1-2Y, 2-4Y, 4-6Y, 6-8Y, 8-10Y, 10-12Y, One Size |
| `Color` | String | Primary color | Pink | 15 colors (Pink, Blue, White, Yellow, etc.) |
| `SeasonalDemand` | String | Peak season | Summer | Values: Summer, Winter, Spring, Fall, All-Season |

**Relationships**:
- `SupplierID` → suppliers.csv (Many-to-One)

**Business Rules**:
- Margin = (Price - Cost) / Price × 100%
- Average product margin: 45%
- Girls Clothing has highest price points ($35 avg)
- Accessories have lowest COGS (60% margin)

---

### 4. inventory.csv

**Description**: Current stock levels and warehouse information  
**Rows**: 900 (one per product)  
**Grain**: One row per product-warehouse combination

| Column | Data Type | Description | Example | Constraints |
|--------|-----------|-------------|---------|-------------|
| `ProductID` | String | Product identifier | P0001 | Foreign Key → products.csv |
| `WarehouseID` | String | Warehouse location | WH001 | Values: WH001 (West), WH002 (East), WH003 (Central) |
| `StockLevel` | Integer | Current units in stock | 45 | Range: 0-200, Total: 10,481 units |
| `ReorderPoint` | Integer | Minimum stock threshold | 20 | When StockLevel < ReorderPoint, trigger alert |
| `LeadTime` | Integer | Supplier delivery time (days) | 14 | Range: 10-21 days, Avg: 15 days |
| `LastRestocked` | Date | Last inventory replenishment date | 2024-10-15 | Range: 2023-01-01 to 2024-12-31 |

**Derived Metrics** (in processed data):
- `StockStatus`: Critical (< 50% of reorder point), Low (50-100%), Normal (> 100%)
- `TurnoverRatio`: Annual sales / Average inventory
- `StockValue`: StockLevel × Product.Cost
- `DaysOfInventory`: StockLevel / Avg daily sales

**Business Rules**:
- Critical: 44 products (4.9%) - immediate reorder needed
- Low: 19 products (2.1%) - monitor closely
- Normal: 837 products (93.0%)
- Total stock value: $152,385.51

---

### 5. stores.csv

**Description**: Physical store location information  
**Rows**: 10  
**Grain**: One row per retail store location

| Column | Data Type | Description | Example | Constraints |
|--------|-----------|-------------|---------|-------------|
| `StoreID` | String | Unique store identifier | S001 | Primary Key, Format: S###, 10 stores |
| `StoreName` | String | Store display name | LA Fashion Kids | Unique name per location |
| `City` | String | Store city | Los Angeles | Major US cities |
| `State` | String | Store state | CA | 2-letter state code |
| `Region` | String | Geographic region | West | Values: West, East, Central, South |
| `OpeningDate` | Date | Store opening date | 2020-03-15 | Range: 2015-2022 |
| `SquareFeet` | Integer | Store floor space | 5000 | Range: 3,000-8,000 sq ft |
| `ManagerName` | String | Store manager | Jessica Brown | Manager name |

**Store Performance Metrics** (from sales analysis):
| StoreID | Store Name | Total Revenue | Rank |
|---------|------------|---------------|------|
| S001 | LA Fashion Kids | $122,803 | 1 |
| S005 | Columbus Kids Corner | $120,298 | 2 |
| S002 | NYC Children's Boutique | $119,840 | 3 |

**Business Rules**:
- West region: 3 stores (highest revenue per store: $115K)
- East region: 3 stores
- Central region: 2 stores
- South region: 2 stores

---

### 6. suppliers.csv

**Description**: Supplier partner information and contact details  
**Rows**: 15  
**Grain**: One row per supplier partner

| Column | Data Type | Description | Example | Constraints |
|--------|-----------|-------------|---------|-------------|
| `SupplierID` | String | Unique supplier identifier | SUP001 | Primary Key, Format: SUP###, 15 suppliers |
| `SupplierName` | String | Company name | Baby Boutique Supplies | Unique company name |
| `ContactPerson` | String | Primary contact | John Smith | Contact name |
| `Email` | String | Supplier email | john@babyboutique.com | Contact email |
| `Phone` | String | Contact phone | (555) 987-6543 | Format: (###) ###-#### |
| `Country` | String | Supplier country | USA | Values: USA (60%), China (25%), Vietnam (15%) |
| `LeadTime` | Integer | Average delivery time (days) | 12 | Range: 10-21 days |
| `MinimumOrder` | Integer | Minimum order quantity | 50 | Range: 20-100 units |

**Supplier Performance** (from inventory analysis):
| SupplierID | Name | Score | On-Time % | Defect Rate |
|------------|------|-------|-----------|-------------|
| SUP001 | Baby Boutique Supplies | 0.899 | 96% | 2% |
| SUP008 | Fashion Kids Suppliers | 0.892 | 95% | 3% |
| SUP004 | ABC Textiles Ltd | 0.890 | 96% | 3% |

**Scoring Formula**:
```
Score = (0.4 × OnTimeDelivery%) + (0.4 × (1 - DefectRate%)) + (0.2 × (1 - NormalizedLeadTime))
```

---

### 7. web_analytics.csv

**Description**: Website user behavior and event tracking  
**Rows**: 395,312  
**Date Range**: January 1, 2023 - December 31, 2024  
**Grain**: One row per page view event

| Column | Data Type | Description | Example | Constraints |
|--------|-----------|-------------|---------|-------------|
| `EventID` | String | Unique event identifier | EV000001 | Primary Key, Format: EV######, Sequential |
| `SessionID` | String | User session identifier | SESS0001 | Groups events within same session |
| `CustomerID` | String | Customer ID (if logged in) | C0001 or NULL | Foreign Key → customers.csv, ~30% logged in |
| `EventType` | String | Page type visited | product_view | Values: homepage, category_view, product_view, add_to_cart, checkout, purchase |
| `ProductID` | String | Product viewed/interacted | P0123 or NULL | Foreign Key → products.csv, NULL for homepage |
| `Timestamp` | Datetime | Event occurrence time | 2024-06-15 14:23:45 | Format: YYYY-MM-DD HH:MM:SS |
| `DeviceType` | String | Device category | Mobile | Values: Mobile (57.7%), Desktop (35.3%), Tablet (7%) |
| `TrafficSource` | String | How user arrived | Organic Search | Values: Organic (42%), Paid (18%), Social (15%), Direct (12%), Referral (8%), Email (5%) |
| `PageLoadTime` | Float | Page load time (seconds) | 2.3 | Range: 0.5-5.0 seconds |

**Session Metrics** (aggregated):
- Total Sessions: 200,000
- Avg Pages per Session: 1.98
- Avg Session Duration: 109 seconds (1.8 minutes)
- Bounce Rate: 59.99%

**Conversion Funnel**:
```
Homepage:     200,000 (100%)
Category:      80,014 (40.0%)
Product:       56,085 (28.0%)
Cart:          22,456 (11.2%)
Checkout:       7,271 (3.6%)
Purchase:       3,515 (1.8%)
```

---

## Processed Datasets

Located in: `data/processed/`

### Sales Analysis Outputs

Generated by: `scripts/02_sales_analysis.py`

#### 1. sales_summary.csv

**Description**: Overall sales KPIs and aggregated metrics

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `TotalRevenue` | Float | Total sales revenue | $1,956,784.20 |
| `TotalTransactions` | Integer | Number of transactions | 50,000 |
| `TotalQuantity` | Integer | Total units sold | 72,618 |
| `UniqueCustomers` | Integer | Distinct customers | 15,768 |
| `AvgOrderValue` | Float | Average transaction value | $39.14 |
| `AvgUnitsPerTransaction` | Float | Average quantity per order | 1.45 |

#### 2. category_performance.csv

**Description**: Sales breakdown by product category

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Category` | String | Product category | Girls Clothing |
| `TotalRevenue` | Float | Category revenue | $884,504.91 |
| `Transactions` | Integer | Number of transactions | 22,626 |
| `Quantity` | Integer | Units sold | 32,818 |
| `AvgOrderValue` | Float | Category AOV | $39.09 |
| `RevenueShare` | Float | % of total revenue | 45.2% |

**Category Rankings**:
1. Girls Clothing: $884,505 (45.2%)
2. Boys Clothing: $552,420 (28.2%)
3. Infants: $339,057 (17.3%)
4. Accessories: $180,802 (9.2%)

#### 3. store_performance.csv

**Description**: Sales metrics by store location

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `StoreID` | String | Store identifier | S001 |
| `StoreName` | String | Store name | LA Fashion Kids |
| `TotalRevenue` | Float | Store revenue | $122,803.43 |
| `Transactions` | Integer | Number of transactions | 3,138 |
| `AvgOrderValue` | Float | Store AOV | $39.13 |
| `RevenueRank` | Integer | Store ranking | 1 |

#### 4. monthly_trends.csv

**Description**: Time-series sales data by month

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Year` | Integer | Year | 2024 |
| `Month` | Integer | Month number | 7 |
| `MonthName` | String | Month name | July |
| `TotalRevenue` | Float | Monthly revenue | $118,965.12 |
| `Transactions` | Integer | Monthly transactions | 3,045 |
| `GrowthRate` | Float | MoM growth rate | 8.5% |

**Seasonal Patterns**:
- Peak: Summer (June-Aug): $427K
- Q4 Holiday: $249K (35% of annual)
- Back-to-School: August surge

#### 5. seasonal_performance.csv

**Description**: Sales aggregated by season

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Season` | String | Season name | Summer |
| `TotalRevenue` | Float | Seasonal revenue | $427,289.34 |
| `Transactions` | Integer | Seasonal transactions | 10,923 |
| `AvgOrderValue` | Float | Seasonal AOV | $39.12 |
| `RevenueShare` | Float | % of annual revenue | 21.8% |

#### 6. top_products.csv

**Description**: Best-selling products by revenue

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `ProductID` | String | Product identifier | P0456 |
| `ProductName` | String | Product name | KidStyle Cotton T-Shirt |
| `Category` | String | Product category | Girls Clothing |
| `TotalRevenue` | Float | Product revenue | $12,345.67 |
| `UnitsSold` | Integer | Quantity sold | 456 |
| `AvgPrice` | Float | Average selling price | $27.06 |

#### 7. channel_performance.csv

**Description**: Online vs Offline sales comparison

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Channel` | String | Sales channel | Online |
| `TotalRevenue` | Float | Channel revenue | $822,853.96 |
| `Transactions` | Integer | Channel transactions | 20,874 |
| `AvgOrderValue` | Float | Channel AOV | $39.42 |
| `RevenueShare` | Float | % of total revenue | 42.1% |

**Channel Comparison**:
- Online: 42.1% revenue, $39.42 AOV, 1.76% conversion
- Offline: 57.9% revenue, $38.93 AOV, in-store traffic

#### 8. payment_analysis.csv

**Description**: Payment method usage and performance

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `PaymentMethod` | String | Payment type | Credit Card |
| `TotalRevenue` | Float | Payment method revenue | $888,674.23 |
| `Transactions` | Integer | Number of transactions | 22,681 |
| `AvgOrderValue` | Float | AOV for payment method | $39.18 |
| `Share` | Float | % of transactions | 45.4% |

#### 9. regional_performance.csv

**Description**: Sales by geographic region

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Region` | String | Geographic region | West |
| `TotalRevenue` | Float | Regional revenue | $345,678.90 |
| `Stores` | Integer | Number of stores | 3 |
| `RevenuePerStore` | Float | Avg revenue per store | $115,226.30 |
| `RevenueShare` | Float | % of total revenue | 30.5% |

#### 10. category_channel.csv

**Description**: Cross-analysis of category × channel performance

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Category` | String | Product category | Girls Clothing |
| `Channel` | String | Sales channel | Online |
| `TotalRevenue` | Float | Revenue for combo | $420,345.67 |
| `AvgOrderValue` | Float | AOV for combo | $47.49 |

---

### Customer Segmentation Outputs

Generated by: `scripts/03_customer_segmentation.py`

#### 1. customer_rfm.csv

**Description**: RFM scores for all customers

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `CustomerID` | String | Customer identifier | C0001 |
| `Recency` | Integer | Days since last purchase | 45 |
| `Frequency` | Integer | Total number of purchases | 12 |
| `Monetary` | Float | Total lifetime spend | $567.89 |
| `R_Score` | Integer | Recency score (1-5) | 4 |
| `F_Score` | Integer | Frequency score (1-5) | 5 |
| `M_Score` | Integer | Monetary score (1-5) | 4 |
| `RFM_Score` | String | Combined score | 454 |

**RFM Scoring Logic**:
- Recency: Lower is better → 1 (>300 days) to 5 (<30 days)
- Frequency: Higher is better → 1 (1 purchase) to 5 (10+ purchases)
- Monetary: Higher is better → 1 (<$50) to 5 (>$300)

#### 2. customer_segments.csv

**Description**: Customer segmentation with CLV

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `CustomerID` | String | Customer identifier | C0001 |
| `Segment` | String | Customer segment | Champions |
| `CLV` | Float | Customer Lifetime Value | $717.86 |
| `Recency` | Integer | Days since last purchase | 12 |
| `Frequency` | Integer | Purchase count | 15 |
| `Monetary` | Float | Total spend | $789.12 |

**10 Customer Segments**:
1. **Champions** (1,677 - 17.1%): R=5, F=5, M=5 → CLV: $717.86
2. **Loyal Customers** (1,171 - 11.9%): R=4-5, F=4-5 → CLV: $558.91
3. **Potential Loyalists** (1,360 - 13.8%): R=4-5, F=2-3 → CLV: $143.99
4. **New Customers** (983 - 10.0%): R=5, F=1 → CLV: $41.31
5. **Promising** (885 - 9.0%): R=3-4, F=1-2 → CLV: $51.80
6. **Need Attention** (1,702 - 17.3%): R=3, F=3-4 → CLV: $446.73
7. **About to Sleep** (984 - 10.0%): R=2-3, F=2-3 → CLV: $278.71
8. **At Risk** (563 - 5.7%): R=1-2, F=4-5 → CLV: $469.78
9. **Can't Lose Them** (449 - 4.6%): R=1, F=5 → CLV: $661.82
10. **Lost** (49 - 0.5%): R=1, F=1 → CLV: $36.49

#### 3. clv_by_segment.csv

**Description**: Aggregated CLV metrics by segment

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Segment` | String | Customer segment | Champions |
| `CustomerCount` | Integer | Customers in segment | 1,677 |
| `AvgCLV` | Float | Average CLV | $717.86 |
| `TotalCLV` | Float | Total CLV for segment | $1,203,665.22 |
| `SegmentShare` | Float | % of total customers | 17.1% |

#### 4. customer_geography.csv

**Description**: Customer distribution by location

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `City` | String | Customer city | New York |
| `State` | String | Customer state | NY |
| `Region` | String | Geographic region | East |
| `CustomerCount` | Integer | Customers in city | 534 |
| `TotalRevenue` | Float | Revenue from city | $85,545.68 |
| `AvgCLV` | Float | Avg CLV in city | $160.24 |

**Top Cities**:
1. New York: $85,546 (534 customers)
2. Columbus: $83,125 (512 customers)
3. Denver: $79,890 (498 customers)

#### 5. demographics_age.csv

**Description**: Customer distribution by age group

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `AgeGroup` | String | Age bracket | 26-35 |
| `CustomerCount` | Integer | Customers in group | 3,456 |
| `AvgCLV` | Float | Average CLV | $435.83 |
| `TotalSpend` | Float | Total spend | $1,506,028.48 |

#### 6. demographics_gender.csv

**Description**: Customer distribution by gender

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Gender` | String | Customer gender | Female |
| `CustomerCount` | Integer | Customers | 6,385 |
| `AvgCLV` | Float | Average CLV | $439.25 |
| `Share` | Float | % of customers | 65.0% |

#### 7. cohort_analysis.csv

**Description**: Customer retention by signup cohort

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `SignupMonth` | String | Cohort month | 2023-01 |
| `CohortSize` | Integer | Initial customers | 245 |
| `Month_0` | Float | 100% retention | 100% |
| `Month_1` | Float | Month 1 retention | 78% |
| `Month_6` | Float | Month 6 retention | 45% |
| `Month_12` | Float | Month 12 retention | 32% |

#### 8. repeat_customer_analysis.csv

**Description**: Repeat purchase behavior metrics

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Metric` | String | Metric name | RepeatRate |
| `Value` | Float | Metric value | 92.49% |

**Repeat Metrics**:
- Repeat Purchase Rate: 92.49%
- One-Time Buyers: 7.51%
- Avg Purchases per Customer: 4.07
- Avg Days Between Purchases: 89.4

---

### Inventory Management Outputs

Generated by: `scripts/04_inventory_management.py`

#### 1. reorder_alerts.csv

**Description**: Products requiring immediate reorder

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `ProductID` | String | Product identifier | P0123 |
| `ProductName` | String | Product name | Cotton T-Shirt |
| `Category` | String | Product category | Girls Clothing |
| `StockLevel` | Integer | Current stock | 8 |
| `ReorderPoint` | Integer | Reorder threshold | 20 |
| `StockStatus` | String | Status level | Critical |
| `ReorderQuantity` | Integer | Suggested reorder qty | 50 |
| `ReorderCost` | Float | Cost to reorder | $275.00 |
| `Priority` | Integer | Urgency rank | 1 |

**Stock Status Breakdown**:
- Critical: 44 items (4.9%) - $5,876.36 reorder cost
- Low: 19 items (2.1%) - $1,087.01 reorder cost
- Normal: 837 items (93.0%)

#### 2. inventory_turnover.csv

**Description**: Inventory turnover analysis by product

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `ProductID` | String | Product identifier | P0456 |
| `ProductName` | String | Product name | Denim Jeans |
| `Category` | String | Product category | Boys Clothing |
| `AnnualSales` | Integer | Units sold annually | 456 |
| `AvgInventory` | Float | Average stock level | 45.3 |
| `TurnoverRatio` | Float | Sales / Avg inventory | 10.07 |
| `TurnoverCategory` | String | Speed category | Fast-moving |

**Turnover Categories**:
- Fast-moving: 240 items (10.54x avg turnover)
- Regular: 541 items (3.15x avg turnover)
- Slow: 103 items (1.66x avg turnover)
- Dead stock: 16 items (0x turnover)

#### 3. supplier_performance.csv

**Description**: Supplier performance scoring

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `SupplierID` | String | Supplier identifier | SUP001 |
| `SupplierName` | String | Supplier name | Baby Boutique Supplies |
| `ProductsSupplied` | Integer | Number of SKUs | 67 |
| `AvgLeadTime` | Integer | Avg delivery days | 12 |
| `OnTimeDelivery` | Float | % on-time | 96% |
| `DefectRate` | Float | % defective | 2% |
| `PerformanceScore` | Float | Overall score (0-1) | 0.899 |
| `Rank` | Integer | Supplier ranking | 1 |

**Scoring Formula**:
```
Score = (0.4 × OnTime%) + (0.4 × (1 - Defect%)) + (0.2 × (1 - Normalized Lead Time))
```

#### 4. warehouse_analysis.csv

**Description**: Warehouse utilization metrics

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `WarehouseID` | String | Warehouse identifier | WH001 |
| `Location` | String | Warehouse name | West Coast |
| `TotalProducts` | Integer | SKUs stored | 300 |
| `TotalUnits` | Integer | Total units | 3,456 |
| `StockValue` | Float | Total value | $45,678.90 |
| `ValueShare` | Float | % of total value | 30.0% |

#### 5. category_inventory.csv

**Description**: Inventory breakdown by category

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Category` | String | Product category | Girls Clothing |
| `ProductCount` | Integer | Number of SKUs | 360 |
| `TotalUnits` | Integer | Total units in stock | 4,234 |
| `StockValue` | Float | Total value | $68,925.34 |
| `AvgTurnover` | Float | Category turnover | 8.2x |

#### 6. stock_status_summary.csv

**Description**: Summary of stock status distribution

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `StockStatus` | String | Status category | Critical |
| `ProductCount` | Integer | Number of products | 44 |
| `Percentage` | Float | % of total products | 4.9% |
| `TotalValue` | Float | Value of products | $8,234.56 |

#### 7. days_of_inventory.csv

**Description**: Days of inventory on hand (DOI)

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `ProductID` | String | Product identifier | P0789 |
| `Category` | String | Product category | Accessories |
| `StockLevel` | Integer | Current units | 67 |
| `AvgDailySales` | Float | Avg units sold/day | 2.3 |
| `DaysOfInventory` | Float | Days until stockout | 29.1 |

#### 8. stock_age_analysis.csv

**Description**: Inventory ageing analysis

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `AgeCategory` | String | Age bracket | 90+ days |
| `ProductCount` | Integer | Number of products | 338 |
| `Percentage` | Float | % of inventory | 37.5% |
| `StockValue` | Float | Value | $57,144.56 |

#### 9. slow_moving_inventory.csv

**Description**: Slow and dead stock items

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `ProductID` | String | Product identifier | P0234 |
| `ProductName` | String | Product name | Winter Coat |
| `Category` | String | Product category | Boys Clothing |
| `StockLevel` | Integer | Current units | 45 |
| `StockValue` | Float | Value | $567.89 |
| `TurnoverRatio` | Float | Turnover rate | 0.8x |
| `Status` | String | Movement status | Slow-moving |
| `Recommendation` | String | Action | Discount 30% |

**Slow Inventory Summary**:
- Total slow-moving: 119 items
- Value locked: $23,119.88 (15.17% of total)
- Recommendation: Clearance sale

---

### Executive Summary Outputs

Generated by: `scripts/05_executive_summary.py`

#### 1. financial_summary.csv

**Description**: High-level P&L statement

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Metric` | String | Financial line item | Total Revenue |
| `Value` | Float | Amount | $1,956,784.20 |
| `Percentage` | Float | % of revenue | 100% |

**P&L Structure**:
```
Revenue:                 $1,956,784  (100%)
COGS:                   ($1,071,650) (54.77%)
────────────────────────────────────────
Gross Profit:              $885,134  (45.23%)
Operating Expenses:       ($587,035) (30.00%)
────────────────────────────────────────
Operating Profit:          $298,099  (15.23%)
Taxes (25%):               ($74,525) (3.81%)
────────────────────────────────────────
Net Profit:                $223,574  (11.43%)

EBITDA:                    $337,235
```

#### 2. kpi_summary.csv

**Description**: Key performance indicators

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `KPI` | String | KPI name | Average Order Value |
| `Value` | Float | Current value | $39.14 |
| `Target` | Float | Target value | $45.00 |
| `Status` | String | Performance status | Below Target |

**KPI List**:
- Total Revenue: $1,956,784
- Gross Margin: 45.23% (Target: 45%) ✅
- Net Margin: 11.43% (Target: 15%) ❌
- Transactions: 50,000
- Average Order Value: $39.14 (Target: $45) ❌
- Active Customers: 9,823
- Inventory Turnover: 7.03x (Target: 5x) ✅
- Customer Acquisition Cost: $8.81
- Customer Lifetime Value: $199.20
- CLV/CAC Ratio: 22.62x (Target: 5x) ✅

#### 3. yearly_comparison.csv

**Description**: Year-over-year performance

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Year` | Integer | Year | 2024 |
| `TotalRevenue` | Float | Annual revenue | $978,754.81 |
| `Transactions` | Integer | Annual transactions | 25,000 |
| `AvgOrderValue` | Float | Annual AOV | $39.15 |
| `GrowthRate` | Float | YoY growth | +0.07% |

**YoY Comparison**:
- 2023: $978,029.39 (25,000 transactions)
- 2024: $978,754.81 (25,000 transactions)
- Growth: +0.07% (flat, mature market)

#### 4. quarterly_performance.csv

**Description**: Quarterly breakdown

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Year` | Integer | Year | 2024 |
| `Quarter` | String | Quarter | Q4 |
| `TotalRevenue` | Float | Quarterly revenue | $249,234.56 |
| `Transactions` | Integer | Quarterly transactions | 6,372 |
| `AvgOrderValue` | Float | Quarterly AOV | $39.11 |

**Quarterly Pattern**:
- Q1: $235K (lowest - post-holiday)
- Q2: $242K (spring season)
- Q3: $245K (back-to-school)
- Q4: $249K (holiday peak) 🎄

#### 5. category_financial.csv

**Description**: Financial performance by category

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Category` | String | Product category | Girls Clothing |
| `TotalRevenue` | Float | Category revenue | $884,504.91 |
| `COGS` | Float | Cost of goods sold | $486,477.70 |
| `GrossProfit` | Float | Gross profit | $398,027.21 |
| `GrossMargin` | Float | Gross margin % | 45.0% |

**Category Margins**:
1. Accessories: 60% (best margin)
2. Girls Clothing: 45%
3. Boys Clothing: 43%
4. Infants: 42%

#### 6. channel_financial.csv

**Description**: Financial performance by channel

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Channel` | String | Sales channel | Online |
| `TotalRevenue` | Float | Channel revenue | $822,853.96 |
| `COGS` | Float | Cost of goods sold | $452,569.68 |
| `GrossProfit` | Float | Gross profit | $370,284.28 |
| `GrossMargin` | Float | Gross margin % | 45.0% |

#### 7. monthly_profitability.csv

**Description**: Monthly profit trends

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Year` | Integer | Year | 2024 |
| `Month` | Integer | Month | 7 |
| `Revenue` | Float | Monthly revenue | $118,965.12 |
| `GrossProfit` | Float | Gross profit | $53,826.70 |
| `NetProfit` | Float | Net profit | $13,593.18 |
| `NetMargin` | Float | Net margin % | 11.43% |

#### 8. revenue_forecast.csv

**Description**: 6-month revenue forecast

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Month` | String | Forecast month | 2025-01 |
| `ForecastRevenue` | Float | Predicted revenue | $81,663.40 |
| `ConfidenceLower` | Float | Lower bound (90% CI) | $75,432.10 |
| `ConfidenceUpper` | Float | Upper bound (90% CI) | $87,894.70 |

**6-Month Forecast**:
- Total: $489,980.37
- Method: Linear regression on historical trends
- Assumes 0.07% growth continuation

#### 9. executive_scorecard.csv

**Description**: Executive KPI scorecard with status

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `KPI` | String | KPI name | Gross Margin |
| `CurrentValue` | Float | Actual value | 45.23% |
| `TargetValue` | Float | Target value | 45.00% |
| `Status` | String | Performance indicator | Green |
| `Variance` | Float | Difference from target | +0.23% |

**Scorecard Summary**:
- 🟢 Green (3): Gross Margin, Inventory Turnover, CLV/CAC
- 🔴 Red (2): Net Margin, Average Transaction Value

---

### E-commerce Analytics Outputs

Generated by: `scripts/06_ecommerce_analysis.py`

#### 1. conversion_funnel.csv

**Description**: Step-by-step conversion funnel

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `FunnelStage` | String | Stage name | Homepage |
| `Sessions` | Integer | Sessions at stage | 200,000 |
| `PercentageOfTotal` | Float | % of initial traffic | 100% |
| `DropOffRate` | Float | % lost to next stage | 59.99% |
| `ConversionRate` | Float | % converting to purchase | 1.76% |

**Funnel Breakdown**:
1. Homepage: 200,000 (100%) → 59.99% drop
2. Category: 80,014 (40%) → 29.91% drop
3. Product: 56,085 (28%) → 59.96% drop
4. Cart: 22,456 (11%) → 67.62% drop ⚠️
5. Checkout: 7,271 (4%) → 51.66% drop ⚠️
6. Purchase: 3,515 (1.76%)

**Critical Drop-off Points**:
- Homepage→Category: 60% (high bounce rate)
- Product→Cart: 60% (decision barrier)
- Cart→Checkout: 68% (cart abandonment)

#### 2. traffic_source_analysis.csv

**Description**: Performance by traffic source

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `TrafficSource` | String | Source name | Organic Search |
| `Sessions` | Integer | Total sessions | 84,125 |
| `SessionShare` | Float | % of total traffic | 42.1% |
| `PageViews` | Integer | Total page views | 166,589 |
| `AvgPagesPerSession` | Float | Engagement metric | 1.98 |
| `Conversions` | Integer | Purchases | 1,422 |
| `ConversionRate` | Float | % converting | 1.69% |
| `Revenue` | Float | Total revenue | $346,329.56 |

**Traffic Source Rankings**:
1. 🔍 Organic Search: 84,125 (42.1%) - 1.69% conv
2. 💰 Paid Search: 35,832 (17.9%) - 1.84% conv
3. 📱 Social Media: 29,981 (15.0%) - 1.76% conv
4. 🔗 Direct: 24,095 (12.1%) - 1.89% conv (best)
5. 🌐 Referral: 16,026 (8.0%) - 1.71% conv
6. 📧 Email: 9,941 (5.0%) - 1.79% conv

#### 3. device_analysis.csv

**Description**: Performance by device type

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `DeviceType` | String | Device category | Mobile |
| `Sessions` | Integer | Total sessions | 115,432 |
| `SessionShare` | Float | % of traffic | 57.7% |
| `AvgSessionDuration` | Float | Avg duration (seconds) | 108 |
| `Conversions` | Integer | Purchases | 2,020 |
| `ConversionRate` | Float | % converting | 1.75% |
| `Revenue` | Float | Total revenue | $474,923.45 |

**Device Comparison**:
| Device | Sessions | Share | Conversion | Revenue |
|--------|----------|-------|------------|---------|
| 📱 Mobile | 115,432 | 57.7% | 1.75% | $474,923 |
| 💻 Desktop | 70,573 | 35.3% | 1.75% | $292,187 |
| 📱 Tablet | 13,995 | 7.0% | 1.81% | $55,744 |

**Insight**: Tablet has best conversion (1.81%) despite lowest traffic

#### 4. product_page_performance.csv

**Description**: Product page metrics

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `ProductID` | String | Product identifier | P0456 |
| `ProductName` | String | Product name | PetitMode Leggings |
| `Category` | String | Product category | Girls Clothing |
| `PageViews` | Integer | Total views | 87 |
| `AddToCarts` | Integer | Cart additions | 55 |
| `AddToCartRate` | Float | % adding to cart | 63.2% |
| `Purchases` | Integer | Completed purchases | 12 |
| `ViewToPurchase` | Float | % purchasing | 13.8% |

**Top Performing Pages**:
- Highest views: Product P0123 (87 views)
- Best add-to-cart rate: 63.2% (P0456)
- Best purchase rate: 15.2% (P0789)

#### 5. hourly_traffic.csv

**Description**: Traffic patterns by hour of day

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Hour` | Integer | Hour (0-23) | 14 |
| `Sessions` | Integer | Total sessions | 12,345 |
| `ConversionRate` | Float | % converting | 1.82% |
| `Revenue` | Float | Hourly revenue | $48,256.78 |

**Peak Hours**:
- 🌅 Morning (6-11): Low traffic, 1.65% conv
- ☀️ Afternoon (12-17): Peak traffic, 1.78% conv
- 🌙 Evening (18-23): High traffic, 1.82% conv (best)
- 🌃 Night (0-5): Lowest traffic, 1.45% conv

#### 6. dow_traffic.csv

**Description**: Traffic patterns by day of week

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `DayOfWeek` | String | Day name | Saturday |
| `Sessions` | Integer | Total sessions | 32,456 |
| `ConversionRate` | Float | % converting | 1.87% |
| `Revenue` | Float | Daily revenue | $127,845.67 |

**Day Rankings**:
1. 🎉 Saturday: 1.87% conv (best)
2. 🛍️ Sunday: 1.83% conv
3. 📅 Friday: 1.78% conv
4. ⚡ Monday: 1.65% conv (lowest)

#### 7. online_category_performance.csv

**Description**: E-commerce category metrics

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Category` | String | Product category | Girls Clothing |
| `Sessions` | Integer | Category page sessions | 28,456 |
| `Revenue` | Float | Category revenue | $420,345.67 |
| `AOV` | Float | Average order value | $47.49 |
| `ConversionRate` | Float | % converting | 1.79% |

#### 8. cart_abandonment_reasons.csv

**Description**: Why customers abandon carts

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Reason` | String | Abandonment reason | High Shipping Costs |
| `Count` | Integer | Number of occurrences | 7,186 |
| `Percentage` | Float | % of abandonments | 32.0% |

**Top 5 Reasons**:
1. 🚚 High Shipping Costs: 32%
2. 💰 Better Price Elsewhere: 18%
3. 💳 Payment Issues: 15%
4. 👀 Just Browsing: 20%
5. 🐛 Website Errors: 8%

**Abandonment Rate**: 84.35% (22,456 carts → 3,515 purchases)

#### 9. customer_journey_summary.csv

**Description**: Common user paths through site

| Column | Data Type | Description | Sample Value |
|--------|-----------|-------------|--------------|
| `Journey` | String | Page sequence | Homepage→Category→Product→Cart→Purchase |
| `SessionCount` | Integer | Times this path taken | 3,515 |
| `ConversionRate` | Float | % completing purchase | 100% |
| `AvgTimeToConversion` | Float | Avg seconds to purchase | 325 |

---

## Data Relationships

### Entity Relationship Diagram

```
stores
  ↑
  | (1:M)
  |
sales_transactions ← (M:1) → customers
  ↓                            ↓
  | (M:1)                      | (1:M)
  ↓                            ↓
products ← (M:1) → suppliers   customer_rfm
  ↓
  | (1:1)
  ↓
inventory


web_analytics
  ↓
  | (M:1)
  ↓
products
```

### Key Relationships:

1. **sales_transactions → stores**: Each transaction occurs at one store (or ONLINE)
2. **sales_transactions → products**: Each transaction line has one product
3. **sales_transactions → customers**: Each transaction has one customer (or guest)
4. **products → suppliers**: Each product sourced from one supplier
5. **products ← inventory**: One-to-one relationship (stock for each product)
6. **web_analytics → products**: Product views link to product catalog
7. **customers ← customer_rfm**: One-to-one (RFM score per customer)

---

## Data Quality Notes

### Validation Rules

1. **Referential Integrity**:
   - All foreign keys reference valid primary keys
   - No orphaned records in transaction tables
   - Guest customers (GUEST####) don't exist in customers table

2. **Data Consistency**:
   - Dates are within valid ranges (2023-2024)
   - Monetary values are positive
   - Percentages sum to 100% where applicable
   - Stock levels are non-negative

3. **Business Logic**:
   - Transaction dates ≥ customer signup dates
   - Reorder alerts only for items with stock < reorder point
   - RFM scores between 1-5
   - Conversion rates ≤ 100%

### Known Limitations

1. **Synthetic Data**: All data is generated for demonstration purposes
2. **Simplified Model**: Real-world scenarios may have additional complexity
3. **Static Suppliers**: Supplier relationships are static (one per product)
4. **Guest Transactions**: Guest purchases not included in CLV calculations
5. **Seasonality**: Patterns are simulated, may not reflect actual retail behavior

---

## Data Lineage

### Data Flow

```
Raw Data (7 files)
    ↓
Python Analysis Scripts (5 scripts)
    ↓
Processed Data (50+ files)
    ↓
Tableau Workbook (5 dashboards)
    ↓
Business Insights & Decisions
```

### Processing Pipeline

1. **Data Generation** (`01_generate_data.py`):
   - Creates 7 raw CSV files with realistic patterns
   - Total: 456,222 rows

2. **Sales Analysis** (`02_sales_analysis.py`):
   - Aggregates transactions by multiple dimensions
   - Outputs: 10 processed files

3. **Customer Segmentation** (`03_customer_segmentation.py`):
   - Calculates RFM scores, segments, CLV
   - Outputs: 8 processed files

4. **Inventory Management** (`04_inventory_management.py`):
   - Analyzes stock levels, turnover, suppliers
   - Outputs: 9 processed files

5. **Executive Summary** (`05_executive_summary.py`):
   - Calculates financial KPIs, forecasts
   - Outputs: 9 processed files

6. **E-commerce Analytics** (`06_ecommerce_analysis.py`):
   - Analyzes web funnel, traffic, conversions
   - Outputs: 9 processed files

---

## Appendix

### Glossary

- **AOV**: Average Order Value (Total Revenue / Transactions)
- **CLV**: Customer Lifetime Value (predicted total spend)
- **COGS**: Cost of Goods Sold (product cost × quantity)
- **CAC**: Customer Acquisition Cost (marketing cost / new customers)
- **RFM**: Recency, Frequency, Monetary (segmentation method)
- **SKU**: Stock Keeping Unit (unique product identifier)
- **YoY**: Year-over-Year (comparison with previous year)
- **EBITDA**: Earnings Before Interest, Taxes, Depreciation, Amortization
- **DOI**: Days of Inventory on Hand

### Contact

For questions about this data dictionary:

**Nitin DB**  
📧 nitindb901@gmail.com  
🐙 GitHub: [Nitindb901/Nitin-Fiverr-Portfolio](https://github.com/Nitindb901/Nitin-Fiverr-Portfolio)

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Project**: 03_Kids_Clothing_Insights - Enterprise Analytics Hub
