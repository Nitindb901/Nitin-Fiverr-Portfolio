"""
Inventory Management & Supply Chain Analysis Script
Analyzes stock levels, reorder needs, and supplier performance
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("📦 Starting Inventory & Supply Chain Analysis...")
print("=" * 60)

# Load datasets
print("\n📂 Loading datasets...")
df_inventory = pd.read_csv('data/raw/inventory.csv')
df_products = pd.read_csv('data/raw/products.csv')
df_suppliers = pd.read_csv('data/raw/suppliers.csv')
df_transactions = pd.read_csv('data/raw/sales_transactions.csv')

df_inventory['LastRestocked'] = pd.to_datetime(df_inventory['LastRestocked'])
df_transactions['Date'] = pd.to_datetime(df_transactions['Date'])

print(f"✓ Loaded {len(df_inventory):,} inventory records")
print(f"✓ Loaded {len(df_products):,} products")
print(f"✓ Loaded {len(df_suppliers):,} suppliers")
print(f"✓ Loaded {len(df_transactions):,} transactions")

# Debug: Check columns
print(f"  Inventory columns: {df_inventory.columns.tolist()}")
print(f"  Products columns: {df_products.columns.tolist()[:10]}")  # First 10 columns
print(f"  Suppliers columns: {df_suppliers.columns.tolist()}")

# Merge datasets - keep SupplierID from both
df_inv_full = df_inventory.merge(df_products, on='ProductID', how='left', suffixes=('', '_product'))

# Check if SupplierID exists after first merge
print(f"  Columns after product merge: {[c for c in df_inv_full.columns if 'Supplier' in c]}")

# Use the correct SupplierID column
if 'SupplierID' in df_inv_full.columns:
    df_inv_full = df_inv_full.merge(df_suppliers, on='SupplierID', how='left')
elif 'SupplierID_product' in df_inv_full.columns:
    # Rename and use product's supplier
    df_inv_full['SupplierID'] = df_inv_full['SupplierID_product']
    df_inv_full = df_inv_full.merge(df_suppliers, on='SupplierID', how='left')


print(f"✓ Created unified inventory dataset")

# ============================================================================
# 1. OVERALL INVENTORY METRICS
# ============================================================================
print("\n📊 Calculating Overall Inventory Metrics...")

total_stock_value = df_inventory['StockValue'].sum()
total_units = df_inventory['StockLevel'].sum()
avg_stock_per_product = df_inventory['StockLevel'].mean()
critical_stock_count = (df_inventory['StockStatus'] == 'Critical').sum()
low_stock_count = (df_inventory['StockStatus'] == 'Low').sum()
normal_stock_count = (df_inventory['StockStatus'] == 'Normal').sum()

print(f"\n📦 Inventory Overview:")
print(f"  Total Stock Value: ${total_stock_value:,.2f}")
print(f"  Total Units in Stock: {total_units:,}")
print(f"  Avg Units per Product: {avg_stock_per_product:.1f}")
print(f"  Critical Stock Items: {critical_stock_count} ({critical_stock_count/len(df_inventory)*100:.1f}%)")
print(f"  Low Stock Items: {low_stock_count} ({low_stock_count/len(df_inventory)*100:.1f}%)")
print(f"  Normal Stock Items: {normal_stock_count} ({normal_stock_count/len(df_inventory)*100:.1f}%)")

# ============================================================================
# 2. STOCK STATUS ANALYSIS
# ============================================================================
print("\n🚨 Analyzing Stock Status by Category...")

stock_status_category = df_inv_full.groupby(['Category', 'StockStatus']).agg({
    'ProductID': 'count',
    'StockValue': 'sum'
}).reset_index()

stock_status_category.columns = ['Category', 'StockStatus', 'ProductCount', 'StockValue']

print(f"\nStock Status by Category:")
for category in df_inv_full['Category'].unique():
    cat_data = stock_status_category[stock_status_category['Category'] == category]
    critical = cat_data[cat_data['StockStatus'] == 'Critical']['ProductCount'].sum()
    low = cat_data[cat_data['StockStatus'] == 'Low']['ProductCount'].sum()
    print(f"  {category}: {critical} critical, {low} low stock items")

# ============================================================================
# 3. REORDER ALERTS
# ============================================================================
print("\n⚠️ Generating Reorder Alerts...")

# Items that need immediate reordering
reorder_critical = df_inv_full[df_inv_full['StockStatus'] == 'Critical'].copy()
reorder_critical['ReorderQuantity'] = (reorder_critical['ReorderPoint'] * 2 - reorder_critical['StockLevel']).clip(lower=0)
reorder_critical['EstimatedCost'] = (reorder_critical['ReorderQuantity'] * reorder_critical['Cost']).round(2)
reorder_critical['ExpectedDelivery'] = pd.Timestamp('2025-01-01') + pd.to_timedelta(reorder_critical['LeadTime'], unit='D')

reorder_critical = reorder_critical[['ProductID', 'ProductName', 'Category', 'StockLevel', 'ReorderPoint', 
                                     'ReorderQuantity', 'EstimatedCost', 'SupplierName', 'LeadTime', 'ExpectedDelivery']]
reorder_critical = reorder_critical.sort_values('EstimatedCost', ascending=False)

print(f"\n🔴 Critical Reorder Alerts: {len(reorder_critical)} items")
print(f"  Total Reorder Cost: ${reorder_critical['EstimatedCost'].sum():,.2f}")

if len(reorder_critical) > 0:
    print(f"\n  Top 5 Urgent Reorders:")
    for idx, row in reorder_critical.head(5).iterrows():
        print(f"    {row['ProductName'][:40]}: {row['ReorderQuantity']} units | ${row['EstimatedCost']:,.2f}")

# Low stock warnings
reorder_low = df_inv_full[df_inv_full['StockStatus'] == 'Low'].copy()
reorder_low['ReorderQuantity'] = (reorder_low['ReorderPoint'] * 1.5 - reorder_low['StockLevel']).clip(lower=0)
reorder_low['EstimatedCost'] = (reorder_low['ReorderQuantity'] * reorder_low['Cost']).round(2)

print(f"\n🟡 Low Stock Warnings: {len(reorder_low)} items")
print(f"  Estimated Reorder Cost: ${reorder_low['EstimatedCost'].sum():,.2f}")

# ============================================================================
# 4. INVENTORY TURNOVER ANALYSIS
# ============================================================================
print("\n🔄 Calculating Inventory Turnover...")

# Calculate sales in last 12 months
last_12_months = df_transactions['Date'].max() - timedelta(days=365)
recent_sales = df_transactions[df_transactions['Date'] >= last_12_months].groupby('ProductID').agg({
    'Quantity': 'sum'
}).reset_index()

recent_sales.columns = ['ProductID', 'UnitsSold_12M']

# Merge with inventory
turnover_analysis = df_inv_full.merge(recent_sales, on='ProductID', how='left')
turnover_analysis['UnitsSold_12M'] = turnover_analysis['UnitsSold_12M'].fillna(0)

# Calculate turnover ratio
turnover_analysis['TurnoverRatio'] = np.where(
    turnover_analysis['StockLevel'] > 0,
    turnover_analysis['UnitsSold_12M'] / turnover_analysis['StockLevel'],
    0
).round(2)

# Categorize turnover
def categorize_turnover(ratio):
    if ratio >= 5:
        return 'Fast Moving'
    elif ratio >= 2:
        return 'Regular'
    elif ratio >= 0.5:
        return 'Slow Moving'
    else:
        return 'Very Slow/Dead Stock'

turnover_analysis['TurnoverCategory'] = turnover_analysis['TurnoverRatio'].apply(categorize_turnover)

turnover_summary = turnover_analysis.groupby('TurnoverCategory').agg({
    'ProductID': 'count',
    'StockValue': 'sum',
    'TurnoverRatio': 'mean'
}).reset_index()

turnover_summary.columns = ['TurnoverCategory', 'ProductCount', 'StockValue', 'AvgTurnoverRatio']
turnover_summary = turnover_summary.sort_values('AvgTurnoverRatio', ascending=False)

print(f"\nInventory Turnover Analysis:")
for _, row in turnover_summary.iterrows():
    print(f"  {row['TurnoverCategory']}: {row['ProductCount']} items | ${row['StockValue']:,.2f} | Avg Ratio: {row['AvgTurnoverRatio']:.2f}x")

# Identify slow-moving inventory
slow_moving = turnover_analysis[turnover_analysis['TurnoverCategory'].isin(['Slow Moving', 'Very Slow/Dead Stock'])]
slow_moving_value = slow_moving['StockValue'].sum()

print(f"\n⚠️ Slow-Moving Inventory:")
print(f"  Items: {len(slow_moving)}")
print(f"  Value Locked: ${slow_moving_value:,.2f}")
print(f"  % of Total Inventory: {slow_moving_value/total_stock_value*100:.2f}%")

# ============================================================================
# 5. SUPPLIER PERFORMANCE
# ============================================================================
print("\n🏭 Analyzing Supplier Performance...")

supplier_performance = df_inv_full.groupby(['SupplierID', 'SupplierName', 'Country', 
                                            'OnTimeDeliveryRate', 'DefectRate']).agg({
    'ProductID': 'count',
    'StockValue': 'sum',
    'LeadTime': 'mean'
}).reset_index()

supplier_performance.columns = ['SupplierID', 'SupplierName', 'Country', 'OnTimeDeliveryRate', 
                                'DefectRate', 'ProductCount', 'StockValue', 'AvgLeadTime']

# Calculate supplier score (weighted)
supplier_performance['SupplierScore'] = (
    supplier_performance['OnTimeDeliveryRate'] * 0.4 +
    (1 - supplier_performance['DefectRate']) * 0.4 +
    (1 - supplier_performance['AvgLeadTime'] / 35) * 0.2  # Normalize lead time (35 days max)
).round(3)

supplier_performance = supplier_performance.sort_values('SupplierScore', ascending=False)

print(f"\nTop 5 Suppliers by Performance Score:")
for idx, row in supplier_performance.head(5).iterrows():
    print(f"  {row['SupplierName']} ({row['Country']}): Score {row['SupplierScore']:.3f} | "
          f"{row['ProductCount']} products | ${row['StockValue']:,.2f}")

print(f"\nBottom 3 Suppliers:")
for idx, row in supplier_performance.tail(3).iterrows():
    print(f"  {row['SupplierName']}: Score {row['SupplierScore']:.3f} | "
          f"OTD: {row['OnTimeDeliveryRate']*100:.1f}% | Defect: {row['DefectRate']*100:.1f}%")

# ============================================================================
# 6. WAREHOUSE ANALYSIS
# ============================================================================
print("\n🏢 Analyzing Warehouse Distribution...")

warehouse_analysis = df_inv_full.groupby('WarehouseID').agg({
    'ProductID': 'count',
    'StockLevel': 'sum',
    'StockValue': 'sum'
}).reset_index()

warehouse_analysis.columns = ['WarehouseID', 'ProductCount', 'TotalUnits', 'StockValue']
warehouse_analysis['AvgValuePerProduct'] = (warehouse_analysis['StockValue'] / warehouse_analysis['ProductCount']).round(2)

print(f"\nWarehouse Distribution:")
for _, row in warehouse_analysis.iterrows():
    print(f"  {row['WarehouseID']}: {row['ProductCount']} products | {row['TotalUnits']:,} units | ${row['StockValue']:,.2f}")

# ============================================================================
# 7. CATEGORY-WISE INVENTORY ANALYSIS
# ============================================================================
print("\n📊 Analyzing Inventory by Category...")

category_inventory = df_inv_full.groupby('Category').agg({
    'ProductID': 'count',
    'StockLevel': 'sum',
    'StockValue': 'sum',
    'Cost': 'mean'
}).reset_index()

category_inventory.columns = ['Category', 'ProductCount', 'TotalUnits', 'StockValue', 'AvgCost']
category_inventory['ValueShare'] = (category_inventory['StockValue'] / total_stock_value * 100).round(2)
category_inventory = category_inventory.sort_values('StockValue', ascending=False)

print(f"\nInventory by Category:")
for _, row in category_inventory.iterrows():
    print(f"  {row['Category']}: ${row['StockValue']:,.2f} ({row['ValueShare']:.1f}%) | "
          f"{row['TotalUnits']:,} units | Avg Cost: ${row['AvgCost']:.2f}")

# ============================================================================
# 8. DAYS OF INVENTORY
# ============================================================================
print("\n📅 Calculating Days of Inventory...")

# Calculate daily sales rate
daily_sales = df_transactions.groupby('ProductID')['Quantity'].sum() / 730  # 2 years of data

days_inventory = df_inv_full.copy()
days_inventory = days_inventory.merge(daily_sales.reset_index(), on='ProductID', how='left')
days_inventory.columns = list(days_inventory.columns[:-1]) + ['DailySalesRate']
days_inventory['DailySalesRate'] = days_inventory['DailySalesRate'].fillna(0)

days_inventory['DaysOfInventory'] = np.where(
    days_inventory['DailySalesRate'] > 0,
    days_inventory['StockLevel'] / days_inventory['DailySalesRate'],
    999  # High number for no sales
).round(0)

# Categorize
def categorize_days(days):
    if days <= 30:
        return 'Under 30 days'
    elif days <= 60:
        return '30-60 days'
    elif days <= 90:
        return '60-90 days'
    elif days <= 180:
        return '90-180 days'
    else:
        return 'Over 180 days'

days_inventory['DOI_Category'] = days_inventory['DaysOfInventory'].apply(categorize_days)

doi_summary = days_inventory.groupby('DOI_Category').agg({
    'ProductID': 'count',
    'StockValue': 'sum'
}).reset_index()

doi_summary.columns = ['DOI_Category', 'ProductCount', 'StockValue']

print(f"\nDays of Inventory Distribution:")
for _, row in doi_summary.iterrows():
    print(f"  {row['DOI_Category']}: {row['ProductCount']} items | ${row['StockValue']:,.2f}")

# ============================================================================
# 9. STOCK AGE ANALYSIS
# ============================================================================
print("\n⏰ Analyzing Stock Age...")

current_date = pd.Timestamp('2025-01-01')
df_inv_full['DaysSinceRestock'] = (current_date - df_inv_full['LastRestocked']).dt.days

def categorize_age(days):
    if days <= 30:
        return 'Fresh (0-30 days)'
    elif days <= 60:
        return 'Recent (31-60 days)'
    elif days <= 90:
        return 'Normal (61-90 days)'
    else:
        return 'Ageing (90+ days)'

df_inv_full['StockAge'] = df_inv_full['DaysSinceRestock'].apply(categorize_age)

stock_age_analysis = df_inv_full.groupby('StockAge').agg({
    'ProductID': 'count',
    'StockValue': 'sum',
    'StockLevel': 'sum'
}).reset_index()

stock_age_analysis.columns = ['StockAge', 'ProductCount', 'StockValue', 'TotalUnits']
stock_age_analysis['ValueShare'] = (stock_age_analysis['StockValue'] / total_stock_value * 100).round(2)

print(f"\nStock Age Distribution:")
for _, row in stock_age_analysis.iterrows():
    print(f"  {row['StockAge']}: {row['ProductCount']} items | {row['TotalUnits']:,} units | "
          f"${row['StockValue']:,.2f} ({row['ValueShare']:.1f}%)")

# ============================================================================
# SAVE PROCESSED DATA
# ============================================================================
print("\n💾 Saving processed datasets...")

# Reorder alerts
reorder_all = pd.concat([reorder_critical, reorder_low])
reorder_all.to_csv('data/processed/reorder_alerts.csv', index=False)
print("✓ Saved reorder_alerts.csv")

# Turnover analysis
turnover_analysis[['ProductID', 'ProductName', 'Category', 'StockLevel', 'UnitsSold_12M', 
                   'TurnoverRatio', 'TurnoverCategory', 'StockValue']].to_csv('data/processed/inventory_turnover.csv', index=False)
print("✓ Saved inventory_turnover.csv")

# Supplier performance
supplier_performance.to_csv('data/processed/supplier_performance.csv', index=False)
print("✓ Saved supplier_performance.csv")

# Warehouse analysis
warehouse_analysis.to_csv('data/processed/warehouse_analysis.csv', index=False)
print("✓ Saved warehouse_analysis.csv")

# Category inventory
category_inventory.to_csv('data/processed/category_inventory.csv', index=False)
print("✓ Saved category_inventory.csv")

# Stock status summary
stock_status_category.to_csv('data/processed/stock_status_summary.csv', index=False)
print("✓ Saved stock_status_summary.csv")

# Days of inventory
doi_summary.to_csv('data/processed/days_of_inventory.csv', index=False)
print("✓ Saved days_of_inventory.csv")

# Stock age
stock_age_analysis.to_csv('data/processed/stock_age_analysis.csv', index=False)
print("✓ Saved stock_age_analysis.csv")

# Slow moving inventory
slow_moving[['ProductID', 'ProductName', 'Category', 'StockLevel', 'UnitsSold_12M', 
             'TurnoverRatio', 'StockValue']].to_csv('data/processed/slow_moving_inventory.csv', index=False)
print("✓ Saved slow_moving_inventory.csv")

print("\n" + "=" * 60)
print("✅ Inventory & Supply Chain Analysis Complete!")
print("=" * 60)
print(f"\n📊 Key Insights:")
print(f"  • Total Stock Value: ${total_stock_value:,.2f}")
print(f"  • Critical Items: {critical_stock_count} (need immediate reorder)")
print(f"  • Slow-Moving Value: ${slow_moving_value:,.2f}")
print(f"  • Best Supplier: {supplier_performance.iloc[0]['SupplierName']} (Score: {supplier_performance.iloc[0]['SupplierScore']:.3f})")
print(f"  • Avg Inventory Turnover: {turnover_analysis['TurnoverRatio'].mean():.2f}x")
