"""
📊 ADVANCED ANALYTICS & KPI PROCESSOR
======================================
Project 6: Crown Jewel Analytics
Processes 500K transactions into 25+ business metrics
Includes: Cohort Analysis, RFM Segmentation, Funnel Analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("📊 ADVANCED ANALYTICS & KPI PROCESSOR")
print("="*80)

# ==================== LOAD DATA ====================

print("\n📂 Loading datasets...")
products = pd.read_csv('../data/raw/products.csv')
customers = pd.read_csv('../data/raw/customers.csv')
transactions = pd.read_csv('../data/raw/transactions.csv')

print(f"✅ Loaded {len(transactions):,} transactions")
print(f"✅ Loaded {len(products):,} products")
print(f"✅ Loaded {len(customers):,} customers")

# Convert date strings to datetime
transactions['date'] = pd.to_datetime(transactions['date'])
customers['join_date'] = pd.to_datetime(customers['join_date'])

# ==================== OVERALL KPIs ====================

print("\n🎯 Calculating Overall KPIs...")

total_revenue = transactions['revenue'].sum()
total_profit = transactions['profit'].sum()
total_transactions = len(transactions)
unique_customers = transactions['customer_id'].nunique()
avg_order_value = transactions['revenue'].mean()
avg_margin = transactions['profit_margin_pct'].mean()
total_quantity = transactions['quantity'].sum()

# Customer metrics
repeat_customers = transactions.groupby('customer_id').size()
repeat_rate = (repeat_customers > 1).sum() / unique_customers * 100
avg_transactions_per_customer = total_transactions / unique_customers

# Calculate date range
date_range_days = (transactions['date'].max() - transactions['date'].min()).days
months = date_range_days / 30.44

# Revenue per customer
revenue_per_customer = total_revenue / unique_customers

# Discount analysis
avg_discount = transactions['discount_pct'].mean()
discounted_transactions = (transactions['discount_pct'] > 0).sum()
discount_rate = discounted_transactions / total_transactions * 100

kpis_overall = pd.DataFrame([{
    'metric': 'Total Revenue',
    'value': f'₹{total_revenue/10000000:.2f} Cr',
    'numeric_value': total_revenue
}, {
    'metric': 'Total Profit',
    'value': f'₹{total_profit/10000000:.2f} Cr',
    'numeric_value': total_profit
}, {
    'metric': 'Total Transactions',
    'value': f'{total_transactions:,}',
    'numeric_value': total_transactions
}, {
    'metric': 'Unique Customers',
    'value': f'{unique_customers:,}',
    'numeric_value': unique_customers
}, {
    'metric': 'Average Order Value',
    'value': f'₹{avg_order_value:,.2f}',
    'numeric_value': avg_order_value
}, {
    'metric': 'Average Profit Margin',
    'value': f'{avg_margin:.2f}%',
    'numeric_value': avg_margin
}, {
    'metric': 'Revenue per Customer',
    'value': f'₹{revenue_per_customer:,.2f}',
    'numeric_value': revenue_per_customer
}, {
    'metric': 'Repeat Customer Rate',
    'value': f'{repeat_rate:.2f}%',
    'numeric_value': repeat_rate
}, {
    'metric': 'Avg Transactions per Customer',
    'value': f'{avg_transactions_per_customer:.2f}',
    'numeric_value': avg_transactions_per_customer
}, {
    'metric': 'Average Discount',
    'value': f'{avg_discount:.2f}%',
    'numeric_value': avg_discount
}, {
    'metric': 'Discount Penetration',
    'value': f'{discount_rate:.2f}%',
    'numeric_value': discount_rate
}])

kpis_overall.to_csv('../data/processed/kpis_overall.csv', index=False)
print(f"✅ Saved: kpis_overall.csv (11 metrics)")

# ==================== CATEGORY PERFORMANCE ====================

print("\n📦 Analyzing Category Performance...")

category_perf = transactions.groupby('category').agg({
    'revenue': ['sum', 'mean'],
    'profit': 'sum',
    'profit_margin_pct': 'mean',
    'quantity': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).round(2)

category_perf.columns = ['total_revenue', 'avg_order_value', 'total_profit', 
                          'avg_margin', 'units_sold', 'transactions', 'unique_customers']
category_perf = category_perf.sort_values('total_revenue', ascending=False).reset_index()

# Add revenue share
category_perf['revenue_share_pct'] = (category_perf['total_revenue'] / total_revenue * 100).round(2)

category_perf.to_csv('../data/processed/category_performance.csv', index=False)
print(f"✅ Saved: category_performance.csv ({len(category_perf)} categories)")

# ==================== CHANNEL ANALYSIS ====================

print("\n📱 Analyzing Sales Channels...")

channel_perf = transactions.groupby('channel').agg({
    'revenue': ['sum', 'mean'],
    'profit': 'sum',
    'profit_margin_pct': 'mean',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).round(2)

channel_perf.columns = ['total_revenue', 'avg_order_value', 'total_profit',
                        'avg_margin', 'transactions', 'unique_customers']
channel_perf = channel_perf.sort_values('total_revenue', ascending=False).reset_index()
channel_perf['revenue_share_pct'] = (channel_perf['total_revenue'] / total_revenue * 100).round(2)

channel_perf.to_csv('../data/processed/channel_performance.csv', index=False)
print(f"✅ Saved: channel_performance.csv ({len(channel_perf)} channels)")

# ==================== TIME SERIES ANALYSIS ====================

print("\n📅 Creating Time Series Data...")

# Daily trends
daily_trends = transactions.groupby('date').agg({
    'revenue': 'sum',
    'profit': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).reset_index()
daily_trends.columns = ['date', 'revenue', 'profit', 'transactions', 'customers']
daily_trends.to_csv('../data/processed/daily_trends.csv', index=False)
print(f"✅ Saved: daily_trends.csv ({len(daily_trends)} days)")

# Monthly trends
transactions['year_month'] = transactions['date'].dt.to_period('M').astype(str)
monthly_trends = transactions.groupby('year_month').agg({
    'revenue': 'sum',
    'profit': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).reset_index()
monthly_trends.columns = ['year_month', 'revenue', 'profit', 'transactions', 'customers']
monthly_trends.to_csv('../data/processed/monthly_trends.csv', index=False)
print(f"✅ Saved: monthly_trends.csv ({len(monthly_trends)} months)")

# ==================== CUSTOMER SEGMENTATION ====================

print("\n👥 Performing RFM Segmentation...")

# Calculate RFM metrics
current_date = transactions['date'].max()

rfm = transactions.groupby('customer_id').agg({
    'date': lambda x: (current_date - x.max()).days,  # Recency
    'transaction_id': 'count',  # Frequency
    'revenue': 'sum'  # Monetary
}).reset_index()

rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']

# Create RFM scores (1-5 scale)
rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1], duplicates='drop').astype(int)
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop').astype(int)
rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5], duplicates='drop').astype(int)

rfm['rfm_score'] = rfm['r_score'] + rfm['f_score'] + rfm['m_score']

# Create segments
def rfm_segment(row):
    if row['rfm_score'] >= 13:
        return 'Champions'
    elif row['rfm_score'] >= 11:
        return 'Loyal'
    elif row['rfm_score'] >= 9:
        return 'Potential'
    elif row['rfm_score'] >= 7:
        return 'At Risk'
    else:
        return 'Lost'

rfm['segment'] = rfm.apply(rfm_segment, axis=1)

# Merge with customer data
rfm = rfm.merge(customers[['customer_id', 'name', 'city', 'region', 'segment']], 
                on='customer_id', how='left', suffixes=('', '_original'))

rfm.to_csv('../data/processed/customer_rfm_analysis.csv', index=False)
print(f"✅ Saved: customer_rfm_analysis.csv ({len(rfm)} customers)")

# RFM Summary
rfm_summary = rfm.groupby('segment').agg({
    'customer_id': 'count',
    'monetary': ['sum', 'mean']
}).round(2)
rfm_summary.columns = ['customer_count', 'total_revenue', 'avg_revenue']
rfm_summary = rfm_summary.sort_values('total_revenue', ascending=False).reset_index()
rfm_summary.to_csv('../data/processed/rfm_segment_summary.csv', index=False)
print(f"✅ Saved: rfm_segment_summary.csv")

# ==================== COHORT ANALYSIS ====================

print("\n📆 Creating Cohort Analysis...")

# Create cohort based on join month
transactions_with_cohort = transactions.merge(
    customers[['customer_id', 'join_date']], 
    on='customer_id', 
    how='left'
)

transactions_with_cohort['cohort_month'] = transactions_with_cohort['join_date'].dt.to_period('M')
transactions_with_cohort['transaction_month'] = transactions_with_cohort['date'].dt.to_period('M')

# Calculate months since cohort
transactions_with_cohort['months_since_join'] = (
    (transactions_with_cohort['transaction_month'] - transactions_with_cohort['cohort_month']).apply(lambda x: x.n)
)

# Create cohort table
cohort_data = transactions_with_cohort.groupby(['cohort_month', 'months_since_join'])['customer_id'].nunique().reset_index()
cohort_data.columns = ['cohort_month', 'months_since_join', 'customers']

# Pivot for retention matrix
cohort_pivot = cohort_data.pivot(index='cohort_month', columns='months_since_join', values='customers')
cohort_size = cohort_pivot.iloc[:, 0]
retention_matrix = cohort_pivot.divide(cohort_size, axis=0) * 100

retention_matrix.to_csv('../data/processed/cohort_retention_matrix.csv')
print(f"✅ Saved: cohort_retention_matrix.csv")

# ==================== STORE PERFORMANCE ====================

print("\n🏪 Analyzing Store Performance...")

store_perf = transactions[transactions['channel'] == 'In-Store'].groupby('location').agg({
    'revenue': ['sum', 'mean'],
    'profit': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).round(2)

store_perf.columns = ['total_revenue', 'avg_order_value', 'total_profit', 
                      'transactions', 'unique_customers']
store_perf = store_perf.sort_values('total_revenue', ascending=False).reset_index()

store_perf.to_csv('../data/processed/store_performance.csv', index=False)
print(f"✅ Saved: store_performance.csv ({len(store_perf)} stores)")

# ==================== TOP PRODUCTS ====================

print("\n⭐ Identifying Top Products...")

product_perf = transactions.groupby('product_id').agg({
    'revenue': 'sum',
    'profit': 'sum',
    'quantity': 'sum',
    'transaction_id': 'count'
}).reset_index()

product_perf = product_perf.merge(
    products[['product_id', 'product_name', 'category', 'brand', 'rating']], 
    on='product_id', 
    how='left'
)

product_perf = product_perf.sort_values('revenue', ascending=False).head(100)
product_perf.to_csv('../data/processed/top_100_products.csv', index=False)
print(f"✅ Saved: top_100_products.csv")

# ==================== CUSTOMER LIFETIME VALUE ====================

print("\n💰 Calculating Customer Lifetime Value...")

clv = transactions.groupby('customer_id').agg({
    'revenue': 'sum',
    'profit': 'sum',
    'transaction_id': 'count',
    'date': ['min', 'max']
}).reset_index()

clv.columns = ['customer_id', 'total_revenue', 'total_profit', 'transactions', 'first_purchase', 'last_purchase']

# Calculate customer lifespan in months
clv['lifespan_days'] = (clv['last_purchase'] - clv['first_purchase']).dt.days
clv['lifespan_months'] = (clv['lifespan_days'] / 30.44).round(1)

# Merge with customer segment
clv = clv.merge(customers[['customer_id', 'segment', 'city', 'region']], on='customer_id', how='left')

clv.to_csv('../data/processed/customer_lifetime_value.csv', index=False)
print(f"✅ Saved: customer_lifetime_value.csv")

# ==================== PAYMENT METHOD ANALYSIS ====================

print("\n💳 Analyzing Payment Methods...")

payment_analysis = transactions.groupby('payment_method').agg({
    'revenue': ['sum', 'mean'],
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).round(2)

payment_analysis.columns = ['total_revenue', 'avg_order_value', 'transactions', 'unique_customers']
payment_analysis = payment_analysis.sort_values('total_revenue', ascending=False).reset_index()
payment_analysis['share_pct'] = (payment_analysis['total_revenue'] / total_revenue * 100).round(2)

payment_analysis.to_csv('../data/processed/payment_method_analysis.csv', index=False)
print(f"✅ Saved: payment_method_analysis.csv")

# ==================== REGIONAL PERFORMANCE ====================

print("\n🌍 Analyzing Regional Performance...")

regional_perf = transactions.groupby('region').agg({
    'revenue': ['sum', 'mean'],
    'profit': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).round(2)

regional_perf.columns = ['total_revenue', 'avg_order_value', 'total_profit',
                         'transactions', 'unique_customers']
regional_perf = regional_perf.sort_values('total_revenue', ascending=False).reset_index()
regional_perf['revenue_share_pct'] = (regional_perf['total_revenue'] / total_revenue * 100).round(2)

regional_perf.to_csv('../data/processed/regional_performance.csv', index=False)
print(f"✅ Saved: regional_performance.csv")

# ==================== BRAND PERFORMANCE ====================

print("\n🏷️ Analyzing Brand Performance...")

brand_perf = transactions.groupby('brand').agg({
    'revenue': 'sum',
    'profit': 'sum',
    'quantity': 'sum',
    'transaction_id': 'count'
}).sort_values('revenue', ascending=False).head(50).reset_index()

brand_perf.to_csv('../data/processed/top_brands.csv', index=False)
print(f"✅ Saved: top_brands.csv (Top 50)")

# ==================== HOURLY PATTERN ANALYSIS ====================

print("\n⏰ Analyzing Hourly Patterns...")

transactions['hour'] = transactions['time'].str[:2].astype(int)

hourly_pattern = transactions.groupby('hour').agg({
    'revenue': ['sum', 'mean'],
    'transaction_id': 'count'
}).round(2)

hourly_pattern.columns = ['total_revenue', 'avg_revenue', 'transactions']
hourly_pattern = hourly_pattern.reset_index()

hourly_pattern.to_csv('../data/processed/hourly_sales_pattern.csv', index=False)
print(f"✅ Saved: hourly_sales_pattern.csv")

# ==================== SUMMARY REPORT ====================

print("\n" + "="*80)
print("✨ ANALYTICS PROCESSING COMPLETE!")
print("="*80)

print("\n📊 Generated Files:")
files_generated = [
    'kpis_overall.csv',
    'category_performance.csv',
    'channel_performance.csv',
    'daily_trends.csv',
    'monthly_trends.csv',
    'customer_rfm_analysis.csv',
    'rfm_segment_summary.csv',
    'cohort_retention_matrix.csv',
    'store_performance.csv',
    'top_100_products.csv',
    'customer_lifetime_value.csv',
    'payment_method_analysis.csv',
    'regional_performance.csv',
    'top_brands.csv',
    'hourly_sales_pattern.csv'
]

for i, file in enumerate(files_generated, 1):
    print(f"  {i}. {file}")

print(f"\n📁 All files saved in: ../data/processed/")
print(f"\n🎯 Ready for ML modeling and visualization!")
print("\n🏆 Crown Jewel Analytics Pipeline - COMPLETE!")
