"""
ETL & Data Cleaning Script
Cleans raw retail transaction data:
- Handles missing values
- Removes duplicates
- Validates data types
- Adds derived features (Month, Week, DayOfWeek, PriceSegment, etc.)
- Detects and handles outliers
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_data(file_path):
    """Load raw data from CSV"""
    print(f"Loading data from: {file_path}")
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} records")
    return df

def clean_data(df):
    """Perform data cleaning operations"""
    
    print("\n" + "="*60)
    print("DATA CLEANING")
    print("="*60)
    
    # Initial shape
    initial_rows = len(df)
    print(f"\nInitial records: {initial_rows}")
    
    # 1. Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    print("✓ Date column converted to datetime")
    
    # 2. Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        print(f"\nMissing values found:")
        print(missing_values[missing_values > 0])
        df = df.dropna()
        print(f"✓ Dropped rows with missing values")
    else:
        print("✓ No missing values found")
    
    # 3. Remove duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates()
        print(f"✓ Removed {duplicates} duplicate records")
    else:
        print("✓ No duplicates found")
    
    # 4. Validate numeric columns
    numeric_cols = ['MRP', 'SellingPrice', 'Qty', 'NETAMT', 'Footfall', 'ConversionPct', 'DiscountPct']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=numeric_cols)
    print("✓ Validated numeric columns")
    
    # 5. Remove negative values
    for col in ['MRP', 'SellingPrice', 'Qty', 'NETAMT']:
        invalid = (df[col] <= 0).sum()
        if invalid > 0:
            df = df[df[col] > 0]
            print(f"✓ Removed {invalid} records with invalid {col}")
    
    # 6. Validate business logic
    # MRP should be >= SellingPrice
    invalid_price = (df['MRP'] < df['SellingPrice']).sum()
    if invalid_price > 0:
        df = df[df['MRP'] >= df['SellingPrice']]
        print(f"✓ Removed {invalid_price} records where SellingPrice > MRP")
    
    # NETAMT should equal SellingPrice * Qty (with small tolerance)
    df['calculated_netamt'] = df['SellingPrice'] * df['Qty']
    amt_diff = abs(df['NETAMT'] - df['calculated_netamt'])
    invalid_amt = (amt_diff > 1).sum()
    if invalid_amt > 0:
        df = df[amt_diff <= 1]
        print(f"✓ Removed {invalid_amt} records with incorrect NETAMT calculation")
    df = df.drop('calculated_netamt', axis=1)
    
    # 7. Handle outliers (using IQR method)
    def remove_outliers(df, column, multiplier=3):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - multiplier * IQR
        upper = Q3 + multiplier * IQR
        before = len(df)
        df = df[(df[column] >= lower) & (df[column] <= upper)]
        removed = before - len(df)
        if removed > 0:
            print(f"✓ Removed {removed} outliers from {column}")
        return df
    
    df = remove_outliers(df, 'NETAMT')
    df = remove_outliers(df, 'Qty')
    
    final_rows = len(df)
    print(f"\nFinal records: {final_rows}")
    print(f"Records removed: {initial_rows - final_rows} ({(initial_rows - final_rows) / initial_rows * 100:.2f}%)")
    
    return df

def add_features(df):
    """Add derived features for analysis"""
    
    print("\n" + "="*60)
    print("FEATURE ENGINEERING")
    print("="*60)
    
    # Time-based features
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['MonthName'] = df['Date'].dt.strftime('%B')
    df['Week'] = df['Date'].dt.isocalendar().week
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['DayName'] = df['Date'].dt.strftime('%A')
    df['Quarter'] = df['Date'].dt.quarter
    df['IsWeekend'] = df['DayOfWeek'].isin([5, 6]).astype(int)
    print("✓ Added time-based features")
    
    # Price-based features
    df['DiscountAmount'] = df['MRP'] - df['SellingPrice']
    df['ProfitMargin'] = ((df['SellingPrice'] - df['MRP'] * 0.6) / df['SellingPrice'] * 100).round(2)
    print("✓ Added price-based features")
    
    # Price segment
    def categorize_price(mrp):
        if mrp < 500:
            return 'Budget'
        elif mrp < 2000:
            return 'Economy'
        elif mrp < 10000:
            return 'Mid-Range'
        else:
            return 'Premium'
    
    df['PriceSegment'] = df['MRP'].apply(categorize_price)
    print("✓ Added price segment")
    
    # Discount segment
    def categorize_discount(discount):
        if discount == 0:
            return 'No Discount'
        elif discount < 10:
            return 'Low Discount'
        elif discount < 25:
            return 'Medium Discount'
        else:
            return 'High Discount'
    
    df['DiscountSegment'] = df['DiscountPct'].apply(categorize_discount)
    print("✓ Added discount segment")
    
    # Transaction size
    df['TransactionSize'] = pd.cut(df['NETAMT'], 
                                    bins=[0, 500, 2000, 10000, float('inf')],
                                    labels=['Small', 'Medium', 'Large', 'Extra Large'])
    print("✓ Added transaction size category")
    
    # Average Unit Price
    df['AvgUnitPrice'] = (df['NETAMT'] / df['Qty']).round(2)
    print("✓ Added average unit price")
    
    print(f"\nTotal features: {len(df.columns)}")
    
    return df

def generate_summary_stats(df):
    """Generate summary statistics"""
    
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    
    stats = {
        'Total Transactions': len(df),
        'Total Revenue': f"${df['NETAMT'].sum():,.2f}",
        'Avg Transaction Value': f"${df['NETAMT'].mean():,.2f}",
        'Median Transaction Value': f"${df['NETAMT'].median():,.2f}",
        'Total Quantity Sold': f"{df['Qty'].sum():,}",
        'Avg Discount': f"{df['DiscountPct'].mean():.2f}%",
        'Date Range': f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}",
        'Number of Stores': df['Store'].nunique(),
        'Number of Categories': df['Category'].nunique(),
        'Number of Brands': df['Brand'].nunique(),
        'Unique SKUs': df['SKU'].nunique()
    }
    
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    return stats

def main():
    """Main execution function"""
    
    # File paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, 'data', 'retail_transactions_raw.csv')
    output_file = os.path.join(base_dir, 'data', 'retail_transactions_clean.csv')
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        print("Please run generate_data.py first to create the raw data.")
        return
    
    # Load data
    df = load_data(input_file)
    
    # Clean data
    df = clean_data(df)
    
    # Add features
    df = add_features(df)
    
    # Generate summary statistics
    generate_summary_stats(df)
    
    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"\n✓ Cleaned data saved to: {output_file}")
    
    # Save summary by category
    category_summary = df.groupby('Category').agg({
        'NETAMT': ['sum', 'mean', 'count'],
        'Qty': 'sum',
        'DiscountPct': 'mean'
    }).round(2)
    category_summary.columns = ['Total_Revenue', 'Avg_Transaction', 'Transaction_Count', 'Total_Qty', 'Avg_Discount']
    
    summary_file = os.path.join(base_dir, 'results', 'category_summary.csv')
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)
    category_summary.to_csv(summary_file)
    print(f"✓ Category summary saved to: {summary_file}")
    
    print("\n" + "="*60)
    print("ETL PROCESS COMPLETED SUCCESSFULLY")
    print("="*60)

if __name__ == "__main__":
    main()
