"""
Project 7: Sales Forecasting ML - Ultimate Interactive Dashboard
Script 1: Generate 150K Transactions (5 Years: 2020-2025)

Features:
- 150,000 transactions across 5 years
- 25 stores in 5 regions
- 1,000 products in 6 categories
- Realistic seasonal patterns, trends, holidays
- ₹2,500+ Crore revenue target
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("🚀 Starting Data Generation for Project 7: Sales Forecasting ML")
print("=" * 70)

# ============================================================================
# CONFIGURATION
# ============================================================================

START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2025, 11, 29)
NUM_TRANSACTIONS = 150000

# Categories with weights and price ranges
CATEGORIES = {
    'Electronics': {'weight': 0.25, 'price_range': (5000, 150000), 'margin': (10, 18)},
    'Fashion': {'weight': 0.20, 'price_range': (500, 15000), 'margin': (35, 50)},
    'Home & Furniture': {'weight': 0.18, 'price_range': (2000, 80000), 'margin': (20, 35)},
    'Grocery': {'weight': 0.15, 'price_range': (100, 5000), 'margin': (8, 15)},
    'Beauty & Personal Care': {'weight': 0.12, 'price_range': (200, 8000), 'margin': (30, 45)},
    'Sports & Fitness': {'weight': 0.10, 'price_range': (500, 25000), 'margin': (25, 40)}
}

# Regions and stores
REGIONS = {
    'North': {'stores': ['Delhi CP', 'Delhi Saket', 'Gurgaon', 'Noida', 'Chandigarh'], 'multiplier': 1.2},
    'South': {'stores': ['Bangalore', 'Chennai', 'Hyderabad', 'Kochi', 'Pune'], 'multiplier': 1.15},
    'West': {'stores': ['Mumbai Bandra', 'Mumbai Andheri', 'Ahmedabad', 'Surat', 'Nashik'], 'multiplier': 1.1},
    'East': {'stores': ['Kolkata', 'Bhubaneswar', 'Patna', 'Guwahati', 'Ranchi'], 'multiplier': 0.95},
    'Central': {'stores': ['Indore', 'Bhopal', 'Nagpur', 'Raipur', 'Jabalpur'], 'multiplier': 0.90}
}

# Channels
CHANNELS = ['In-Store', 'Website', 'Mobile App', 'Social Commerce']

# Customer segments
CUSTOMER_SEGMENTS = ['VIP', 'Premium', 'Regular', 'Occasional', 'New']

print(f"📅 Date Range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
print(f"📊 Target Transactions: {NUM_TRANSACTIONS:,}")
print(f"🏪 Total Stores: {sum(len(v['stores']) for v in REGIONS.values())}")
print(f"📦 Categories: {len(CATEGORIES)}")
print()

# ============================================================================
# GENERATE PRODUCTS
# ============================================================================

def generate_products(num_products=1000):
    """Generate product catalog"""
    print("📦 Generating Products...")
    
    products = []
    product_id = 1
    
    for category, config in CATEGORIES.items():
        num_cat_products = int(num_products * config['weight'])
        
        for i in range(num_cat_products):
            base_price = np.random.uniform(config['price_range'][0], config['price_range'][1])
            margin_pct = np.random.uniform(config['margin'][0], config['margin'][1])
            
            products.append({
                'product_id': f'P{product_id:04d}',
                'category': category,
                'product_name': f'{category} Product {i+1}',
                'base_price': round(base_price, 2),
                'margin_percent': round(margin_pct, 2),
                'cost': round(base_price * (1 - margin_pct/100), 2)
            })
            product_id += 1
    
    products_df = pd.DataFrame(products)
    print(f"   ✅ Generated {len(products_df)} products")
    return products_df

# ============================================================================
# GENERATE STORES
# ============================================================================

def generate_stores():
    """Generate store master data"""
    print("🏪 Generating Stores...")
    
    stores = []
    store_id = 1
    
    for region, config in REGIONS.items():
        for store_name in config['stores']:
            stores.append({
                'store_id': f'S{store_id:03d}',
                'store_name': store_name,
                'region': region,
                'region_multiplier': config['multiplier']
            })
            store_id += 1
    
    stores_df = pd.DataFrame(stores)
    print(f"   ✅ Generated {len(stores_df)} stores across {len(REGIONS)} regions")
    return stores_df

# ============================================================================
# GENERATE TRANSACTIONS WITH ADVANCED PATTERNS
# ============================================================================

def get_seasonal_multiplier(date):
    """Calculate seasonal multiplier based on date"""
    month = date.month
    day = date.day
    
    # Festive seasons
    if month == 1 and day <= 15:  # New Year
        return 1.5
    elif month == 2 and 10 <= day <= 20:  # Valentine's
        return 1.25
    elif month == 3 and 5 <= day <= 15:  # Holi
        return 1.3
    elif month == 8 and 10 <= day <= 20:  # Independence Day
        return 1.2
    elif month == 10 and 15 <= day <= 31:  # Diwali season
        return 1.8
    elif month == 11 and 1 <= day <= 10:  # Diwali continued
        return 1.6
    elif month == 12 and 15 <= day <= 31:  # Christmas & Year End
        return 1.7
    else:
        return 1.0

def get_day_multiplier(date):
    """Weekends and paydays have higher sales"""
    if date.weekday() >= 5:  # Weekend
        return 1.3
    elif date.day in [1, 2, 15, 16]:  # Payday periods
        return 1.15
    else:
        return 1.0

def get_year_growth_multiplier(date):
    """Year-over-year growth trend"""
    year_diff = date.year - 2020
    # 15% annual growth
    return 1.0 + (year_diff * 0.15)

def generate_transactions(products_df, stores_df, num_transactions=150000):
    """Generate realistic transactions with multiple patterns"""
    print("💳 Generating Transactions...")
    print("   This may take a few minutes for 150K transactions...")
    
    # Calculate total days
    total_days = (END_DATE - START_DATE).days + 1
    
    # Distribute transactions across dates with some randomness
    dates = []
    for _ in range(num_transactions):
        random_day = random.randint(0, total_days - 1)
        trans_date = START_DATE + timedelta(days=random_day)
        dates.append(trans_date)
    
    dates = sorted(dates)
    
    transactions = []
    
    for i, trans_date in enumerate(dates):
        if (i + 1) % 25000 == 0:
            print(f"   Processing: {i+1:,}/{num_transactions:,} transactions...")
        
        # Select random product and store
        product = products_df.sample(1).iloc[0]
        store = stores_df.sample(1).iloc[0]
        
        # Base price with some variation
        price_variation = np.random.uniform(0.95, 1.05)
        base_price = product['base_price'] * price_variation
        
        # Apply all multipliers
        seasonal_mult = get_seasonal_multiplier(trans_date)
        day_mult = get_day_multiplier(trans_date)
        growth_mult = get_year_growth_multiplier(trans_date)
        region_mult = store['region_multiplier']
        
        # Final price
        final_price = base_price * seasonal_mult * day_mult * growth_mult * region_mult
        
        # Random quantity (1-5 for most items)
        quantity = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.5, 0.2, 0.1, 0.1, 0.05, 0.05])
        
        # Revenue and profit
        revenue = final_price * quantity
        cost = product['cost'] * quantity
        profit = revenue - cost
        margin = (profit / revenue * 100) if revenue > 0 else 0
        
        # Discount (0-30%)
        discount_pct = np.random.choice([0, 5, 10, 15, 20, 25, 30], 
                                       p=[0.4, 0.2, 0.15, 0.1, 0.08, 0.05, 0.02])
        discount_amount = revenue * (discount_pct / 100)
        final_revenue = revenue - discount_amount
        
        # Channel selection (influenced by year)
        if trans_date.year <= 2020:
            channel = np.random.choice(CHANNELS, p=[0.7, 0.2, 0.05, 0.05])
        elif trans_date.year <= 2022:
            channel = np.random.choice(CHANNELS, p=[0.5, 0.3, 0.15, 0.05])
        else:
            channel = np.random.choice(CHANNELS, p=[0.3, 0.3, 0.3, 0.1])
        
        # Customer segment
        segment = np.random.choice(CUSTOMER_SEGMENTS, p=[0.05, 0.15, 0.40, 0.30, 0.10])
        
        transactions.append({
            'transaction_id': f'T{i+1:06d}',
            'date': trans_date.strftime('%Y-%m-%d'),
            'year': trans_date.year,
            'month': trans_date.month,
            'quarter': (trans_date.month - 1) // 3 + 1,
            'day_of_week': trans_date.strftime('%A'),
            'is_weekend': 1 if trans_date.weekday() >= 5 else 0,
            'store_id': store['store_id'],
            'store_name': store['store_name'],
            'region': store['region'],
            'product_id': product['product_id'],
            'category': product['category'],
            'quantity': quantity,
            'unit_price': round(final_price, 2),
            'gross_revenue': round(revenue, 2),
            'discount_percent': discount_pct,
            'discount_amount': round(discount_amount, 2),
            'final_revenue': round(final_revenue, 2),
            'cost': round(cost, 2),
            'profit': round(final_revenue - cost, 2),
            'margin_percent': round(((final_revenue - cost) / final_revenue * 100) if final_revenue > 0 else 0, 2),
            'channel': channel,
            'customer_segment': segment
        })
    
    trans_df = pd.DataFrame(transactions)
    print(f"   ✅ Generated {len(trans_df):,} transactions")
    return trans_df

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Generate all data
    products_df = generate_products(1000)
    stores_df = generate_stores()
    transactions_df = generate_transactions(products_df, stores_df, NUM_TRANSACTIONS)
    
    # Save to CSV
    print("\n💾 Saving Data...")
    import os
    os.makedirs('data/raw', exist_ok=True)
    products_df.to_csv('data/raw/products.csv', index=False)
    stores_df.to_csv('data/raw/stores.csv', index=False)
    transactions_df.to_csv('data/raw/transactions.csv', index=False)
    
    # Business Summary
    print("\n" + "=" * 70)
    print("📊 BUSINESS SUMMARY")
    print("=" * 70)
    
    total_revenue = transactions_df['final_revenue'].sum()
    total_profit = transactions_df['profit'].sum()
    avg_margin = transactions_df['margin_percent'].mean()
    
    print(f"💰 Total Revenue: ₹{total_revenue/10000000:.2f} Crore")
    print(f"💵 Total Profit: ₹{total_profit/10000000:.2f} Crore")
    print(f"📈 Average Margin: {avg_margin:.2f}%")
    print(f"🛍️  Total Transactions: {len(transactions_df):,}")
    print(f"📅 Date Range: {transactions_df['date'].min()} to {transactions_df['date'].max()}")
    print(f"🏪 Active Stores: {transactions_df['store_id'].nunique()}")
    print(f"📦 Products Sold: {transactions_df['product_id'].nunique()}")
    
    print("\n📊 Category Performance:")
    category_stats = transactions_df.groupby('category')['final_revenue'].agg(['sum', 'count'])
    category_stats['revenue_cr'] = category_stats['sum'] / 10000000
    category_stats['share_pct'] = (category_stats['sum'] / total_revenue * 100)
    for cat in category_stats.index:
        rev = category_stats.loc[cat, 'revenue_cr']
        share = category_stats.loc[cat, 'share_pct']
        print(f"   {cat}: ₹{rev:.2f} Cr ({share:.1f}%)")
    
    print("\n🌍 Regional Performance:")
    region_stats = transactions_df.groupby('region')['final_revenue'].sum() / 10000000
    for region in region_stats.index:
        print(f"   {region}: ₹{region_stats[region]:.2f} Cr")
    
    print("\n" + "=" * 70)
    print("✅ DATA GENERATION COMPLETE!")
    print("=" * 70)
    print("\n📁 Files saved:")
    print("   - data/raw/products.csv")
    print("   - data/raw/stores.csv")
    print("   - data/raw/transactions.csv")
