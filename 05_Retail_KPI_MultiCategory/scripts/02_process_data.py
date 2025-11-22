"""
Multi-Category Retail KPI Data Processing & Analysis
====================================================
Processes raw data and calculates comprehensive KPIs:
- Category-wise performance metrics
- Time series analysis (daily, weekly, monthly, quarterly)
- Store performance analysis
- Customer segment analysis
- Product performance tracking
- Channel analysis
- Advanced KPI calculations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# Create output directory
os.makedirs('../data/processed', exist_ok=True)

print("=" * 80)
print("MULTI-CATEGORY RETAIL KPI PROCESSOR")
print("=" * 80)

# ============================================================================
# 1. LOAD RAW DATA
# ============================================================================

def load_data():
    """Load all raw datasets"""
    
    print("\n📂 Loading Raw Data...")
    
    products = pd.read_csv('../data/raw/products.csv')
    customers = pd.read_csv('../data/raw/customers.csv')
    transactions = pd.read_csv('../data/raw/transactions.csv')
    
    # Convert date columns
    transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
    customers['join_date'] = pd.to_datetime(customers['join_date'])
    
    print(f"  ✅ Products: {len(products):,} rows")
    print(f"  ✅ Customers: {len(customers):,} rows")
    print(f"  ✅ Transactions: {len(transactions):,} rows")
    
    # Data quality check
    print("\n🔍 Data Quality Check:")
    print(f"  • Missing values in transactions: {transactions.isnull().sum().sum()}")
    print(f"  • Duplicate transactions: {transactions['transaction_id'].duplicated().sum()}")
    print(f"  • Date range: {transactions['transaction_date'].min().date()} to {transactions['transaction_date'].max().date()}")
    
    return products, customers, transactions

# ============================================================================
# 2. CALCULATE OVERALL KPIs
# ============================================================================

def calculate_overall_kpis(df):
    """Calculate high-level business KPIs"""
    
    print("\n📊 Calculating Overall KPIs...")
    
    kpis = {
        # Revenue Metrics
        'total_revenue': df['net_amount'].sum(),
        'total_transactions': len(df),
        'total_profit': df['profit'].sum(),
        'avg_transaction_value': df['net_amount'].mean(),
        'avg_profit_per_transaction': df['profit'].mean(),
        'avg_margin_pct': df['margin_pct'].mean(),
        
        # Customer Metrics
        'total_customers': df['customer_id'].nunique(),
        'avg_transactions_per_customer': len(df) / df['customer_id'].nunique(),
        'avg_revenue_per_customer': df['net_amount'].sum() / df['customer_id'].nunique(),
        
        # Product Metrics
        'total_products_sold': df['product_id'].nunique(),
        'total_quantity_sold': df['quantity'].sum(),
        'avg_quantity_per_transaction': df['quantity'].mean(),
        
        # Discount Metrics
        'total_discount': df['discount_amount'].sum(),
        'avg_discount_pct': df['discount_pct'].mean(),
        'discount_to_revenue_ratio': (df['discount_amount'].sum() / df['gross_amount'].sum() * 100),
        
        # Period Metrics
        'start_date': df['transaction_date'].min(),
        'end_date': df['transaction_date'].max(),
        'total_days': (df['transaction_date'].max() - df['transaction_date'].min()).days,
        'avg_daily_revenue': df['net_amount'].sum() / (df['transaction_date'].max() - df['transaction_date'].min()).days
    }
    
    # Convert to DataFrame
    kpi_df = pd.DataFrame([kpis])
    
    print(f"  ✅ Calculated {len(kpis)} overall KPIs")
    print(f"\n  Key Highlights:")
    print(f"    • Total Revenue: ₹{kpis['total_revenue']/10000000:.2f} Cr")
    print(f"    • Total Profit: ₹{kpis['total_profit']/10000000:.2f} Cr")
    print(f"    • Avg Margin: {kpis['avg_margin_pct']:.2f}%")
    print(f"    • Total Customers: {kpis['total_customers']:,}")
    print(f"    • Avg Transaction Value: ₹{kpis['avg_transaction_value']:.2f}")
    
    return kpi_df

# ============================================================================
# 3. CATEGORY-WISE KPI ANALYSIS
# ============================================================================

def analyze_category_performance(df):
    """Detailed category-wise performance analysis"""
    
    print("\n📦 Analyzing Category Performance...")
    
    category_kpis = df.groupby('category').agg({
        'transaction_id': 'count',
        'net_amount': ['sum', 'mean'],
        'profit': ['sum', 'mean'],
        'margin_pct': 'mean',
        'quantity': 'sum',
        'customer_id': 'nunique',
        'product_id': 'nunique',
        'discount_amount': 'sum',
        'discount_pct': 'mean'
    }).reset_index()
    
    # Flatten column names
    category_kpis.columns = [
        'category', 'transactions', 'revenue', 'avg_transaction_value',
        'profit', 'avg_profit', 'avg_margin_pct', 'quantity_sold',
        'unique_customers', 'unique_products', 'total_discount', 'avg_discount_pct'
    ]
    
    # Calculate additional metrics
    category_kpis['revenue_share_pct'] = (category_kpis['revenue'] / category_kpis['revenue'].sum() * 100)
    category_kpis['profit_share_pct'] = (category_kpis['profit'] / category_kpis['profit'].sum() * 100)
    category_kpis['transactions_per_customer'] = category_kpis['transactions'] / category_kpis['unique_customers']
    category_kpis['revenue_per_customer'] = category_kpis['revenue'] / category_kpis['unique_customers']
    
    # Sort by revenue
    category_kpis = category_kpis.sort_values('revenue', ascending=False).reset_index(drop=True)
    
    print(f"  ✅ Analyzed {len(category_kpis)} categories")
    print(f"\n  Top 3 Categories by Revenue:")
    for idx, row in category_kpis.head(3).iterrows():
        print(f"    {idx+1}. {row['category']}: ₹{row['revenue']/10000000:.2f} Cr ({row['revenue_share_pct']:.1f}%)")
    
    return category_kpis

# ============================================================================
# 4. TIME SERIES ANALYSIS
# ============================================================================

def create_time_series_data(df):
    """Create daily, weekly, monthly, and quarterly time series"""
    
    print("\n📅 Creating Time Series Data...")
    
    # Daily aggregation
    daily = df.groupby('transaction_date').agg({
        'transaction_id': 'count',
        'net_amount': 'sum',
        'profit': 'sum',
        'margin_pct': 'mean',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    
    daily.columns = ['date', 'transactions', 'revenue', 'profit', 'avg_margin_pct', 'customers', 'quantity']
    print(f"  ✅ Daily data: {len(daily)} days")
    
    # Add time features
    daily['year'] = daily['date'].dt.year
    daily['month'] = daily['date'].dt.month
    daily['quarter'] = daily['date'].dt.quarter
    daily['week'] = daily['date'].dt.isocalendar().week
    daily['day_of_week'] = daily['date'].dt.dayofweek
    daily['day_name'] = daily['date'].dt.day_name()
    daily['is_weekend'] = daily['day_of_week'].isin([5, 6]).astype(int)
    
    # Monthly aggregation
    df['year_month'] = df['transaction_date'].dt.to_period('M')
    monthly = df.groupby('year_month').agg({
        'transaction_id': 'count',
        'net_amount': 'sum',
        'profit': 'sum',
        'margin_pct': 'mean',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    
    monthly.columns = ['year_month', 'transactions', 'revenue', 'profit', 'avg_margin_pct', 'customers', 'quantity']
    monthly['year_month'] = monthly['year_month'].astype(str)
    
    # Calculate growth rates
    monthly['revenue_growth_pct'] = monthly['revenue'].pct_change() * 100
    monthly['transaction_growth_pct'] = monthly['transactions'].pct_change() * 100
    
    print(f"  ✅ Monthly data: {len(monthly)} months")
    
    # Quarterly aggregation
    df['year_quarter'] = df['transaction_date'].dt.to_period('Q')
    quarterly = df.groupby('year_quarter').agg({
        'transaction_id': 'count',
        'net_amount': 'sum',
        'profit': 'sum',
        'margin_pct': 'mean',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    
    quarterly.columns = ['year_quarter', 'transactions', 'revenue', 'profit', 'avg_margin_pct', 'customers', 'quantity']
    quarterly['year_quarter'] = quarterly['year_quarter'].astype(str)
    
    print(f"  ✅ Quarterly data: {len(quarterly)} quarters")
    
    return daily, monthly, quarterly

# ============================================================================
# 5. STORE PERFORMANCE ANALYSIS
# ============================================================================

def analyze_store_performance(df):
    """Analyze performance by store"""
    
    print("\n🏪 Analyzing Store Performance...")
    
    store_kpis = df.groupby(['store_id', 'store_name', 'store_type']).agg({
        'transaction_id': 'count',
        'net_amount': 'sum',
        'profit': 'sum',
        'margin_pct': 'mean',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    
    store_kpis.columns = [
        'store_id', 'store_name', 'store_type', 'transactions',
        'revenue', 'profit', 'avg_margin_pct', 'customers', 'quantity'
    ]
    
    # Calculate metrics
    store_kpis['revenue_share_pct'] = (store_kpis['revenue'] / store_kpis['revenue'].sum() * 100)
    store_kpis['avg_transaction_value'] = store_kpis['revenue'] / store_kpis['transactions']
    store_kpis['revenue_per_customer'] = store_kpis['revenue'] / store_kpis['customers']
    
    # Sort by revenue
    store_kpis = store_kpis.sort_values('revenue', ascending=False).reset_index(drop=True)
    
    print(f"  ✅ Analyzed {len(store_kpis)} stores")
    print(f"\n  Top 5 Stores by Revenue:")
    for idx, row in store_kpis.head(5).iterrows():
        print(f"    {idx+1}. {row['store_name']}: ₹{row['revenue']/10000000:.2f} Cr ({row['store_type']})")
    
    return store_kpis

# ============================================================================
# 6. CUSTOMER SEGMENT ANALYSIS
# ============================================================================

def analyze_customer_segments(df, customers):
    """Analyze performance by customer segment"""
    
    print("\n👥 Analyzing Customer Segments...")
    
    segment_kpis = df.groupby('customer_segment').agg({
        'transaction_id': 'count',
        'net_amount': 'sum',
        'profit': 'sum',
        'margin_pct': 'mean',
        'customer_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    
    segment_kpis.columns = [
        'segment', 'transactions', 'revenue', 'profit',
        'avg_margin_pct', 'customers', 'quantity'
    ]
    
    # Calculate metrics
    segment_kpis['revenue_per_customer'] = segment_kpis['revenue'] / segment_kpis['customers']
    segment_kpis['transactions_per_customer'] = segment_kpis['transactions'] / segment_kpis['customers']
    segment_kpis['avg_transaction_value'] = segment_kpis['revenue'] / segment_kpis['transactions']
    segment_kpis['customer_share_pct'] = (segment_kpis['customers'] / segment_kpis['customers'].sum() * 100)
    segment_kpis['revenue_share_pct'] = (segment_kpis['revenue'] / segment_kpis['revenue'].sum() * 100)
    
    # Sort by revenue per customer
    segment_kpis = segment_kpis.sort_values('revenue_per_customer', ascending=False).reset_index(drop=True)
    
    print(f"  ✅ Analyzed {len(segment_kpis)} customer segments")
    print(f"\n  Segment Value Rankings:")
    for idx, row in segment_kpis.iterrows():
        print(f"    {idx+1}. {row['segment']}: ₹{row['revenue_per_customer']:,.0f} per customer ({row['customer_share_pct']:.1f}% of base)")
    
    return segment_kpis

# ============================================================================
# 7. CHANNEL ANALYSIS
# ============================================================================

def analyze_channel_performance(df):
    """Analyze performance by sales channel"""
    
    print("\n📱 Analyzing Channel Performance...")
    
    channel_kpis = df.groupby('channel').agg({
        'transaction_id': 'count',
        'net_amount': 'sum',
        'profit': 'sum',
        'margin_pct': 'mean',
        'customer_id': 'nunique',
        'discount_pct': 'mean'
    }).reset_index()
    
    channel_kpis.columns = [
        'channel', 'transactions', 'revenue', 'profit',
        'avg_margin_pct', 'customers', 'avg_discount_pct'
    ]
    
    # Calculate metrics
    channel_kpis['revenue_share_pct'] = (channel_kpis['revenue'] / channel_kpis['revenue'].sum() * 100)
    channel_kpis['transaction_share_pct'] = (channel_kpis['transactions'] / channel_kpis['transactions'].sum() * 100)
    channel_kpis['avg_transaction_value'] = channel_kpis['revenue'] / channel_kpis['transactions']
    
    # Sort by revenue
    channel_kpis = channel_kpis.sort_values('revenue', ascending=False).reset_index(drop=True)
    
    print(f"  ✅ Analyzed {len(channel_kpis)} channels")
    for idx, row in channel_kpis.iterrows():
        print(f"    • {row['channel']}: ₹{row['revenue']/10000000:.2f} Cr ({row['revenue_share_pct']:.1f}%)")
    
    return channel_kpis

# ============================================================================
# 8. PRODUCT PERFORMANCE ANALYSIS
# ============================================================================

def analyze_product_performance(df):
    """Analyze top performing products"""
    
    print("\n🏆 Analyzing Product Performance...")
    
    product_kpis = df.groupby(['product_id', 'product_name', 'category', 'brand']).agg({
        'transaction_id': 'count',
        'net_amount': 'sum',
        'profit': 'sum',
        'margin_pct': 'mean',
        'quantity': 'sum'
    }).reset_index()
    
    product_kpis.columns = [
        'product_id', 'product_name', 'category', 'brand',
        'transactions', 'revenue', 'profit', 'avg_margin_pct', 'quantity'
    ]
    
    # Sort by revenue
    product_kpis = product_kpis.sort_values('revenue', ascending=False).reset_index(drop=True)
    
    print(f"  ✅ Analyzed {len(product_kpis)} products")
    print(f"\n  Top 10 Products by Revenue:")
    for idx, row in product_kpis.head(10).iterrows():
        print(f"    {idx+1}. {row['product_name'][:50]}: ₹{row['revenue']/100000:.2f} L")
    
    return product_kpis

# ============================================================================
# 9. CATEGORY-MONTH MATRIX
# ============================================================================

def create_category_month_matrix(df):
    """Create category performance by month for trend analysis"""
    
    print("\n📊 Creating Category-Month Performance Matrix...")
    
    df['year_month'] = df['transaction_date'].dt.to_period('M').astype(str)
    
    category_month = df.groupby(['year_month', 'category']).agg({
        'transaction_id': 'count',
        'net_amount': 'sum',
        'profit': 'sum',
        'margin_pct': 'mean',
        'customer_id': 'nunique'
    }).reset_index()
    
    category_month.columns = [
        'year_month', 'category', 'transactions', 'revenue',
        'profit', 'avg_margin_pct', 'customers'
    ]
    
    print(f"  ✅ Created matrix with {len(category_month)} records")
    
    return category_month

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\nStarting KPI processing...\n")
    
    # Load data
    products, customers, transactions = load_data()
    
    # Calculate KPIs
    overall_kpis = calculate_overall_kpis(transactions)
    category_kpis = analyze_category_performance(transactions)
    daily_ts, monthly_ts, quarterly_ts = create_time_series_data(transactions)
    store_kpis = analyze_store_performance(transactions)
    segment_kpis = analyze_customer_segments(transactions, customers)
    channel_kpis = analyze_channel_performance(transactions)
    product_kpis = analyze_product_performance(transactions)
    category_month = create_category_month_matrix(transactions)
    
    # Save all processed data
    print("\n💾 Saving Processed Data...")
    
    overall_kpis.to_csv('../data/processed/overall_kpis.csv', index=False)
    print(f"  ✅ Saved: overall_kpis.csv")
    
    category_kpis.to_csv('../data/processed/category_kpis.csv', index=False)
    print(f"  ✅ Saved: category_kpis.csv")
    
    daily_ts.to_csv('../data/processed/daily_time_series.csv', index=False)
    print(f"  ✅ Saved: daily_time_series.csv ({len(daily_ts)} days)")
    
    monthly_ts.to_csv('../data/processed/monthly_time_series.csv', index=False)
    print(f"  ✅ Saved: monthly_time_series.csv ({len(monthly_ts)} months)")
    
    quarterly_ts.to_csv('../data/processed/quarterly_time_series.csv', index=False)
    print(f"  ✅ Saved: quarterly_time_series.csv ({len(quarterly_ts)} quarters)")
    
    store_kpis.to_csv('../data/processed/store_kpis.csv', index=False)
    print(f"  ✅ Saved: store_kpis.csv ({len(store_kpis)} stores)")
    
    segment_kpis.to_csv('../data/processed/segment_kpis.csv', index=False)
    print(f"  ✅ Saved: segment_kpis.csv ({len(segment_kpis)} segments)")
    
    channel_kpis.to_csv('../data/processed/channel_kpis.csv', index=False)
    print(f"  ✅ Saved: channel_kpis.csv ({len(channel_kpis)} channels)")
    
    product_kpis.to_csv('../data/processed/product_kpis.csv', index=False)
    print(f"  ✅ Saved: product_kpis.csv ({len(product_kpis)} products)")
    
    category_month.to_csv('../data/processed/category_month_matrix.csv', index=False)
    print(f"  ✅ Saved: category_month_matrix.csv ({len(category_month)} records)")
    
    print("\n" + "=" * 80)
    print("✨ KPI PROCESSING COMPLETE!")
    print("=" * 80)
    print("\n📁 Files saved in: ../data/processed/")
    print("  • overall_kpis.csv")
    print("  • category_kpis.csv")
    print("  • daily_time_series.csv")
    print("  • monthly_time_series.csv")
    print("  • quarterly_time_series.csv")
    print("  • store_kpis.csv")
    print("  • segment_kpis.csv")
    print("  • channel_kpis.csv")
    print("  • product_kpis.csv")
    print("  • category_month_matrix.csv")
    print("\n🎯 Ready for ML modeling!")
