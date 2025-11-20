"""
Synthetic Retail Data Generator
Generates 12 months of realistic retail transaction data with:
- Weekly seasonality (weekends higher)
- Promotional spikes (festivals/holidays)
- Store-level variations
- Discount effects on quantity sold
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

def generate_retail_data():
    """Generate synthetic retail dataset for 12 months"""
    
    # Configuration
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Master data
    stores = ['Store_A', 'Store_B', 'Store_C', 'Store_D', 'Store_E']
    categories = {
        'Electronics': ['Mobile', 'Laptop', 'Tablet', 'Accessories'],
        'Apparel': ['Mens', 'Womens', 'Kids', 'Footwear'],
        'Home': ['Furniture', 'Decor', 'Kitchen', 'Bedding'],
        'Grocery': ['Staples', 'Snacks', 'Beverages', 'Dairy']
    }
    
    brands = {
        'Electronics': ['Samsung', 'Apple', 'Sony', 'LG', 'OnePlus'],
        'Apparel': ['Nike', 'Adidas', 'Zara', 'H&M', 'Levis'],
        'Home': ['IKEA', 'Urban', 'HomeStyle', 'Comfort', 'Elite'],
        'Grocery': ['Nestle', 'ITC', 'Britannia', 'Amul', 'PepsiCo']
    }
    
    # Festival/promotional dates (higher sales)
    festival_dates = [
        datetime(2024, 1, 26),  # Republic Day
        datetime(2024, 2, 14),  # Valentine's Day
        datetime(2024, 3, 8),   # Women's Day
        datetime(2024, 3, 25),  # Holi
        datetime(2024, 4, 21),  # Easter
        datetime(2024, 8, 15),  # Independence Day
        datetime(2024, 10, 12), # Dussehra
        datetime(2024, 11, 1),  # Diwali
        datetime(2024, 11, 29), # Black Friday
        datetime(2024, 12, 25)  # Christmas
    ]
    
    # Store characteristics (avg footfall per day)
    store_footfall = {
        'Store_A': 1200,
        'Store_B': 1500,
        'Store_C': 1000,
        'Store_D': 1800,
        'Store_E': 1300
    }
    
    data = []
    
    print("Generating synthetic retail data...")
    
    for date in date_range:
        # Day of week effect (weekends higher)
        day_of_week = date.weekday()
        weekend_multiplier = 1.4 if day_of_week in [5, 6] else 1.0
        
        # Festival effect (within 3 days window)
        festival_multiplier = 1.0
        for festival in festival_dates:
            if abs((date - festival).days) <= 3:
                festival_multiplier = 1.8
                break
        
        # Month-end effect
        month_end_multiplier = 1.2 if date.day > 25 else 1.0
        
        for store in stores:
            # Calculate daily footfall
            base_footfall = store_footfall[store]
            daily_footfall = int(base_footfall * weekend_multiplier * 
                                festival_multiplier * month_end_multiplier * 
                                np.random.uniform(0.85, 1.15))
            
            # Conversion rate (footfall to transactions)
            conversion_rate = np.random.uniform(0.15, 0.35)
            num_transactions = int(daily_footfall * conversion_rate)
            
            for _ in range(num_transactions):
                # Select category and subcategory
                category = np.random.choice(list(categories.keys()), 
                                           p=[0.25, 0.35, 0.20, 0.20])
                subcategory = np.random.choice(categories[category])
                brand = np.random.choice(brands[category])
                
                # Generate SKU
                sku = f"{category[:3].upper()}-{subcategory[:3].upper()}-{np.random.randint(1000, 9999)}"
                
                # Price logic based on category
                if category == 'Electronics':
                    mrp = np.random.uniform(5000, 80000)
                elif category == 'Apparel':
                    mrp = np.random.uniform(500, 5000)
                elif category == 'Home':
                    mrp = np.random.uniform(1000, 15000)
                else:  # Grocery
                    mrp = np.random.uniform(50, 1000)
                
                # Discount logic
                if festival_multiplier > 1.0:
                    discount_pct = np.random.uniform(10, 40)
                else:
                    discount_pct = np.random.uniform(0, 20)
                
                selling_price = mrp * (1 - discount_pct / 100)
                
                # Quantity based on discount
                if discount_pct > 20:
                    qty = np.random.randint(1, 5)
                else:
                    qty = np.random.randint(1, 3)
                
                net_amount = selling_price * qty
                
                # Record transaction
                data.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Store': store,
                    'Category': category,
                    'SubCategory': subcategory,
                    'SKU': sku,
                    'Brand': brand,
                    'MRP': round(mrp, 2),
                    'SellingPrice': round(selling_price, 2),
                    'Qty': qty,
                    'NETAMT': round(net_amount, 2),
                    'Footfall': daily_footfall,
                    'ConversionPct': round(conversion_rate * 100, 2),
                    'DiscountPct': round(discount_pct, 2)
                })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    print(f"Generated {len(df)} transaction records")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Total revenue: ${df['NETAMT'].sum():,.2f}")
    
    return df

def main():
    """Main execution function"""
    
    # Generate data
    df = generate_retail_data()
    
    # Create output directory if not exists
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to CSV
    output_file = os.path.join(output_dir, 'retail_transactions_raw.csv')
    df.to_csv(output_file, index=False)
    print(f"\n✓ Data saved to: {output_file}")
    
    # Display sample statistics
    print("\n" + "="*60)
    print("DATASET SUMMARY")
    print("="*60)
    print(f"Total Transactions: {len(df):,}")
    print(f"Date Range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Stores: {df['Store'].nunique()}")
    print(f"Categories: {df['Category'].nunique()}")
    print(f"Unique SKUs: {df['SKU'].nunique()}")
    print(f"\nTotal Revenue: ${df['NETAMT'].sum():,.2f}")
    print(f"Avg Transaction Value: ${df['NETAMT'].mean():,.2f}")
    print(f"Avg Discount: {df['DiscountPct'].mean():.2f}%")
    print(f"Avg Conversion Rate: {df['ConversionPct'].mean():.2f}%")
    print("\nCategory-wise Revenue:")
    print(df.groupby('Category')['NETAMT'].sum().sort_values(ascending=False).apply(lambda x: f"${x:,.2f}"))
    print("="*60)

if __name__ == "__main__":
    main()
