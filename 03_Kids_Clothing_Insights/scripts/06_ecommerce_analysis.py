"""
E-commerce Analytics & Funnel Analysis Script
Analyzes website traffic, conversion funnel, and online behavior
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("🌐 Starting E-commerce Analytics...")
print("=" * 60)

# Load datasets
print("\n📂 Loading datasets...")
df_web = pd.read_csv('data/raw/web_analytics.csv')
df_transactions = pd.read_csv('data/raw/sales_transactions.csv')
df_products = pd.read_csv('data/raw/products.csv')

df_web['Date'] = pd.to_datetime(df_web['Date'])
df_transactions['Date'] = pd.to_datetime(df_transactions['Date'])

print(f"✓ Loaded {len(df_web):,} web events")
print(f"✓ Loaded {len(df_transactions):,} transactions")
print(f"✓ Loaded {len(df_products):,} products")

# ============================================================================
# 1. OVERALL WEB METRICS
# ============================================================================
print("\n📊 Calculating Overall Web Metrics...")

total_sessions = df_web['SessionID'].nunique()
total_page_views = len(df_web)
avg_pages_per_session = total_page_views / total_sessions
avg_session_duration = df_web.groupby('SessionID')['Duration'].sum().mean()

homepage_visits = df_web[df_web['Page'] == 'Homepage']['SessionID'].nunique()
product_views = df_web[df_web['Page'] == 'Product']['SessionID'].nunique()
cart_views = df_web[df_web['Page'] == 'Cart']['SessionID'].nunique()
checkout_views = df_web[df_web['Page'] == 'Checkout']['SessionID'].nunique()
purchases = df_web[df_web['Action'] == 'PlaceOrder']['SessionID'].nunique()

# Conversion rate
conversion_rate = (purchases / total_sessions * 100) if total_sessions > 0 else 0

print(f"\n🌐 Web Traffic Overview:")
print(f"  Total Sessions: {total_sessions:,}")
print(f"  Total Page Views: {total_page_views:,}")
print(f"  Avg Pages/Session: {avg_pages_per_session:.2f}")
print(f"  Avg Session Duration: {avg_session_duration:.0f} seconds ({avg_session_duration/60:.1f} minutes)")
print(f"  Overall Conversion Rate: {conversion_rate:.2f}%")

# ============================================================================
# 2. CONVERSION FUNNEL ANALYSIS
# ============================================================================
print("\n🎯 Analyzing Conversion Funnel...")

funnel_data = {
    'Stage': ['Homepage', 'Category', 'Product', 'Cart', 'Checkout', 'Purchase'],
    'Sessions': [
        homepage_visits,
        df_web[df_web['Page'] == 'Category']['SessionID'].nunique(),
        product_views,
        cart_views,
        checkout_views,
        purchases
    ]
}

df_funnel = pd.DataFrame(funnel_data)
df_funnel['Conversion%'] = (df_funnel['Sessions'] / df_funnel['Sessions'].iloc[0] * 100).round(2)
df_funnel['DropOff%'] = df_funnel['Conversion%'].diff().fillna(0).abs().round(2)

print(f"\n📉 Conversion Funnel:")
for _, row in df_funnel.iterrows():
    print(f"  {row['Stage']}: {row['Sessions']:,} sessions ({row['Conversion%']:.2f}% conversion)")

# Calculate drop-off rates between stages
print(f"\n⚠️ Drop-off Rates:")
for i in range(1, len(df_funnel)):
    prev_sessions = df_funnel.iloc[i-1]['Sessions']
    curr_sessions = df_funnel.iloc[i]['Sessions']
    dropoff = ((prev_sessions - curr_sessions) / prev_sessions * 100) if prev_sessions > 0 else 0
    print(f"  {df_funnel.iloc[i-1]['Stage']} → {df_funnel.iloc[i]['Stage']}: {dropoff:.2f}% drop-off")

# ============================================================================
# 3. CART ABANDONMENT ANALYSIS
# ============================================================================
print("\n🛒 Analyzing Cart Abandonment...")

add_to_cart_sessions = df_web[df_web['Action'] == 'AddToCart']['SessionID'].nunique()
purchase_sessions = df_web[df_web['Action'] == 'PlaceOrder']['SessionID'].nunique()

cart_abandonment_rate = ((add_to_cart_sessions - purchase_sessions) / add_to_cart_sessions * 100) if add_to_cart_sessions > 0 else 0

print(f"\nCart Abandonment Metrics:")
print(f"  Sessions with Add to Cart: {add_to_cart_sessions:,}")
print(f"  Sessions with Purchase: {purchase_sessions:,}")
print(f"  Cart Abandonment Rate: {cart_abandonment_rate:.2f}%")

# Simulated abandonment reasons
abandonment_reasons = pd.DataFrame({
    'Reason': ['High Shipping Costs', 'Better Price Elsewhere', 'Payment Issues', 
               'Just Browsing', 'Website Errors', 'Other'],
    'Percentage': [32, 18, 15, 20, 8, 7]
})

print(f"\nTop Cart Abandonment Reasons (Estimated):")
for _, row in abandonment_reasons.iterrows():
    print(f"  {row['Reason']}: {row['Percentage']}%")

# ============================================================================
# 4. TRAFFIC SOURCE ANALYSIS
# ============================================================================
print("\n🚀 Analyzing Traffic Sources...")

traffic_analysis = df_web.groupby('TrafficSource')['SessionID'].nunique().reset_index()
traffic_analysis.columns = ['TrafficSource', 'Sessions']
traffic_analysis['SessionShare'] = (traffic_analysis['Sessions'] / total_sessions * 100).round(2)

# Calculate conversion by traffic source
traffic_conversions = df_web[df_web['Action'] == 'PlaceOrder'].groupby('TrafficSource')['SessionID'].nunique().reset_index()
traffic_conversions.columns = ['TrafficSource', 'Conversions']

traffic_analysis = traffic_analysis.merge(traffic_conversions, on='TrafficSource', how='left')
traffic_analysis['Conversions'] = traffic_analysis['Conversions'].fillna(0)
traffic_analysis['ConversionRate'] = (traffic_analysis['Conversions'] / traffic_analysis['Sessions'] * 100).round(2)
traffic_analysis = traffic_analysis.sort_values('Sessions', ascending=False)

print(f"\nTraffic Source Performance:")
for _, row in traffic_analysis.iterrows():
    print(f"  {row['TrafficSource']}: {row['Sessions']:,} sessions ({row['SessionShare']:.1f}%) | "
          f"Conversion: {row['ConversionRate']:.2f}%")

# ============================================================================
# 5. DEVICE ANALYSIS
# ============================================================================
print("\n📱 Analyzing Device Performance...")

device_analysis = df_web.groupby('DeviceType')['SessionID'].nunique().reset_index()
device_analysis.columns = ['DeviceType', 'Sessions']
device_analysis['SessionShare'] = (device_analysis['Sessions'] / total_sessions * 100).round(2)

# Calculate conversion by device
device_conversions = df_web[df_web['Action'] == 'PlaceOrder'].groupby('DeviceType')['SessionID'].nunique().reset_index()
device_conversions.columns = ['DeviceType', 'Conversions']

device_analysis = device_analysis.merge(device_conversions, on='DeviceType', how='left')
device_analysis['Conversions'] = device_analysis['Conversions'].fillna(0)
device_analysis['ConversionRate'] = (device_analysis['Conversions'] / device_analysis['Sessions'] * 100).round(2)

# Calculate avg session duration by device
device_duration = df_web.groupby(['DeviceType', 'SessionID'])['Duration'].sum().reset_index()
device_duration = device_duration.groupby('DeviceType')['Duration'].mean().reset_index()
device_duration.columns = ['DeviceType', 'AvgDuration']

device_analysis = device_analysis.merge(device_duration, on='DeviceType', how='left')
device_analysis = device_analysis.sort_values('Sessions', ascending=False)

print(f"\nDevice Performance:")
for _, row in device_analysis.iterrows():
    print(f"  {row['DeviceType']}: {row['Sessions']:,} sessions ({row['SessionShare']:.1f}%) | "
          f"Conversion: {row['ConversionRate']:.2f}% | Avg Duration: {row['AvgDuration']:.0f}s")

# ============================================================================
# 6. PRODUCT PAGE PERFORMANCE
# ============================================================================
print("\n🏷️ Analyzing Product Page Performance...")

product_views = df_web[df_web['Page'] == 'Product'].copy()
product_views = product_views[product_views['ProductID'].notna()]

# Views per product
product_page_stats = product_views.groupby('ProductID').agg({
    'SessionID': 'nunique',
    'Duration': 'mean'
}).reset_index()

product_page_stats.columns = ['ProductID', 'Views', 'AvgTimeOnPage']

# Add to cart rate per product
add_to_cart = df_web[df_web['Action'] == 'AddToCart'].groupby('ProductID')['SessionID'].nunique().reset_index()
add_to_cart.columns = ['ProductID', 'AddToCartCount']

product_page_stats = product_page_stats.merge(add_to_cart, on='ProductID', how='left')
product_page_stats['AddToCartCount'] = product_page_stats['AddToCartCount'].fillna(0)
product_page_stats['AddToCartRate'] = (product_page_stats['AddToCartCount'] / product_page_stats['Views'] * 100).round(2)

# Merge with product details
product_page_stats = product_page_stats.merge(df_products[['ProductID', 'ProductName', 'Category', 'Price']], 
                                               on='ProductID', how='left')

product_page_stats = product_page_stats.sort_values('Views', ascending=False)

print(f"\nTop 10 Most Viewed Products:")
for idx, row in product_page_stats.head(10).iterrows():
    print(f"  {row['ProductName'][:40]}: {row['Views']:,} views | {row['AddToCartRate']:.1f}% add-to-cart rate")

# Products with best add-to-cart rates (min 20 views)
high_performing = product_page_stats[product_page_stats['Views'] >= 20].sort_values('AddToCartRate', ascending=False)

print(f"\nTop 5 Products by Add-to-Cart Rate (min 20 views):")
for idx, row in high_performing.head(5).iterrows():
    print(f"  {row['ProductName'][:40]}: {row['AddToCartRate']:.1f}% | {row['Views']} views")

# ============================================================================
# 7. TIME-BASED ANALYSIS
# ============================================================================
print("\n⏰ Analyzing Time-based Patterns...")

df_web['Hour'] = pd.to_datetime(df_web['Time'], format='%H:%M:%S').dt.hour
df_web['DayOfWeek'] = df_web['Date'].dt.day_name()

# Hourly traffic
hourly_traffic = df_web.groupby('Hour')['SessionID'].nunique().reset_index()
hourly_traffic.columns = ['Hour', 'Sessions']
hourly_traffic = hourly_traffic.sort_values('Sessions', ascending=False)

print(f"\nTop 5 Peak Traffic Hours:")
for _, row in hourly_traffic.head(5).iterrows():
    print(f"  {row['Hour']:02d}:00 - {row['Hour']:02d}:59: {row['Sessions']:,} sessions")

# Day of week analysis
dow_traffic = df_web.groupby('DayOfWeek')['SessionID'].nunique().reset_index()
dow_traffic.columns = ['DayOfWeek', 'Sessions']

# Calculate conversion by day
dow_conversions = df_web[df_web['Action'] == 'PlaceOrder'].groupby('DayOfWeek')['SessionID'].nunique().reset_index()
dow_conversions.columns = ['DayOfWeek', 'Conversions']

dow_traffic = dow_traffic.merge(dow_conversions, on='DayOfWeek', how='left')
dow_traffic['Conversions'] = dow_traffic['Conversions'].fillna(0)
dow_traffic['ConversionRate'] = (dow_traffic['Conversions'] / dow_traffic['Sessions'] * 100).round(2)

# Sort by day of week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dow_traffic['DayNum'] = dow_traffic['DayOfWeek'].apply(lambda x: day_order.index(x))
dow_traffic = dow_traffic.sort_values('DayNum')

print(f"\nTraffic by Day of Week:")
for _, row in dow_traffic.iterrows():
    print(f"  {row['DayOfWeek']}: {row['Sessions']:,} sessions | Conversion: {row['ConversionRate']:.2f}%")

# ============================================================================
# 8. ONLINE REVENUE ANALYSIS
# ============================================================================
print("\n💰 Analyzing Online Revenue...")

online_transactions = df_transactions[df_transactions['Channel'] == 'Online']
online_revenue = online_transactions['TotalAmount'].sum()
online_orders = len(online_transactions)
online_aov = online_transactions['TotalAmount'].mean()

total_revenue = df_transactions['TotalAmount'].sum()
online_revenue_share = (online_revenue / total_revenue * 100) if total_revenue > 0 else 0

print(f"\nOnline Channel Performance:")
print(f"  Online Revenue: ${online_revenue:,.2f} ({online_revenue_share:.1f}% of total)")
print(f"  Online Orders: {online_orders:,}")
print(f"  Avg Order Value: ${online_aov:.2f}")
print(f"  Revenue per Session: ${online_revenue/total_sessions:.2f}")

# Category performance online
online_category = online_transactions.merge(df_products[['ProductID', 'Category']], on='ProductID', how='left')
category_online = online_category.groupby('Category').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'nunique'
}).reset_index()

category_online.columns = ['Category', 'Revenue', 'Orders']
category_online['AvgOrderValue'] = (category_online['Revenue'] / category_online['Orders']).round(2)
category_online = category_online.sort_values('Revenue', ascending=False)

print(f"\nOnline Revenue by Category:")
for _, row in category_online.iterrows():
    print(f"  {row['Category']}: ${row['Revenue']:,.2f} | {row['Orders']:,} orders | AOV: ${row['AvgOrderValue']:.2f}")

# ============================================================================
# 9. CUSTOMER JOURNEY ANALYSIS
# ============================================================================
print("\n🗺️ Analyzing Customer Journey...")

# Calculate avg pages before purchase
purchase_sessions = df_web[df_web['Action'] == 'PlaceOrder']['SessionID'].unique()
journey_analysis = df_web[df_web['SessionID'].isin(purchase_sessions)].groupby('SessionID').agg({
    'Page': 'count',
    'Duration': 'sum'
}).reset_index()

journey_analysis.columns = ['SessionID', 'PagesViewed', 'TotalDuration']

avg_pages_before_purchase = journey_analysis['PagesViewed'].mean()
avg_time_before_purchase = journey_analysis['TotalDuration'].mean()

print(f"\nPurchase Journey Metrics:")
print(f"  Avg Pages Before Purchase: {avg_pages_before_purchase:.1f}")
print(f"  Avg Time Before Purchase: {avg_time_before_purchase:.0f} seconds ({avg_time_before_purchase/60:.1f} minutes)")

# Most common paths (first 3 pages)
session_paths = df_web.sort_values(['SessionID', 'Time']).groupby('SessionID')['Page'].apply(
    lambda x: ' → '.join(x.head(3))
).reset_index()

session_paths.columns = ['SessionID', 'Path']
path_frequency = session_paths['Path'].value_counts().head(10).reset_index()
path_frequency.columns = ['Path', 'Frequency']

print(f"\nTop 5 Most Common User Paths:")
for idx, row in path_frequency.head(5).iterrows():
    print(f"  {row['Path']}: {row['Frequency']:,} sessions")

# ============================================================================
# SAVE PROCESSED DATA
# ============================================================================
print("\n💾 Saving processed datasets...")

# Funnel data
df_funnel.to_csv('data/processed/conversion_funnel.csv', index=False)
print("✓ Saved conversion_funnel.csv")

# Traffic source analysis
traffic_analysis.to_csv('data/processed/traffic_source_analysis.csv', index=False)
print("✓ Saved traffic_source_analysis.csv")

# Device analysis
device_analysis.to_csv('data/processed/device_analysis.csv', index=False)
print("✓ Saved device_analysis.csv")

# Product page performance
product_page_stats.to_csv('data/processed/product_page_performance.csv', index=False)
print("✓ Saved product_page_performance.csv")

# Hourly traffic
hourly_traffic.to_csv('data/processed/hourly_traffic.csv', index=False)
print("✓ Saved hourly_traffic.csv")

# Day of week analysis
dow_traffic.to_csv('data/processed/dow_traffic.csv', index=False)
print("✓ Saved dow_traffic.csv")

# Online category performance
category_online.to_csv('data/processed/online_category_performance.csv', index=False)
print("✓ Saved online_category_performance.csv")

# Cart abandonment reasons
abandonment_reasons.to_csv('data/processed/cart_abandonment_reasons.csv', index=False)
print("✓ Saved cart_abandonment_reasons.csv")

# Journey analysis
journey_summary = pd.DataFrame({
    'Metric': ['Avg Pages Before Purchase', 'Avg Time Before Purchase (seconds)', 
               'Total Sessions', 'Purchase Sessions', 'Overall Conversion Rate'],
    'Value': [avg_pages_before_purchase, avg_time_before_purchase, 
              total_sessions, purchases, conversion_rate]
})
journey_summary.to_csv('data/processed/customer_journey_summary.csv', index=False)
print("✓ Saved customer_journey_summary.csv")

print("\n" + "=" * 60)
print("✅ E-commerce Analytics Complete!")
print("=" * 60)
print(f"\n📊 Key Insights:")
print(f"  • Total Sessions: {total_sessions:,}")
print(f"  • Conversion Rate: {conversion_rate:.2f}%")
print(f"  • Cart Abandonment: {cart_abandonment_rate:.2f}%")
print(f"  • Top Traffic Source: {traffic_analysis.iloc[0]['TrafficSource']} ({traffic_analysis.iloc[0]['SessionShare']:.1f}%)")
print(f"  • Best Device: {device_analysis.iloc[0]['DeviceType']} ({device_analysis.iloc[0]['SessionShare']:.1f}% sessions)")
print(f"  • Online Revenue Share: {online_revenue_share:.1f}%")
