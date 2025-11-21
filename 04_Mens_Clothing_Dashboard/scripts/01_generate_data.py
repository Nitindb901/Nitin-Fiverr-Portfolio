"""
Men's Clothing Retail Data Generator with ML Features
=====================================================
Generates realistic men's clothing retail transaction data with:
- Multiple product categories (Formal, Casual, Sports, Accessories)
- Customer behavior patterns for ML analysis
- Seasonal trends and promotions
- Size variations and inventory data
- Price segments and brand positioning
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

print("=" * 70)
print("MEN'S CLOTHING RETAIL DATA GENERATOR")
print("=" * 70)

# Configuration
NUM_TRANSACTIONS = 100000  # 100K transactions
NUM_CUSTOMERS = 12000  # 12K unique customers
NUM_PRODUCTS = 500  # 500 unique products
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

# Product Categories
CATEGORIES = {
    'Formal Wear': {
        'subcategories': ['Suits', 'Dress Shirts', 'Blazers', 'Trousers', 'Waistcoats'],
        'price_range': (800, 5000),
        'share': 0.25
    },
    'Casual Wear': {
        'subcategories': ['T-Shirts', 'Jeans', 'Casual Shirts', 'Chinos', 'Shorts'],
        'price_range': (400, 2500),
        'share': 0.40
    },
    'Sports & Activewear': {
        'subcategories': ['Gym Wear', 'Track Pants', 'Sports Shoes', 'Jackets', 'Hoodies'],
        'price_range': (600, 3500),
        'share': 0.20
    },
    'Accessories': {
        'subcategories': ['Belts', 'Wallets', 'Ties', 'Watches', 'Sunglasses', 'Bags'],
        'price_range': (300, 4000),
        'share': 0.15
    }
}

# Sizes
SIZES = {
    'Clothing': ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL'],
    'Shoes': ['7', '8', '9', '10', '11', '12'],
    'Accessories': ['One Size']
}

# Brands
BRANDS = {
    'Premium': ['Armani', 'Hugo Boss', 'Ralph Lauren', 'Calvin Klein'],
    'Mid-Range': ['Levi\'s', 'Tommy Hilfiger', 'Nike', 'Adidas', 'Puma'],
    'Budget': ['H&M', 'Zara', 'Uniqlo', 'GAP']
}

# Stores
STORES = [
    'Mumbai MG Road', 'Delhi Connaught Place', 'Bangalore Indiranagar',
    'Pune FC Road', 'Hyderabad Banjara Hills', 'Chennai T Nagar',
    'Kolkata Park Street', 'Ahmedabad CG Road', 'Jaipur MI Road', 'Chandigarh Sector 17'
]

# Sales Channels
CHANNELS = ['In-Store', 'Online', 'Mobile App']

print("\n📊 Generating Product Catalog...")

# Generate Product Catalog
products = []
product_id = 1

for category, details in CATEGORIES.items():
    num_products = int(NUM_PRODUCTS * details['share'])
    
    for _ in range(num_products):
        subcategory = random.choice(details['subcategories'])
        
        # Brand selection based on price
        price = np.random.uniform(details['price_range'][0], details['price_range'][1])
        if price > details['price_range'][1] * 0.7:
            brand_tier = 'Premium'
        elif price > details['price_range'][1] * 0.4:
            brand_tier = 'Mid-Range'
        else:
            brand_tier = 'Budget'
        
        brand = random.choice(BRANDS[brand_tier])
        
        # Size
        if subcategory in ['Sports Shoes']:
            size = random.choice(SIZES['Shoes'])
        elif category == 'Accessories':
            size = 'One Size'
        else:
            size = random.choice(SIZES['Clothing'])
        
        # Cost (60-70% of price for margin calculation)
        cost = price * np.random.uniform(0.55, 0.70)
        
        products.append({
            'ProductID': f'P{product_id:05d}',
            'ProductName': f'{brand} {subcategory}',
            'Category': category,
            'SubCategory': subcategory,
            'Brand': brand,
            'BrandTier': brand_tier,
            'Size': size,
            'Price': round(price, 2),
            'Cost': round(cost, 2),
            'Margin': round(((price - cost) / price) * 100, 2)
        })
        product_id += 1

products_df = pd.DataFrame(products)
print(f"✅ Generated {len(products_df)} products across {len(CATEGORIES)} categories")

print("\n👥 Generating Customer Base...")

# Generate Customers
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    # Customer segments
    segment = np.random.choice(
        ['Premium', 'Value-Conscious', 'Trendy', 'Casual Shopper', 'Fitness Enthusiast'],
        p=[0.15, 0.25, 0.20, 0.25, 0.15]
    )
    
    # Age groups
    age = int(np.random.normal(35, 12))
    age = max(18, min(65, age))  # Clamp between 18-65
    
    # Income level affects spending
    if segment == 'Premium':
        income_level = 'High'
    elif segment in ['Trendy', 'Fitness Enthusiast']:
        income_level = 'Medium-High'
    elif segment == 'Value-Conscious':
        income_level = 'Medium'
    else:
        income_level = 'Medium-Low'
    
    customers.append({
        'CustomerID': f'C{i:06d}',
        'Segment': segment,
        'Age': age,
        'IncomeLevel': income_level,
        'JoinDate': START_DATE + timedelta(days=random.randint(0, 365))
    })

customers_df = pd.DataFrame(customers)
print(f"✅ Generated {len(customers_df)} customers across 5 segments")

print("\n🛍️ Generating Transactions...")

# Generate Transactions
transactions = []

for i in range(1, NUM_TRANSACTIONS + 1):
    # Select random date with seasonal bias
    day_offset = random.randint(0, (END_DATE - START_DATE).days)
    trans_date = START_DATE + timedelta(days=day_offset)
    month = trans_date.month
    
    # Seasonal adjustments
    season_boost = 1.0
    if month in [10, 11, 12]:  # Festive season
        season_boost = 1.5
    elif month in [1, 7]:  # Sale months
        season_boost = 1.3
    
    # Customer selection (repeat customers more likely)
    if random.random() < 0.6:  # 60% repeat customers
        customer = customers_df.sample(1, weights=customers_df.groupby('CustomerID').cumcount() + 1).iloc[0]
    else:
        customer = customers_df.sample(1).iloc[0]
    
    # Product selection based on customer segment
    if customer['Segment'] == 'Premium':
        product = products_df[products_df['BrandTier'] == 'Premium'].sample(1).iloc[0]
    elif customer['Segment'] == 'Value-Conscious':
        product = products_df[products_df['BrandTier'] == 'Budget'].sample(1).iloc[0]
    elif customer['Segment'] == 'Fitness Enthusiast':
        product = products_df[products_df['Category'] == 'Sports & Activewear'].sample(1).iloc[0]
    elif customer['Segment'] == 'Trendy':
        product = products_df[products_df['Category'].isin(['Casual Wear', 'Accessories'])].sample(1).iloc[0]
    else:
        product = products_df.sample(1).iloc[0]
    
    # Quantity (mostly 1, sometimes 2-3)
    quantity = np.random.choice([1, 2, 3], p=[0.7, 0.25, 0.05])
    
    # Discount
    if month in [1, 7]:  # Sale months
        discount_pct = np.random.uniform(20, 50)
    elif month in [11, 12]:  # Festive offers
        discount_pct = np.random.uniform(10, 30)
    else:
        discount_pct = np.random.uniform(0, 15)
    
    # Price calculations
    unit_price = product['Price']
    discount_amount = unit_price * (discount_pct / 100)
    final_price = unit_price - discount_amount
    total_amount = final_price * quantity
    
    # Store and Channel
    store = random.choice(STORES)
    channel = random.choice(CHANNELS)
    
    # Payment method
    payment = np.random.choice(
        ['Credit Card', 'Debit Card', 'UPI', 'Cash', 'Wallet'],
        p=[0.30, 0.25, 0.25, 0.10, 0.10]
    )
    
    transactions.append({
        'TransactionID': f'T{i:07d}',
        'Date': trans_date.strftime('%Y-%m-%d'),
        'CustomerID': customer['CustomerID'],
        'ProductID': product['ProductID'],
        'Category': product['Category'],
        'SubCategory': product['SubCategory'],
        'Brand': product['Brand'],
        'BrandTier': product['BrandTier'],
        'Size': product['Size'],
        'Quantity': quantity,
        'UnitPrice': round(unit_price, 2),
        'DiscountPercent': round(discount_pct, 2),
        'DiscountAmount': round(discount_amount, 2),
        'FinalPrice': round(final_price, 2),
        'TotalAmount': round(total_amount, 2),
        'Store': store,
        'Channel': channel,
        'PaymentMethod': payment,
        'Month': trans_date.month,
        'Year': trans_date.year,
        'Quarter': f'Q{(trans_date.month-1)//3 + 1}'
    })
    
    if i % 10000 == 0:
        print(f"   Generated {i:,} transactions...")

transactions_df = pd.DataFrame(transactions)
print(f"✅ Generated {len(transactions_df):,} transactions")

# Save datasets
print("\n💾 Saving Datasets...")

output_dir = '../data/raw/'
import os
os.makedirs(output_dir, exist_ok=True)

transactions_df.to_csv(f'{output_dir}transactions.csv', index=False)
products_df.to_csv(f'{output_dir}products.csv', index=False)
customers_df.to_csv(f'{output_dir}customers.csv', index=False)

print(f"✅ Saved transactions.csv ({len(transactions_df):,} rows)")
print(f"✅ Saved products.csv ({len(products_df):,} rows)")
print(f"✅ Saved customers.csv ({len(customers_df):,} rows)")

# Summary Statistics
print("\n" + "=" * 70)
print("DATA SUMMARY")
print("=" * 70)

print(f"\n📊 Transaction Overview:")
print(f"   Total Transactions: {len(transactions_df):,}")
print(f"   Total Revenue: ₹{transactions_df['TotalAmount'].sum():,.2f}")
print(f"   Average Transaction Value: ₹{transactions_df['TotalAmount'].mean():,.2f}")
print(f"   Date Range: {transactions_df['Date'].min()} to {transactions_df['Date'].max()}")

print(f"\n🏷️ Category Breakdown:")
for category in transactions_df['Category'].unique():
    cat_data = transactions_df[transactions_df['Category'] == category]
    revenue = cat_data['TotalAmount'].sum()
    pct = (revenue / transactions_df['TotalAmount'].sum()) * 100
    print(f"   {category}: ₹{revenue:,.0f} ({pct:.1f}%)")

print(f"\n👥 Customer Insights:")
print(f"   Total Customers: {len(customers_df):,}")
print(f"   Unique Buyers: {transactions_df['CustomerID'].nunique():,}")
print(f"   Avg Purchases per Customer: {len(transactions_df) / transactions_df['CustomerID'].nunique():.1f}")

print(f"\n🏪 Store Performance:")
print(f"   Total Stores: {len(STORES)}")
print(f"   Avg Revenue per Store: ₹{transactions_df.groupby('Store')['TotalAmount'].sum().mean():,.2f}")

print(f"\n🌐 Channel Distribution:")
for channel in transactions_df['Channel'].unique():
    count = len(transactions_df[transactions_df['Channel'] == channel])
    pct = (count / len(transactions_df)) * 100
    print(f"   {channel}: {count:,} ({pct:.1f}%)")

print("\n" + "=" * 70)
print("✅ DATA GENERATION COMPLETE!")
print("=" * 70)
