"""
Generate Business Visualizations and Insights
=============================================
Creates professional charts and graphs for men's clothing dashboard
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

print("=" * 70)
print("GENERATING VISUALIZATIONS - MEN'S CLOTHING DASHBOARD")
print("=" * 70)

# Load all processed data
print("\n📥 Loading Data...")
data_dir = '../data/processed/'
transactions = pd.read_csv(f'{data_dir}transactions_processed.csv')
transactions['Date'] = pd.to_datetime(transactions['Date'])
category_perf = pd.read_csv(f'{data_dir}category_performance.csv')
brand_perf = pd.read_csv(f'{data_dir}brand_performance.csv')
store_perf = pd.read_csv(f'{data_dir}store_performance.csv')
channel_perf = pd.read_csv(f'{data_dir}channel_performance.csv')
monthly_totals = pd.read_csv(f'{data_dir}monthly_totals.csv')
rfm = pd.read_csv(f'{data_dir}rfm_analysis.csv')
clv = pd.read_csv(f'{data_dir}customer_lifetime_value.csv')

# ML results
ml_dir = '../data/ml_results/'
forecast = pd.read_csv(f'{ml_dir}revenue_forecast.csv')
clusters = pd.read_csv(f'{ml_dir}customer_clusters.csv')
cluster_summary = pd.read_csv(f'{ml_dir}cluster_summary.csv')

print("✅ All data loaded successfully")

# Create output directory
viz_dir = '../visualizations/'
os.makedirs(viz_dir, exist_ok=True)

# Color palette
colors = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent1': '#F18F01',
    'accent2': '#C73E1D',
    'success': '#06A77D',
    'formal': '#2C3E50',
    'casual': '#3498DB',
    'sports': '#E74C3C',
    'accessories': '#9B59B6'
}

print(f"\n🎨 Creating Visualizations...")
viz_count = 0

# ============================================================================
# 1. CATEGORY PERFORMANCE BAR CHART
# ============================================================================
viz_count += 1
print(f"   {viz_count}. Category Performance...")

plt.figure(figsize=(12, 7))
bars = plt.bar(category_perf['Category'], category_perf['Revenue']/1000000, 
               color=[colors['formal'], colors['casual'], colors['sports'], colors['accessories']], 
               edgecolor='black', linewidth=1.5)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'₹{height:.1f}M\n({category_perf.iloc[bars.index(bar)]["RevenueShare"]:.1f}%)',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.xlabel('Category', fontsize=12, fontweight='bold')
plt.ylabel('Revenue (Millions ₹)', fontsize=12, fontweight='bold')
plt.title('Category Revenue Performance', fontsize=14, fontweight='bold', pad=20)
plt.xticks(rotation=15, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{viz_dir}01_category_performance.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 2. MONTHLY REVENUE TREND
# ============================================================================
viz_count += 1
print(f"   {viz_count}. Monthly Revenue Trend...")

monthly_totals['Month'] = pd.to_datetime(monthly_totals['Month'])
plt.figure(figsize=(14, 7))
plt.plot(monthly_totals['Month'], monthly_totals['Revenue']/1000000, 
         marker='o', linewidth=2.5, color=colors['primary'], markersize=8)
plt.fill_between(monthly_totals['Month'], monthly_totals['Revenue']/1000000, 
                 alpha=0.3, color=colors['primary'])
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Revenue (Millions ₹)', fontsize=12, fontweight='bold')
plt.title('Monthly Revenue Trend (2023-2024)', fontsize=14, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{viz_dir}02_monthly_trend.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 3. CHANNEL DISTRIBUTION PIE CHART
# ============================================================================
viz_count += 1
print(f"   {viz_count}. Channel Distribution...")

plt.figure(figsize=(10, 10))
colors_pie = [colors['primary'], colors['secondary'], colors['accent1']]
explode = (0.05, 0.05, 0.05)
plt.pie(channel_perf['Revenue'], labels=channel_perf['Channel'], autopct='%1.1f%%',
        colors=colors_pie, explode=explode, startangle=90, 
        textprops={'fontsize': 12, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
plt.title('Sales Channel Distribution', fontsize=14, fontweight='bold', pad=20)
plt.savefig(f'{viz_dir}03_channel_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 4. TOP 10 STORES BY REVENUE
# ============================================================================
viz_count += 1
print(f"   {viz_count}. Top Stores Performance...")

plt.figure(figsize=(12, 8))
top_stores = store_perf.nlargest(10, 'Revenue')
bars = plt.barh(top_stores['Store'], top_stores['Revenue']/1000000, 
                color=colors['success'], edgecolor='black', linewidth=1)

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2.,
             f'₹{width:.1f}M',
             ha='left', va='center', fontsize=10, fontweight='bold', 
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

plt.xlabel('Revenue (Millions ₹)', fontsize=12, fontweight='bold')
plt.ylabel('Store', fontsize=12, fontweight='bold')
plt.title('Top 10 Stores by Revenue', fontsize=14, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{viz_dir}04_top_stores.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 5. BRAND PERFORMANCE (TOP 10)
# ============================================================================
viz_count += 1
print(f"   {viz_count}. Brand Performance...")

plt.figure(figsize=(12, 8))
top_brands = brand_perf.nlargest(10, 'Revenue')
colors_brand = [colors['primary'] if tier == 'Premium' else colors['secondary'] if tier == 'Mid-Range' else colors['accent1'] 
                for tier in top_brands['BrandTier']]
bars = plt.bar(range(len(top_brands)), top_brands['Revenue']/1000000, 
               color=colors_brand, edgecolor='black', linewidth=1.5)

# Add value labels
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'₹{height:.1f}M',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.xlabel('Brand', fontsize=12, fontweight='bold')
plt.ylabel('Revenue (Millions ₹)', fontsize=12, fontweight='bold')
plt.title('Top 10 Brands by Revenue', fontsize=14, fontweight='bold', pad=20)
plt.xticks(range(len(top_brands)), top_brands['Brand'], rotation=45, ha='right')

# Legend for brand tiers
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=colors['primary'], edgecolor='black', label='Premium'),
    Patch(facecolor=colors['secondary'], edgecolor='black', label='Mid-Range'),
    Patch(facecolor=colors['accent1'], edgecolor='black', label='Budget')
]
plt.legend(handles=legend_elements, loc='upper right', fontsize=10)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{viz_dir}05_brand_performance.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 6. RFM SEGMENT DISTRIBUTION
# ============================================================================
viz_count += 1
print(f"   {viz_count}. RFM Segmentation...")

plt.figure(figsize=(12, 8))
segment_counts = rfm['RFM_Segment'].value_counts()
colors_rfm = plt.cm.viridis(np.linspace(0, 1, len(segment_counts)))
bars = plt.bar(segment_counts.index, segment_counts.values, 
               color=colors_rfm, edgecolor='black', linewidth=1.5)

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}\n({height/len(rfm)*100:.1f}%)',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.xlabel('Customer Segment', fontsize=12, fontweight='bold')
plt.ylabel('Number of Customers', fontsize=12, fontweight='bold')
plt.title('Customer Segmentation (RFM Analysis)', fontsize=14, fontweight='bold', pad=20)
plt.xticks(rotation=30, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{viz_dir}06_rfm_segments.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 7. TRANSACTION VALUE DISTRIBUTION
# ============================================================================
viz_count += 1
print(f"   {viz_count}. Transaction Distribution...")

plt.figure(figsize=(12, 7))
plt.hist(transactions['TotalAmount'], bins=50, color=colors['primary'], 
         edgecolor='black', alpha=0.7)
plt.axvline(transactions['TotalAmount'].mean(), color='red', linestyle='--', 
            linewidth=2, label=f'Mean: ₹{transactions["TotalAmount"].mean():,.0f}')
plt.axvline(transactions['TotalAmount'].median(), color='green', linestyle='--', 
            linewidth=2, label=f'Median: ₹{transactions["TotalAmount"].median():,.0f}')
plt.xlabel('Transaction Amount (₹)', fontsize=12, fontweight='bold')
plt.ylabel('Frequency', fontsize=12, fontweight='bold')
plt.title('Transaction Value Distribution', fontsize=14, fontweight='bold', pad=20)
plt.legend(fontsize=11)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{viz_dir}07_transaction_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 8. WEEKDAY vs WEEKEND SALES
# ============================================================================
viz_count += 1
print(f"   {viz_count}. Weekday vs Weekend Analysis...")

weekend_sales = transactions.groupby('IsWeekend').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'count'
}).reset_index()
weekend_sales['IsWeekend'] = weekend_sales['IsWeekend'].map({0: 'Weekday', 1: 'Weekend'})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Revenue comparison
bars1 = ax1.bar(weekend_sales['IsWeekend'], weekend_sales['TotalAmount']/1000000, 
                color=[colors['primary'], colors['secondary']], edgecolor='black', linewidth=1.5)
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'₹{height:.1f}M',
             ha='center', va='bottom', fontsize=11, fontweight='bold')
ax1.set_ylabel('Revenue (Millions ₹)', fontsize=11, fontweight='bold')
ax1.set_title('Revenue: Weekday vs Weekend', fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Transaction count comparison
bars2 = ax2.bar(weekend_sales['IsWeekend'], weekend_sales['TransactionID'], 
                color=[colors['primary'], colors['secondary']], edgecolor='black', linewidth=1.5)
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=11, fontweight='bold')
ax2.set_ylabel('Number of Transactions', fontsize=11, fontweight='bold')
ax2.set_title('Transactions: Weekday vs Weekend', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

plt.suptitle('Weekend vs Weekday Sales Analysis', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{viz_dir}08_weekday_weekend.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 9. CUSTOMER LIFETIME VALUE DISTRIBUTION
# ============================================================================
viz_count += 1
print(f"   {viz_count}. CLV Distribution...")

plt.figure(figsize=(12, 7))
clv_segments = clv.groupby('RFM_Segment')['TotalRevenue'].mean().sort_values(ascending=False)
colors_clv = plt.cm.plasma(np.linspace(0, 1, len(clv_segments)))
bars = plt.barh(clv_segments.index, clv_segments.values, 
                color=colors_clv, edgecolor='black', linewidth=1.5)

# Add value labels
for bar in bars:
    width = bar.get_width()
    plt.text(width, bar.get_y() + bar.get_height()/2.,
             f'₹{width:,.0f}',
             ha='left', va='center', fontsize=10, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

plt.xlabel('Average Customer Lifetime Value (₹)', fontsize=12, fontweight='bold')
plt.ylabel('Customer Segment', fontsize=12, fontweight='bold')
plt.title('Average CLV by Customer Segment', fontsize=14, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{viz_dir}09_clv_by_segment.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 10. DISCOUNT ANALYSIS
# ============================================================================
viz_count += 1
print(f"   {viz_count}. Discount Impact Analysis...")

# Create discount brackets
transactions['DiscountBracket'] = pd.cut(transactions['DiscountPercent'], 
                                          bins=[0, 10, 20, 30, 50], 
                                          labels=['0-10%', '10-20%', '20-30%', '30-50%'])
discount_impact = transactions.groupby('DiscountBracket').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'count'
}).reset_index()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Revenue by discount bracket
colors_disc = [colors['success'], colors['primary'], colors['secondary'], colors['accent2']]
bars1 = ax1.bar(discount_impact['DiscountBracket'], discount_impact['TotalAmount']/1000000, 
                color=colors_disc, edgecolor='black', linewidth=1.5)
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'₹{height:.1f}M',
             ha='center', va='bottom', fontsize=10, fontweight='bold')
ax1.set_xlabel('Discount Range', fontsize=11, fontweight='bold')
ax1.set_ylabel('Revenue (Millions ₹)', fontsize=11, fontweight='bold')
ax1.set_title('Revenue by Discount Range', fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Transaction count by discount bracket
bars2 = ax2.bar(discount_impact['DiscountBracket'], discount_impact['TransactionID'], 
                color=colors_disc, edgecolor='black', linewidth=1.5)
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height):,}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')
ax2.set_xlabel('Discount Range', fontsize=11, fontweight='bold')
ax2.set_ylabel('Number of Transactions', fontsize=11, fontweight='bold')
ax2.set_title('Transactions by Discount Range', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

plt.suptitle('Discount Impact on Sales', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(f'{viz_dir}10_discount_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"\n✅ Generated {viz_count} visualizations")

# Generate insights summary
print("\n" + "=" * 70)
print("KEY BUSINESS INSIGHTS")
print("=" * 70)

insights = []

# Category insights
top_cat = category_perf.iloc[0]
insights.append(f"📊 {top_cat['Category']} is the top category with ₹{top_cat['Revenue']/1000000:.1f}M ({top_cat['RevenueShare']:.1f}% of total revenue)")

# Growth insight
first_month_rev = monthly_totals.iloc[0]['Revenue']
last_month_rev = monthly_totals.iloc[-1]['Revenue']
growth = ((last_month_rev - first_month_rev) / first_month_rev * 100)
insights.append(f"📈 Revenue grew {growth:+.1f}% from {monthly_totals.iloc[0]['Month']} to {monthly_totals.iloc[-1]['Month']}")

# Channel insight
top_channel = channel_perf.iloc[0]
insights.append(f"🌐 {top_channel['Channel']} leads with {top_channel['RevenueShare']:.1f}% of sales")

# Customer insight
top_segment = rfm['RFM_Segment'].value_counts().iloc[0]
insights.append(f"👥 {rfm['RFM_Segment'].value_counts().index[0]} is the largest segment with {top_segment:,} customers ({top_segment/len(rfm)*100:.1f}%)")

# CLV insight
avg_clv = clv['TotalRevenue'].mean()
champions_clv = clv[clv['RFM_Segment'] == 'Champions']['TotalRevenue'].mean()
insights.append(f"💰 Champions segment has {champions_clv/avg_clv:.1f}x higher CLV (₹{champions_clv:,.0f}) than average (₹{avg_clv:,.0f})")

# Store insight
top_store = store_perf.iloc[0]
insights.append(f"🏪 {top_store['Store']} is the top-performing store with ₹{top_store['Revenue']/1000000:.1f}M revenue")

# Weekend insight
weekend_rev = transactions[transactions['IsWeekend'] == 1]['TotalAmount'].sum()
weekday_rev = transactions[transactions['IsWeekend'] == 0]['TotalAmount'].sum()
weekend_pct = (weekend_rev / (weekend_rev + weekday_rev) * 100)
insights.append(f"📅 Weekend sales contribute {weekend_pct:.1f}% of total revenue")

# Brand insight
top_brand = brand_perf.iloc[0]
insights.append(f"🏆 {top_brand['Brand']} is the top brand with ₹{top_brand['Revenue']/1000000:.1f}M revenue")

# Margin insight
avg_margin_pct = (transactions['MarginAmount'].sum() / transactions['TotalAmount'].sum() * 100)
insights.append(f"💵 Average profit margin is {avg_margin_pct:.2f}%")

# Print insights
for i, insight in enumerate(insights, 1):
    print(f"\n{i}. {insight}")

# Save insights to file
with open(f'{viz_dir}insights.txt', 'w', encoding='utf-8') as f:
    f.write("KEY BUSINESS INSIGHTS\n")
    f.write("=" * 70 + "\n\n")
    for i, insight in enumerate(insights, 1):
        f.write(f"{i}. {insight}\n")

print(f"\n💾 Saved insights to {viz_dir}insights.txt")

print("\n" + "=" * 70)
print("✅ VISUALIZATION GENERATION COMPLETE!")
print("=" * 70)
print(f"\nGenerated {viz_count} professional visualizations:")
print("   1. Category Performance Bar Chart")
print("   2. Monthly Revenue Trend Line")
print("   3. Channel Distribution Pie Chart")
print("   4. Top 10 Stores Performance")
print("   5. Top 10 Brands Analysis")
print("   6. RFM Customer Segmentation")
print("   7. Transaction Value Distribution")
print("   8. Weekday vs Weekend Analysis")
print("   9. CLV by Customer Segment")
print("   10. Discount Impact Analysis")
