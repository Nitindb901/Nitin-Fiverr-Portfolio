"""
Grocery + Fashion Integrated Dashboard - POS Data Generation
Generates synthetic data for POS1 and POS2 with realistic business logic
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("=" * 60)
print("GROCERY + FASHION DASHBOARD - DATA GENERATION")
print("=" * 60)
print()

# ============================================
# CONFIGURATION
# ============================================

# Date range
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)
DATE_RANGE = pd.date_range(START_DATE, END_DATE, freq='D')

# POS Configuration
POS_SYSTEMS = ['POS1', 'POS2']
STORES = {
    'POS1': ['Store_A', 'Store_B', 'Store_C'],
    'POS2': ['Store_D', 'Store_E']
}

# Category Configuration
CATEGORIES = {
    'Grocery': {
        'subcategories': ['FMCG', 'Staples', 'Dairy', 'Snacks'],
        'brands': ['BrandG1', 'BrandG2', 'BrandG3', 'BrandG4', 'BrandG5'],
        'price_range': (50, 2000),  # INR
        'margin_range': (5, 25),  # %
        'shelf_life_days': (30, 365)  # Days
    },
    'Fashion': {
        'subcategories': ['Men', 'Women', 'Kids', 'Accessories'],
        'brands': ['BrandF1', 'BrandF2', 'BrandF3', 'BrandF4', 'BrandF5'],
        'price_range': (500, 15000),  # INR
        'margin_range': (30, 60),  # %
        'shelf_life_days': (90, 730)  # Days (seasonal inventory)
    }
}

# Business Logic Parameters
WEEKDAY_MULTIPLIER = 1.0
WEEKEND_MULTIPLIER = 1.5
FESTIVAL_MULTIPLIER = 2.0
MONTH_END_MULTIPLIER = 1.3

# Festival Dates in 2024
FESTIVALS = [
    datetime(2024, 1, 26),  # Republic Day
    datetime(2024, 3, 8),   # Holi
    datetime(2024, 8, 15),  # Independence Day
    datetime(2024, 10, 12), # Dussehra
    datetime(2024, 11, 1),  # Diwali
    datetime(2024, 11, 29), # Black Friday
    datetime(2024, 12, 25), # Christmas
]

print("Configuration:")
print(f"  Date Range: {START_DATE.date()} to {END_DATE.date()}")
print(f"  POS Systems: {POS_SYSTEMS}")
print(f"  Total Stores: {sum(len(stores) for stores in STORES.values())}")
print(f"  Categories: {list(CATEGORIES.keys())}")
print()

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_seasonality_factor(date):
    """Calculate seasonality factor based on date"""
    factor = 1.0
    
    # Weekend boost
    if date.weekday() >= 5:  # Saturday=5, Sunday=6
        factor *= WEEKEND_MULTIPLIER
    
    # Festival boost (±3 days)
    for festival in FESTIVALS:
        if abs((date - festival).days) <= 3:
            factor *= FESTIVAL_MULTIPLIER
            break
    
    # Month-end boost (last 5 days)
    last_day = (date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    if (last_day - date).days < 5:
        factor *= MONTH_END_MULTIPLIER
    
    return factor

def generate_sku_id(category, subcategory, brand):
    """Generate unique SKU ID"""
    cat_code = category[:3].upper()
    sub_code = subcategory[:3].upper()
    brand_code = brand[-1]
    random_num = random.randint(1000, 9999)
    return f"{cat_code}{sub_code}{brand_code}{random_num}"

def calculate_stock_age(manufacturing_date, transaction_date):
    """Calculate stock age in days"""
    return (transaction_date - manufacturing_date).days

# ============================================
# DATA GENERATION
# ============================================

all_transactions = []
transaction_id = 1

print("Generating transactions...")
print()

for pos_system in POS_SYSTEMS:
    print(f"Processing {pos_system}...")
    stores = STORES[pos_system]
    
    for store in stores:
        print(f"  Generating data for {store}...", end=" ")
        
        store_transactions = 0
        
        for date in DATE_RANGE:
            # Calculate daily volume based on seasonality
            base_transactions = random.randint(30, 60)
            seasonality = get_seasonality_factor(date)
            daily_transactions = int(base_transactions * seasonality)
            
            for _ in range(daily_transactions):
                # Select category (60% Grocery, 40% Fashion)
                category = random.choices(
                    list(CATEGORIES.keys()),
                    weights=[0.6, 0.4]
                )[0]
                
                cat_config = CATEGORIES[category]
                subcategory = random.choice(cat_config['subcategories'])
                brand = random.choice(cat_config['brands'])
                
                # Generate SKU
                sku_id = generate_sku_id(category, subcategory, brand)
                
                # Pricing
                mrp = round(random.uniform(*cat_config['price_range']), 2)
                discount_pct = random.choice([0, 5, 10, 15, 20, 25, 30])
                selling_price = round(mrp * (1 - discount_pct/100), 2)
                
                # Quantity (fashion tends to have lower qty per transaction)
                if category == 'Fashion':
                    quantity = random.randint(1, 3)
                else:
                    quantity = random.randint(1, 5)
                
                net_amount = round(selling_price * quantity, 2)
                
                # Margin calculation
                margin_pct = random.uniform(*cat_config['margin_range'])
                cost_price = round(selling_price / (1 + margin_pct/100), 2)
                profit = round((selling_price - cost_price) * quantity, 2)
                
                # Stock information
                manufacturing_date = date - timedelta(days=random.randint(1, 180))
                shelf_life_days = random.randint(*cat_config['shelf_life_days'])
                stock_age_days = calculate_stock_age(manufacturing_date, date)
                expiry_date = manufacturing_date + timedelta(days=shelf_life_days)
                days_to_expiry = (expiry_date - date).days
                
                # Stock age category
                if stock_age_days <= 30:
                    stock_age_category = 'Fresh'
                elif stock_age_days <= 90:
                    stock_age_category = 'Normal'
                elif stock_age_days <= 180:
                    stock_age_category = 'Ageing'
                else:
                    stock_age_category = 'Old'
                
                # Create transaction record
                transaction = {
                    'TransactionID': f"{pos_system}_{store}_{transaction_id:08d}",
                    'POS_System': pos_system,
                    'Store': store,
                    'Date': date.strftime('%Y-%m-%d'),
                    'Category': category,
                    'SubCategory': subcategory,
                    'SKU_ID': sku_id,
                    'Brand': brand,
                    'MRP': mrp,
                    'SellingPrice': selling_price,
                    'DiscountPercent': discount_pct,
                    'Quantity': quantity,
                    'NetAmount': net_amount,
                    'CostPrice': cost_price,
                    'MarginPercent': round(margin_pct, 2),
                    'Profit': profit,
                    'ManufacturingDate': manufacturing_date.strftime('%Y-%m-%d'),
                    'ExpiryDate': expiry_date.strftime('%Y-%m-%d'),
                    'StockAgeDays': stock_age_days,
                    'DaysToExpiry': days_to_expiry,
                    'StockAgeCategory': stock_age_category
                }
                
                all_transactions.append(transaction)
                transaction_id += 1
                store_transactions += 1
        
        print(f"✓ {store_transactions:,} transactions")

print()
print("=" * 60)

# ============================================
# CREATE SEPARATE POS DATASETS
# ============================================

print("Creating POS datasets...")

df_all = pd.DataFrame(all_transactions)

# Split by POS system
df_pos1 = df_all[df_all['POS_System'] == 'POS1'].copy()
df_pos2 = df_all[df_all['POS_System'] == 'POS2'].copy()

# Save separate POS files
df_pos1.to_csv('data/pos1_transactions.csv', index=False)
df_pos2.to_csv('data/pos2_transactions.csv', index=False)

print(f"✓ POS1 dataset: {len(df_pos1):,} transactions")
print(f"✓ POS2 dataset: {len(df_pos2):,} transactions")
print()

# ============================================
# SUMMARY STATISTICS
# ============================================

print("=" * 60)
print("DATA GENERATION SUMMARY")
print("=" * 60)
print()

print(f"Total Transactions: {len(df_all):,}")
print(f"  POS1: {len(df_pos1):,} ({len(df_pos1)/len(df_all)*100:.1f}%)")
print(f"  POS2: {len(df_pos2):,} ({len(df_pos2)/len(df_all)*100:.1f}%)")
print()

print("By Category:")
for category in df_all['Category'].unique():
    count = len(df_all[df_all['Category'] == category])
    revenue = df_all[df_all['Category'] == category]['NetAmount'].sum()
    print(f"  {category}: {count:,} transactions, ₹{revenue:,.2f}")
print()

print("By Store:")
for store in sorted(df_all['Store'].unique()):
    count = len(df_all[df_all['Store'] == store])
    revenue = df_all[df_all['Store'] == store]['NetAmount'].sum()
    pos = df_all[df_all['Store'] == store]['POS_System'].iloc[0]
    print(f"  {store} ({pos}): {count:,} transactions, ₹{revenue:,.2f}")
print()

print("Revenue Summary:")
total_revenue = df_all['NetAmount'].sum()
total_profit = df_all['Profit'].sum()
avg_margin = df_all['MarginPercent'].mean()
print(f"  Total Revenue: ₹{total_revenue:,.2f}")
print(f"  Total Profit: ₹{total_profit:,.2f}")
print(f"  Average Margin: {avg_margin:.2f}%")
print()

print("Stock Ageing:")
for age_cat in ['Fresh', 'Normal', 'Ageing', 'Old']:
    count = len(df_all[df_all['StockAgeCategory'] == age_cat])
    pct = count / len(df_all) * 100
    print(f"  {age_cat}: {count:,} ({pct:.1f}%)")
print()

print("Files created:")
print("  ✓ data/pos1_transactions.csv")
print("  ✓ data/pos2_transactions.csv")
print()
print("=" * 60)
print("DATA GENERATION COMPLETED SUCCESSFULLY!")
print("=" * 60)
