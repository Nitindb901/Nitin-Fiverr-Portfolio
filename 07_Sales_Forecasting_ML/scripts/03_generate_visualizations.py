"""
Project 7: Sales Forecasting ML - Generate High-Quality Visualizations
========================================================================
This script generates 15+ professional charts @ 300 DPI for analysis

Author: Nitin Dubey
Date: November 2025
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Color palette
COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
          '#F7DC6F', '#BB8FCE', '#85C1E2']

# Create output directory
os.makedirs('visualizations', exist_ok=True)

print("🎨 GENERATING VISUALIZATIONS")
print("="*70)
print("📊 Creating 15+ high-quality charts @ 300 DPI")
print("="*70 + "\n")

# ============================================================================
# LOAD DATA
# ============================================================================

print("📂 Loading data...")
transactions = pd.read_csv('data/raw/transactions.csv')
transactions['date'] = pd.to_datetime(transactions['date'])
daily_revenue = pd.read_csv('data/processed/daily_revenue.csv')
daily_revenue['date'] = pd.to_datetime(daily_revenue['date'])
model_comparison = pd.read_csv('data/forecasts/model_comparison.csv')
forecast_90 = pd.read_csv('data/forecasts/forecast_90day.csv')
forecast_90['date'] = pd.to_datetime(forecast_90['date'])

print(f"   ✅ Loaded {len(transactions):,} transactions")
print(f"   ✅ Loaded {len(daily_revenue):,} daily records")
print(f"   ✅ Loaded {len(model_comparison)} models")
print(f"   ✅ Loaded {len(forecast_90)} forecast days\n")

# ============================================================================
# CHART 1: Revenue Trend (5 Years)
# ============================================================================

print("📊 Chart 1: Revenue Trend (5 Years)...")
fig, ax = plt.subplots(figsize=(14, 8))

monthly_revenue = transactions.groupby(pd.Grouper(key='date', freq='M'))['final_revenue'].sum()
ax.plot(monthly_revenue.index, monthly_revenue.values / 1e7, linewidth=2.5, 
        color=COLORS[0], marker='o', markersize=4)

ax.set_title('Monthly Revenue Trend (2020-2025)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Revenue (Crores ₹)', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('visualizations/01_revenue_trend.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 01_revenue_trend.png\n")

# ============================================================================
# CHART 2: Category Performance
# ============================================================================

print("📊 Chart 2: Category Performance...")
fig, ax = plt.subplots(figsize=(12, 8))

category_revenue = transactions.groupby('category')['final_revenue'].sum().sort_values(ascending=True)
bars = ax.barh(category_revenue.index, category_revenue.values / 1e7, color=COLORS[:len(category_revenue)])

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width + 5, bar.get_y() + bar.get_height()/2, 
            f'₹{width:.1f} Cr', ha='left', va='center', fontsize=10, fontweight='bold')

ax.set_title('Revenue by Category', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Revenue (Crores ₹)', fontsize=12, fontweight='bold')
ax.set_ylabel('Category', fontsize=12, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('visualizations/02_category_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 02_category_performance.png\n")

# ============================================================================
# CHART 3: Regional Performance
# ============================================================================

print("📊 Chart 3: Regional Performance...")
fig, ax = plt.subplots(figsize=(12, 8))

regional_revenue = transactions.groupby('region')['final_revenue'].sum().sort_values(ascending=False)
bars = ax.bar(regional_revenue.index, regional_revenue.values / 1e7, color=COLORS[:len(regional_revenue)])

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 5,
            f'₹{height:.1f} Cr', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_title('Revenue by Region', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Region', fontsize=12, fontweight='bold')
ax.set_ylabel('Revenue (Crores ₹)', fontsize=12, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('visualizations/03_regional_performance.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 03_regional_performance.png\n")

# ============================================================================
# CHART 4: Store Ranking
# ============================================================================

print("📊 Chart 4: Store Ranking (Top 25)...")
fig, ax = plt.subplots(figsize=(14, 10))

store_revenue = transactions.groupby('store_name')['final_revenue'].sum().sort_values(ascending=True)
bars = ax.barh(range(len(store_revenue)), store_revenue.values / 1e7, color=COLORS[1])

ax.set_yticks(range(len(store_revenue)))
ax.set_yticklabels(store_revenue.index, fontsize=8)
ax.set_title('Store Performance Ranking', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Revenue (Crores ₹)', fontsize=12, fontweight='bold')
ax.set_ylabel('Store', fontsize=12, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('visualizations/04_store_ranking.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 04_store_ranking.png\n")

# ============================================================================
# CHART 5: Channel Evolution
# ============================================================================

print("📊 Chart 5: Channel Evolution...")
fig, ax = plt.subplots(figsize=(14, 8))

channel_yearly = transactions.groupby(['year', 'channel'])['final_revenue'].sum().unstack()
channel_yearly.plot(kind='bar', stacked=True, ax=ax, color=COLORS[:len(channel_yearly.columns)])

ax.set_title('Channel Mix Evolution (2020-2025)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Revenue (₹)', fontsize=12, fontweight='bold')
ax.legend(title='Channel', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig('visualizations/05_channel_evolution.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 05_channel_evolution.png\n")

# ============================================================================
# CHART 6: Seasonal Patterns
# ============================================================================

print("📊 Chart 6: Seasonal Patterns (Monthly Heatmap)...")
fig, ax = plt.subplots(figsize=(14, 8))

transactions['year_str'] = transactions['year'].astype(str)
monthly_pivot = transactions.groupby(['year_str', 'month'])['final_revenue'].sum().unstack()
monthly_pivot = monthly_pivot / 1e7  # Convert to Crores

sns.heatmap(monthly_pivot, annot=True, fmt='.1f', cmap='YlOrRd', 
            cbar_kws={'label': 'Revenue (Crores ₹)'}, ax=ax)

ax.set_title('Monthly Revenue Patterns (Crores ₹)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Month', fontsize=12, fontweight='bold')
ax.set_ylabel('Year', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/06_seasonal_patterns.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 06_seasonal_patterns.png\n")

# ============================================================================
# CHART 7: Day of Week Analysis
# ============================================================================

print("📊 Chart 7: Day of Week Analysis...")
fig, ax = plt.subplots(figsize=(12, 8))

day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_avg = transactions.groupby('day_of_week')['final_revenue'].mean()
bars = ax.bar(day_names, daily_avg.values, color=COLORS[3])

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 5000,
            f'₹{height:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_title('Average Daily Revenue by Day of Week', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Day', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Revenue (₹)', fontsize=12, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('visualizations/07_day_of_week.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 07_day_of_week.png\n")

# ============================================================================
# CHART 8: Model Comparison
# ============================================================================

print("📊 Chart 8: Model Comparison...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# MAPE comparison
successful_models = model_comparison[model_comparison['Status'] == 'Success']
bars1 = ax1.bar(successful_models['Model'], successful_models['MAPE'], color=COLORS[4])

for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height + 0.5,
             f'{height:.2f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax1.set_title('Model Accuracy (MAPE - Lower is Better)', fontsize=14, fontweight='bold')
ax1.set_ylabel('MAPE (%)', fontsize=11, fontweight='bold')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# R² comparison
bars2 = ax2.bar(successful_models['Model'], successful_models['R2'], color=COLORS[5])

for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height + 0.02,
             f'{height:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax2.set_title('Model Fit (R² - Higher is Better)', fontsize=14, fontweight='bold')
ax2.set_ylabel('R² Score', fontsize=11, fontweight='bold')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.suptitle('ML Model Performance Comparison', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('visualizations/08_model_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 08_model_comparison.png\n")

# ============================================================================
# CHART 9: Forecast Visualization
# ============================================================================

print("📊 Chart 9: 90-Day Forecast...")
fig, ax = plt.subplots(figsize=(14, 8))

# Historical (last 180 days)
historical = daily_revenue.tail(180)
ax.plot(historical['date'], historical['revenue'] / 1e7, 
        linewidth=2, color=COLORS[0], label='Historical', marker='o', markersize=3)

# Forecasts
if 'arima_forecast' in forecast_90.columns:
    ax.plot(forecast_90['date'], forecast_90['arima_forecast'] / 1e7,
            linewidth=2, color=COLORS[1], label='ARIMA', linestyle='--', alpha=0.7)

if 'prophet_forecast' in forecast_90.columns:
    ax.plot(forecast_90['date'], forecast_90['prophet_forecast'] / 1e7,
            linewidth=2, color=COLORS[2], label='Prophet', linestyle='--', alpha=0.7)

if 'xgboost_forecast' in forecast_90.columns:
    ax.plot(forecast_90['date'], forecast_90['xgboost_forecast'] / 1e7,
            linewidth=2, color=COLORS[3], label='XGBoost', linestyle='--', alpha=0.7)

if 'ensemble_forecast' in forecast_90.columns:
    ax.plot(forecast_90['date'], forecast_90['ensemble_forecast'] / 1e7,
            linewidth=3, color=COLORS[6], label='Ensemble', linestyle='-', alpha=0.9)

ax.axvline(x=daily_revenue['date'].max(), color='red', linestyle=':', linewidth=2, alpha=0.5)
ax.text(daily_revenue['date'].max(), ax.get_ylim()[1] * 0.9, 'Forecast Start', 
        rotation=90, va='top', ha='right', fontsize=10)

ax.set_title('90-Day Sales Forecast (Multiple Models)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Daily Revenue (Crores ₹)', fontsize=12, fontweight='bold')
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('visualizations/09_forecast_90day.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 09_forecast_90day.png\n")

# ============================================================================
# CHART 10: Revenue Distribution
# ============================================================================

print("📊 Chart 10: Revenue Distribution...")
fig, ax = plt.subplots(figsize=(12, 8))

ax.hist(daily_revenue['revenue'] / 1e6, bins=50, color=COLORS[4], edgecolor='black', alpha=0.7)

ax.axvline(daily_revenue['revenue'].mean() / 1e6, color='red', linestyle='--', 
           linewidth=2, label=f"Mean: ₹{daily_revenue['revenue'].mean() / 1e6:.2f}M")
ax.axvline(daily_revenue['revenue'].median() / 1e6, color='green', linestyle='--', 
           linewidth=2, label=f"Median: ₹{daily_revenue['revenue'].median() / 1e6:.2f}M")

ax.set_title('Daily Revenue Distribution', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Daily Revenue (Millions ₹)', fontsize=12, fontweight='bold')
ax.set_ylabel('Frequency (Days)', fontsize=12, fontweight='bold')
ax.legend(fontsize=11)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('visualizations/10_revenue_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 10_revenue_distribution.png\n")

# ============================================================================
# CHART 11: Customer Segment Analysis
# ============================================================================

print("📊 Chart 11: Customer Segment Analysis...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Revenue by segment
segment_revenue = transactions.groupby('customer_segment')['final_revenue'].sum().sort_values(ascending=False)
segment_revenue_pct = (segment_revenue / segment_revenue.sum() * 100)

colors_segment = [COLORS[i % len(COLORS)] for i in range(len(segment_revenue))]
wedges, texts, autotexts = ax1.pie(segment_revenue, labels=segment_revenue.index, autopct='%1.1f%%',
                                     colors=colors_segment, startangle=90)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax1.set_title('Revenue by Customer Segment', fontsize=14, fontweight='bold')

# Transaction count by segment
segment_count = transactions.groupby('customer_segment').size().sort_values(ascending=True)
bars = ax2.barh(segment_count.index, segment_count.values, color=colors_segment)

for i, bar in enumerate(bars):
    width = bar.get_width()
    ax2.text(width + 500, bar.get_y() + bar.get_height()/2,
             f'{width:,}', ha='left', va='center', fontsize=10, fontweight='bold')

ax2.set_title('Transactions by Customer Segment', fontsize=14, fontweight='bold')
ax2.set_xlabel('Transaction Count', fontsize=11, fontweight='bold')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.suptitle('Customer Segment Performance', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('visualizations/11_customer_segments.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 11_customer_segments.png\n")

# ============================================================================
# CHART 12: Profit Margins
# ============================================================================

print("📊 Chart 12: Profit Margins by Category...")
fig, ax = plt.subplots(figsize=(12, 8))

category_margin = transactions.groupby('category').agg({
    'final_revenue': 'sum',
    'profit': 'sum'
}).reset_index()
category_margin['margin_pct'] = (category_margin['profit'] / category_margin['final_revenue'] * 100)
category_margin = category_margin.sort_values('margin_pct', ascending=True)

bars = ax.barh(category_margin['category'], category_margin['margin_pct'], color=COLORS[7])

for i, bar in enumerate(bars):
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
            f'{width:.1f}%', ha='left', va='center', fontsize=10, fontweight='bold')

ax.set_title('Profit Margin by Category', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Margin (%)', fontsize=12, fontweight='bold')
ax.set_ylabel('Category', fontsize=12, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('visualizations/12_profit_margins.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 12_profit_margins.png\n")

# ============================================================================
# CHART 13: YoY Growth
# ============================================================================

print("📊 Chart 13: Year-over-Year Growth...")
fig, ax = plt.subplots(figsize=(12, 8))

yearly_revenue = transactions.groupby('year')['final_revenue'].sum()
yoy_growth = yearly_revenue.pct_change() * 100

bars = ax.bar(yoy_growth.index[1:], yoy_growth.values[1:], color=COLORS[2])

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_title('Year-over-Year Revenue Growth', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Growth Rate (%)', fontsize=12, fontweight='bold')
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('visualizations/13_yoy_growth.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 13_yoy_growth.png\n")

# ============================================================================
# CHART 14: Discount Impact
# ============================================================================

print("📊 Chart 14: Discount Impact Analysis...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Discount distribution
discount_bins = [0, 5, 10, 15, 20, 25, 30]
transactions['discount_bin'] = pd.cut(transactions['discount_percent'], bins=discount_bins)
discount_dist = transactions.groupby('discount_bin')['final_revenue'].sum() / 1e7

bars1 = ax1.bar(range(len(discount_dist)), discount_dist.values, color=COLORS[0])
ax1.set_xticks(range(len(discount_dist)))
ax1.set_xticklabels([f'{int(b.left)}-{int(b.right)}%' for b in discount_dist.index], rotation=45)
ax1.set_title('Revenue by Discount Range', fontsize=14, fontweight='bold')
ax1.set_xlabel('Discount Range', fontsize=11, fontweight='bold')
ax1.set_ylabel('Revenue (Crores ₹)', fontsize=11, fontweight='bold')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Transaction count by discount
discount_count = transactions.groupby('discount_bin').size()
bars2 = ax2.bar(range(len(discount_count)), discount_count.values, color=COLORS[1])
ax2.set_xticks(range(len(discount_count)))
ax2.set_xticklabels([f'{int(b.left)}-{int(b.right)}%' for b in discount_count.index], rotation=45)
ax2.set_title('Transaction Count by Discount Range', fontsize=14, fontweight='bold')
ax2.set_xlabel('Discount Range', fontsize=11, fontweight='bold')
ax2.set_ylabel('Transaction Count', fontsize=11, fontweight='bold')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.suptitle('Discount Strategy Analysis', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('visualizations/14_discount_impact.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 14_discount_impact.png\n")

# ============================================================================
# CHART 15: KPI Summary Dashboard
# ============================================================================

print("📊 Chart 15: KPI Summary Dashboard...")
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Total Revenue
ax1 = fig.add_subplot(gs[0, 0])
total_revenue = transactions['final_revenue'].sum() / 1e7
ax1.text(0.5, 0.5, f'₹{total_revenue:.1f} Cr', ha='center', va='center', 
         fontsize=24, fontweight='bold', color=COLORS[0])
ax1.text(0.5, 0.2, 'Total Revenue', ha='center', va='center', fontsize=14)
ax1.axis('off')

# Total Profit
ax2 = fig.add_subplot(gs[0, 1])
total_profit = transactions['profit'].sum() / 1e7
ax2.text(0.5, 0.5, f'₹{total_profit:.1f} Cr', ha='center', va='center',
         fontsize=24, fontweight='bold', color=COLORS[1])
ax2.text(0.5, 0.2, 'Total Profit', ha='center', va='center', fontsize=14)
ax2.axis('off')

# Avg Margin
ax3 = fig.add_subplot(gs[0, 2])
avg_margin = (transactions['profit'].sum() / transactions['final_revenue'].sum() * 100)
ax3.text(0.5, 0.5, f'{avg_margin:.1f}%', ha='center', va='center',
         fontsize=24, fontweight='bold', color=COLORS[2])
ax3.text(0.5, 0.2, 'Average Margin', ha='center', va='center', fontsize=14)
ax3.axis('off')

# Transaction Count
ax4 = fig.add_subplot(gs[1, 0])
total_txns = len(transactions)
ax4.text(0.5, 0.5, f'{total_txns:,}', ha='center', va='center',
         fontsize=24, fontweight='bold', color=COLORS[3])
ax4.text(0.5, 0.2, 'Total Transactions', ha='center', va='center', fontsize=14)
ax4.axis('off')

# Store Count
ax5 = fig.add_subplot(gs[1, 1])
store_count = transactions['store_id'].nunique()
ax5.text(0.5, 0.5, f'{store_count}', ha='center', va='center',
         fontsize=24, fontweight='bold', color=COLORS[4])
ax5.text(0.5, 0.2, 'Active Stores', ha='center', va='center', fontsize=14)
ax5.axis('off')

# Product Count
ax6 = fig.add_subplot(gs[1, 2])
product_count = transactions['product_id'].nunique()
ax6.text(0.5, 0.5, f'{product_count:,}', ha='center', va='center',
         fontsize=24, fontweight='bold', color=COLORS[5])
ax6.text(0.5, 0.2, 'Products Sold', ha='center', va='center', fontsize=14)
ax6.axis('off')

# Best Model
ax7 = fig.add_subplot(gs[2, 0])
best_model = successful_models.loc[successful_models['MAPE'].idxmin(), 'Model']
best_mape = successful_models['MAPE'].min()
ax7.text(0.5, 0.5, f'{best_model}', ha='center', va='center',
         fontsize=20, fontweight='bold', color=COLORS[6])
ax7.text(0.5, 0.2, f'Best Model ({best_mape:.2f}% MAPE)', ha='center', va='center', fontsize=12)
ax7.axis('off')

# Forecast Days
ax8 = fig.add_subplot(gs[2, 1])
ax8.text(0.5, 0.5, '90 Days', ha='center', va='center',
         fontsize=24, fontweight='bold', color=COLORS[7])
ax8.text(0.5, 0.2, 'Forecast Period', ha='center', va='center', fontsize=14)
ax8.axis('off')

# Date Range
ax9 = fig.add_subplot(gs[2, 2])
start_date = transactions['date'].min().strftime('%Y-%m-%d')
end_date = transactions['date'].max().strftime('%Y-%m-%d')
ax9.text(0.5, 0.6, f'{start_date}', ha='center', va='center', fontsize=14, fontweight='bold')
ax9.text(0.5, 0.5, 'to', ha='center', va='center', fontsize=10)
ax9.text(0.5, 0.4, f'{end_date}', ha='center', va='center', fontsize=14, fontweight='bold')
ax9.text(0.5, 0.2, 'Data Period', ha='center', va='center', fontsize=12)
ax9.axis('off')

plt.suptitle('PROJECT 7: SALES FORECASTING ML - KEY METRICS', 
             fontsize=18, fontweight='bold', y=0.98)
plt.savefig('visualizations/15_kpi_summary.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: 15_kpi_summary.png\n")

# ============================================================================
# SUMMARY
# ============================================================================

print("="*70)
print("✅ VISUALIZATION GENERATION COMPLETE!")
print("="*70)
print(f"\n📁 Generated 15 high-quality charts @ 300 DPI")
print(f"📂 Location: visualizations/")
print("\n📊 Chart List:")
charts = [
    "01_revenue_trend.png - Monthly revenue over 5 years",
    "02_category_performance.png - Revenue by category",
    "03_regional_performance.png - Revenue by region",
    "04_store_ranking.png - Top 25 stores ranked",
    "05_channel_evolution.png - Channel mix evolution",
    "06_seasonal_patterns.png - Monthly heatmap",
    "07_day_of_week.png - Day-wise analysis",
    "08_model_comparison.png - ML model metrics",
    "09_forecast_90day.png - 90-day forecast",
    "10_revenue_distribution.png - Revenue histogram",
    "11_customer_segments.png - Segment analysis",
    "12_profit_margins.png - Margins by category",
    "13_yoy_growth.png - Year-over-year growth",
    "14_discount_impact.png - Discount analysis",
    "15_kpi_summary.png - KPI dashboard"
]

for i, chart in enumerate(charts, 1):
    print(f"   {i:2d}. {chart}")

print("\n🎯 Ready for portfolio deployment!")
print("="*70 + "\n")
