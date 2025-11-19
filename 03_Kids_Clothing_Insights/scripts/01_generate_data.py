"""
Kids Clothing Insights - Data Generation Script
Generates realistic datasets for enterprise analytics dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Create directories
Path("data/raw").mkdir(parents=True, exist_ok=True)
Path("data/processed").mkdir(parents=True, exist_ok=True)

print("🎯 Starting Kids Clothing Data Generation...")
print("=" * 60)

# ============================================================================
# 1. GENERATE STORES DATA
# ============================================================================
print("\n📍 Generating Stores Data...")

stores_data = {
    'StoreID': [f'ST{str(i).zfill(3)}' for i in range(1, 11)],
    'StoreName': [
        'Manhattan Kids Hub', 'LA Fashion Kids', 'Chicago Little Ones',
        'Houston Tiny Trends', 'Miami Kids Corner', 'Phoenix Children Store',
        'Dallas Kids Boutique', 'San Diego Mini Fashion', 'Boston Kids Plaza',
        'Seattle Children Hub'
    ],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami', 
             'Phoenix', 'Dallas', 'San Diego', 'Boston', 'Seattle'],
    'State': ['NY', 'CA', 'IL', 'TX', 'FL', 'AZ', 'TX', 'CA', 'MA', 'WA'],
    'Region': ['Northeast', 'West', 'Midwest', 'South', 'South', 
               'West', 'South', 'West', 'Northeast', 'West'],
    'OpenDate': pd.date_range(start='2020-01-01', periods=10, freq='60D'),
    'SquareFeet': [3200, 2800, 3500, 2900, 2600, 2400, 3100, 2700, 3300, 2500],
    'StoreType': ['Flagship', 'Regular', 'Regular', 'Regular', 'Regular',
                  'Small', 'Regular', 'Small', 'Flagship', 'Regular']
}

df_stores = pd.DataFrame(stores_data)
df_stores['Latitude'] = [40.7589, 34.0522, 41.8781, 29.7604, 25.7617,
                         33.4484, 32.7767, 32.7157, 42.3601, 47.6062]
df_stores['Longitude'] = [-73.9851, -118.2437, -87.6298, -95.3698, -80.1918,
                          -112.0740, -96.7970, -117.1611, -71.0589, -122.3321]

print(f"✓ Generated {len(df_stores)} stores across {df_stores['Region'].nunique()} regions")

# ============================================================================
# 2. GENERATE SUPPLIERS DATA
# ============================================================================
print("\n🏭 Generating Suppliers Data...")

suppliers_data = {
    'SupplierID': [f'SUP{str(i).zfill(3)}' for i in range(1, 16)],
    'SupplierName': [
        'ABC Textiles Ltd', 'KidsFashion Co', 'TinyThreads Inc',
        'Little Style Manufacturers', 'Children Wear Factory',
        'Baby Boutique Supplies', 'Youth Fashion Group',
        'Junior Apparel Co', 'Mini Mode Textiles', 'Kids Clothing Factory',
        'Infant Wear Solutions', 'Fashion Kids Suppliers',
        'Little Ones Manufacturing', 'Children Style Ltd', 'Tiny Trends Inc'
    ],
    'Country': ['USA', 'China', 'Vietnam', 'Bangladesh', 'India',
                'USA', 'China', 'Mexico', 'Vietnam', 'Bangladesh',
                'India', 'USA', 'China', 'Vietnam', 'Mexico'],
    'OnTimeDeliveryRate': [0.96, 0.88, 0.92, 0.85, 0.89,
                           0.94, 0.87, 0.91, 0.90, 0.84,
                           0.88, 0.95, 0.86, 0.93, 0.89],
    'DefectRate': [0.02, 0.05, 0.03, 0.06, 0.04,
                   0.02, 0.05, 0.03, 0.03, 0.07,
                   0.04, 0.02, 0.06, 0.03, 0.04],
    'AverageLeadTime': [15, 28, 22, 30, 25, 12, 26, 18, 20, 32, 24, 14, 27, 21, 19]
}

df_suppliers = pd.DataFrame(suppliers_data)
print(f"✓ Generated {len(df_suppliers)} suppliers from {df_suppliers['Country'].nunique()} countries")

# ============================================================================
# 3. GENERATE PRODUCTS DATA
# ============================================================================
print("\n👕 Generating Products Catalog...")

categories = {
    'Boys Clothing': {
        'subcategories': ['Shirts', 'Pants', 'Shorts', 'Jackets', 'Sweaters'],
        'count': 250,
        'price_range': (12, 45),
        'color': '#4A90E2'
    },
    'Girls Clothing': {
        'subcategories': ['Dresses', 'Tops', 'Skirts', 'Leggings', 'Jackets'],
        'count': 300,
        'price_range': (15, 55),
        'color': '#FF6B9D'
    },
    'Infants': {
        'subcategories': ['Onesies', 'Sleepwear', 'Rompers', 'Bibs', 'Blankets'],
        'count': 200,
        'price_range': (8, 35),
        'color': '#FFC845'
    },
    'Accessories': {
        'subcategories': ['Shoes', 'Hats', 'Bags', 'Socks', 'Belts'],
        'count': 150,
        'price_range': (5, 40),
        'color': '#9B59B6'
    }
}

sizes_mapping = {
    'Infants': ['0-3M', '3-6M', '6-12M', '12-18M', '18-24M'],
    'Boys Clothing': ['2T', '3T', '4T', '5T', '6', '7', '8', '10', '12', '14'],
    'Girls Clothing': ['2T', '3T', '4T', '5T', '6', '7', '8', '10', '12', '14'],
    'Accessories': ['XS', 'S', 'M', 'L', 'XL']
}

seasons = ['Spring', 'Summer', 'Fall', 'Winter', 'All Season']
brands = ['KidsStyle', 'TinyTrends', 'LittleFashion', 'MiniMode', 'JuniorWear',
          'BabyChic', 'YouthStyle', 'KiddoFashion', 'PetitMode', 'SmallStyle']
colors = ['Red', 'Blue', 'Pink', 'Green', 'Yellow', 'White', 'Black', 'Purple', 
          'Orange', 'Navy', 'Gray', 'Beige']

products_list = []
product_id = 1

for category, details in categories.items():
    subcategories = details['subcategories']
    count = details['count']
    price_min, price_max = details['price_range']
    
    items_per_sub = count // len(subcategories)
    
    for subcategory in subcategories:
        for i in range(items_per_sub):
            size = random.choice(sizes_mapping[category])
            season = random.choice(seasons)
            brand = random.choice(brands)
            color = random.choice(colors)
            
            price = round(np.random.uniform(price_min, price_max), 2)
            cost = round(price * np.random.uniform(0.45, 0.60), 2)
            
            product_name = f"{brand} {subcategory} {color} {size}"
            
            products_list.append({
                'ProductID': f'P{str(product_id).zfill(4)}',
                'ProductName': product_name,
                'Category': category,
                'Subcategory': subcategory,
                'Size': size,
                'Season': season,
                'Color': color,
                'Brand': brand,
                'Cost': cost,
                'Price': price,
                'SupplierID': random.choice(df_suppliers['SupplierID'].tolist()),
                'LaunchDate': pd.Timestamp('2022-01-01') + timedelta(days=random.randint(0, 700))
            })
            product_id += 1

df_products = pd.DataFrame(products_list)
df_products['Margin'] = ((df_products['Price'] - df_products['Cost']) / df_products['Price'] * 100).round(2)

print(f"✓ Generated {len(df_products)} products across {df_products['Category'].nunique()} categories")
print(f"  - Boys Clothing: {len(df_products[df_products['Category']=='Boys Clothing'])} items")
print(f"  - Girls Clothing: {len(df_products[df_products['Category']=='Girls Clothing'])} items")
print(f"  - Infants: {len(df_products[df_products['Category']=='Infants'])} items")
print(f"  - Accessories: {len(df_products[df_products['Category']=='Accessories'])} items")

# ============================================================================
# 4. GENERATE CUSTOMERS DATA
# ============================================================================
print("\n👥 Generating Customers Data...")

first_names = ['Emma', 'Olivia', 'Ava', 'Sophia', 'Isabella', 'Mia', 'Charlotte', 'Amelia',
               'Liam', 'Noah', 'William', 'James', 'Oliver', 'Benjamin', 'Elijah', 'Lucas',
               'Mason', 'Logan', 'Alexander', 'Ethan', 'Jacob', 'Michael', 'Daniel', 'Henry']

last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
              'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
              'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Walker', 'Hall']

cities_data = [
    ('New York', 'NY', '10001'), ('Los Angeles', 'CA', '90001'), ('Chicago', 'IL', '60601'),
    ('Houston', 'TX', '77001'), ('Phoenix', 'AZ', '85001'), ('Philadelphia', 'PA', '19019'),
    ('San Antonio', 'TX', '78201'), ('San Diego', 'CA', '92093'), ('Dallas', 'TX', '75201'),
    ('San Jose', 'CA', '95101'), ('Austin', 'TX', '78701'), ('Jacksonville', 'FL', '32099'),
    ('Fort Worth', 'TX', '76101'), ('Columbus', 'OH', '43004'), ('San Francisco', 'CA', '94102'),
    ('Charlotte', 'NC', '28201'), ('Indianapolis', 'IN', '46201'), ('Seattle', 'WA', '98101'),
    ('Denver', 'CO', '80201'), ('Boston', 'MA', '02101'), ('Miami', 'FL', '33101')
]

customers_list = []
signup_start = datetime(2022, 1, 1)
signup_end = datetime(2024, 10, 1)

for i in range(1, 10001):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    city, state, zipcode = random.choice(cities_data)
    
    signup_date = signup_start + timedelta(days=random.randint(0, (signup_end - signup_start).days))
    age = random.randint(22, 48)
    gender = random.choice(['Male', 'Female'])
    
    customers_list.append({
        'CustomerID': f'C{str(i).zfill(5)}',
        'FirstName': first_name,
        'LastName': last_name,
        'Email': f"{first_name.lower()}.{last_name.lower()}{random.randint(1,999)}@email.com",
        'City': city,
        'State': state,
        'ZipCode': zipcode,
        'SignupDate': signup_date,
        'Age': age,
        'Gender': gender
    })

df_customers = pd.DataFrame(customers_list)
print(f"✓ Generated {len(df_customers)} customers across {df_customers['City'].nunique()} cities")

# ============================================================================
# 5. GENERATE SALES TRANSACTIONS DATA
# ============================================================================
print("\n💰 Generating Sales Transactions... (This may take a moment)")

transactions_list = []
transaction_id = 1

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
total_days = (end_date - start_date).days

# Generate transactions with realistic patterns
num_transactions = 50000

for _ in range(num_transactions):
    # Date with seasonal patterns
    day_offset = random.randint(0, total_days)
    transaction_date = start_date + timedelta(days=day_offset)
    month = transaction_date.month
    
    # Seasonal multiplier (higher in back-to-school and holidays)
    if month in [8, 9]:  # Back to school
        seasonal_factor = 1.3
    elif month in [11, 12]:  # Holidays
        seasonal_factor = 1.5
    elif month in [1, 2]:  # Winter clearance
        seasonal_factor = 0.8
    else:
        seasonal_factor = 1.0
    
    # Weekend boost
    if transaction_date.weekday() >= 5:  # Saturday/Sunday
        weekend_factor = 1.3
    else:
        weekend_factor = 1.0
    
    # Channel (online vs offline)
    channel = np.random.choice(['Online', 'Offline'], p=[0.42, 0.58])
    
    if channel == 'Online':
        store_id = 'ONLINE'
    else:
        store_id = random.choice(df_stores['StoreID'].tolist())
    
    # Customer (80% existing, 20% new)
    if random.random() < 0.8:
        customer_id = random.choice(df_customers['CustomerID'].tolist())
    else:
        customer_id = f'GUEST{random.randint(1000, 9999)}'
    
    # Product selection (weighted by category popularity)
    category_weights = [0.28, 0.38, 0.22, 0.12]  # Boys, Girls, Infants, Accessories
    selected_category = np.random.choice(df_products['Category'].unique(), p=category_weights)
    product = df_products[df_products['Category'] == selected_category].sample(1).iloc[0]
    
    # Quantity (most buy 1-2 items)
    quantity = np.random.choice([1, 2, 3], p=[0.65, 0.25, 0.10])
    
    # Price with occasional discounts
    base_price = product['Price']
    if random.random() < 0.15:  # 15% chance of discount
        discount = np.random.choice([0.10, 0.20, 0.30, 0.40])
        unit_price = round(base_price * (1 - discount), 2)
    else:
        unit_price = base_price
    
    total_amount = round(unit_price * quantity, 2)
    
    payment_method = np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash'], 
                                     p=[0.45, 0.25, 0.20, 0.10])
    
    transactions_list.append({
        'TransactionID': f'TXN{str(transaction_id).zfill(6)}',
        'Date': transaction_date.date(),
        'Time': f"{random.randint(9, 20):02d}:{random.randint(0, 59):02d}:00",
        'StoreID': store_id,
        'ProductID': product['ProductID'],
        'CustomerID': customer_id,
        'Quantity': quantity,
        'UnitPrice': unit_price,
        'TotalAmount': total_amount,
        'PaymentMethod': payment_method,
        'Channel': channel
    })
    
    transaction_id += 1
    
    if transaction_id % 10000 == 0:
        print(f"  Progress: {transaction_id:,} / {num_transactions:,} transactions...")

df_transactions = pd.DataFrame(transactions_list)
df_transactions['Date'] = pd.to_datetime(df_transactions['Date'])

print(f"✓ Generated {len(df_transactions):,} transactions")
print(f"  Total Revenue: ${df_transactions['TotalAmount'].sum():,.2f}")
print(f"  Average Order Value: ${df_transactions['TotalAmount'].mean():.2f}")
print(f"  Online Sales: {(df_transactions['Channel']=='Online').sum():,} ({(df_transactions['Channel']=='Online').sum()/len(df_transactions)*100:.1f}%)")

# ============================================================================
# 6. GENERATE INVENTORY DATA
# ============================================================================
print("\n📦 Generating Inventory Data...")

inventory_list = []

for _, product in df_products.iterrows():
    # Calculate average monthly sales for this product
    product_sales = df_transactions[df_transactions['ProductID'] == product['ProductID']]['Quantity'].sum()
    monthly_avg_sales = product_sales / 24  # 2 years of data
    
    # Stock level based on sales velocity
    if monthly_avg_sales > 50:
        stock_level = random.randint(80, 200)
        reorder_point = 40
    elif monthly_avg_sales > 20:
        stock_level = random.randint(40, 100)
        reorder_point = 20
    elif monthly_avg_sales > 5:
        stock_level = random.randint(15, 50)
        reorder_point = 10
    else:
        stock_level = random.randint(5, 20)
        reorder_point = 5
    
    # Occasionally create low stock situations
    if random.random() < 0.10:
        stock_level = random.randint(0, reorder_point)
    
    last_restocked = datetime(2024, 12, 1) - timedelta(days=random.randint(0, 90))
    
    inventory_list.append({
        'ProductID': product['ProductID'],
        'WarehouseID': random.choice(['WH001', 'WH002', 'WH003']),
        'StockLevel': stock_level,
        'ReorderPoint': reorder_point,
        'LeadTime': df_suppliers[df_suppliers['SupplierID'] == product['SupplierID']]['AverageLeadTime'].values[0],
        'SupplierID': product['SupplierID'],
        'LastRestocked': last_restocked.date(),
        'StockValue': round(stock_level * product['Cost'], 2)
    })

df_inventory = pd.DataFrame(inventory_list)
df_inventory['StockStatus'] = df_inventory.apply(
    lambda row: 'Critical' if row['StockLevel'] < row['ReorderPoint'] * 0.5 
    else ('Low' if row['StockLevel'] < row['ReorderPoint'] else 'Normal'), axis=1
)

print(f"✓ Generated inventory data for {len(df_inventory)} products")
print(f"  Total Stock Value: ${df_inventory['StockValue'].sum():,.2f}")
print(f"  Critical Stock Items: {(df_inventory['StockStatus']=='Critical').sum()}")
print(f"  Low Stock Items: {(df_inventory['StockStatus']=='Low').sum()}")

# ============================================================================
# 7. GENERATE WEB ANALYTICS DATA
# ============================================================================
print("\n🌐 Generating Web Analytics Data...")

pages = ['Homepage', 'Category', 'Product', 'Cart', 'Checkout', 'OrderConfirmation']
actions = {
    'Homepage': ['View', 'Click'],
    'Category': ['View', 'Filter', 'Sort'],
    'Product': ['View', 'AddToCart', 'AddToWishlist'],
    'Cart': ['View', 'UpdateQuantity', 'RemoveItem', 'Checkout'],
    'Checkout': ['View', 'EnterShipping', 'EnterPayment', 'PlaceOrder'],
    'OrderConfirmation': ['View']
}

traffic_sources = ['Organic Search', 'Paid Search', 'Social Media', 'Direct', 'Email', 'Referral']
devices = ['Desktop', 'Mobile', 'Tablet']

web_analytics_list = []
session_id = 1

# Generate 200K web sessions
num_sessions = 200000

for _ in range(num_sessions):
    session_date = start_date + timedelta(days=random.randint(0, total_days))
    session_time = f"{random.randint(6, 23):02d}:{random.randint(0, 59):02d}:00"
    
    traffic_source = np.random.choice(traffic_sources, p=[0.42, 0.18, 0.15, 0.12, 0.08, 0.05])
    device = np.random.choice(devices, p=[0.35, 0.58, 0.07])
    
    customer_id = random.choice(df_customers['CustomerID'].tolist()) if random.random() < 0.3 else None
    
    # Simulate user journey (funnel)
    current_page = 'Homepage'
    session_duration = 0
    
    # Homepage
    web_analytics_list.append({
        'SessionID': f'SES{str(session_id).zfill(7)}',
        'Date': session_date.date(),
        'Time': session_time,
        'Page': current_page,
        'Action': 'View',
        'ProductID': None,
        'CustomerID': customer_id,
        'DeviceType': device,
        'TrafficSource': traffic_source,
        'Duration': random.randint(10, 60)
    })
    
    # Continue to category (60% bounce rate)
    if random.random() > 0.60:
        current_page = 'Category'
        web_analytics_list.append({
            'SessionID': f'SES{str(session_id).zfill(7)}',
            'Date': session_date.date(),
            'Time': session_time,
            'Page': current_page,
            'Action': 'View',
            'ProductID': None,
            'CustomerID': customer_id,
            'DeviceType': device,
            'TrafficSource': traffic_source,
            'Duration': random.randint(30, 120)
        })
        
        # View product (70% continue)
        if random.random() > 0.30:
            current_page = 'Product'
            product_id = random.choice(df_products['ProductID'].tolist())
            web_analytics_list.append({
                'SessionID': f'SES{str(session_id).zfill(7)}',
                'Date': session_date.date(),
                'Time': session_time,
                'Page': current_page,
                'Action': 'View',
                'ProductID': product_id,
                'CustomerID': customer_id,
                'DeviceType': device,
                'TrafficSource': traffic_source,
                'Duration': random.randint(45, 180)
            })
            
            # Add to cart (40% conversion)
            if random.random() > 0.60:
                web_analytics_list.append({
                    'SessionID': f'SES{str(session_id).zfill(7)}',
                    'Date': session_date.date(),
                    'Time': session_time,
                    'Page': current_page,
                    'Action': 'AddToCart',
                    'ProductID': product_id,
                    'CustomerID': customer_id,
                    'DeviceType': device,
                    'TrafficSource': traffic_source,
                    'Duration': 5
                })
                
                current_page = 'Cart'
                web_analytics_list.append({
                    'SessionID': f'SES{str(session_id).zfill(7)}',
                    'Date': session_date.date(),
                    'Time': session_time,
                    'Page': current_page,
                    'Action': 'View',
                    'ProductID': product_id,
                    'CustomerID': customer_id,
                    'DeviceType': device,
                    'TrafficSource': traffic_source,
                    'Duration': random.randint(20, 90)
                })
                
                # Proceed to checkout (32% abandon cart)
                if random.random() > 0.68:
                    current_page = 'Checkout'
                    web_analytics_list.append({
                        'SessionID': f'SES{str(session_id).zfill(7)}',
                        'Date': session_date.date(),
                        'Time': session_time,
                        'Page': current_page,
                        'Action': 'View',
                        'ProductID': product_id,
                        'CustomerID': customer_id,
                        'DeviceType': device,
                        'TrafficSource': traffic_source,
                        'Duration': random.randint(60, 240)
                    })
                    
                    # Complete purchase (50% complete)
                    if random.random() > 0.50:
                        web_analytics_list.append({
                            'SessionID': f'SES{str(session_id).zfill(7)}',
                            'Date': session_date.date(),
                            'Time': session_time,
                            'Page': current_page,
                            'Action': 'PlaceOrder',
                            'ProductID': product_id,
                            'CustomerID': customer_id,
                            'DeviceType': device,
                            'TrafficSource': traffic_source,
                            'Duration': 10
                        })
                        
                        current_page = 'OrderConfirmation'
                        web_analytics_list.append({
                            'SessionID': f'SES{str(session_id).zfill(7)}',
                            'Date': session_date.date(),
                            'Time': session_time,
                            'Page': current_page,
                            'Action': 'View',
                            'ProductID': product_id,
                            'CustomerID': customer_id,
                            'DeviceType': device,
                            'TrafficSource': traffic_source,
                            'Duration': random.randint(15, 45)
                        })
    
    session_id += 1
    
    if session_id % 50000 == 0:
        print(f"  Progress: {session_id:,} / {num_sessions:,} sessions...")

df_web_analytics = pd.DataFrame(web_analytics_list)
df_web_analytics['Date'] = pd.to_datetime(df_web_analytics['Date'])

print(f"✓ Generated {len(df_web_analytics):,} web events from {num_sessions:,} sessions")
print(f"  Homepage Views: {(df_web_analytics['Page']=='Homepage').sum():,}")
print(f"  Product Views: {(df_web_analytics['Page']=='Product').sum():,}")
print(f"  Add to Cart: {(df_web_analytics['Action']=='AddToCart').sum():,}")
print(f"  Purchases: {(df_web_analytics['Action']=='PlaceOrder').sum():,}")

# ============================================================================
# 8. SAVE ALL DATASETS
# ============================================================================
print("\n💾 Saving all datasets...")

df_stores.to_csv('data/raw/stores.csv', index=False)
print("✓ Saved stores.csv")

df_suppliers.to_csv('data/raw/suppliers.csv', index=False)
print("✓ Saved suppliers.csv")

df_products.to_csv('data/raw/products.csv', index=False)
print("✓ Saved products.csv")

df_customers.to_csv('data/raw/customers.csv', index=False)
print("✓ Saved customers.csv")

df_transactions.to_csv('data/raw/sales_transactions.csv', index=False)
print("✓ Saved sales_transactions.csv")

df_inventory.to_csv('data/raw/inventory.csv', index=False)
print("✓ Saved inventory.csv")

df_web_analytics.to_csv('data/raw/web_analytics.csv', index=False)
print("✓ Saved web_analytics.csv")

# ============================================================================
# 9. GENERATE SUMMARY STATISTICS
# ============================================================================
print("\n" + "=" * 60)
print("📊 DATA GENERATION COMPLETE - SUMMARY STATISTICS")
print("=" * 60)

print(f"\n📁 Files Generated:")
print(f"  1. stores.csv           - {len(df_stores):,} rows")
print(f"  2. suppliers.csv        - {len(df_suppliers):,} rows")
print(f"  3. products.csv         - {len(df_products):,} rows")
print(f"  4. customers.csv        - {len(df_customers):,} rows")
print(f"  5. sales_transactions.csv - {len(df_transactions):,} rows")
print(f"  6. inventory.csv        - {len(df_inventory):,} rows")
print(f"  7. web_analytics.csv    - {len(df_web_analytics):,} rows")

print(f"\n💰 Key Business Metrics:")
print(f"  Total Revenue: ${df_transactions['TotalAmount'].sum():,.2f}")
print(f"  Total Transactions: {len(df_transactions):,}")
print(f"  Average Order Value: ${df_transactions['TotalAmount'].mean():.2f}")
print(f"  Total Customers: {len(df_customers):,}")
print(f"  Active Products: {len(df_products):,}")
print(f"  Total Inventory Value: ${df_inventory['StockValue'].sum():,.2f}")

print(f"\n🌐 E-commerce Metrics:")
funnel_stats = df_web_analytics.groupby('Page').size()
print(f"  Homepage Visits: {funnel_stats.get('Homepage', 0):,}")
print(f"  Product Views: {funnel_stats.get('Product', 0):,}")
add_to_cart = (df_web_analytics['Action']=='AddToCart').sum()
purchases = (df_web_analytics['Action']=='PlaceOrder').sum()
print(f"  Add to Cart: {add_to_cart:,}")
print(f"  Purchases: {purchases:,}")
if funnel_stats.get('Product', 0) > 0:
    conversion_rate = (purchases / funnel_stats.get('Homepage', 1)) * 100
    print(f"  Conversion Rate: {conversion_rate:.2f}%")

print("\n✅ All data generation completed successfully!")
print("=" * 60)
