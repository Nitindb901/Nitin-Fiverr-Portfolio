"""
ETL Pipeline - Merge and Clean POS1 + POS2 Data
Combines data from both POS systems with conflict resolution and data quality checks
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 60)
print("ETL PIPELINE - MERGE & CLEAN POS DATA")
print("=" * 60)
print()

# ============================================
# LOAD DATA
# ============================================

print("Step 1: Loading POS datasets...")
print()

try:
    df_pos1 = pd.read_csv('data/pos1_transactions.csv')
    df_pos2 = pd.read_csv('data/pos2_transactions.csv')
    
    print(f"✓ POS1 loaded: {len(df_pos1):,} records")
    print(f"✓ POS2 loaded: {len(df_pos2):,} records")
    print()
except FileNotFoundError as e:
    print(f"ERROR: {e}")
    print("Please run generate_pos_data.py first!")
    exit(1)

# ============================================
# MERGE DATASETS
# ============================================

print("Step 2: Merging datasets...")
print()

# Combine both POS systems
df_combined = pd.concat([df_pos1, df_pos2], ignore_index=True)
print(f"✓ Combined dataset: {len(df_combined):,} records")

# Check for duplicates
duplicates = df_combined.duplicated(subset=['TransactionID']).sum()
print(f"✓ Duplicate check: {duplicates} duplicates found")
if duplicates > 0:
    df_combined = df_combined.drop_duplicates(subset=['TransactionID'])
    print(f"  Removed duplicates, new count: {len(df_combined):,}")
print()

# ============================================
# DATA CLEANING & VALIDATION
# ============================================

print("Step 3: Data cleaning and validation...")
print()

initial_count = len(df_combined)

# Convert date columns
date_columns = ['Date', 'ManufacturingDate', 'ExpiryDate']
for col in date_columns:
    df_combined[col] = pd.to_datetime(df_combined[col])

print("✓ Date columns converted to datetime")

# Validate numerical columns
numeric_cols = ['MRP', 'SellingPrice', 'Quantity', 'NetAmount', 'CostPrice', 'Profit']

# Remove rows with negative or zero values in critical columns
for col in numeric_cols:
    invalid_count = (df_combined[col] <= 0).sum()
    if invalid_count > 0:
        print(f"  Warning: {invalid_count} invalid values in {col}")
        df_combined = df_combined[df_combined[col] > 0]

print(f"✓ Numerical validation complete")

# Validate pricing logic (SellingPrice <= MRP)
price_issues = (df_combined['SellingPrice'] > df_combined['MRP']).sum()
if price_issues > 0:
    print(f"  Warning: {price_issues} records with SellingPrice > MRP")
    df_combined = df_combined[df_combined['SellingPrice'] <= df_combined['MRP']]

# Validate margin calculations
df_combined['CalculatedMargin'] = ((df_combined['SellingPrice'] - df_combined['CostPrice']) / df_combined['CostPrice'] * 100)
margin_diff = abs(df_combined['MarginPercent'] - df_combined['CalculatedMargin'])
margin_issues = (margin_diff > 1).sum()  # Allow 1% tolerance
if margin_issues > 0:
    print(f"  Warning: {margin_issues} records with margin calculation issues")
    # Recalculate margin for these records
    df_combined.loc[margin_diff > 1, 'MarginPercent'] = df_combined.loc[margin_diff > 1, 'CalculatedMargin']

df_combined = df_combined.drop('CalculatedMargin', axis=1)

print(f"✓ Pricing validation complete")

# Validate date logic
date_issues = (df_combined['ManufacturingDate'] > df_combined['Date']).sum()
if date_issues > 0:
    print(f"  Warning: {date_issues} records with manufacturing date after transaction date")
    df_combined = df_combined[df_combined['ManufacturingDate'] <= df_combined['Date']]

expiry_issues = (df_combined['ExpiryDate'] < df_combined['ManufacturingDate']).sum()
if expiry_issues > 0:
    print(f"  Warning: {expiry_issues} records with expiry before manufacturing")
    df_combined = df_combined[df_combined['ExpiryDate'] >= df_combined['ManufacturingDate']]

print(f"✓ Date validation complete")

# Check for missing values
missing_values = df_combined.isnull().sum()
if missing_values.sum() > 0:
    print("\n  Missing values detected:")
    print(missing_values[missing_values > 0])
    df_combined = df_combined.dropna()
    print(f"  Removed rows with missing values")

final_count = len(df_combined)
removed = initial_count - final_count

print()
print(f"✓ Cleaning complete: {removed:,} invalid records removed ({removed/initial_count*100:.2f}%)")
print(f"✓ Final dataset: {final_count:,} valid records")
print()

# ============================================
# FEATURE ENGINEERING
# ============================================

print("Step 4: Feature engineering...")
print()

# Add Month, Quarter, Year
df_combined['Year'] = df_combined['Date'].dt.year
df_combined['Month'] = df_combined['Date'].dt.month
df_combined['MonthName'] = df_combined['Date'].dt.strftime('%b')
df_combined['Quarter'] = df_combined['Date'].dt.quarter
df_combined['DayOfWeek'] = df_combined['Date'].dt.day_name()
df_combined['WeekNumber'] = df_combined['Date'].dt.isocalendar().week

# Add IsWeekend flag
df_combined['IsWeekend'] = df_combined['Date'].dt.dayofweek.isin([5, 6]).astype(int)

# Add Margin Category
df_combined['MarginCategory'] = pd.cut(
    df_combined['MarginPercent'],
    bins=[0, 15, 30, 45, 100],
    labels=['Low', 'Medium', 'High', 'Very High']
)

# Add Revenue Category
df_combined['RevenueCategory'] = pd.cut(
    df_combined['NetAmount'],
    bins=[0, 500, 2000, 5000, float('inf')],
    labels=['Low', 'Medium', 'High', 'Very High']
)

# Add Stock Health Flag
df_combined['StockHealth'] = df_combined['StockAgeCategory'].map({
    'Fresh': 'Excellent',
    'Normal': 'Good',
    'Ageing': 'Warning',
    'Old': 'Critical'
})

print("✓ Added temporal features (Year, Month, Quarter, Week, DayOfWeek)")
print("✓ Added weekend flag")
print("✓ Added margin categories")
print("✓ Added revenue categories")
print("✓ Added stock health indicators")
print()

# ============================================
# SAVE MERGED DATA
# ============================================

print("Step 5: Saving merged dataset...")
print()

# Save with date columns as strings for compatibility
df_save = df_combined.copy()
for col in date_columns:
    df_save[col] = df_save[col].dt.strftime('%Y-%m-%d')

df_save.to_csv('data/merged_pos_data.csv', index=False)
print("✓ Saved: data/merged_pos_data.csv")
print()

# ============================================
# SUMMARY STATISTICS
# ============================================

print("=" * 60)
print("MERGED DATASET SUMMARY")
print("=" * 60)
print()

print(f"Total Records: {len(df_combined):,}")
print(f"Date Range: {df_combined['Date'].min().date()} to {df_combined['Date'].max().date()}")
print(f"Unique SKUs: {df_combined['SKU_ID'].nunique():,}")
print()

print("By POS System:")
for pos in df_combined['POS_System'].unique():
    count = len(df_combined[df_combined['POS_System'] == pos])
    revenue = df_combined[df_combined['POS_System'] == pos]['NetAmount'].sum()
    print(f"  {pos}: {count:,} records ({count/len(df_combined)*100:.1f}%), ₹{revenue:,.2f}")
print()

print("By Category:")
for cat in df_combined['Category'].unique():
    cat_data = df_combined[df_combined['Category'] == cat]
    count = len(cat_data)
    revenue = cat_data['NetAmount'].sum()
    avg_margin = cat_data['MarginPercent'].mean()
    print(f"  {cat}:")
    print(f"    Records: {count:,} ({count/len(df_combined)*100:.1f}%)")
    print(f"    Revenue: ₹{revenue:,.2f}")
    print(f"    Avg Margin: {avg_margin:.2f}%")
print()

print("By SubCategory:")
for subcat in sorted(df_combined['SubCategory'].unique()):
    subcat_data = df_combined[df_combined['SubCategory'] == subcat]
    count = len(subcat_data)
    revenue = subcat_data['NetAmount'].sum()
    print(f"  {subcat}: {count:,} records, ₹{revenue:,.2f}")
print()

print("Financial Summary:")
total_revenue = df_combined['NetAmount'].sum()
total_profit = df_combined['Profit'].sum()
avg_margin = df_combined['MarginPercent'].mean()
avg_transaction = df_combined['NetAmount'].mean()
print(f"  Total Revenue: ₹{total_revenue:,.2f}")
print(f"  Total Profit: ₹{total_profit:,.2f}")
print(f"  Average Margin: {avg_margin:.2f}%")
print(f"  Average Transaction: ₹{avg_transaction:.2f}")
print()

print("Stock Ageing Analysis:")
for age_cat in ['Fresh', 'Normal', 'Ageing', 'Old']:
    age_data = df_combined[df_combined['StockAgeCategory'] == age_cat]
    count = len(age_data)
    pct = count / len(df_combined) * 100
    revenue = age_data['NetAmount'].sum()
    print(f"  {age_cat}: {count:,} ({pct:.1f}%), ₹{revenue:,.2f}")
print()

print("Top 5 Brands by Revenue:")
top_brands = df_combined.groupby('Brand')['NetAmount'].sum().sort_values(ascending=False).head()
for brand, revenue in top_brands.items():
    print(f"  {brand}: ₹{revenue:,.2f}")
print()

print("=" * 60)
print("ETL PIPELINE COMPLETED SUCCESSFULLY!")
print("=" * 60)
