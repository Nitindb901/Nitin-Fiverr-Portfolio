"""
🚀 ULTIMATE E-COMMERCE + RETAIL DATA GENERATOR
================================================
Project 6: Crown Jewel of Portfolio
500,000 Transactions | 50,000 Customers | 2,000 Products
8 Categories | 20 Physical Stores + E-commerce Channels
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker('en_IN')
random.seed(42)
np.random.seed(42)

print("="*80)
print("🚀 ULTIMATE E-COMMERCE + RETAIL DATA GENERATOR")
print("="*80)
print("\nStarting data generation for Project 6...\n")

# ==================== CONFIGURATION ====================

# 8 Categories: Retail + E-commerce
CATEGORIES = {
    'Electronics': {
        'weight': 0.22,
        'subcategories': ['Smartphones', 'Laptops', 'Tablets', 'Smart Watches', 'Headphones', 
                          'Cameras', 'Gaming Consoles', 'Accessories'],
        'brands': ['Apple', 'Samsung', 'OnePlus', 'Xiaomi', 'Realme', 'Dell', 'HP', 'Lenovo', 
                   'Sony', 'Canon', 'Nikon', 'JBL', 'Boat', 'PS5', 'Xbox'],
        'price_range': (5000, 150000),
        'margin_range': (12, 22)
    },
    'Fashion': {
        'weight': 0.18,
        'subcategories': ['Mens Wear', 'Womens Wear', 'Kids Wear', 'Footwear', 'Accessories', 
                          'Ethnic Wear', 'Western Wear', 'Sports Wear'],
        'brands': ['Zara', 'H&M', 'Nike', 'Adidas', 'Puma', 'Levis', 'UCB', 'Biba', 
                   'FabIndia', 'Allen Solly', 'Van Heusen', 'W', 'Rare'],
        'price_range': (399, 12000),
        'margin_range': (35, 55)
    },
    'Home & Furniture': {
        'weight': 0.15,
        'subcategories': ['Furniture', 'Home Decor', 'Kitchen & Dining', 'Bedding', 'Lighting',
                          'Storage', 'Garden & Outdoor', 'Smart Home'],
        'brands': ['IKEA', 'Godrej', 'Durian', 'Urban Ladder', 'Pepperfry', 'Nilkamal', 
                   'Hometown', 'HomeTown', 'Spacewood'],
        'price_range': (500, 50000),
        'margin_range': (25, 40)
    },
    'Grocery & Food': {
        'weight': 0.12,
        'subcategories': ['Fruits & Vegetables', 'Dairy & Eggs', 'Beverages', 'Snacks', 
                          'Staples', 'Personal Care', 'Household Items', 'Organic'],
        'brands': ['Amul', 'Mother Dairy', 'Nestle', 'Britannia', 'ITC', 'Haldirams', 
                   'Patanjali', 'Fortune', 'Tata'],
        'price_range': (20, 5000),
        'margin_range': (8, 18)
    },
    'Beauty & Personal Care': {
        'weight': 0.10,
        'subcategories': ['Skincare', 'Makeup', 'Haircare', 'Fragrances', 'Bath & Body',
                          'Men Grooming', 'Wellness', 'Luxury Beauty'],
        'brands': ['Lakme', 'Maybelline', 'Loreal', 'Nivea', 'Dove', 'Garnier', 
                   'The Body Shop', 'MAC', 'Estee Lauder', 'Clinique'],
        'price_range': (199, 15000),
        'margin_range': (30, 50)
    },
    'Books & Media': {
        'weight': 0.08,
        'subcategories': ['Fiction', 'Non-Fiction', 'Academic', 'Comics', 'Magazines',
                          'Music', 'Movies', 'Gaming'],
        'brands': ['Penguin', 'Harper', 'Scholastic', 'Marvel', 'DC', 'Sony Music',
                   'Universal', 'T-Series', 'Zee Music'],
        'price_range': (99, 3000),
        'margin_range': (18, 35)
    },
    'Sports & Fitness': {
        'weight': 0.08,
        'subcategories': ['Fitness Equipment', 'Sports Shoes', 'Sportswear', 'Yoga', 
                          'Outdoor Sports', 'Cricket', 'Football', 'Cycling'],
        'brands': ['Nike', 'Adidas', 'Puma', 'Reebok', 'Decathlon', 'Cosco', 
                   'Nivia', 'Yonex', 'Kookaburra'],
        'price_range': (299, 25000),
        'margin_range': (20, 40)
    },
    'Toys & Baby Products': {
        'weight': 0.07,
        'subcategories': ['Toys', 'Baby Care', 'Diapers', 'Baby Gear', 'Feeding', 
                          'Nursery', 'Educational Toys', 'Gaming Toys'],
        'brands': ['Pampers', 'Huggies', 'Johnson & Johnson', 'Chicco', 'Fisher Price',
                   'Lego', 'Hasbro', 'Mattel', 'Hot Wheels'],
        'price_range': (199, 8000),
        'margin_range': (25, 45)
    }
}

# 20 Physical Stores + E-commerce Channels
STORES = [
    # Flagship Stores (8)
    {'id': 'S01', 'name': 'Delhi Connaught Place', 'city': 'Delhi', 'type': 'Flagship', 'region': 'North'},
    {'id': 'S02', 'name': 'Mumbai Bandra', 'city': 'Mumbai', 'type': 'Flagship', 'region': 'West'},
    {'id': 'S03', 'name': 'Bangalore Koramangala', 'city': 'Bangalore', 'type': 'Flagship', 'region': 'South'},
    {'id': 'S04', 'name': 'Hyderabad Jubilee Hills', 'city': 'Hyderabad', 'type': 'Flagship', 'region': 'South'},
    {'id': 'S05', 'name': 'Chennai T Nagar', 'city': 'Chennai', 'type': 'Flagship', 'region': 'South'},
    {'id': 'S06', 'name': 'Kolkata Park Street', 'city': 'Kolkata', 'type': 'Flagship', 'region': 'East'},
    {'id': 'S07', 'name': 'Pune Koregaon Park', 'city': 'Pune', 'type': 'Flagship', 'region': 'West'},
    {'id': 'S08', 'name': 'Ahmedabad Satellite', 'city': 'Ahmedabad', 'type': 'Flagship', 'region': 'West'},
    
    # Premium Stores (6)
    {'id': 'S09', 'name': 'Jaipur MI Road', 'city': 'Jaipur', 'type': 'Premium', 'region': 'North'},
    {'id': 'S10', 'name': 'Lucknow Hazratganj', 'city': 'Lucknow', 'type': 'Premium', 'region': 'North'},
    {'id': 'S11', 'name': 'Kochi MG Road', 'city': 'Kochi', 'type': 'Premium', 'region': 'South'},
    {'id': 'S12', 'name': 'Indore Vijay Nagar', 'city': 'Indore', 'type': 'Premium', 'region': 'Central'},
    {'id': 'S13', 'name': 'Chandigarh Sector 17', 'city': 'Chandigarh', 'type': 'Premium', 'region': 'North'},
    {'id': 'S14', 'name': 'Gurgaon Cyber City', 'city': 'Gurgaon', 'type': 'Premium', 'region': 'North'},
    
    # Standard Stores (6)
    {'id': 'S15', 'name': 'Nagpur Sitabuldi', 'city': 'Nagpur', 'type': 'Standard', 'region': 'Central'},
    {'id': 'S16', 'name': 'Surat Ring Road', 'city': 'Surat', 'type': 'Standard', 'region': 'West'},
    {'id': 'S17', 'name': 'Coimbatore RS Puram', 'city': 'Coimbatore', 'type': 'Standard', 'region': 'South'},
    {'id': 'S18', 'name': 'Bhopal MP Nagar', 'city': 'Bhopal', 'type': 'Standard', 'region': 'Central'},
    {'id': 'S19', 'name': 'Vadodara Alkapuri', 'city': 'Vadodara', 'type': 'Standard', 'region': 'West'},
    {'id': 'S20', 'name': 'Visakhapatnam Beach Road', 'city': 'Visakhapatnam', 'type': 'Standard', 'region': 'South'}
]

# Enhanced Customer Segments
CUSTOMER_SEGMENTS = {
    'Diamond': {'share': 0.03, 'avg_transactions': 25, 'avg_order_multiplier': 3.5},
    'Platinum': {'share': 0.07, 'avg_transactions': 18, 'avg_order_multiplier': 2.8},
    'Gold': {'share': 0.12, 'avg_transactions': 15, 'avg_order_multiplier': 2.2},
    'Silver': {'share': 0.18, 'avg_transactions': 12, 'avg_order_multiplier': 1.8},
    'Regular': {'share': 0.30, 'avg_transactions': 10, 'avg_order_multiplier': 1.4},
    'Occasional': {'share': 0.20, 'avg_transactions': 6, 'avg_order_multiplier': 1.2},
    'New': {'share': 0.10, 'avg_transactions': 3, 'avg_order_multiplier': 1.0}
}

# Sales Channels
CHANNELS = {
    'In-Store': 0.40,
    'Website': 0.28,
    'Mobile App': 0.22,
    'Social Commerce': 0.10
}

# Payment Methods
PAYMENT_METHODS = ['Card', 'UPI', 'Net Banking', 'Wallet', 'COD', 'EMI']

# ==================== PRODUCT GENERATION ====================

def generate_products(n=2000):
    print(f"📦 Generating {n:,} Products...")
    products = []
    product_id = 1
    
    for category, config in CATEGORIES.items():
        category_count = int(n * config['weight'])
        
        for _ in range(category_count):
            subcategory = random.choice(config['subcategories'])
            brand = random.choice(config['brands'])
            product_name = f"{brand} {subcategory} {fake.catch_phrase()[:20]}"
            
            base_price = random.uniform(*config['price_range'])
            margin_pct = random.uniform(*config['margin_range'])
            cost = base_price / (1 + margin_pct/100)
            
            products.append({
                'product_id': f'P{product_id:05d}',
                'category': category,
                'subcategory': subcategory,
                'brand': brand,
                'product_name': product_name,
                'price': round(base_price, 2),
                'cost': round(cost, 2),
                'margin_pct': round(margin_pct, 2),
                'rating': round(random.uniform(3.5, 5.0), 1),
                'stock_status': random.choice(['In Stock', 'In Stock', 'In Stock', 'Limited', 'Out of Stock'])
            })
            product_id += 1
    
    df = pd.DataFrame(products)
    print(f"✅ Generated {len(df):,} products across {len(CATEGORIES)} categories\n")
    
    print("Category Distribution:")
    print(df['category'].value_counts())
    
    return df

# ==================== CUSTOMER GENERATION ====================

def generate_customers(n=50000):
    print(f"\n👥 Generating {n:,} Customers...")
    customers = []
    
    for i in range(1, n+1):
        segment = random.choices(
            list(CUSTOMER_SEGMENTS.keys()),
            weights=[v['share'] for v in CUSTOMER_SEGMENTS.values()]
        )[0]
        
        city = random.choice([s['city'] for s in STORES])
        region = next(s['region'] for s in STORES if s['city'] == city)
        
        customers.append({
            'customer_id': f'C{i:06d}',
            'name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'city': city,
            'region': region,
            'segment': segment,
            'join_date': fake.date_between(start_date='-3y', end_date='today'),
            'preferred_channel': random.choice(list(CHANNELS.keys())),
            'is_prime': random.choice([True, False]) if segment in ['Diamond', 'Platinum', 'Gold'] else False
        })
    
    df = pd.DataFrame(customers)
    print(f"✅ Generated {len(df):,} customers\n")
    
    print("Segment Distribution:")
    print(df['segment'].value_counts())
    print(f"\nPrime Members: {df['is_prime'].sum():,} ({df['is_prime'].sum()/len(df)*100:.1f}%)")
    
    return df

# ==================== TRANSACTION GENERATION ====================

def generate_transactions(products, customers, n=500000):
    print(f"\n💳 Generating {n:,} Transactions...")
    print("This may take a few minutes...\n")
    
    transactions = []
    start_date = datetime(2022, 11, 24)
    end_date = datetime(2025, 11, 22)
    total_days = (end_date - start_date).days
    
    # Pre-calculate customer transaction counts
    customer_txn_counts = {}
    for _, customer in customers.iterrows():
        segment_config = CUSTOMER_SEGMENTS[customer['segment']]
        expected_txns = int(segment_config['avg_transactions'] * random.uniform(0.7, 1.3))
        customer_txn_counts[customer['customer_id']] = expected_txns
    
    # Weight customers by their expected transaction count
    customer_weights = [customer_txn_counts[cid] for cid in customers['customer_id']]
    
    for i in range(n):
        if (i + 1) % 100000 == 0:
            print(f"  → Generated {i+1:,} transactions...")
        
        # Select customer based on weights
        customer = customers.sample(1, weights=customer_weights).iloc[0]
        segment_config = CUSTOMER_SEGMENTS[customer['segment']]
        
        # Transaction date with seasonal patterns
        random_day = random.randint(0, total_days)
        txn_date = start_date + timedelta(days=random_day)
        month = txn_date.month
        
        # Seasonal multiplier
        if month in [10, 11, 12]:  # Festival + Year-end
            seasonal_factor = random.uniform(1.4, 1.8)
        elif month in [1, 2]:  # New Year + Republic Day
            seasonal_factor = random.uniform(1.2, 1.5)
        elif month in [6, 7, 8]:  # Monsoon Sale
            seasonal_factor = random.uniform(1.1, 1.3)
        else:
            seasonal_factor = random.uniform(0.9, 1.1)
        
        # Select product
        product = products.sample(1).iloc[0]
        
        # Quantity
        if product['category'] in ['Grocery & Food', 'Beauty & Personal Care']:
            quantity = random.randint(1, 5)
        else:
            quantity = random.randint(1, 2)
        
        # Pricing
        base_price = product['price']
        
        # Dynamic discount
        if customer['segment'] in ['Diamond', 'Platinum']:
            discount_pct = random.uniform(10, 25)
        elif customer['is_prime']:
            discount_pct = random.uniform(5, 15)
        else:
            discount_pct = random.uniform(0, 10)
        
        # Seasonal discount boost
        discount_pct = min(discount_pct * seasonal_factor * 0.5, 40)
        
        unit_price = base_price * (1 - discount_pct/100)
        revenue = unit_price * quantity
        cost = product['cost'] * quantity
        profit = revenue - cost
        profit_margin_pct = (profit / revenue * 100) if revenue > 0 else 0
        
        # Channel selection
        if customer['preferred_channel']:
            channel_prob = [0.7 if ch == customer['preferred_channel'] else 0.1 for ch in CHANNELS.keys()]
            channel = random.choices(list(CHANNELS.keys()), weights=channel_prob)[0]
        else:
            channel = random.choices(list(CHANNELS.keys()), weights=list(CHANNELS.values()))[0]
        
        # Store/Location
        if channel == 'In-Store':
            store = next(s for s in STORES if s['city'] == customer['city'])
            location = store['name']
            store_id = store['id']
            store_type = store['type']
        else:
            store_id = 'ONLINE'
            store_type = 'E-commerce'
            location = f"{customer['city']} - {channel}"
        
        # Payment method
        if channel == 'In-Store':
            payment = random.choice(['Card', 'UPI', 'Cash', 'Wallet'])
        else:
            payment = random.choice(['Card', 'UPI', 'Net Banking', 'Wallet', 'COD'])
        
        # Delivery time (for online)
        if channel != 'In-Store':
            delivery_days = random.randint(1, 7) if customer['is_prime'] else random.randint(2, 10)
        else:
            delivery_days = 0
        
        transactions.append({
            'transaction_id': f'T{i+1:07d}',
            'customer_id': customer['customer_id'],
            'product_id': product['product_id'],
            'date': txn_date.strftime('%Y-%m-%d'),
            'time': f"{random.randint(8, 22):02d}:{random.randint(0, 59):02d}",
            'store_id': store_id,
            'store_type': store_type,
            'location': location,
            'channel': channel,
            'category': product['category'],
            'subcategory': product['subcategory'],
            'brand': product['brand'],
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'revenue': round(revenue, 2),
            'cost': round(cost, 2),
            'profit': round(profit, 2),
            'profit_margin_pct': round(profit_margin_pct, 2),
            'discount_pct': round(discount_pct, 2),
            'payment_method': payment,
            'delivery_days': delivery_days,
            'customer_segment': customer['segment'],
            'region': customer['region']
        })
    
    df = pd.DataFrame(transactions)
    print(f"\n✅ Generated {len(df):,} transactions\n")
    
    # Business Summary
    total_revenue = df['revenue'].sum() / 10000000  # Crores
    total_profit = df['profit'].sum() / 10000000
    avg_margin = df['profit_margin_pct'].mean()
    
    print("📊 Business Summary:")
    print(f"  • Total Revenue: ₹{total_revenue:.2f} Crore")
    print(f"  • Total Profit: ₹{total_profit:.2f} Crore")
    print(f"  • Average Margin: {avg_margin:.2f}%")
    print(f"  • Date Range: {df['date'].min()} to {df['date'].max()}")
    print(f"  • Unique Customers: {df['customer_id'].nunique():,}")
    
    print(f"\n📈 Channel-wise Revenue:")
    channel_revenue = df.groupby('channel')['revenue'].sum() / 10000000
    for channel, revenue in channel_revenue.sort_values(ascending=False).items():
        print(f"  • {channel}: ₹{revenue:.2f} Cr ({revenue/total_revenue*100:.1f}%)")
    
    print(f"\n🏆 Top 5 Categories by Revenue:")
    category_revenue = df.groupby('category')['revenue'].sum() / 10000000
    for i, (cat, revenue) in enumerate(category_revenue.sort_values(ascending=False).head().items(), 1):
        print(f"  {i}. {cat}: ₹{revenue:.2f} Cr ({revenue/total_revenue*100:.1f}%)")
    
    return df

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    # Generate datasets
    products_df = generate_products(2000)
    customers_df = generate_customers(50000)
    transactions_df = generate_transactions(products_df, customers_df, 500000)
    
    # Save datasets
    print("\n💾 Saving datasets...")
    products_df.to_csv('../data/raw/products.csv', index=False, encoding='utf-8')
    print(f"  ✅ Saved: products.csv ({len(products_df):,} rows)")
    
    customers_df.to_csv('../data/raw/customers.csv', index=False, encoding='utf-8')
    print(f"  ✅ Saved: customers.csv ({len(customers_df):,} rows)")
    
    transactions_df.to_csv('../data/raw/transactions.csv', index=False, encoding='utf-8')
    print(f"  ✅ Saved: transactions.csv ({len(transactions_df):,} rows)")
    
    print("\n" + "="*80)
    print("✨ DATA GENERATION COMPLETE!")
    print("="*80)
    print("\n📁 Files saved in: ../data/raw/")
    print("  • products.csv")
    print("  • customers.csv")
    print("  • transactions.csv")
    print("\n🎯 Ready for advanced analytics and ML modeling!")
    print("\n🚀 This is THE CROWN JEWEL of your portfolio!")
