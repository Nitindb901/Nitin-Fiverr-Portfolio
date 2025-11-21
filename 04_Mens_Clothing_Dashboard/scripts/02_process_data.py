"""
Data Processing and Analysis Script for Men's Clothing Dashboard
================================================================
Processes raw transaction data and performs:
- Data cleaning and validation
- Feature engineering for ML models
- RFM (Recency, Frequency, Monetary) analysis
- Time series aggregations
- Customer segmentation preparation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

print("=" * 70)
print("MEN'S CLOTHING DATA PROCESSING & ANALYSIS")
print("=" * 70)

# Load raw data
print("\n📥 Loading Raw Data...")
data_dir = '../data/raw/'
transactions_df = pd.read_csv(f'{data_dir}transactions.csv')
products_df = pd.read_csv(f'{data_dir}products.csv')
customers_df = pd.read_csv(f'{data_dir}customers.csv')

print(f"✅ Loaded {len(transactions_df):,} transactions")
print(f"✅ Loaded {len(products_df):,} products")
print(f"✅ Loaded {len(customers_df):,} customers")

# Convert date column
transactions_df['Date'] = pd.to_datetime(transactions_df['Date'])
customers_df['JoinDate'] = pd.to_datetime(customers_df['JoinDate'])

# Data Quality Checks
print("\n🔍 Performing Data Quality Checks...")
print(f"   Missing values in transactions: {transactions_df.isnull().sum().sum()}")
print(f"   Duplicate transactions: {transactions_df.duplicated().sum()}")
print(f"   Date range: {transactions_df['Date'].min()} to {transactions_df['Date'].max()}")
print("✅ Data quality validated")

# Feature Engineering
print("\n🔧 Engineering Features...")

# Add time-based features
transactions_df['DayOfWeek'] = transactions_df['Date'].dt.day_name()
transactions_df['WeekOfYear'] = transactions_df['Date'].dt.isocalendar().week
transactions_df['IsWeekend'] = transactions_df['DayOfWeek'].isin(['Saturday', 'Sunday']).astype(int)
transactions_df['MonthName'] = transactions_df['Date'].dt.strftime('%B')

# Calculate margin amount
merged_df = transactions_df.merge(products_df[['ProductID', 'Cost']], on='ProductID', how='left')
transactions_df['CostAmount'] = merged_df['Cost'] * transactions_df['Quantity']
transactions_df['MarginAmount'] = transactions_df['TotalAmount'] - transactions_df['CostAmount']

print("✅ Added time-based and financial features")

# RFM Analysis
print("\n📊 Calculating RFM Metrics...")

# Define analysis date (most recent transaction date + 1 day)
analysis_date = transactions_df['Date'].max() + timedelta(days=1)

# Calculate RFM for each customer
rfm = transactions_df.groupby('CustomerID').agg({
    'Date': lambda x: (analysis_date - x.max()).days,  # Recency
    'TransactionID': 'count',  # Frequency
    'TotalAmount': 'sum'  # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

# Add RFM scores (1-5 scale)
rfm['R_Score'] = pd.qcut(rfm['Recency'], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
rfm['M_Score'] = pd.qcut(rfm['Monetary'], q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')

# Calculate RFM total score
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
rfm['RFM_Total'] = rfm['R_Score'].astype(int) + rfm['F_Score'].astype(int) + rfm['M_Score'].astype(int)

# Segment customers based on RFM
def segment_customers(row):
    if row['RFM_Total'] >= 13:
        return 'Champions'
    elif row['RFM_Total'] >= 10:
        return 'Loyal Customers'
    elif row['RFM_Total'] >= 7:
        return 'Potential Loyalists'
    elif row['RFM_Total'] >= 5 and row['R_Score'] >= 3:
        return 'Recent Customers'
    elif row['RFM_Total'] >= 5:
        return 'At Risk'
    else:
        return 'Lost Customers'

rfm['RFM_Segment'] = rfm.apply(segment_customers, axis=1)

# Merge RFM back with customer data
customers_analysis = customers_df.merge(rfm, on='CustomerID', how='left')

print(f"✅ Calculated RFM metrics for {len(rfm):,} customers")
print(f"\n   Segment Distribution:")
for segment in rfm['RFM_Segment'].value_counts().items():
    print(f"   {segment[0]}: {segment[1]:,} ({segment[1]/len(rfm)*100:.1f}%)")

# Monthly Aggregations for Time Series
print("\n📈 Creating Time Series Aggregations...")

monthly_sales = transactions_df.groupby([
    transactions_df['Date'].dt.to_period('M'),
    'Category'
]).agg({
    'TotalAmount': 'sum',
    'TransactionID': 'count',
    'CustomerID': 'nunique',
    'Quantity': 'sum'
}).reset_index()

monthly_sales.columns = ['Month', 'Category', 'Revenue', 'Transactions', 'Customers', 'Units']
monthly_sales['Month'] = monthly_sales['Month'].astype(str)

# Overall monthly totals
monthly_totals = transactions_df.groupby(
    transactions_df['Date'].dt.to_period('M')
).agg({
    'TotalAmount': 'sum',
    'TransactionID': 'count',
    'CustomerID': 'nunique',
    'Quantity': 'sum',
    'MarginAmount': 'sum'
}).reset_index()

monthly_totals.columns = ['Month', 'Revenue', 'Transactions', 'Customers', 'Units', 'Margin']
monthly_totals['Month'] = monthly_totals['Month'].astype(str)
monthly_totals['AvgTransactionValue'] = monthly_totals['Revenue'] / monthly_totals['Transactions']

print(f"✅ Created {len(monthly_totals)} months of time series data")

# Category Performance
print("\n🏷️ Analyzing Category Performance...")

category_performance = transactions_df.groupby('Category').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'count',
    'CustomerID': 'nunique',
    'Quantity': 'sum',
    'MarginAmount': 'sum'
}).reset_index()

category_performance.columns = ['Category', 'Revenue', 'Transactions', 'Customers', 'Units', 'Margin']
category_performance['RevenueShare'] = (category_performance['Revenue'] / category_performance['Revenue'].sum() * 100).round(2)
category_performance['AvgTransactionValue'] = (category_performance['Revenue'] / category_performance['Transactions']).round(2)
category_performance['MarginPercent'] = (category_performance['Margin'] / category_performance['Revenue'] * 100).round(2)

category_performance = category_performance.sort_values('Revenue', ascending=False)

print(f"✅ Analyzed {len(category_performance)} categories")

# Brand Performance
print("\n🏆 Analyzing Brand Performance...")

brand_performance = transactions_df.groupby(['Brand', 'BrandTier']).agg({
    'TotalAmount': 'sum',
    'TransactionID': 'count',
    'Quantity': 'sum'
}).reset_index()

brand_performance.columns = ['Brand', 'BrandTier', 'Revenue', 'Transactions', 'Units']
brand_performance = brand_performance.sort_values('Revenue', ascending=False)

print(f"✅ Analyzed {len(brand_performance)} brands")

# Store Performance
print("\n🏪 Analyzing Store Performance...")

store_performance = transactions_df.groupby('Store').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'count',
    'CustomerID': 'nunique',
    'MarginAmount': 'sum'
}).reset_index()

store_performance.columns = ['Store', 'Revenue', 'Transactions', 'Customers', 'Margin']
store_performance['AvgTransactionValue'] = (store_performance['Revenue'] / store_performance['Transactions']).round(2)
store_performance = store_performance.sort_values('Revenue', ascending=False)

print(f"✅ Analyzed {len(store_performance)} stores")

# Channel Analysis
print("\n🌐 Analyzing Channel Performance...")

channel_performance = transactions_df.groupby('Channel').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'count',
    'CustomerID': 'nunique'
}).reset_index()

channel_performance.columns = ['Channel', 'Revenue', 'Transactions', 'Customers']
channel_performance['RevenueShare'] = (channel_performance['Revenue'] / channel_performance['Revenue'].sum() * 100).round(2)

print(f"✅ Analyzed {len(channel_performance)} channels")

# Customer Lifetime Value
print("\n💰 Calculating Customer Lifetime Value...")

clv_data = transactions_df.groupby('CustomerID').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'count',
    'Date': ['min', 'max']
}).reset_index()

clv_data.columns = ['CustomerID', 'TotalRevenue', 'TotalPurchases', 'FirstPurchase', 'LastPurchase']
clv_data['CustomerTenure'] = (clv_data['LastPurchase'] - clv_data['FirstPurchase']).dt.days
clv_data['AvgOrderValue'] = clv_data['TotalRevenue'] / clv_data['TotalPurchases']

# Merge with customer segments
clv_data = clv_data.merge(customers_analysis[['CustomerID', 'RFM_Segment']], on='CustomerID', how='left')

print(f"✅ Calculated CLV for {len(clv_data):,} customers")

# Product Performance
print("\n📦 Analyzing Product Performance...")

product_performance = transactions_df.groupby(['ProductID']).agg({
    'TotalAmount': 'sum',
    'Quantity': 'sum',
    'TransactionID': 'count'
}).reset_index()

product_performance.columns = ['ProductID', 'Revenue', 'UnitsSold', 'Transactions']
product_performance = product_performance.merge(
    products_df[['ProductID', 'ProductName', 'Category', 'Brand', 'Price']], 
    on='ProductID', 
    how='left'
)
product_performance = product_performance.sort_values('Revenue', ascending=False)

print(f"✅ Analyzed {len(product_performance)} products")

# Save Processed Data
print("\n💾 Saving Processed Datasets...")

output_dir = '../data/processed/'
os.makedirs(output_dir, exist_ok=True)

# Save all processed datasets
transactions_df.to_csv(f'{output_dir}transactions_processed.csv', index=False)
customers_analysis.to_csv(f'{output_dir}customers_rfm.csv', index=False)
rfm.to_csv(f'{output_dir}rfm_analysis.csv', index=False)
monthly_sales.to_csv(f'{output_dir}monthly_sales_by_category.csv', index=False)
monthly_totals.to_csv(f'{output_dir}monthly_totals.csv', index=False)
category_performance.to_csv(f'{output_dir}category_performance.csv', index=False)
brand_performance.to_csv(f'{output_dir}brand_performance.csv', index=False)
store_performance.to_csv(f'{output_dir}store_performance.csv', index=False)
channel_performance.to_csv(f'{output_dir}channel_performance.csv', index=False)
clv_data.to_csv(f'{output_dir}customer_lifetime_value.csv', index=False)
product_performance.to_csv(f'{output_dir}product_performance.csv', index=False)

print(f"✅ Saved 11 processed datasets to {output_dir}")

# Generate Summary Report
print("\n" + "=" * 70)
print("PROCESSING SUMMARY")
print("=" * 70)

print(f"\n📊 Overall Metrics:")
print(f"   Total Revenue: ₹{transactions_df['TotalAmount'].sum():,.2f}")
print(f"   Total Margin: ₹{transactions_df['MarginAmount'].sum():,.2f}")
print(f"   Avg Margin %: {(transactions_df['MarginAmount'].sum() / transactions_df['TotalAmount'].sum() * 100):.2f}%")
print(f"   Total Transactions: {len(transactions_df):,}")
print(f"   Unique Customers: {transactions_df['CustomerID'].nunique():,}")
print(f"   Avg Transaction Value: ₹{transactions_df['TotalAmount'].mean():,.2f}")

print(f"\n🏆 Top Performing Category:")
top_cat = category_performance.iloc[0]
print(f"   {top_cat['Category']}: ₹{top_cat['Revenue']:,.0f} ({top_cat['RevenueShare']:.1f}%)")

print(f"\n🏪 Top Performing Store:")
top_store = store_performance.iloc[0]
print(f"   {top_store['Store']}: ₹{top_store['Revenue']:,.0f}")

print(f"\n👥 Top Customer Segment:")
top_segment = rfm['RFM_Segment'].value_counts().iloc[0]
print(f"   {rfm['RFM_Segment'].value_counts().index[0]}: {top_segment:,} customers")

print(f"\n💰 CLV Insights:")
print(f"   Avg Customer Lifetime Value: ₹{clv_data['TotalRevenue'].mean():,.2f}")
print(f"   Avg Customer Tenure: {clv_data['CustomerTenure'].mean():.0f} days")
print(f"   Avg Purchases per Customer: {clv_data['TotalPurchases'].mean():.1f}")

print(f"\n📈 Growth Metrics:")
first_month_revenue = monthly_totals.iloc[0]['Revenue']
last_month_revenue = monthly_totals.iloc[-1]['Revenue']
growth = ((last_month_revenue - first_month_revenue) / first_month_revenue * 100)
print(f"   Revenue Growth: {growth:+.1f}% (first vs last month)")

print("\n" + "=" * 70)
print("✅ DATA PROCESSING COMPLETE!")
print("=" * 70)
print("\nProcessed datasets ready for:")
print("   • ML Model Training (Forecasting & Segmentation)")
print("   • Dashboard Visualization")
print("   • Business Intelligence Reporting")
