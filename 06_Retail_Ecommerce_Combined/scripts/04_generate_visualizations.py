"""
📊 PROFESSIONAL VISUALIZATION GENERATOR
========================================
Project 6: Crown Jewel Visualizations
18 High-Quality Charts @ 300 DPI
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

print("="*80)
print("📊 PROFESSIONAL VISUALIZATION GENERATOR - PROJECT 6")
print("="*80)

# Load data
print("\n📂 Loading datasets...")
kpis = pd.read_csv('../data/processed/kpis_overall.csv')
categories = pd.read_csv('../data/processed/category_performance.csv')
channels = pd.read_csv('../data/processed/channel_performance.csv')
daily_trends = pd.read_csv('../data/processed/daily_trends.csv')
monthly_trends = pd.read_csv('../data/processed/monthly_trends.csv')
rfm_summary = pd.read_csv('../data/processed/rfm_segment_summary.csv')
regional = pd.read_csv('../data/processed/regional_performance.csv')
stores = pd.read_csv('../data/processed/store_performance.csv')
payment = pd.read_csv('../data/processed/payment_method_analysis.csv')
forecast = pd.read_csv('../data/ml_results/sales_forecast_30days.csv')
ml_summary = pd.read_csv('../data/ml_results/ml_models_summary.csv')
hourly = pd.read_csv('../data/processed/hourly_sales_pattern.csv')

daily_trends['date'] = pd.to_datetime(daily_trends['date'])
forecast['date'] = pd.to_datetime(forecast['date'])

print("✅ All datasets loaded\n")

# Color palette
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']

# ========== VIZ 1: REVENUE OVERVIEW ==========
print("📊 1/18: Revenue Overview Dashboard...")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('💰 REVENUE OVERVIEW DASHBOARD', fontsize=20, fontweight='bold', y=0.98)

# Total revenue by category
categories_sorted = categories.sort_values('total_revenue', ascending=True)
ax1.barh(categories_sorted['category'], categories_sorted['total_revenue']/10000000, color=colors)
ax1.set_xlabel('Revenue (₹ Crore)', fontsize=12, fontweight='bold')
ax1.set_title('Revenue by Category', fontsize=14, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Channel distribution
ax2.pie(channels['total_revenue'], labels=channels['channel'], autopct='%1.1f%%', 
        colors=colors, startangle=90, textprops={'fontsize': 11})
ax2.set_title('Revenue Share by Channel', fontsize=14, fontweight='bold')

# Regional performance
regional_sorted = regional.sort_values('total_revenue', ascending=False)
ax3.bar(regional_sorted['region'], regional_sorted['total_revenue']/10000000, color=colors)
ax3.set_xlabel('Region', fontsize=12, fontweight='bold')
ax3.set_ylabel('Revenue (₹ Crore)', fontsize=12, fontweight='bold')
ax3.set_title('Regional Revenue Distribution', fontsize=14, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)

# Payment methods
payment_sorted = payment.sort_values('total_revenue', ascending=True)
ax4.barh(payment_sorted['payment_method'], payment_sorted['total_revenue']/10000000, color=colors)
ax4.set_xlabel('Revenue (₹ Crore)', fontsize=12, fontweight='bold')
ax4.set_title('Revenue by Payment Method', fontsize=14, fontweight='bold')
ax4.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('../visualizations/01_revenue_overview.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 01_revenue_overview.png")
plt.close()

# ========== VIZ 2: DAILY REVENUE TREND ==========
print("📊 2/18: Daily Revenue Trend...")
plt.figure(figsize=(16, 8))
plt.plot(daily_trends['date'], daily_trends['revenue']/100000, linewidth=2, color='#4ECDC4', alpha=0.8)
plt.fill_between(daily_trends['date'], daily_trends['revenue']/100000, alpha=0.2, color='#4ECDC4')
plt.xlabel('Date', fontsize=14, fontweight='bold')
plt.ylabel('Revenue (₹ Lakh)', fontsize=14, fontweight='bold')
plt.title('📈 DAILY REVENUE TREND (3 Years)', fontsize=18, fontweight='bold', pad=20)
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../visualizations/02_daily_revenue_trend.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 02_daily_revenue_trend.png")
plt.close()

# ========== VIZ 3: MONTHLY TRENDS ==========
print("📊 3/18: Monthly Trends...")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10))

ax1.plot(monthly_trends['year_month'], monthly_trends['revenue']/10000000, 
         marker='o', linewidth=2.5, color='#FF6B6B', markersize=6, label='Revenue')
ax1.fill_between(monthly_trends['year_month'], monthly_trends['revenue']/10000000, alpha=0.2, color='#FF6B6B')
ax1.set_ylabel('Revenue (₹ Crore)', fontsize=12, fontweight='bold')
ax1.set_title('📅 MONTHLY REVENUE TREND', fontsize=16, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(alpha=0.3)
ax1.tick_params(axis='x', rotation=90)

ax2.plot(monthly_trends['year_month'], monthly_trends['transactions']/1000, 
         marker='s', linewidth=2.5, color='#45B7D1', markersize=6, label='Transactions (K)')
ax2.fill_between(monthly_trends['year_month'], monthly_trends['transactions']/1000, alpha=0.2, color='#45B7D1')
ax2.set_xlabel('Month', fontsize=12, fontweight='bold')
ax2.set_ylabel('Transactions (Thousands)', fontsize=12, fontweight='bold')
ax2.set_title('📅 MONTHLY TRANSACTION VOLUME', fontsize=16, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(alpha=0.3)
ax2.tick_params(axis='x', rotation=90)

plt.tight_layout()
plt.savefig('../visualizations/03_monthly_trends.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 03_monthly_trends.png")
plt.close()

# ========== VIZ 4: CATEGORY PERFORMANCE ==========
print("📊 4/18: Category Deep Dive...")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('📦 CATEGORY PERFORMANCE ANALYSIS', fontsize=20, fontweight='bold', y=0.98)

# Revenue
categories_sorted = categories.sort_values('total_revenue', ascending=True)
ax1.barh(categories_sorted['category'], categories_sorted['total_revenue']/10000000, color=colors[0])
ax1.set_xlabel('Total Revenue (₹ Cr)', fontsize=11, fontweight='bold')
ax1.set_title('Revenue by Category', fontsize=13, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Profit margin
categories_sorted_margin = categories.sort_values('avg_margin', ascending=True)
ax2.barh(categories_sorted_margin['category'], categories_sorted_margin['avg_margin'], color=colors[1])
ax2.set_xlabel('Average Margin (%)', fontsize=11, fontweight='bold')
ax2.set_title('Profit Margin by Category', fontsize=13, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

# Units sold
categories_sorted_units = categories.sort_values('units_sold', ascending=True)
ax3.barh(categories_sorted_units['category'], categories_sorted_units['units_sold']/1000, color=colors[2])
ax3.set_xlabel('Units Sold (Thousands)', fontsize=11, fontweight='bold')
ax3.set_title('Volume by Category', fontsize=13, fontweight='bold')
ax3.grid(axis='x', alpha=0.3)

# Transaction count
categories_sorted_txn = categories.sort_values('transactions', ascending=True)
ax4.barh(categories_sorted_txn['category'], categories_sorted_txn['transactions']/1000, color=colors[3])
ax4.set_xlabel('Transactions (Thousands)', fontsize=11, fontweight='bold')
ax4.set_title('Transaction Count by Category', fontsize=13, fontweight='bold')
ax4.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('../visualizations/04_category_performance.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 04_category_performance.png")
plt.close()

# ========== VIZ 5: CHANNEL ANALYSIS ==========
print("📊 5/18: Channel Analysis...")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('📱 SALES CHANNEL ANALYSIS', fontsize=20, fontweight='bold', y=0.98)

# Revenue pie
ax1.pie(channels['total_revenue'], labels=channels['channel'], autopct='%1.1f%%', 
        colors=colors, startangle=90, textprops={'fontsize': 11})
ax1.set_title('Revenue Distribution', fontsize=14, fontweight='bold')

# Transaction count
ax2.bar(channels['channel'], channels['transactions']/1000, color=colors)
ax2.set_ylabel('Transactions (Thousands)', fontsize=11, fontweight='bold')
ax2.set_title('Transaction Volume by Channel', fontsize=14, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)
ax2.tick_params(axis='x', rotation=15)

# Average order value
ax3.bar(channels['channel'], channels['avg_order_value'], color=colors)
ax3.set_ylabel('Average Order Value (₹)', fontsize=11, fontweight='bold')
ax3.set_title('AOV by Channel', fontsize=14, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)
ax3.tick_params(axis='x', rotation=15)

# Unique customers
ax4.bar(channels['channel'], channels['unique_customers']/1000, color=colors)
ax4.set_ylabel('Unique Customers (Thousands)', fontsize=11, fontweight='bold')
ax4.set_title('Customer Reach by Channel', fontsize=14, fontweight='bold')
ax4.grid(axis='y', alpha=0.3)
ax4.tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig('../visualizations/05_channel_analysis.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 05_channel_analysis.png")
plt.close()

# ========== VIZ 6: RFM SEGMENTATION ==========
print("📊 6/18: RFM Customer Segmentation...")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('👥 RFM CUSTOMER SEGMENTATION', fontsize=20, fontweight='bold', y=0.98)

# Customer count by segment
rfm_sorted = rfm_summary.sort_values('customer_count', ascending=True)
ax1.barh(rfm_sorted['segment'], rfm_sorted['customer_count'], color=colors[0])
ax1.set_xlabel('Customer Count', fontsize=11, fontweight='bold')
ax1.set_title('Customer Distribution', fontsize=14, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)

# Revenue by segment
rfm_sorted_rev = rfm_summary.sort_values('total_revenue', ascending=True)
ax2.barh(rfm_sorted_rev['segment'], rfm_sorted_rev['total_revenue']/10000000, color=colors[1])
ax2.set_xlabel('Total Revenue (₹ Cr)', fontsize=11, fontweight='bold')
ax2.set_title('Revenue by Segment', fontsize=14, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

# Avg revenue per customer
rfm_sorted_avg = rfm_summary.sort_values('avg_revenue', ascending=True)
ax3.barh(rfm_sorted_avg['segment'], rfm_sorted_avg['avg_revenue']/1000, color=colors[2])
ax3.set_xlabel('Avg Revenue per Customer (₹ K)', fontsize=11, fontweight='bold')
ax3.set_title('Average Customer Value', fontsize=14, fontweight='bold')
ax3.grid(axis='x', alpha=0.3)

# Pie chart
ax4.pie(rfm_summary['total_revenue'], labels=rfm_summary['segment'], autopct='%1.1f%%', 
        colors=colors, startangle=90, textprops={'fontsize': 10})
ax4.set_title('Revenue Share by Segment', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('../visualizations/06_rfm_segmentation.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 06_rfm_segmentation.png")
plt.close()

# ========== VIZ 7: REGIONAL PERFORMANCE ==========
print("📊 7/18: Regional Performance...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('🌍 REGIONAL PERFORMANCE', fontsize=20, fontweight='bold')

# Revenue bar chart
regional_sorted = regional.sort_values('total_revenue', ascending=False)
ax1.bar(regional_sorted['region'], regional_sorted['total_revenue']/10000000, color=colors)
ax1.set_ylabel('Revenue (₹ Crore)', fontsize=12, fontweight='bold')
ax1.set_title('Revenue by Region', fontsize=15, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

# Transaction count
ax2.bar(regional_sorted['region'], regional_sorted['transactions']/1000, color=colors[::-1])
ax2.set_ylabel('Transactions (Thousands)', fontsize=12, fontweight='bold')
ax2.set_title('Transaction Volume by Region', fontsize=15, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('../visualizations/07_regional_performance.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 07_regional_performance.png")
plt.close()

# ========== VIZ 8: TOP STORES ==========
print("📊 8/18: Top 10 Stores...")
plt.figure(figsize=(14, 8))
top_stores = stores.sort_values('total_revenue', ascending=False).head(10)
plt.barh(top_stores['location'], top_stores['total_revenue']/10000000, color=colors[4])
plt.xlabel('Revenue (₹ Crore)', fontsize=12, fontweight='bold')
plt.title('🏪 TOP 10 STORES BY REVENUE', fontsize=18, fontweight='bold', pad=20)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('../visualizations/08_top_stores.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 08_top_stores.png")
plt.close()

# ========== VIZ 9: HOURLY PATTERN ==========
print("📊 9/18: Hourly Sales Pattern...")
plt.figure(figsize=(16, 7))
plt.plot(hourly['hour'], hourly['total_revenue']/100000, marker='o', linewidth=3, 
         markersize=8, color='#FF6B6B')
plt.fill_between(hourly['hour'], hourly['total_revenue']/100000, alpha=0.3, color='#FF6B6B')
plt.xlabel('Hour of Day', fontsize=13, fontweight='bold')
plt.ylabel('Revenue (₹ Lakh)', fontsize=13, fontweight='bold')
plt.title('⏰ HOURLY SALES PATTERN', fontsize=18, fontweight='bold', pad=20)
plt.xticks(range(8, 23))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('../visualizations/09_hourly_pattern.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 09_hourly_pattern.png")
plt.close()

# ========== VIZ 10: SALES FORECAST ==========
print("📊 10/18: Sales Forecast with Historical...")
plt.figure(figsize=(16, 8))

# Last 90 days of actual
last_90 = daily_trends.tail(90)
plt.plot(last_90['date'], last_90['revenue']/100000, linewidth=2.5, 
         color='#4ECDC4', label='Actual Revenue', alpha=0.9)

# Forecast
plt.plot(forecast['date'], forecast['predicted_revenue']/100000, linewidth=2.5, 
         color='#FF6B6B', linestyle='--', label='Forecasted Revenue', alpha=0.9)
plt.fill_between(forecast['date'], forecast['lower_bound']/100000, 
                 forecast['upper_bound']/100000, alpha=0.2, color='#FF6B6B', label='Confidence Interval')

plt.xlabel('Date', fontsize=13, fontweight='bold')
plt.ylabel('Revenue (₹ Lakh)', fontsize=13, fontweight='bold')
plt.title('🔮 SALES FORECAST (Next 30 Days)', fontsize=18, fontweight='bold', pad=20)
plt.legend(fontsize=12, loc='upper left')
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../visualizations/10_sales_forecast.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 10_sales_forecast.png")
plt.close()

# ========== VIZ 11: ML MODEL PERFORMANCE ==========
print("📊 11/18: ML Model Performance...")
plt.figure(figsize=(14, 8))

model_names = ml_summary['model_name'].str.split('(').str[0].str.strip()
metric_values = ml_summary['metric_value'].astype(float)

bars = plt.barh(model_names, metric_values, color=colors[:4])
plt.xlabel('Performance Score', fontsize=12, fontweight='bold')
plt.title('🤖 ML MODEL PERFORMANCE SUMMARY', fontsize=18, fontweight='bold', pad=20)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, metric_values)):
    if val > 1:
        label = f'{val:,.0f}'
    else:
        label = f'{val:.4f}'
    plt.text(val + 0.01, i, label, va='center', fontsize=11, fontweight='bold')

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('../visualizations/11_ml_performance.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 11_ml_performance.png")
plt.close()

# ========== VIZ 12: PAYMENT METHODS ==========
print("📊 12/18: Payment Method Distribution...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('💳 PAYMENT METHOD ANALYSIS', fontsize=20, fontweight='bold')

# Pie chart
ax1.pie(payment['total_revenue'], labels=payment['payment_method'], autopct='%1.1f%%',
        colors=colors, startangle=90, textprops={'fontsize': 12})
ax1.set_title('Revenue Share', fontsize=15, fontweight='bold')

# Bar chart
payment_sorted = payment.sort_values('transactions', ascending=True)
ax2.barh(payment_sorted['payment_method'], payment_sorted['transactions']/1000, color=colors)
ax2.set_xlabel('Transactions (Thousands)', fontsize=12, fontweight='bold')
ax2.set_title('Transaction Count', fontsize=15, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('../visualizations/12_payment_methods.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 12_payment_methods.png")
plt.close()

# ========== VIZ 13-18: Additional Charts ==========
print("📊 13/18: Revenue & Profit Comparison...")
fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(categories))
width = 0.35
ax.bar(x - width/2, categories['total_revenue']/10000000, width, label='Revenue', color=colors[0])
ax.bar(x + width/2, categories['total_profit']/10000000, width, label='Profit', color=colors[1])
ax.set_xlabel('Category', fontsize=12, fontweight='bold')
ax.set_ylabel('Amount (₹ Crore)', fontsize=12, fontweight='bold')
ax.set_title('💰 REVENUE vs PROFIT BY CATEGORY', fontsize=18, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(categories['category'], rotation=45, ha='right')
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('../visualizations/13_revenue_profit_comparison.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 13_revenue_profit_comparison.png")
plt.close()

print("📊 14/18: Transaction Velocity...")
plt.figure(figsize=(16, 7))
plt.plot(daily_trends['date'], daily_trends['transactions'], linewidth=2, color='#45B7D1', alpha=0.8)
plt.fill_between(daily_trends['date'], daily_trends['transactions'], alpha=0.2, color='#45B7D1')
plt.xlabel('Date', fontsize=13, fontweight='bold')
plt.ylabel('Transaction Count', fontsize=13, fontweight='bold')
plt.title('🚀 DAILY TRANSACTION VELOCITY', fontsize=18, fontweight='bold', pad=20)
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../visualizations/14_transaction_velocity.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 14_transaction_velocity.png")
plt.close()

print("📊 15/18: Customer Acquisition by Month...")
plt.figure(figsize=(16, 7))
plt.bar(monthly_trends['year_month'], monthly_trends['customers'], color=colors[2])
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Unique Customers', fontsize=12, fontweight='bold')
plt.title('👥 CUSTOMER ENGAGEMENT BY MONTH', fontsize=18, fontweight='bold', pad=20)
plt.xticks(rotation=90)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('../visualizations/15_customer_acquisition.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 15_customer_acquisition.png")
plt.close()

print("📊 16/18: Category Market Share...")
plt.figure(figsize=(12, 12))
plt.pie(categories['total_revenue'], labels=categories['category'], autopct='%1.1f%%',
        colors=colors, startangle=90, textprops={'fontsize': 13})
plt.title('📦 CATEGORY MARKET SHARE', fontsize=20, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('../visualizations/16_category_market_share.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 16_category_market_share.png")
plt.close()

print("📊 17/18: Average Order Value Trend...")
monthly_trends['aov'] = monthly_trends['revenue'] / monthly_trends['transactions']
plt.figure(figsize=(16, 7))
plt.plot(monthly_trends['year_month'], monthly_trends['aov'], marker='o', 
         linewidth=2.5, markersize=6, color='#FFA07A')
plt.fill_between(monthly_trends['year_month'], monthly_trends['aov'], alpha=0.2, color='#FFA07A')
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Average Order Value (₹)', fontsize=12, fontweight='bold')
plt.title('💵 AVERAGE ORDER VALUE TREND', fontsize=18, fontweight='bold', pad=20)
plt.xticks(rotation=90)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('../visualizations/17_aov_trend.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 17_aov_trend.png")
plt.close()

print("📊 18/18: Complete Business Metrics KPI Panel...")
fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
fig.suptitle('📊 COMPLETE BUSINESS METRICS DASHBOARD', fontsize=22, fontweight='bold', y=0.98)

# KPI boxes
kpi_data = [
    ('Total Revenue', f"₹{kpis[kpis['metric']=='Total Revenue']['value'].iloc[0]}", '#FF6B6B'),
    ('Total Profit', f"₹{kpis[kpis['metric']=='Total Profit']['value'].iloc[0]}", '#4ECDC4'),
    ('Transactions', kpis[kpis['metric']=='Total Transactions']['value'].iloc[0], '#45B7D1'),
    ('Customers', kpis[kpis['metric']=='Unique Customers']['value'].iloc[0], '#FFA07A'),
    ('Avg Order Value', kpis[kpis['metric']=='Average Order Value']['value'].iloc[0], '#98D8C8'),
    ('Profit Margin', kpis[kpis['metric']=='Average Profit Margin']['value'].iloc[0], '#F7DC6F'),
    ('Revenue/Customer', kpis[kpis['metric']=='Revenue per Customer']['value'].iloc[0], '#BB8FCE'),
    ('Repeat Rate', kpis[kpis['metric']=='Repeat Customer Rate']['value'].iloc[0], '#85C1E2'),
    ('Avg Discount', kpis[kpis['metric']=='Average Discount']['value'].iloc[0], '#F8B400')
]

positions = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

for (row, col), (title, value, color) in zip(positions, kpi_data):
    ax = fig.add_subplot(gs[row, col])
    ax.text(0.5, 0.6, value, ha='center', va='center', fontsize=28, fontweight='bold', color='white')
    ax.text(0.5, 0.2, title, ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(color)
    ax.axis('off')

plt.savefig('../visualizations/18_kpi_dashboard.png', bbox_inches='tight', dpi=300)
print("  ✅ Saved: 18_kpi_dashboard.png")
plt.close()

print("\n" + "="*80)
print("✨ ALL VISUALIZATIONS COMPLETE!")
print("="*80)
print("\n📊 Generated 18 High-Quality Charts:")
viz_list = [
    '01_revenue_overview.png',
    '02_daily_revenue_trend.png',
    '03_monthly_trends.png',
    '04_category_performance.png',
    '05_channel_analysis.png',
    '06_rfm_segmentation.png',
    '07_regional_performance.png',
    '08_top_stores.png',
    '09_hourly_pattern.png',
    '10_sales_forecast.png',
    '11_ml_performance.png',
    '12_payment_methods.png',
    '13_revenue_profit_comparison.png',
    '14_transaction_velocity.png',
    '15_customer_acquisition.png',
    '16_category_market_share.png',
    '17_aov_trend.png',
    '18_kpi_dashboard.png'
]

for i, viz in enumerate(viz_list, 1):
    print(f"  {i}. {viz}")

print("\n📁 All visualizations saved in: ../visualizations/")
print("🎯 Resolution: 300 DPI (Print Quality)")
print("\n🏆 Crown Jewel Visualization Pipeline - COMPLETE!")
