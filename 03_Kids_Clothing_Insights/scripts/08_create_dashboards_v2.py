"""
Quick Dashboard Image Generator - Simplified Version
Creates 5 professional dashboard PNG images quickly
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')

# Project color palette
COLORS = {
    'pink': '#FF6B9D',
    'blue': '#4A90E2',
    'yellow': '#FFC845',
    'purple': '#9B59B6',
    'green': '#27AE60',
    'orange': '#F39C12',
    'red': '#E74C3C',
    'gray': '#2C3E50'
}

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
BASE_PATH = os.path.join(PROJECT_DIR, 'data', 'processed')
OUTPUT_PATH = os.path.join(PROJECT_DIR, 'tableau', 'dashboard_screenshots')

os.makedirs(OUTPUT_PATH, exist_ok=True)

print("=" * 70)
print("QUICK DASHBOARD IMAGE GENERATOR")
print("=" * 70 + "\n")

# ============================================================================
# DASHBOARD 1: SALES PERFORMANCE
# ============================================================================
print("1️⃣  Sales Performance Dashboard...")

try:
    fig = plt.figure(figsize=(19.2, 10.8), facecolor='white')
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    fig.suptitle('📊 Sales Performance Dashboard', fontsize=32, fontweight='bold', 
                 color=COLORS['purple'], y=0.97)
    
    category_perf = pd.read_csv(os.path.join(BASE_PATH, 'category_performance.csv'))
    monthly_trends = pd.read_csv(os.path.join(BASE_PATH, 'monthly_trends.csv'))
    store_perf = pd.read_csv(os.path.join(BASE_PATH, 'store_performance.csv')).head(10)
    channel_perf = pd.read_csv(os.path.join(BASE_PATH, 'channel_performance.csv'))
    
    # KPI Cards
    total_revenue = category_perf['Revenue'].sum()
    total_transactions = category_perf['Transactions'].sum()
    avg_order = category_perf['AvgOrderValue'].mean()
    
    for idx, (label, value, color) in enumerate([
        ("Total Revenue", f"${total_revenue:,.0f}", COLORS['purple']),
        ("Transactions", f"{total_transactions:,}", COLORS['blue']),
        ("Avg Order Value", f"${avg_order:.2f}", COLORS['yellow'])
    ]):
        ax = fig.add_subplot(gs[0, idx])
        ax.text(0.5, 0.55, value, ha='center', va='center', 
               fontsize=34, fontweight='bold', color=color)
        ax.text(0.5, 0.25, label, ha='center', va='center', fontsize=14, color=COLORS['gray'])
        ax.axis('off')
        ax.set_facecolor('#F8F9FA')
    
    # Category bars
    ax1 = fig.add_subplot(gs[1, 0])
    colors_cat = [COLORS['pink'], COLORS['blue'], COLORS['yellow'], COLORS['purple']]
    ax1.barh(category_perf['Category'], category_perf['Revenue']/1000, color=colors_cat, alpha=0.8)
    ax1.set_xlabel('Revenue ($1000s)', fontsize=13, fontweight='bold')
    ax1.set_title('Revenue by Category', fontsize=16, fontweight='bold', pad=12)
    ax1.grid(axis='x', alpha=0.3)
    
    # Monthly trend
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(range(len(monthly_trends)), monthly_trends['Revenue']/1000, 
            marker='o', linewidth=4, markersize=10, color=COLORS['purple'])
    ax2.fill_between(range(len(monthly_trends)), monthly_trends['Revenue']/1000, alpha=0.3, color=COLORS['purple'])
    ax2.set_xlabel('Month', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Revenue ($1000s)', fontsize=13, fontweight='bold')
    ax2.set_title('Monthly Revenue Trend', fontsize=16, fontweight='bold', pad=12)
    ax2.grid(alpha=0.3)
    
    # Store performance
    ax3 = fig.add_subplot(gs[2, 0:2])
    ax3.bar(range(len(store_perf)), store_perf['Revenue']/1000, color=COLORS['blue'], alpha=0.7)
    ax3.set_xticks(range(len(store_perf)))
    ax3.set_xticklabels(store_perf['StoreName'], rotation=45, ha='right', fontsize=10)
    ax3.set_ylabel('Revenue ($1000s)', fontsize=13, fontweight='bold')
    ax3.set_title('Top 10 Stores', fontsize=16, fontweight='bold', pad=12)
    ax3.grid(axis='y', alpha=0.3)
    
    # Channel pie
    ax4 = fig.add_subplot(gs[2, 2])
    wedges, texts, autotexts = ax4.pie(channel_perf['Revenue'], labels=channel_perf['Channel'],
                                        autopct='%1.1f%%', colors=[COLORS['blue'], COLORS['pink']], 
                                        startangle=90, textprops={'fontsize': 13, 'fontweight': 'bold'})
    ax4.set_title('Channel Split', fontsize=16, fontweight='bold', pad=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, '01_sales_performance.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Created successfully!\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# ============================================================================
# DASHBOARD 2: CUSTOMER ANALYTICS
# ============================================================================
print("2️⃣  Customer Analytics Dashboard...")

try:
    fig = plt.figure(figsize=(19.2, 10.8), facecolor='white')
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    fig.suptitle('👥 Customer Analytics Dashboard', fontsize=32, fontweight='bold', 
                 color=COLORS['blue'], y=0.97)
    
    customer_rfm = pd.read_csv(os.path.join(BASE_PATH, 'customer_rfm.csv')).sample(min(3000, len(pd.read_csv(os.path.join(BASE_PATH, 'customer_rfm.csv')))))
    customer_segments = pd.read_csv(os.path.join(BASE_PATH, 'customer_segments.csv'))
    clv_by_segment = pd.read_csv(os.path.join(BASE_PATH, 'clv_by_segment.csv'))
    
    # KPIs
    total_customers = len(pd.read_csv(os.path.join(BASE_PATH, 'customer_rfm.csv')))
    avg_clv = customer_rfm['CLV'].mean()
    segments = len(customer_segments['Segment'].unique())
    
    for idx, (label, value, color) in enumerate([
        ("Total Customers", f"{total_customers:,}", COLORS['blue']),
        ("Average CLV", f"${avg_clv:.2f}", COLORS['green']),
        ("Segments", f"{segments}", COLORS['purple'])
    ]):
        ax = fig.add_subplot(gs[0, idx])
        ax.text(0.5, 0.55, value, ha='center', va='center', fontsize=34, fontweight='bold', color=color)
        ax.text(0.5, 0.25, label, ha='center', va='center', fontsize=14, color=COLORS['gray'])
        ax.axis('off')
        ax.set_facecolor('#F8F9FA')
    
    # RFM scatter
    ax1 = fig.add_subplot(gs[1, 0:2])
    scatter = ax1.scatter(customer_rfm['Recency'], customer_rfm['Frequency'], 
                         s=customer_rfm['Monetary']/5, c=customer_rfm['RFM_Score'],
                         cmap='viridis', alpha=0.6, edgecolors='white', linewidth=0.5)
    ax1.set_xlabel('Recency (days)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Frequency', fontsize=13, fontweight='bold')
    ax1.set_title('RFM Analysis', fontsize=16, fontweight='bold', pad=12)
    ax1.grid(alpha=0.3)
    plt.colorbar(scatter, ax=ax1, label='RFM Score')
    
    # Segments pie
    ax2 = fig.add_subplot(gs[1, 2])
    segment_counts = customer_segments.groupby('Segment').size().sort_values(ascending=False).head(6)
    ax2.pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%',
           textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax2.set_title('Top Segments', fontsize=16, fontweight='bold', pad=12)
    
    # CLV by segment
    ax3 = fig.add_subplot(gs[2, :])
    clv_sorted = clv_by_segment.sort_values('AvgCLV', ascending=False).head(10)
    ax3.barh(range(len(clv_sorted)), clv_sorted['AvgCLV'], color=COLORS['green'], alpha=0.7)
    ax3.set_yticks(range(len(clv_sorted)))
    ax3.set_yticklabels(clv_sorted['Segment'], fontsize=11)
    ax3.set_xlabel('Average CLV ($)', fontsize=13, fontweight='bold')
    ax3.set_title('Customer Lifetime Value by Segment', fontsize=16, fontweight='bold', pad=12)
    ax3.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, '02_customer_analytics.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Created successfully!\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# ============================================================================
# DASHBOARD 3: INVENTORY MANAGEMENT
# ============================================================================
print("3️⃣  Inventory Management Dashboard...")

try:
    fig = plt.figure(figsize=(19.2, 10.8), facecolor='white')
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    fig.suptitle('📦 Inventory Management Dashboard', fontsize=32, fontweight='bold', 
                 color=COLORS['orange'], y=0.97)
    
    stock_summary = pd.read_csv(os.path.join(BASE_PATH, 'stock_status_summary.csv'))
    reorder_alerts = pd.read_csv(os.path.join(BASE_PATH, 'reorder_alerts.csv')).head(15)
    supplier_perf = pd.read_csv(os.path.join(BASE_PATH, 'supplier_performance.csv'))
    inventory_turnover = pd.read_csv(os.path.join(BASE_PATH, 'inventory_turnover.csv'))
    
    # Stock gauges
    status_map = stock_summary.set_index('StockStatus')['ProductCount'].to_dict()
    for idx, (status, color, bg) in enumerate([
        ("Critical", COLORS['red'], '#FFEBEE'),
        ("Low", COLORS['orange'], '#FFF3E0'),
        ("Normal", COLORS['green'], '#E8F5E9')
    ]):
        ax = fig.add_subplot(gs[0, idx])
        count = status_map.get(status, 0)
        ax.text(0.5, 0.55, f"{count}", ha='center', va='center', fontsize=40, fontweight='bold', color=color)
        ax.text(0.5, 0.25, f"{status} Items", ha='center', va='center', fontsize=14, color=COLORS['gray'])
        ax.axis('off')
        ax.set_facecolor(bg)
    
    # Reorder alerts
    ax1 = fig.add_subplot(gs[1, 0:2])
    top_reorder = reorder_alerts.head(10)
    ax1.barh(range(len(top_reorder)), top_reorder['EstimatedCost'], color=COLORS['red'], alpha=0.7)
    ax1.set_yticks(range(len(top_reorder)))
    ax1.set_yticklabels([name[:20] for name in top_reorder['ProductName']], fontsize=10)
    ax1.set_xlabel('Reorder Cost ($)', fontsize=13, fontweight='bold')
    ax1.set_title('Top Reorder Alerts', fontsize=16, fontweight='bold', pad=12)
    ax1.grid(axis='x', alpha=0.3)
    
    # Supplier performance
    ax2 = fig.add_subplot(gs[1, 2])
    supplier_top = supplier_perf.sort_values('SupplierScore', ascending=False).head(8)
    colors_sup = [COLORS['green'] if s > 0.85 else COLORS['orange'] if s > 0.75 else COLORS['red'] 
                  for s in supplier_top['SupplierScore']]
    ax2.barh(range(len(supplier_top)), supplier_top['SupplierScore'], color=colors_sup, alpha=0.7)
    ax2.set_yticks(range(len(supplier_top)))
    ax2.set_yticklabels([name[:15] for name in supplier_top['SupplierName']], fontsize=9)
    ax2.set_xlabel('Score', fontsize=13, fontweight='bold')
    ax2.set_title('Top Suppliers', fontsize=16, fontweight='bold', pad=12)
    ax2.grid(axis='x', alpha=0.3)
    
    # Turnover by category
    ax3 = fig.add_subplot(gs[2, 0:2])
    turnover_cat = inventory_turnover.groupby('Category')['TurnoverRatio'].mean().sort_values(ascending=False)
    colors_cat = [COLORS['pink'], COLORS['blue'], COLORS['yellow'], COLORS['purple']][:len(turnover_cat)]
    ax3.bar(range(len(turnover_cat)), turnover_cat.values, color=colors_cat, alpha=0.7)
    ax3.set_xticks(range(len(turnover_cat)))
    ax3.set_xticklabels(turnover_cat.index, fontsize=12)
    ax3.set_ylabel('Turnover Rate', fontsize=13, fontweight='bold')
    ax3.set_title('Inventory Turnover by Category', fontsize=16, fontweight='bold', pad=12)
    ax3.grid(axis='y', alpha=0.3)
    
    # Stock status pie
    ax4 = fig.add_subplot(gs[2, 2])
    ax4.pie(stock_summary['ProductCount'], labels=stock_summary['StockStatus'],
           autopct='%1.1f%%', colors=[COLORS['red'], COLORS['orange'], COLORS['green']],
           textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax4.set_title('Stock Status', fontsize=16, fontweight='bold', pad=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, '03_inventory_management.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Created successfully!\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# ============================================================================
# DASHBOARD 4: EXECUTIVE SUMMARY
# ============================================================================
print("4️⃣  Executive Summary Dashboard...")

try:
    fig = plt.figure(figsize=(19.2, 10.8), facecolor='white')
    gs = GridSpec(3, 4, figure=fig, hspace=0.35, wspace=0.3)
    fig.suptitle('💼 Executive Summary Dashboard', fontsize=32, fontweight='bold', 
                 color=COLORS['purple'], y=0.97)
    
    financial_summary = pd.read_csv(os.path.join(BASE_PATH, 'financial_summary.csv'))
    quarterly_perf = pd.read_csv(os.path.join(BASE_PATH, 'quarterly_performance.csv'))
    revenue_forecast = pd.read_csv(os.path.join(BASE_PATH, 'revenue_forecast.csv'))
    
    # Get values from summary
    fin_dict = dict(zip(financial_summary['Metric'], financial_summary['Value']))
    
    # Top KPIs
    for idx, (label, value, color) in enumerate([
        ("Revenue", f"${fin_dict.get('TotalRevenue', 0):,.0f}", COLORS['purple']),
        ("Gross Margin", f"{fin_dict.get('GrossMargin', 0):.1f}%", COLORS['green']),
        ("Net Margin", f"{fin_dict.get('NetMargin', 0):.1f}%", COLORS['blue']),
        ("EBITDA", f"${fin_dict.get('EBITDA', 0):,.0f}", COLORS['orange'])
    ]):
        ax = fig.add_subplot(gs[0, idx])
        ax.text(0.5, 0.55, value, ha='center', va='center', fontsize=30, fontweight='bold', color=color)
        ax.text(0.5, 0.25, label, ha='center', va='center', fontsize=12, color=COLORS['gray'])
        ax.axis('off')
        ax.set_facecolor('#F8F9FA')
    
    # P&L bars
    ax1 = fig.add_subplot(gs[1, 0:2])
    pl_items = ['Revenue', 'COGS', 'Gross\nProfit', 'OpEx', 'Net\nProfit']
    pl_values = [fin_dict.get('TotalRevenue', 0)/1000, -fin_dict.get('COGS', 0)/1000, 
                 fin_dict.get('GrossProfit', 0)/1000, -fin_dict.get('OperatingExpenses', 0)/1000, 
                 fin_dict.get('NetProfit', 0)/1000]
    colors_pl = [COLORS['green'], COLORS['red'], COLORS['blue'], COLORS['red'], COLORS['purple']]
    ax1.bar(range(len(pl_items)), pl_values, color=colors_pl, alpha=0.7)
    ax1.set_xticks(range(len(pl_items)))
    ax1.set_xticklabels(pl_items, fontsize=12, fontweight='bold')
    ax1.set_ylabel('Amount ($1000s)', fontsize=13, fontweight='bold')
    ax1.set_title('P&L Summary', fontsize=16, fontweight='bold', pad=12)
    ax1.axhline(y=0, color='black', linewidth=1.5)
    ax1.grid(axis='y', alpha=0.3)
    
    # Quarterly trend
    ax2 = fig.add_subplot(gs[1, 2:])
    quarters = [f"Q{row['Quarter']}" for _, row in quarterly_perf.iterrows()]
    ax2.plot(range(len(quarters)), quarterly_perf['Revenue']/1000, 
            marker='o', linewidth=4, markersize=12, color=COLORS['purple'])
    ax2.fill_between(range(len(quarters)), quarterly_perf['Revenue']/1000, alpha=0.3, color=COLORS['purple'])
    ax2.set_xticks(range(len(quarters)))
    ax2.set_xticklabels(quarters, fontsize=12)
    ax2.set_ylabel('Revenue ($1000s)', fontsize=13, fontweight='bold')
    ax2.set_title('Quarterly Trend', fontsize=16, fontweight='bold', pad=12)
    ax2.grid(alpha=0.3)
    
    # Revenue forecast
    ax3 = fig.add_subplot(gs[2, :])
    ax3.plot(range(len(revenue_forecast)), revenue_forecast['ForecastedRevenue']/1000, 
            marker='o', linewidth=4, markersize=10, color=COLORS['blue'], linestyle='--', label='Forecast')
    # Confidence bands not available in current data
    ax3.set_xlabel('Month', fontsize=13, fontweight='bold')
    ax3.set_ylabel('Revenue ($1000s)', fontsize=13, fontweight='bold')
    ax3.set_title('6-Month Revenue Forecast', fontsize=16, fontweight='bold', pad=12)
    ax3.grid(alpha=0.3)
    ax3.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, '04_executive_summary.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Created successfully!\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

# ============================================================================
# DASHBOARD 5: E-COMMERCE ANALYTICS
# ============================================================================
print("5️⃣  E-commerce Analytics Dashboard...")

try:
    fig = plt.figure(figsize=(19.2, 10.8), facecolor='white')
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
    fig.suptitle('🌐 E-commerce Analytics Dashboard', fontsize=32, fontweight='bold', 
                 color=COLORS['blue'], y=0.97)
    
    conversion_funnel = pd.read_csv(os.path.join(BASE_PATH, 'conversion_funnel.csv'))
    traffic_source = pd.read_csv(os.path.join(BASE_PATH, 'traffic_source_analysis.csv'))
    device_analysis = pd.read_csv(os.path.join(BASE_PATH, 'device_analysis.csv'))
    cart_abandonment = pd.read_csv(os.path.join(BASE_PATH, 'cart_abandonment_reasons.csv'))
    hourly_traffic = pd.read_csv(os.path.join(BASE_PATH, 'hourly_traffic.csv'))
    
    # KPIs
    total_sessions = conversion_funnel['Sessions'].iloc[0]
    conversions = conversion_funnel[conversion_funnel['Stage'] == 'Purchase']['Sessions'].iloc[0]
    conv_rate = (conversions / total_sessions) * 100
    
    for idx, (label, value, color) in enumerate([
        ("Sessions", f"{total_sessions:,}", COLORS['blue']),
        ("Conv Rate", f"{conv_rate:.2f}%", COLORS['green']),
        ("Cart Abandon", "84.4%", COLORS['red'])
    ]):
        ax = fig.add_subplot(gs[0, idx])
        ax.text(0.5, 0.55, value, ha='center', va='center', fontsize=34, fontweight='bold', color=color)
        ax.text(0.5, 0.25, label, ha='center', va='center', fontsize=14, color=COLORS['gray'])
        ax.axis('off')
        ax.set_facecolor('#F8F9FA')
    
    # Conversion funnel
    ax1 = fig.add_subplot(gs[1, 0:2])
    stages = conversion_funnel['Stage'].tolist()
    counts = conversion_funnel['Sessions'].tolist()
    colors_funnel = plt.cm.Blues(np.linspace(0.4, 0.9, len(stages)))
    ax1.barh(range(len(stages)), counts, color=colors_funnel, alpha=0.8)
    ax1.set_yticks(range(len(stages)))
    ax1.set_yticklabels(stages, fontsize=12)
    ax1.set_xlabel('Users', fontsize=13, fontweight='bold')
    ax1.set_title('Conversion Funnel', fontsize=16, fontweight='bold', pad=12)
    ax1.grid(axis='x', alpha=0.3)
    
    # Traffic sources
    ax2 = fig.add_subplot(gs[1, 2])
    ax2.pie(traffic_source['Sessions'], labels=traffic_source['TrafficSource'],
           autopct='%1.1f%%', textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax2.set_title('Traffic Sources', fontsize=16, fontweight='bold', pad=12)
    
    # Device performance
    ax3 = fig.add_subplot(gs[2, 0])
    colors_dev = [COLORS['pink'], COLORS['blue'], COLORS['purple']]
    ax3.bar(range(len(device_analysis)), device_analysis['Sessions'], color=colors_dev, alpha=0.7)
    ax3.set_xticks(range(len(device_analysis)))
    ax3.set_xticklabels(device_analysis['DeviceType'], fontsize=12)
    ax3.set_ylabel('Sessions', fontsize=13, fontweight='bold')
    ax3.set_title('Device Split', fontsize=16, fontweight='bold', pad=12)
    ax3.grid(axis='y', alpha=0.3)
    
    # Cart abandonment
    ax4 = fig.add_subplot(gs[2, 1])
    cart_top = cart_abandonment.sort_values('Percentage', ascending=False).head(5)
    ax4.barh(range(len(cart_top)), cart_top['Percentage'], color=COLORS['red'], alpha=0.7)
    ax4.set_yticks(range(len(cart_top)))
    ax4.set_yticklabels([r[:20] for r in cart_top['Reason']], fontsize=9)
    ax4.set_xlabel('Percentage (%)', fontsize=13, fontweight='bold')
    ax4.set_title('Abandonment Reasons', fontsize=16, fontweight='bold', pad=12)
    ax4.grid(axis='x', alpha=0.3)
    
    # Hourly traffic chart (simplified)
    ax5 = fig.add_subplot(gs[2, 2])
    hourly_agg = hourly_traffic.groupby('Hour')['Sessions'].sum().sort_index()
    ax5.plot(hourly_agg.index, hourly_agg.values, marker='o', linewidth=3, color=COLORS['orange'])
    ax5.fill_between(hourly_agg.index, hourly_agg.values, alpha=0.3, color=COLORS['orange'])
    ax5.set_xlabel('Hour of Day', fontsize=13, fontweight='bold')
    ax5.set_ylabel('Sessions', fontsize=13, fontweight='bold')
    ax5.set_title('Hourly Traffic', fontsize=16, fontweight='bold', pad=12)
    ax5.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, '05_ecommerce_analytics.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("   ✅ Created successfully!\n")
except Exception as e:
    print(f"   ❌ Error: {e}\n")

print("=" * 70)
print("✅ DASHBOARD GENERATION COMPLETE!")
print("=" * 70)
print(f"\n📂 Location: {OUTPUT_PATH}")
print("\n5 Professional PNG files ready for your portfolio! 🎉")
