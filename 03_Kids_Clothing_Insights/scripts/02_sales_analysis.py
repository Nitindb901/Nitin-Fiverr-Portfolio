"""
Sales Performance Analysis Script
Analyzes sales data and generates metrics for Tableau dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

print("📊 Starting Sales Performance Analysis...")
print("=" * 60)

# Load datasets
print("\n📂 Loading datasets...")
df_transactions = pd.read_csv('data/raw/sales_transactions.csv')
df_products = pd.read_csv('data/raw/products.csv')
df_stores = pd.read_csv('data/raw/stores.csv')

df_transactions['Date'] = pd.to_datetime(df_transactions['Date'])

print(f"✓ Loaded {len(df_transactions):,} transactions")
print(f"✓ Loaded {len(df_products):,} products")
print(f"✓ Loaded {len(df_stores):,} stores")

# Merge data
print("\n🔗 Merging datasets...")
df_sales = df_transactions.merge(df_products, on='ProductID', how='left')
df_sales = df_sales.merge(df_stores, on='StoreID', how='left')

print(f"✓ Created unified sales dataset with {len(df_sales):,} records")

# ============================================================================
# 1. OVERALL KPIs
# ============================================================================
print("\n💰 Calculating Overall KPIs...")

total_revenue = df_sales['TotalAmount'].sum()
total_transactions = len(df_sales)
total_units = df_sales['Quantity'].sum()
avg_order_value = df_sales['TotalAmount'].mean()
unique_customers = df_sales['CustomerID'].nunique()

print(f"  Total Revenue: ${total_revenue:,.2f}")
print(f"  Total Transactions: {total_transactions:,}")
print(f"  Total Units Sold: {total_units:,}")
print(f"  Average Order Value: ${avg_order_value:.2f}")
print(f"  Unique Customers: {unique_customers:,}")

# ============================================================================
# 2. CATEGORY PERFORMANCE
# ============================================================================
print("\n📦 Analyzing Category Performance...")

category_performance = df_sales.groupby('Category').agg({
    'TotalAmount': ['sum', 'mean', 'count'],
    'Quantity': 'sum',
    'TransactionID': 'nunique'
}).round(2)

category_performance.columns = ['Revenue', 'AvgOrderValue', 'Transactions', 'UnitsSold', 'UniqueOrders']
category_performance = category_performance.reset_index()
category_performance['RevenueShare'] = (category_performance['Revenue'] / total_revenue * 100).round(2)
category_performance = category_performance.sort_values('Revenue', ascending=False)

print("\nCategory Performance:")
for _, row in category_performance.iterrows():
    print(f"  {row['Category']}: ${row['Revenue']:,.2f} ({row['RevenueShare']:.1f}%)")

# ============================================================================
# 3. STORE PERFORMANCE
# ============================================================================
print("\n🏪 Analyzing Store Performance...")

store_performance = df_sales[df_sales['StoreID'] != 'ONLINE'].groupby(['StoreID', 'StoreName', 'City', 'State', 'Region']).agg({
    'TotalAmount': 'sum',
    'TransactionID': 'nunique',
    'Quantity': 'sum'
}).round(2)

store_performance.columns = ['Revenue', 'Transactions', 'UnitsSold']
store_performance = store_performance.reset_index()
store_performance['AvgTransactionValue'] = (store_performance['Revenue'] / store_performance['Transactions']).round(2)
store_performance = store_performance.sort_values('Revenue', ascending=False)

print(f"\nTop 5 Performing Stores:")
for idx, row in store_performance.head(5).iterrows():
    print(f"  {row['StoreName']} ({row['City']}): ${row['Revenue']:,.2f}")

# ============================================================================
# 4. MONTHLY TRENDS
# ============================================================================
print("\n📈 Analyzing Monthly Trends...")

df_sales['YearMonth'] = df_sales['Date'].dt.to_period('M')
df_sales['Year'] = df_sales['Date'].dt.year
df_sales['Month'] = df_sales['Date'].dt.month
df_sales['MonthName'] = df_sales['Date'].dt.strftime('%B')

monthly_trends = df_sales.groupby(['Year', 'Month', 'MonthName']).agg({
    'TotalAmount': 'sum',
    'TransactionID': 'nunique',
    'Quantity': 'sum'
}).round(2)

monthly_trends.columns = ['Revenue', 'Transactions', 'UnitsSold']
monthly_trends = monthly_trends.reset_index()
monthly_trends['AvgOrderValue'] = (monthly_trends['Revenue'] / monthly_trends['Transactions']).round(2)

print(f"✓ Calculated monthly trends for {len(monthly_trends)} months")

# ============================================================================
# 5. SEASONAL ANALYSIS
# ============================================================================
print("\n🌤️ Analyzing Seasonal Performance...")

seasonal_performance = df_sales.groupby('Season').agg({
    'TotalAmount': 'sum',
    'Quantity': 'sum',
    'TransactionID': 'nunique'
}).round(2)

seasonal_performance.columns = ['Revenue', 'UnitsSold', 'Transactions']
seasonal_performance = seasonal_performance.reset_index()
seasonal_performance['RevenueShare'] = (seasonal_performance['Revenue'] / total_revenue * 100).round(2)
seasonal_performance = seasonal_performance.sort_values('Revenue', ascending=False)

print("\nSeasonal Performance:")
for _, row in seasonal_performance.iterrows():
    print(f"  {row['Season']}: ${row['Revenue']:,.2f} ({row['RevenueShare']:.1f}%)")

# ============================================================================
# 6. TOP PRODUCTS
# ============================================================================
print("\n🏆 Identifying Top Products...")

product_performance = df_sales.groupby(['ProductID', 'ProductName', 'Category', 'Brand', 'Price']).agg({
    'TotalAmount': 'sum',
    'Quantity': 'sum',
    'TransactionID': 'nunique'
}).round(2)

product_performance.columns = ['Revenue', 'UnitsSold', 'Transactions']
product_performance = product_performance.reset_index()
product_performance = product_performance.sort_values('Revenue', ascending=False)

print(f"\nTop 10 Products by Revenue:")
for idx, row in product_performance.head(10).iterrows():
    print(f"  {row['ProductName'][:40]}: ${row['Revenue']:,.2f}")

# ============================================================================
# 7. CHANNEL ANALYSIS
# ============================================================================
print("\n🌐 Analyzing Sales Channels...")

channel_performance = df_sales.groupby('Channel').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'nunique',
    'Quantity': 'sum'
}).round(2)

channel_performance.columns = ['Revenue', 'Transactions', 'UnitsSold']
channel_performance = channel_performance.reset_index()
channel_performance['RevenueShare'] = (channel_performance['Revenue'] / total_revenue * 100).round(2)
channel_performance['AvgOrderValue'] = (channel_performance['Revenue'] / channel_performance['Transactions']).round(2)

print("\nChannel Performance:")
for _, row in channel_performance.iterrows():
    print(f"  {row['Channel']}: ${row['Revenue']:,.2f} ({row['RevenueShare']:.1f}%) | AOV: ${row['AvgOrderValue']:.2f}")

# ============================================================================
# 8. PAYMENT METHOD ANALYSIS
# ============================================================================
print("\n💳 Analyzing Payment Methods...")

payment_analysis = df_sales.groupby('PaymentMethod').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'count'
}).round(2)

payment_analysis.columns = ['Revenue', 'Transactions']
payment_analysis = payment_analysis.reset_index()
payment_analysis['Share'] = (payment_analysis['Transactions'] / total_transactions * 100).round(2)
payment_analysis = payment_analysis.sort_values('Transactions', ascending=False)

print("\nPayment Method Distribution:")
for _, row in payment_analysis.iterrows():
    print(f"  {row['PaymentMethod']}: {row['Transactions']:,} transactions ({row['Share']:.1f}%)")

# ============================================================================
# 9. REGIONAL ANALYSIS
# ============================================================================
print("\n🗺️ Analyzing Regional Performance...")

regional_performance = df_sales[df_sales['StoreID'] != 'ONLINE'].groupby('Region').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'nunique',
    'Quantity': 'sum',
    'StoreID': 'nunique'
}).round(2)

regional_performance.columns = ['Revenue', 'Transactions', 'UnitsSold', 'StoreCount']
regional_performance = regional_performance.reset_index()
regional_performance['RevenuePerStore'] = (regional_performance['Revenue'] / regional_performance['StoreCount']).round(2)
regional_performance = regional_performance.sort_values('Revenue', ascending=False)

print("\nRegional Performance:")
for _, row in regional_performance.iterrows():
    print(f"  {row['Region']}: ${row['Revenue']:,.2f} | {row['StoreCount']} stores | ${row['RevenuePerStore']:,.2f}/store")

# ============================================================================
# 10. CATEGORY × CHANNEL ANALYSIS
# ============================================================================
print("\n📊 Analyzing Category × Channel Performance...")

category_channel = df_sales.groupby(['Category', 'Channel']).agg({
    'TotalAmount': 'sum',
    'Quantity': 'sum'
}).round(2)

category_channel.columns = ['Revenue', 'UnitsSold']
category_channel = category_channel.reset_index()

# Pivot for better view
category_channel_pivot = category_channel.pivot(index='Category', columns='Channel', values='Revenue').fillna(0)
category_channel_pivot['Total'] = category_channel_pivot.sum(axis=1)
category_channel_pivot['OnlineShare'] = (category_channel_pivot.get('Online', 0) / category_channel_pivot['Total'] * 100).round(2)

print("\nCategory Online Share:")
for category in category_channel_pivot.index:
    online_share = category_channel_pivot.loc[category, 'OnlineShare']
    print(f"  {category}: {online_share:.1f}% online")

# ============================================================================
# SAVE PROCESSED DATA
# ============================================================================
print("\n💾 Saving processed datasets...")

# Summary statistics
summary_stats = pd.DataFrame({
    'Metric': ['Total Revenue', 'Total Transactions', 'Total Units Sold', 'Avg Order Value', 'Unique Customers'],
    'Value': [total_revenue, total_transactions, total_units, avg_order_value, unique_customers]
})
summary_stats.to_csv('data/processed/sales_summary.csv', index=False)
print("✓ Saved sales_summary.csv")

# Category performance
category_performance.to_csv('data/processed/category_performance.csv', index=False)
print("✓ Saved category_performance.csv")

# Store performance
store_performance.to_csv('data/processed/store_performance.csv', index=False)
print("✓ Saved store_performance.csv")

# Monthly trends
monthly_trends.to_csv('data/processed/monthly_trends.csv', index=False)
print("✓ Saved monthly_trends.csv")

# Seasonal performance
seasonal_performance.to_csv('data/processed/seasonal_performance.csv', index=False)
print("✓ Saved seasonal_performance.csv")

# Top products
product_performance.head(50).to_csv('data/processed/top_products.csv', index=False)
print("✓ Saved top_products.csv (top 50)")

# Channel performance
channel_performance.to_csv('data/processed/channel_performance.csv', index=False)
print("✓ Saved channel_performance.csv")

# Payment analysis
payment_analysis.to_csv('data/processed/payment_analysis.csv', index=False)
print("✓ Saved payment_analysis.csv")

# Regional performance
regional_performance.to_csv('data/processed/regional_performance.csv', index=False)
print("✓ Saved regional_performance.csv")

# Category × Channel
category_channel.to_csv('data/processed/category_channel.csv', index=False)
print("✓ Saved category_channel.csv")

print("\n" + "=" * 60)
print("✅ Sales Analysis Complete!")
print("=" * 60)
print(f"\n📊 Key Insights:")
print(f"  • Best Category: {category_performance.iloc[0]['Category']} (${category_performance.iloc[0]['Revenue']:,.2f})")
print(f"  • Best Store: {store_performance.iloc[0]['StoreName']} (${store_performance.iloc[0]['Revenue']:,.2f})")
print(f"  • Online Revenue Share: {channel_performance[channel_performance['Channel']=='Online']['RevenueShare'].values[0]:.1f}%")
print(f"  • Most Popular Payment: {payment_analysis.iloc[0]['PaymentMethod']} ({payment_analysis.iloc[0]['Share']:.1f}%)")
