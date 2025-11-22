"""
Multi-Category Retail KPI Data Generator with Realistic Patterns
================================================================
Generates synthetic retail data for multiple product categories with:
- 6 main categories (Electronics, Fashion, Grocery, Home & Living, Beauty, Sports)
- 200K transactions over 36 months
- 20K customers with segments
- 1000 products across categories
- 15 stores across different cities
- Realistic seasonal patterns and trends
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

# Create directories
os.makedirs('../data/raw', exist_ok=True)

print("=" * 80)
print("MULTI-CATEGORY RETAIL KPI DATA GENERATOR")
print("=" * 80)

# ============================================================================
# 1. GENERATE PRODUCT CATEGORIES AND SUBCATEGORIES
# ============================================================================

def generate_products(n=1000):
    """Generate diverse product catalog across multiple categories"""
    
    print("\n📦 Generating Product Catalog...")
    
    # Define categories with subcategories
    category_structure = {
        'Electronics': {
            'subcategories': ['Mobile Phones', 'Laptops', 'Tablets', 'Accessories', 'Audio', 'Cameras'],
            'brands': ['Samsung', 'Apple', 'Sony', 'LG', 'OnePlus', 'Xiaomi', 'Canon', 'Bose'],
            'price_range': (5000, 150000),
            'margin_range': (0.15, 0.30),
            'weight': 0.20  # 20% of products
        },
        'Fashion': {
            'subcategories': ['Mens Wear', 'Womens Wear', 'Kids Wear', 'Footwear', 'Accessories', 'Ethnic Wear'],
            'brands': ['Zara', 'H&M', 'Levis', 'Nike', 'Adidas', 'Puma', 'Allen Solly', 'Van Heusen'],
            'price_range': (500, 15000),
            'margin_range': (0.35, 0.50),
            'weight': 0.25  # 25% of products
        },
        'Grocery': {
            'subcategories': ['Fresh Produce', 'Dairy', 'Snacks', 'Beverages', 'Staples', 'Personal Care'],
            'brands': ['Amul', 'Nestle', 'ITC', 'HUL', 'Britannia', 'Parle', 'Mother Dairy', 'Dabur'],
            'price_range': (20, 2000),
            'margin_range': (0.10, 0.25),
            'weight': 0.30  # 30% of products
        },
        'Home & Living': {
            'subcategories': ['Furniture', 'Kitchen', 'Decor', 'Bedding', 'Storage', 'Lighting'],
            'brands': ['IKEA', 'Urban Ladder', 'Pepperfry', 'Godrej', 'Prestige', 'Philips', 'Milton', 'Cello'],
            'price_range': (200, 50000),
            'margin_range': (0.25, 0.40),
            'weight': 0.12  # 12% of products
        },
        'Beauty': {
            'subcategories': ['Skincare', 'Makeup', 'Haircare', 'Fragrances', 'Personal Care', 'Beauty Tools'],
            'brands': ['Lakme', 'Maybelline', 'LOreal', 'Nivea', 'Dove', 'Himalaya', 'Biotique', 'The Body Shop'],
            'price_range': (100, 8000),
            'margin_range': (0.30, 0.45),
            'weight': 0.08  # 8% of products
        },
        'Sports': {
            'subcategories': ['Fitness Equipment', 'Sportswear', 'Outdoor Gear', 'Sports Accessories', 'Nutrition', 'Footwear'],
            'brands': ['Nike', 'Adidas', 'Puma', 'Reebok', 'Decathlon', 'Nivia', 'Cosco', 'MuscleBlaze'],
            'price_range': (300, 30000),
            'margin_range': (0.20, 0.35),
            'weight': 0.05  # 5% of products
        }
    }
    
    products = []
    product_id = 1000
    
    for category, details in category_structure.items():
        # Calculate number of products for this category
        n_products = int(n * details['weight'])
        
        for i in range(n_products):
            subcategory = random.choice(details['subcategories'])
            brand = random.choice(details['brands'])
            
            # Generate price with some variation
            base_price = np.random.uniform(details['price_range'][0], details['price_range'][1])
            price = round(base_price, 2)
            
            # Calculate cost based on margin
            margin_pct = np.random.uniform(details['margin_range'][0], details['margin_range'][1])
            cost = round(price * (1 - margin_pct), 2)
            
            # Generate product name
            product_name = f"{brand} {subcategory} {fake.word().title()}"
            
            products.append({
                'product_id': product_id,
                'product_name': product_name,
                'category': category,
                'subcategory': subcategory,
                'brand': brand,
                'price': price,
                'cost': cost,
                'margin_pct': round(margin_pct * 100, 2)
            })
            
            product_id += 1
    
    df = pd.DataFrame(products)
    
    print(f"✅ Generated {len(df)} products across {len(category_structure)} categories")
    print(f"\nCategory Distribution:")
    print(df['category'].value_counts().to_string())
    
    return df

# ============================================================================
# 2. GENERATE CUSTOMERS WITH SEGMENTS
# ============================================================================

def generate_customers(n=20000):
    """Generate customer base with demographics and behavior segments"""
    
    print(f"\n👥 Generating {n:,} Customers...")
    
    cities = [
        'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai',
        'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow',
        'Chandigarh', 'Kochi', 'Indore', 'Nagpur', 'Visakhapatnam'
    ]
    
    segments = ['VIP', 'Premium', 'Regular', 'Occasional', 'New']
    segment_weights = [0.05, 0.15, 0.35, 0.30, 0.15]  # Distribution
    
    customers = []
    
    for i in range(n):
        customer_id = 10000 + i
        
        # Generate demographics
        age = np.random.randint(18, 70)
        gender = random.choice(['Male', 'Female', 'Other'])
        city = random.choice(cities)
        
        # Assign segment
        segment = random.choices(segments, weights=segment_weights)[0]
        
        # Join date (random date in last 3 years)
        days_ago = np.random.randint(0, 1095)  # 3 years
        join_date = datetime.now() - timedelta(days=days_ago)
        
        customers.append({
            'customer_id': customer_id,
            'customer_name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number()[:10],
            'age': age,
            'gender': gender,
            'city': city,
            'segment': segment,
            'join_date': join_date.strftime('%Y-%m-%d')
        })
    
    df = pd.DataFrame(customers)
    
    print(f"✅ Generated {len(df):,} customers")
    print(f"\nSegment Distribution:")
    print(df['segment'].value_counts().to_string())
    
    return df

# ============================================================================
# 3. GENERATE TRANSACTIONS WITH REALISTIC PATTERNS
# ============================================================================

def generate_transactions(products, customers, n=200000):
    """Generate transaction data with realistic patterns"""
    
    print(f"\n💳 Generating {n:,} Transactions...")
    
    # Define stores
    stores = [
        {'store_id': 'ST001', 'store_name': 'Mumbai Central', 'city': 'Mumbai', 'type': 'Flagship'},
        {'store_id': 'ST002', 'store_name': 'Delhi Connaught Place', 'city': 'Delhi', 'type': 'Flagship'},
        {'store_id': 'ST003', 'store_name': 'Bangalore MG Road', 'city': 'Bangalore', 'type': 'Premium'},
        {'store_id': 'ST004', 'store_name': 'Hyderabad Banjara Hills', 'city': 'Hyderabad', 'type': 'Premium'},
        {'store_id': 'ST005', 'store_name': 'Chennai T Nagar', 'city': 'Chennai', 'type': 'Standard'},
        {'store_id': 'ST006', 'store_name': 'Kolkata Park Street', 'city': 'Kolkata', 'type': 'Standard'},
        {'store_id': 'ST007', 'store_name': 'Pune Koregaon Park', 'city': 'Pune', 'type': 'Standard'},
        {'store_id': 'ST008', 'store_name': 'Ahmedabad Satellite', 'city': 'Ahmedabad', 'type': 'Standard'},
        {'store_id': 'ST009', 'store_name': 'Jaipur Pink City', 'city': 'Jaipur', 'type': 'Budget'},
        {'store_id': 'ST010', 'store_name': 'Lucknow Hazratganj', 'city': 'Lucknow', 'type': 'Budget'},
        {'store_id': 'ST011', 'store_name': 'Chandigarh Sector 17', 'city': 'Chandigarh', 'type': 'Budget'},
        {'store_id': 'ST012', 'store_name': 'Kochi Marine Drive', 'city': 'Kochi', 'type': 'Budget'},
        {'store_id': 'ST013', 'store_name': 'Indore Vijay Nagar', 'city': 'Indore', 'type': 'Budget'},
        {'store_id': 'ST014', 'store_name': 'Nagpur Sitabuldi', 'city': 'Nagpur', 'type': 'Budget'},
        {'store_id': 'ST015', 'store_name': 'Visakhapatnam Beach Road', 'city': 'Visakhapatnam', 'type': 'Budget'}
    ]
    
    channels = ['In-Store', 'Online', 'Mobile App']
    
    # Date range: Last 36 months
    start_date = datetime.now() - timedelta(days=1095)
    end_date = datetime.now()
    
    transactions = []
    
    for i in range(n):
        # Generate random date with some seasonal patterns
        random_days = np.random.randint(0, 1095)
        transaction_date = start_date + timedelta(days=random_days)
        
        # Seasonal multipliers (higher sales in festival months)
        month = transaction_date.month
        seasonal_boost = 1.0
        if month in [10, 11, 12]:  # Festival season
            seasonal_boost = 1.5
        elif month in [3, 4]:  # Summer
            seasonal_boost = 1.2
        
        # Select customer (with segment influence)
        customer = customers.sample(1).iloc[0]
        
        # Select product (category preferences vary by season)
        if month in [10, 11, 12]:  # Festival season - more Electronics, Fashion
            category_weights = [0.30, 0.30, 0.15, 0.10, 0.10, 0.05]
        elif month in [5, 6, 7, 8]:  # Monsoon - more Grocery, Home
            category_weights = [0.15, 0.20, 0.35, 0.15, 0.10, 0.05]
        else:
            category_weights = [0.20, 0.25, 0.30, 0.12, 0.08, 0.05]
        
        category = random.choices(
            ['Electronics', 'Fashion', 'Grocery', 'Home & Living', 'Beauty', 'Sports'],
            weights=category_weights
        )[0]
        
        product = products[products['category'] == category].sample(1).iloc[0]
        
        # Select store and channel
        store = random.choice(stores)
        channel = random.choices(channels, weights=[0.45, 0.35, 0.20])[0]
        
        # Quantity (segment influences purchase quantity)
        if customer['segment'] == 'VIP':
            base_qty = np.random.randint(2, 6)
        elif customer['segment'] == 'Premium':
            base_qty = np.random.randint(1, 4)
        else:
            base_qty = np.random.randint(1, 3)
        
        quantity = base_qty
        
        # Apply discount (more discounts for online, festivals)
        discount_pct = 0
        if channel in ['Online', 'Mobile App']:
            discount_pct = np.random.uniform(0, 0.15)
        if month in [10, 11, 12]:
            discount_pct += np.random.uniform(0, 0.10)
        
        discount_pct = min(discount_pct, 0.30)  # Cap at 30%
        
        # Calculate amounts
        unit_price = product['price']
        discount_amount = round(unit_price * quantity * discount_pct, 2)
        gross_amount = round(unit_price * quantity, 2)
        net_amount = round(gross_amount - discount_amount, 2)
        cost_amount = round(product['cost'] * quantity, 2)
        profit = round(net_amount - cost_amount, 2)
        margin_pct = round((profit / net_amount * 100) if net_amount > 0 else 0, 2)
        
        # Payment method
        payment_method = random.choices(
            ['Credit Card', 'Debit Card', 'UPI', 'Cash', 'Wallet'],
            weights=[0.25, 0.20, 0.30, 0.15, 0.10]
        )[0]
        
        transactions.append({
            'transaction_id': f'TXN{100000 + i}',
            'transaction_date': transaction_date.strftime('%Y-%m-%d'),
            'customer_id': customer['customer_id'],
            'customer_segment': customer['segment'],
            'product_id': product['product_id'],
            'product_name': product['product_name'],
            'category': product['category'],
            'subcategory': product['subcategory'],
            'brand': product['brand'],
            'store_id': store['store_id'],
            'store_name': store['store_name'],
            'store_type': store['type'],
            'channel': channel,
            'quantity': quantity,
            'unit_price': unit_price,
            'gross_amount': gross_amount,
            'discount_pct': round(discount_pct * 100, 2),
            'discount_amount': discount_amount,
            'net_amount': net_amount,
            'cost_amount': cost_amount,
            'profit': profit,
            'margin_pct': margin_pct,
            'payment_method': payment_method
        })
        
        if (i + 1) % 50000 == 0:
            print(f"  → Generated {i + 1:,} transactions...")
    
    df = pd.DataFrame(transactions)
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df = df.sort_values('transaction_date').reset_index(drop=True)
    
    # Calculate summary statistics
    total_revenue = df['net_amount'].sum()
    total_profit = df['profit'].sum()
    avg_margin = df['margin_pct'].mean()
    
    print(f"\n✅ Generated {len(df):,} transactions")
    print(f"\n📊 Business Summary:")
    print(f"  • Total Revenue: ₹{total_revenue/10000000:.2f} Crore")
    print(f"  • Total Profit: ₹{total_profit/10000000:.2f} Crore")
    print(f"  • Average Margin: {avg_margin:.2f}%")
    print(f"  • Date Range: {df['transaction_date'].min().date()} to {df['transaction_date'].max().date()}")
    
    print(f"\n📈 Category-wise Revenue:")
    category_revenue = df.groupby('category')['net_amount'].sum().sort_values(ascending=False)
    for cat, rev in category_revenue.items():
        pct = (rev / total_revenue * 100)
        print(f"  • {cat}: ₹{rev/10000000:.2f} Cr ({pct:.1f}%)")
    
    return df

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\nStarting data generation...\n")
    
    # Generate datasets
    products_df = generate_products(n=1000)
    customers_df = generate_customers(n=20000)
    transactions_df = generate_transactions(products_df, customers_df, n=200000)
    
    # Save to CSV
    print("\n💾 Saving datasets...")
    products_df.to_csv('../data/raw/products.csv', index=False)
    print(f"  ✅ Saved: products.csv ({len(products_df):,} rows)")
    
    customers_df.to_csv('../data/raw/customers.csv', index=False)
    print(f"  ✅ Saved: customers.csv ({len(customers_df):,} rows)")
    
    transactions_df.to_csv('../data/raw/transactions.csv', index=False)
    print(f"  ✅ Saved: transactions.csv ({len(transactions_df):,} rows)")
    
    print("\n" + "=" * 80)
    print("✨ DATA GENERATION COMPLETE!")
    print("=" * 80)
    print("\n📁 Files saved in: ../data/raw/")
    print("  • products.csv")
    print("  • customers.csv")
    print("  • transactions.csv")
    print("\n🎯 Ready for KPI analysis and ML modeling!")
