"""
Visualization Generation Script
Creates professional charts and graphs for Grocery + Fashion Dashboard
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

print("=" * 60)
print("VISUALIZATION GENERATION")
print("=" * 60)
print()

# Load data
print("Loading datasets...")
df = pd.read_csv('data/merged_pos_data.csv', parse_dates=['Date'])
print(f"✓ Loaded {len(df):,} records")
print()

# ============================================
# 1. CATEGORY PERFORMANCE COMPARISON
# ============================================

print("Creating visualization 1: Category Performance Comparison...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Grocery vs Fashion - Performance Overview', fontsize=16, fontweight='bold', y=0.995)

# Revenue by Category
cat_revenue = df.groupby('Category')['NetAmount'].sum().sort_values(ascending=False)
colors = ['#2E86AB', '#A23B72']
axes[0, 0].bar(cat_revenue.index, cat_revenue.values / 1e6, color=colors, edgecolor='black', linewidth=1.5)
axes[0, 0].set_title('Total Revenue by Category', fontweight='bold', fontsize=12)
axes[0, 0].set_ylabel('Revenue (Million INR)', fontweight='bold')
axes[0, 0].set_ylim(0, cat_revenue.max() / 1e6 * 1.15)
for i, v in enumerate(cat_revenue.values):
    axes[0, 0].text(i, v / 1e6 + 10, f'₹{v/1e6:.1f}M', ha='center', fontweight='bold', fontsize=10)

# Transactions by Category
cat_trans = df.groupby('Category')['TransactionID'].count()
axes[0, 1].bar(cat_trans.index, cat_trans.values / 1000, color=colors, edgecolor='black', linewidth=1.5)
axes[0, 1].set_title('Total Transactions by Category', fontweight='bold', fontsize=12)
axes[0, 1].set_ylabel('Transactions (Thousands)', fontweight='bold')
for i, v in enumerate(cat_trans.values):
    axes[0, 1].text(i, v / 1000 + 1, f'{v/1000:.1f}K', ha='center', fontweight='bold', fontsize=10)

# Average Margin by Category
cat_margin = df.groupby('Category')['MarginPercent'].mean()
axes[1, 0].bar(cat_margin.index, cat_margin.values, color=colors, edgecolor='black', linewidth=1.5)
axes[1, 0].set_title('Average Margin % by Category', fontweight='bold', fontsize=12)
axes[1, 0].set_ylabel('Margin %', fontweight='bold')
axes[1, 0].set_ylim(0, cat_margin.max() * 1.15)
for i, v in enumerate(cat_margin.values):
    axes[1, 0].text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold', fontsize=10)

# Profit by Category
cat_profit = df.groupby('Category')['Profit'].sum()
axes[1, 1].bar(cat_profit.index, cat_profit.values / 1e6, color=colors, edgecolor='black', linewidth=1.5)
axes[1, 1].set_title('Total Profit by Category', fontweight='bold', fontsize=12)
axes[1, 1].set_ylabel('Profit (Million INR)', fontweight='bold')
for i, v in enumerate(cat_profit.values):
    axes[1, 1].text(i, v / 1e6 + 3, f'₹{v/1e6:.1f}M', ha='center', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('results/01_category_performance.png', bbox_inches='tight')
plt.close()
print("✓ Saved: results/01_category_performance.png")

# ============================================
# 2. SUBCATEGORY PERFORMANCE
# ============================================

print("Creating visualization 2: SubCategory Performance...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('SubCategory Performance Analysis', fontsize=16, fontweight='bold')

# Revenue by SubCategory
subcat_revenue = df.groupby(['Category', 'SubCategory'])['NetAmount'].sum().sort_values(ascending=False)
colors_subcat = ['#2E86AB' if 'Grocery' in str(idx) else '#A23B72' for idx in subcat_revenue.index]
axes[0].barh(range(len(subcat_revenue)), subcat_revenue.values / 1e6, color=colors_subcat, edgecolor='black', linewidth=1)
axes[0].set_yticks(range(len(subcat_revenue)))
axes[0].set_yticklabels([f"{idx[1]}" for idx in subcat_revenue.index], fontsize=10)
axes[0].set_xlabel('Revenue (Million INR)', fontweight='bold')
axes[0].set_title('Revenue by SubCategory', fontweight='bold', fontsize=12)
axes[0].invert_yaxis()
for i, v in enumerate(subcat_revenue.values):
    axes[0].text(v / 1e6 + 3, i, f'₹{v/1e6:.1f}M', va='center', fontsize=9)

# Margin by SubCategory
subcat_margin = df.groupby(['Category', 'SubCategory'])['MarginPercent'].mean().sort_values(ascending=False)
colors_margin = ['#2E86AB' if 'Grocery' in str(idx) else '#A23B72' for idx in subcat_margin.index]
axes[1].barh(range(len(subcat_margin)), subcat_margin.values, color=colors_margin, edgecolor='black', linewidth=1)
axes[1].set_yticks(range(len(subcat_margin)))
axes[1].set_yticklabels([f"{idx[1]}" for idx in subcat_margin.index], fontsize=10)
axes[1].set_xlabel('Average Margin %', fontweight='bold')
axes[1].set_title('Margin % by SubCategory', fontweight='bold', fontsize=12)
axes[1].invert_yaxis()
for i, v in enumerate(subcat_margin.values):
    axes[1].text(v + 1, i, f'{v:.1f}%', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('results/02_subcategory_performance.png', bbox_inches='tight')
plt.close()
print("✓ Saved: results/02_subcategory_performance.png")

# ============================================
# 3. STOCK AGEING ANALYSIS
# ============================================

print("Creating visualization 3: Stock Ageing Analysis...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Stock Ageing Analysis', fontsize=16, fontweight='bold')

# Overall Stock Ageing Distribution
age_counts = df['StockAgeCategory'].value_counts()
age_order = ['Fresh', 'Normal', 'Ageing', 'Old']
age_counts = age_counts.reindex(age_order, fill_value=0)
# Remove zero values
age_counts = age_counts[age_counts > 0]
colors_age = ['#2ECC71', '#3498DB', '#F39C12', '#E74C3C'][:len(age_counts)]
wedges, texts, autotexts = axes[0].pie(age_counts.values, labels=age_counts.index, autopct='%1.1f%%',
                                        colors=colors_age, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
axes[0].set_title('Overall Stock Ageing Distribution', fontweight='bold', fontsize=12)

# Stock Ageing by Category
age_by_cat = df.groupby(['Category', 'StockAgeCategory']).size().unstack(fill_value=0)
# Only use columns that exist
age_order_full = ['Fresh', 'Normal', 'Ageing', 'Old']
age_order_existing = [col for col in age_order_full if col in age_by_cat.columns]
age_by_cat = age_by_cat[age_order_existing]
colors_age_cat = ['#2ECC71', '#3498DB', '#F39C12', '#E74C3C'][:len(age_order_existing)]
age_by_cat_pct = age_by_cat.div(age_by_cat.sum(axis=1), axis=0) * 100
age_by_cat_pct.plot(kind='bar', stacked=True, ax=axes[1], color=colors_age_cat, edgecolor='black', linewidth=1.5)
axes[1].set_title('Stock Ageing by Category (%)', fontweight='bold', fontsize=12)
axes[1].set_xlabel('Category', fontweight='bold')
axes[1].set_ylabel('Percentage', fontweight='bold')
axes[1].set_xticklabels(age_by_cat_pct.index, rotation=0, fontweight='bold')
axes[1].legend(title='Stock Age', loc='upper right')

plt.tight_layout()
plt.savefig('results/03_stock_ageing.png', bbox_inches='tight')
plt.close()
print("✓ Saved: results/03_stock_ageing.png")

# ============================================
# 4. POS SYSTEM COMPARISON
# ============================================

print("Creating visualization 4: POS System Comparison...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('POS1 vs POS2 - Performance Comparison', fontsize=16, fontweight='bold', y=0.995)

# Revenue by POS
pos_revenue = df.groupby('POS_System')['NetAmount'].sum()
colors_pos = ['#FF6B6B', '#4ECDC4']
axes[0, 0].bar(pos_revenue.index, pos_revenue.values / 1e6, color=colors_pos, edgecolor='black', linewidth=1.5)
axes[0, 0].set_title('Revenue by POS System', fontweight='bold', fontsize=12)
axes[0, 0].set_ylabel('Revenue (Million INR)', fontweight='bold')
for i, v in enumerate(pos_revenue.values):
    axes[0, 0].text(i, v / 1e6 + 10, f'₹{v/1e6:.1f}M', ha='center', fontweight='bold')

# Transactions by POS
pos_trans = df.groupby('POS_System')['TransactionID'].count()
axes[0, 1].bar(pos_trans.index, pos_trans.values / 1000, color=colors_pos, edgecolor='black', linewidth=1.5)
axes[0, 1].set_title('Transactions by POS System', fontweight='bold', fontsize=12)
axes[0, 1].set_ylabel('Transactions (Thousands)', fontweight='bold')
for i, v in enumerate(pos_trans.values):
    axes[0, 1].text(i, v / 1000 + 1, f'{v/1000:.1f}K', ha='center', fontweight='bold')

# Store Performance
store_revenue = df.groupby('Store')['NetAmount'].sum().sort_values(ascending=True)
store_pos = df.groupby('Store')['POS_System'].first()
colors_store = [colors_pos[0] if store_pos[store] == 'POS1' else colors_pos[1] for store in store_revenue.index]
axes[1, 0].barh(range(len(store_revenue)), store_revenue.values / 1e6, color=colors_store, edgecolor='black', linewidth=1)
axes[1, 0].set_yticks(range(len(store_revenue)))
axes[1, 0].set_yticklabels(store_revenue.index)
axes[1, 0].set_xlabel('Revenue (Million INR)', fontweight='bold')
axes[1, 0].set_title('Revenue by Store', fontweight='bold', fontsize=12)
for i, v in enumerate(store_revenue.values):
    axes[1, 0].text(v / 1e6 + 3, i, f'₹{v/1e6:.0f}M', va='center')

# Avg Margin by POS
pos_margin = df.groupby('POS_System')['MarginPercent'].mean()
axes[1, 1].bar(pos_margin.index, pos_margin.values, color=colors_pos, edgecolor='black', linewidth=1.5)
axes[1, 1].set_title('Average Margin by POS System', fontweight='bold', fontsize=12)
axes[1, 1].set_ylabel('Margin %', fontweight='bold')
for i, v in enumerate(pos_margin.values):
    axes[1, 1].text(i, v + 0.5, f'{v:.2f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('results/04_pos_comparison.png', bbox_inches='tight')
plt.close()
print("✓ Saved: results/04_pos_comparison.png")

# ============================================
# 5. MONTHLY TRENDS
# ============================================

print("Creating visualization 5: Monthly Trends...")

fig, axes = plt.subplots(2, 1, figsize=(16, 10))
fig.suptitle('Monthly Performance Trends (2024)', fontsize=16, fontweight='bold')

# Monthly Revenue Trends
df['YearMonth'] = df['Date'].dt.to_period('M')
monthly_revenue = df.groupby(['YearMonth', 'Category'])['NetAmount'].sum().unstack() / 1e6

monthly_revenue.plot(ax=axes[0], marker='o', linewidth=2, markersize=6, color=['#2E86AB', '#A23B72'])
axes[0].set_title('Monthly Revenue Trends by Category', fontweight='bold', fontsize=12)
axes[0].set_ylabel('Revenue (Million INR)', fontweight='bold')
axes[0].set_xlabel('Month', fontweight='bold')
axes[0].legend(title='Category', loc='upper left')
axes[0].grid(True, alpha=0.3)

# Monthly Transaction Trends
monthly_trans = df.groupby(['YearMonth', 'Category'])['TransactionID'].count().unstack() / 1000

monthly_trans.plot(ax=axes[1], marker='s', linewidth=2, markersize=6, color=['#2E86AB', '#A23B72'])
axes[1].set_title('Monthly Transaction Trends by Category', fontweight='bold', fontsize=12)
axes[1].set_ylabel('Transactions (Thousands)', fontweight='bold')
axes[1].set_xlabel('Month', fontweight='bold')
axes[1].legend(title='Category', loc='upper left')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/05_monthly_trends.png', bbox_inches='tight')
plt.close()
print("✓ Saved: results/05_monthly_trends.png")

# ============================================
# 6. MARGIN COMPARISON HEATMAP
# ============================================

print("Creating visualization 6: Margin Comparison Heatmap...")

fig, ax = plt.subplots(figsize=(10, 8))
fig.suptitle('Margin % Comparison - Category vs SubCategory', fontsize=14, fontweight='bold')

# Create pivot table for heatmap
margin_pivot = df.pivot_table(values='MarginPercent', index='SubCategory', columns='Category', aggfunc='mean')

sns.heatmap(margin_pivot, annot=True, fmt='.1f', cmap='YlGnBu', cbar_kws={'label': 'Margin %'},
            linewidths=1, linecolor='black', ax=ax, vmin=0, vmax=50)
ax.set_xlabel('Category', fontweight='bold', fontsize=12)
ax.set_ylabel('SubCategory', fontweight='bold', fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontweight='bold')
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

plt.tight_layout()
plt.savefig('results/06_margin_heatmap.png', bbox_inches='tight')
plt.close()
print("✓ Saved: results/06_margin_heatmap.png")

# ============================================
# 7. BRAND PERFORMANCE
# ============================================

print("Creating visualization 7: Top Brands Performance...")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Top 10 Brands Performance', fontsize=16, fontweight='bold')

# Top 10 Brands by Revenue
brand_revenue = df.groupby('Brand')['NetAmount'].sum().sort_values(ascending=False).head(10)
axes[0].barh(range(len(brand_revenue)), brand_revenue.values / 1e6, color='#3498DB', edgecolor='black', linewidth=1)
axes[0].set_yticks(range(len(brand_revenue)))
axes[0].set_yticklabels(brand_revenue.index)
axes[0].set_xlabel('Revenue (Million INR)', fontweight='bold')
axes[0].set_title('Top 10 Brands by Revenue', fontweight='bold', fontsize=12)
axes[0].invert_yaxis()
for i, v in enumerate(brand_revenue.values):
    axes[0].text(v / 1e6 + 2, i, f'₹{v/1e6:.1f}M', va='center', fontweight='bold')

# Top 10 Brands by Transactions
brand_trans = df.groupby('Brand')['TransactionID'].count().sort_values(ascending=False).head(10)
axes[1].barh(range(len(brand_trans)), brand_trans.values / 1000, color='#E67E22', edgecolor='black', linewidth=1)
axes[1].set_yticks(range(len(brand_trans)))
axes[1].set_yticklabels(brand_trans.index)
axes[1].set_xlabel('Transactions (Thousands)', fontweight='bold')
axes[1].set_title('Top 10 Brands by Transactions', fontweight='bold', fontsize=12)
axes[1].invert_yaxis()
for i, v in enumerate(brand_trans.values):
    axes[1].text(v / 1000 + 0.3, i, f'{v/1000:.1f}K', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('results/07_brand_performance.png', bbox_inches='tight')
plt.close()
print("✓ Saved: results/07_brand_performance.png")

# ============================================
# 8. WEEKEND VS WEEKDAY
# ============================================

print("Creating visualization 8: Weekend vs Weekday Analysis...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Weekend vs Weekday Performance', fontsize=16, fontweight='bold')

# Revenue by Day Type
weekend_revenue = df.groupby(['IsWeekend', 'Category'])['NetAmount'].sum().unstack() / 1e6
weekend_revenue.index = ['Weekday', 'Weekend']
weekend_revenue.plot(kind='bar', ax=axes[0], color=['#2E86AB', '#A23B72'], edgecolor='black', linewidth=1.5)
axes[0].set_title('Revenue: Weekend vs Weekday', fontweight='bold', fontsize=12)
axes[0].set_ylabel('Revenue (Million INR)', fontweight='bold')
axes[0].set_xlabel('Day Type', fontweight='bold')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=0)
axes[0].legend(title='Category')

# Transactions by Day Type
weekend_trans = df.groupby(['IsWeekend', 'Category'])['TransactionID'].count().unstack() / 1000
weekend_trans.index = ['Weekday', 'Weekend']
weekend_trans.plot(kind='bar', ax=axes[1], color=['#2E86AB', '#A23B72'], edgecolor='black', linewidth=1.5)
axes[1].set_title('Transactions: Weekend vs Weekday', fontweight='bold', fontsize=12)
axes[1].set_ylabel('Transactions (Thousands)', fontweight='bold')
axes[1].set_xlabel('Day Type', fontweight='bold')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)
axes[1].legend(title='Category')

plt.tight_layout()
plt.savefig('results/08_weekend_analysis.png', bbox_inches='tight')
plt.close()
print("✓ Saved: results/08_weekend_analysis.png")

# ============================================
# 9. QUARTERLY PERFORMANCE
# ============================================

print("Creating visualization 9: Quarterly Performance...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Quarterly Performance Analysis (2024)', fontsize=16, fontweight='bold', y=0.995)

# Revenue by Quarter
quarterly_revenue = df.groupby(['Quarter', 'Category'])['NetAmount'].sum().unstack() / 1e6
quarterly_revenue.plot(kind='bar', ax=axes[0, 0], color=['#2E86AB', '#A23B72'], edgecolor='black', linewidth=1.5)
axes[0, 0].set_title('Quarterly Revenue', fontweight='bold', fontsize=12)
axes[0, 0].set_ylabel('Revenue (Million INR)', fontweight='bold')
axes[0, 0].set_xlabel('Quarter', fontweight='bold')
axes[0, 0].set_xticklabels([f'Q{i}' for i in quarterly_revenue.index], rotation=0)
axes[0, 0].legend(title='Category')

# Transactions by Quarter
quarterly_trans = df.groupby(['Quarter', 'Category'])['TransactionID'].count().unstack() / 1000
quarterly_trans.plot(kind='bar', ax=axes[0, 1], color=['#2E86AB', '#A23B72'], edgecolor='black', linewidth=1.5)
axes[0, 1].set_title('Quarterly Transactions', fontweight='bold', fontsize=12)
axes[0, 1].set_ylabel('Transactions (Thousands)', fontweight='bold')
axes[0, 1].set_xlabel('Quarter', fontweight='bold')
axes[0, 1].set_xticklabels([f'Q{i}' for i in quarterly_trans.index], rotation=0)
axes[0, 1].legend(title='Category')

# Profit by Quarter
quarterly_profit = df.groupby(['Quarter', 'Category'])['Profit'].sum().unstack() / 1e6
quarterly_profit.plot(kind='bar', ax=axes[1, 0], color=['#2E86AB', '#A23B72'], edgecolor='black', linewidth=1.5)
axes[1, 0].set_title('Quarterly Profit', fontweight='bold', fontsize=12)
axes[1, 0].set_ylabel('Profit (Million INR)', fontweight='bold')
axes[1, 0].set_xlabel('Quarter', fontweight='bold')
axes[1, 0].set_xticklabels([f'Q{i}' for i in quarterly_profit.index], rotation=0)
axes[1, 0].legend(title='Category')

# Margin by Quarter
quarterly_margin = df.groupby(['Quarter', 'Category'])['MarginPercent'].mean().unstack()
quarterly_margin.plot(kind='bar', ax=axes[1, 1], color=['#2E86AB', '#A23B72'], edgecolor='black', linewidth=1.5)
axes[1, 1].set_title('Quarterly Average Margin', fontweight='bold', fontsize=12)
axes[1, 1].set_ylabel('Margin %', fontweight='bold')
axes[1, 1].set_xlabel('Quarter', fontweight='bold')
axes[1, 1].set_xticklabels([f'Q{i}' for i in quarterly_margin.index], rotation=0)
axes[1, 1].legend(title='Category')

plt.tight_layout()
plt.savefig('results/09_quarterly_performance.png', bbox_inches='tight')
plt.close()
print("✓ Saved: results/09_quarterly_performance.png")

# ============================================
# 10. COMPREHENSIVE DASHBOARD
# ============================================

print("Creating visualization 10: Comprehensive Dashboard...")

fig = plt.figure(figsize=(18, 12))
fig.suptitle('Grocery + Fashion Dashboard - Complete Overview', fontsize=18, fontweight='bold', y=0.98)

gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

# KPI Metrics (Top)
ax1 = fig.add_subplot(gs[0, :])
ax1.axis('off')
kpis = {
    'Total Revenue': f"₹{df['NetAmount'].sum()/1e6:.1f}M",
    'Total Profit': f"₹{df['Profit'].sum()/1e6:.1f}M",
    'Transactions': f"{len(df):,}",
    'Avg Margin': f"{df['MarginPercent'].mean():.1f}%",
    'Unique SKUs': f"{df['SKU_ID'].nunique():,}",
    'Fresh Stock': f"{len(df[df['StockAgeCategory']=='Fresh'])/len(df)*100:.1f}%"
}
kpi_text = "   |   ".join([f"{k}: {v}" for k, v in kpis.items()])
ax1.text(0.5, 0.5, kpi_text, ha='center', va='center', fontsize=14, fontweight='bold',
         bbox=dict(boxstyle='round', facecolor='#3498DB', alpha=0.2, edgecolor='black', linewidth=2))

# Category Revenue
ax2 = fig.add_subplot(gs[1, 0])
cat_rev = df.groupby('Category')['NetAmount'].sum() / 1e6
ax2.bar(cat_rev.index, cat_rev.values, color=['#2E86AB', '#A23B72'], edgecolor='black', linewidth=1.5)
ax2.set_title('Category Revenue', fontweight='bold')
ax2.set_ylabel('Million INR', fontweight='bold')
for i, v in enumerate(cat_rev.values):
    ax2.text(i, v + 10, f'₹{v:.0f}M', ha='center', fontweight='bold')

# Stock Ageing
ax3 = fig.add_subplot(gs[1, 1])
age_data = df['StockAgeCategory'].value_counts()
colors_age = ['#2ECC71', '#3498DB', '#F39C12', '#E74C3C']
ax3.pie(age_data.values, labels=age_data.index, autopct='%1.1f%%', colors=colors_age, startangle=90)
ax3.set_title('Stock Ageing', fontweight='bold')

# POS Comparison
ax4 = fig.add_subplot(gs[1, 2])
pos_rev = df.groupby('POS_System')['NetAmount'].sum() / 1e6
ax4.bar(pos_rev.index, pos_rev.values, color=['#FF6B6B', '#4ECDC4'], edgecolor='black', linewidth=1.5)
ax4.set_title('POS Revenue', fontweight='bold')
ax4.set_ylabel('Million INR', fontweight='bold')
for i, v in enumerate(pos_rev.values):
    ax4.text(i, v + 10, f'₹{v:.0f}M', ha='center', fontweight='bold')

# Monthly Trends
ax5 = fig.add_subplot(gs[2, :])
monthly_data = df.groupby(['YearMonth', 'Category'])['NetAmount'].sum().unstack() / 1e6
monthly_data.plot(ax=ax5, marker='o', linewidth=2, color=['#2E86AB', '#A23B72'])
ax5.set_title('Monthly Revenue Trends', fontweight='bold')
ax5.set_ylabel('Million INR', fontweight='bold')
ax5.set_xlabel('Month', fontweight='bold')
ax5.legend(title='Category')
ax5.grid(True, alpha=0.3)

plt.savefig('results/10_comprehensive_dashboard.png', bbox_inches='tight')
plt.close()
print("✓ Saved: results/10_comprehensive_dashboard.png")

print()
print("=" * 60)
print("VISUALIZATION GENERATION COMPLETED!")
print("=" * 60)
print()
print("All 10 visualizations created successfully:")
print("  1. Category Performance Comparison")
print("  2. SubCategory Performance")
print("  3. Stock Ageing Analysis")
print("  4. POS System Comparison")
print("  5. Monthly Trends")
print("  6. Margin Comparison Heatmap")
print("  7. Brand Performance")
print("  8. Weekend vs Weekday Analysis")
print("  9. Quarterly Performance")
print(" 10. Comprehensive Dashboard")
print()
print("=" * 60)
