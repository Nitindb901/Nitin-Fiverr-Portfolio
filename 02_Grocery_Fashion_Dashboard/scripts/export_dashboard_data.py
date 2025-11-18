"""
Dashboard Export Script
Prepares aggregated data for Power BI, Excel, and other BI tools
"""

import pandas as pd
import numpy as np

print("=" * 60)
print("DASHBOARD EXPORT - DATA PREPARATION")
print("=" * 60)
print()

# ============================================
# LOAD MERGED DATA
# ============================================

print("Loading merged dataset...")
df = pd.read_csv('data/merged_pos_data.csv', parse_dates=['Date', 'ManufacturingDate', 'ExpiryDate'])
print(f"✓ Loaded {len(df):,} records")
print()

# ============================================
# 1. CATEGORY PERFORMANCE SUMMARY
# ============================================

print("Preparing Category Performance Summary...")

category_summary = df.groupby('Category').agg({
    'TransactionID': 'count',
    'NetAmount': ['sum', 'mean'],
    'Profit': ['sum', 'mean'],
    'MarginPercent': 'mean',
    'Quantity': 'sum',
    'SKU_ID': 'nunique'
}).round(2)

category_summary.columns = ['Transactions', 'TotalRevenue', 'AvgRevenue', 
                             'TotalProfit', 'AvgProfit', 'AvgMargin', 
                             'TotalQuantity', 'UniqueSKUs']

category_summary = category_summary.reset_index()
category_summary.to_csv('dashboard/category_performance.csv', index=False)
print("✓ Saved: dashboard/category_performance.csv")

# ============================================
# 2. SUBCATEGORY PERFORMANCE SUMMARY
# ============================================

print("Preparing SubCategory Performance Summary...")

subcategory_summary = df.groupby(['Category', 'SubCategory']).agg({
    'TransactionID': 'count',
    'NetAmount': ['sum', 'mean'],
    'Profit': 'sum',
    'MarginPercent': 'mean',
    'Quantity': 'sum'
}).round(2)

subcategory_summary.columns = ['Transactions', 'TotalRevenue', 'AvgRevenue', 
                                'TotalProfit', 'AvgMargin', 'TotalQuantity']
subcategory_summary = subcategory_summary.reset_index()
subcategory_summary.to_csv('dashboard/subcategory_performance.csv', index=False)
print("✓ Saved: dashboard/subcategory_performance.csv")

# ============================================
# 3. POS SYSTEM COMPARISON
# ============================================

print("Preparing POS System Comparison...")

pos_summary = df.groupby(['POS_System', 'Store']).agg({
    'TransactionID': 'count',
    'NetAmount': 'sum',
    'Profit': 'sum',
    'MarginPercent': 'mean',
    'Quantity': 'sum',
    'SKU_ID': 'nunique'
}).round(2)

pos_summary.columns = ['Transactions', 'TotalRevenue', 'TotalProfit', 
                        'AvgMargin', 'TotalQuantity', 'UniqueSKUs']
pos_summary = pos_summary.reset_index()
pos_summary.to_csv('dashboard/pos_comparison.csv', index=False)
print("✓ Saved: dashboard/pos_comparison.csv")

# ============================================
# 4. STOCK AGEING ANALYSIS
# ============================================

print("Preparing Stock Ageing Analysis...")

# Overall stock ageing
stock_ageing = df.groupby('StockAgeCategory').agg({
    'TransactionID': 'count',
    'NetAmount': 'sum',
    'Quantity': 'sum',
    'StockAgeDays': 'mean'
}).round(2)

stock_ageing.columns = ['Transactions', 'TotalRevenue', 'TotalQuantity', 'AvgStockAge']
stock_ageing = stock_ageing.reset_index()
stock_ageing.to_csv('dashboard/stock_ageing_overall.csv', index=False)
print("✓ Saved: dashboard/stock_ageing_overall.csv")

# Stock ageing by category
stock_ageing_category = df.groupby(['Category', 'StockAgeCategory']).agg({
    'TransactionID': 'count',
    'NetAmount': 'sum',
    'Quantity': 'sum',
    'StockAgeDays': 'mean'
}).round(2)

stock_ageing_category.columns = ['Transactions', 'TotalRevenue', 'TotalQuantity', 'AvgStockAge']
stock_ageing_category = stock_ageing_category.reset_index()
stock_ageing_category.to_csv('dashboard/stock_ageing_by_category.csv', index=False)
print("✓ Saved: dashboard/stock_ageing_by_category.csv")

# ============================================
# 5. MARGIN ANALYSIS
# ============================================

print("Preparing Margin Analysis...")

# Margin by category and subcategory
margin_analysis = df.groupby(['Category', 'SubCategory']).agg({
    'MarginPercent': ['mean', 'min', 'max'],
    'Profit': 'sum',
    'NetAmount': 'sum'
}).round(2)

margin_analysis.columns = ['AvgMargin', 'MinMargin', 'MaxMargin', 'TotalProfit', 'TotalRevenue']
margin_analysis['ProfitMargin%'] = (margin_analysis['TotalProfit'] / margin_analysis['TotalRevenue'] * 100).round(2)
margin_analysis = margin_analysis.reset_index()
margin_analysis.to_csv('dashboard/margin_analysis.csv', index=False)
print("✓ Saved: dashboard/margin_analysis.csv")

# ============================================
# 6. MONTHLY TRENDS
# ============================================

print("Preparing Monthly Trends...")

df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)

monthly_trends = df.groupby(['YearMonth', 'Category']).agg({
    'TransactionID': 'count',
    'NetAmount': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2)

monthly_trends.columns = ['Transactions', 'Revenue', 'Profit', 'Quantity']
monthly_trends = monthly_trends.reset_index()
monthly_trends.to_csv('dashboard/monthly_trends.csv', index=False)
print("✓ Saved: dashboard/monthly_trends.csv")

# ============================================
# 7. BRAND PERFORMANCE
# ============================================

print("Preparing Brand Performance...")

brand_performance = df.groupby(['Category', 'Brand']).agg({
    'TransactionID': 'count',
    'NetAmount': 'sum',
    'Profit': 'sum',
    'MarginPercent': 'mean',
    'SKU_ID': 'nunique'
}).round(2)

brand_performance.columns = ['Transactions', 'TotalRevenue', 'TotalProfit', 
                              'AvgMargin', 'UniqueSKUs']
brand_performance = brand_performance.reset_index()
brand_performance = brand_performance.sort_values('TotalRevenue', ascending=False)
brand_performance.to_csv('dashboard/brand_performance.csv', index=False)
print("✓ Saved: dashboard/brand_performance.csv")

# ============================================
# 8. WEEKEND VS WEEKDAY ANALYSIS
# ============================================

print("Preparing Weekend vs Weekday Analysis...")

weekend_analysis = df.groupby(['Category', 'IsWeekend']).agg({
    'TransactionID': 'count',
    'NetAmount': ['sum', 'mean'],
    'Quantity': 'sum'
}).round(2)

weekend_analysis.columns = ['Transactions', 'TotalRevenue', 'AvgRevenue', 'TotalQuantity']
weekend_analysis = weekend_analysis.reset_index()
weekend_analysis['Day_Type'] = weekend_analysis['IsWeekend'].map({0: 'Weekday', 1: 'Weekend'})
weekend_analysis = weekend_analysis.drop('IsWeekend', axis=1)
weekend_analysis.to_csv('dashboard/weekend_analysis.csv', index=False)
print("✓ Saved: dashboard/weekend_analysis.csv")

# ============================================
# 9. TOP PERFORMING SKUS
# ============================================

print("Preparing Top Performing SKUs...")

top_skus = df.groupby(['SKU_ID', 'Category', 'SubCategory', 'Brand']).agg({
    'TransactionID': 'count',
    'NetAmount': 'sum',
    'Profit': 'sum',
    'Quantity': 'sum'
}).round(2)

top_skus.columns = ['Transactions', 'TotalRevenue', 'TotalProfit', 'TotalQuantity']
top_skus = top_skus.reset_index()
top_skus = top_skus.sort_values('TotalRevenue', ascending=False).head(100)
top_skus.to_csv('dashboard/top_100_skus.csv', index=False)
print("✓ Saved: dashboard/top_100_skus.csv")

# ============================================
# 10. SUMMARY METRICS (KPIs)
# ============================================

print("Preparing Summary KPIs...")

kpis = {
    'Metric': [
        'Total Transactions',
        'Total Revenue (INR)',
        'Total Profit (INR)',
        'Average Margin (%)',
        'Total Quantity Sold',
        'Unique SKUs',
        'Unique Stores',
        'Fresh Stock (%)',
        'Ageing Stock (%)',
        'Average Transaction Value (INR)',
        'Grocery Revenue (INR)',
        'Fashion Revenue (INR)',
        'POS1 Revenue (INR)',
        'POS2 Revenue (INR)'
    ],
    'Value': [
        f"{len(df):,}",
        f"{df['NetAmount'].sum():,.2f}",
        f"{df['Profit'].sum():,.2f}",
        f"{df['MarginPercent'].mean():.2f}",
        f"{df['Quantity'].sum():,}",
        f"{df['SKU_ID'].nunique():,}",
        f"{df['Store'].nunique()}",
        f"{len(df[df['StockAgeCategory']=='Fresh'])/len(df)*100:.2f}",
        f"{len(df[df['StockAgeCategory']=='Ageing'])/len(df)*100:.2f}",
        f"{df['NetAmount'].mean():,.2f}",
        f"{df[df['Category']=='Grocery']['NetAmount'].sum():,.2f}",
        f"{df[df['Category']=='Fashion']['NetAmount'].sum():,.2f}",
        f"{df[df['POS_System']=='POS1']['NetAmount'].sum():,.2f}",
        f"{df[df['POS_System']=='POS2']['NetAmount'].sum():,.2f}"
    ]
}

kpi_df = pd.DataFrame(kpis)
kpi_df.to_csv('dashboard/summary_kpis.csv', index=False)
print("✓ Saved: dashboard/summary_kpis.csv")

print()
print("=" * 60)
print("DASHBOARD EXPORT SUMMARY")
print("=" * 60)
print()

print("Files Created:")
print("  1. category_performance.csv - Category-level aggregations")
print("  2. subcategory_performance.csv - Subcategory-level metrics")
print("  3. pos_comparison.csv - POS system and store comparison")
print("  4. stock_ageing_overall.csv - Overall stock ageing analysis")
print("  5. stock_ageing_by_category.csv - Stock ageing by category")
print("  6. margin_analysis.csv - Detailed margin analysis")
print("  7. monthly_trends.csv - Month-over-month trends")
print("  8. brand_performance.csv - Brand-level performance")
print("  9. weekend_analysis.csv - Weekend vs weekday comparison")
print(" 10. top_100_skus.csv - Top 100 performing SKUs")
print(" 11. summary_kpis.csv - Key performance indicators")
print()
print("All files are ready for Power BI/Excel import!")
print()
print("=" * 60)
print("DASHBOARD EXPORT COMPLETED SUCCESSFULLY!")
print("=" * 60)
