"""
Dashboard Export Script
Prepares cleaned data for Power BI/Excel dashboards:
- Aggregates data at multiple levels
- Creates dimension tables
- Exports dashboard-ready CSV files
- Generates KPI summary
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_clean_data(file_path):
    """Load cleaned data"""
    print(f"Loading cleaned data from: {file_path}")
    df = pd.read_csv(file_path, parse_dates=['Date'])
    print(f"Loaded {len(df)} records")
    return df

def create_fact_table(df):
    """Create fact table for dashboard"""
    
    print("\n" + "="*60)
    print("CREATING FACT TABLE")
    print("="*60)
    
    # Select essential columns for dashboard
    fact_columns = [
        'Date', 'Year', 'Month', 'MonthName', 'Week', 'Quarter',
        'DayOfWeek', 'DayName', 'IsWeekend',
        'Store', 'Category', 'SubCategory', 'Brand', 'SKU',
        'MRP', 'SellingPrice', 'Qty', 'NETAMT',
        'DiscountPct', 'DiscountAmount', 'DiscountSegment',
        'PriceSegment', 'TransactionSize',
        'Footfall', 'ConversionPct',
        'AvgUnitPrice'
    ]
    
    fact_table = df[fact_columns].copy()
    print(f"✓ Fact table created with {len(fact_table)} records and {len(fact_columns)} columns")
    
    return fact_table

def create_daily_aggregation(df):
    """Create daily level aggregation"""
    
    daily_agg = df.groupby(['Date', 'Store']).agg({
        'NETAMT': 'sum',
        'Qty': 'sum',
        'Footfall': 'mean',
        'ConversionPct': 'mean',
        'DiscountPct': 'mean'
    }).reset_index()
    
    daily_agg.columns = ['Date', 'Store', 'Revenue', 'Units_Sold', 'Footfall', 'Conversion_Rate', 'Avg_Discount']
    daily_agg['Transactions'] = df.groupby(['Date', 'Store']).size().values
    daily_agg['Avg_Transaction_Value'] = (daily_agg['Revenue'] / daily_agg['Transactions']).round(2)
    
    # Add time features
    daily_agg['Year'] = daily_agg['Date'].dt.year
    daily_agg['Month'] = daily_agg['Date'].dt.month
    daily_agg['Week'] = daily_agg['Date'].dt.isocalendar().week
    daily_agg['DayName'] = daily_agg['Date'].dt.strftime('%A')
    
    print(f"✓ Daily aggregation created with {len(daily_agg)} records")
    
    return daily_agg

def create_category_aggregation(df):
    """Create category level aggregation"""
    
    category_agg = df.groupby(['Category', 'SubCategory']).agg({
        'NETAMT': ['sum', 'mean', 'count'],
        'Qty': 'sum',
        'DiscountPct': 'mean',
        'SKU': 'nunique'
    }).reset_index()
    
    category_agg.columns = ['Category', 'SubCategory', 'Total_Revenue', 'Avg_Transaction', 
                           'Transaction_Count', 'Total_Units', 'Avg_Discount', 'Unique_SKUs']
    
    # Calculate revenue percentage
    category_agg['Revenue_Percent'] = (category_agg['Total_Revenue'] / 
                                       category_agg['Total_Revenue'].sum() * 100).round(2)
    
    category_agg = category_agg.sort_values('Total_Revenue', ascending=False)
    
    print(f"✓ Category aggregation created with {len(category_agg)} records")
    
    return category_agg

def create_store_performance(df):
    """Create store performance summary"""
    
    store_perf = df.groupby('Store').agg({
        'NETAMT': ['sum', 'mean'],
        'Qty': 'sum',
        'Footfall': 'mean',
        'ConversionPct': 'mean',
        'DiscountPct': 'mean',
        'SKU': 'nunique'
    }).reset_index()
    
    store_perf.columns = ['Store', 'Total_Revenue', 'Avg_Transaction', 'Total_Units', 
                         'Avg_Footfall', 'Avg_Conversion', 'Avg_Discount', 'Unique_SKUs']
    
    store_perf['Transactions'] = df.groupby('Store').size().values
    
    # Calculate performance score (normalized)
    store_perf['Performance_Score'] = (
        (store_perf['Total_Revenue'] / store_perf['Total_Revenue'].max() * 0.4) +
        (store_perf['Avg_Conversion'] / store_perf['Avg_Conversion'].max() * 0.3) +
        (store_perf['Transactions'] / store_perf['Transactions'].max() * 0.3)
    ) * 100
    
    store_perf['Performance_Score'] = store_perf['Performance_Score'].round(2)
    store_perf = store_perf.sort_values('Performance_Score', ascending=False)
    
    print(f"✓ Store performance created with {len(store_perf)} records")
    
    return store_perf

def create_monthly_trend(df):
    """Create monthly trend analysis"""
    
    monthly_trend = df.groupby(['Year', 'Month', 'MonthName']).agg({
        'NETAMT': 'sum',
        'Qty': 'sum',
        'DiscountPct': 'mean',
        'ConversionPct': 'mean'
    }).reset_index()
    
    monthly_trend.columns = ['Year', 'Month', 'MonthName', 'Revenue', 
                            'Units_Sold', 'Avg_Discount', 'Avg_Conversion']
    
    monthly_trend['Transactions'] = df.groupby(['Year', 'Month', 'MonthName']).size().values
    monthly_trend['Avg_Transaction_Value'] = (monthly_trend['Revenue'] / 
                                              monthly_trend['Transactions']).round(2)
    
    # Calculate month-over-month growth
    monthly_trend = monthly_trend.sort_values(['Year', 'Month'])
    monthly_trend['Revenue_Growth_%'] = monthly_trend['Revenue'].pct_change() * 100
    monthly_trend['Revenue_Growth_%'] = monthly_trend['Revenue_Growth_%'].round(2)
    
    print(f"✓ Monthly trend created with {len(monthly_trend)} records")
    
    return monthly_trend

def create_kpi_summary(df):
    """Create KPI summary for executive dashboard"""
    
    kpis = {
        'Total_Revenue': df['NETAMT'].sum(),
        'Total_Transactions': len(df),
        'Total_Units_Sold': df['Qty'].sum(),
        'Avg_Transaction_Value': df['NETAMT'].mean(),
        'Avg_Discount_Percent': df['DiscountPct'].mean(),
        'Avg_Conversion_Rate': df['ConversionPct'].mean(),
        'Unique_SKUs': df['SKU'].nunique(),
        'Unique_Brands': df['Brand'].nunique(),
        'Number_of_Stores': df['Store'].nunique(),
        'Number_of_Categories': df['Category'].nunique(),
        'Date_Range': f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}",
        'Total_Days': (df['Date'].max() - df['Date'].min()).days + 1,
        'Avg_Daily_Revenue': df.groupby('Date')['NETAMT'].sum().mean(),
        'Peak_Revenue_Day': df.groupby('Date')['NETAMT'].sum().idxmax().strftime('%Y-%m-%d'),
        'Peak_Revenue_Amount': df.groupby('Date')['NETAMT'].sum().max(),
    }
    
    kpi_df = pd.DataFrame([kpis])
    
    # Round numeric columns
    numeric_cols = kpi_df.select_dtypes(include=[np.number]).columns
    kpi_df[numeric_cols] = kpi_df[numeric_cols].round(2)
    
    print(f"✓ KPI summary created with {len(kpis)} metrics")
    
    return kpi_df

def create_top_performers(df):
    """Create top performers analysis"""
    
    # Top 10 SKUs by revenue
    top_skus = df.groupby(['SKU', 'Category', 'Brand'])['NETAMT'].sum().reset_index()
    top_skus = top_skus.sort_values('NETAMT', ascending=False).head(10)
    top_skus.columns = ['SKU', 'Category', 'Brand', 'Revenue']
    
    # Top 10 brands by revenue
    top_brands = df.groupby(['Brand', 'Category'])['NETAMT'].sum().reset_index()
    top_brands = top_brands.sort_values('NETAMT', ascending=False).head(10)
    top_brands.columns = ['Brand', 'Category', 'Revenue']
    
    print(f"✓ Top performers analysis created")
    
    return top_skus, top_brands

def main():
    """Main execution function"""
    
    # File paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, 'data', 'retail_transactions_clean.csv')
    output_dir = os.path.join(base_dir, 'dashboard')
    results_dir = os.path.join(base_dir, 'results')
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        print("Please run etl_clean.py first to create the cleaned data.")
        return
    
    # Load data
    df = load_clean_data(input_file)
    
    # Create output directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    # Create fact table
    fact_table = create_fact_table(df)
    fact_file = os.path.join(output_dir, 'powerbi_ready.csv')
    fact_table.to_csv(fact_file, index=False)
    print(f"✓ Fact table saved to: {fact_file}")
    
    # Create aggregations
    daily_agg = create_daily_aggregation(df)
    daily_file = os.path.join(output_dir, 'daily_aggregation.csv')
    daily_agg.to_csv(daily_file, index=False)
    print(f"✓ Daily aggregation saved to: {daily_file}")
    
    category_agg = create_category_aggregation(df)
    category_file = os.path.join(output_dir, 'category_aggregation.csv')
    category_agg.to_csv(category_file, index=False)
    print(f"✓ Category aggregation saved to: {category_file}")
    
    store_perf = create_store_performance(df)
    store_file = os.path.join(output_dir, 'store_performance.csv')
    store_perf.to_csv(store_file, index=False)
    print(f"✓ Store performance saved to: {store_file}")
    
    monthly_trend = create_monthly_trend(df)
    monthly_file = os.path.join(output_dir, 'monthly_trend.csv')
    monthly_trend.to_csv(monthly_file, index=False)
    print(f"✓ Monthly trend saved to: {monthly_file}")
    
    # Create KPI summary
    kpi_summary = create_kpi_summary(df)
    kpi_file = os.path.join(results_dir, 'kpi_summary.csv')
    kpi_summary.to_csv(kpi_file, index=False)
    print(f"✓ KPI summary saved to: {kpi_file}")
    
    # Create top performers
    top_skus, top_brands = create_top_performers(df)
    top_skus.to_csv(os.path.join(results_dir, 'top_skus.csv'), index=False)
    top_brands.to_csv(os.path.join(results_dir, 'top_brands.csv'), index=False)
    print(f"✓ Top performers saved to: {results_dir}")
    
    print("\n" + "="*60)
    print("DASHBOARD EXPORT COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"\nDashboard files available in: {output_dir}")
    print(f"Analysis results available in: {results_dir}")
    
    # Display KPI summary
    print("\n" + "="*60)
    print("KEY PERFORMANCE INDICATORS")
    print("="*60)
    for col in kpi_summary.columns[:10]:
        print(f"{col}: {kpi_summary[col].values[0]}")

if __name__ == "__main__":
    main()
