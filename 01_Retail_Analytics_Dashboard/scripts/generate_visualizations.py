"""
Generate all visualizations for Retail Analytics Dashboard
Creates professional charts and saves them as PNG files
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

def load_data():
    """Load cleaned data"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, 'data', 'retail_transactions_clean.csv')
    df = pd.read_csv(data_path, parse_dates=['Date'])
    print(f"✓ Loaded {len(df)} records")
    return df

def create_output_dir():
    """Create results directory"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    results_dir = os.path.join(base_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    return results_dir

def chart1_univariate_distributions(df, output_dir):
    """Distribution charts"""
    print("\n1. Creating univariate distributions...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    axes[0, 0].hist(df['NETAMT'], bins=50, edgecolor='black', alpha=0.7, color='#3498db')
    axes[0, 0].set_title('Distribution of Transaction Revenue', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Revenue ($)')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].axvline(df['NETAMT'].mean(), color='red', linestyle='--', linewidth=2, label=f"Mean: ${df['NETAMT'].mean():,.0f}")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    qty_counts = df['Qty'].value_counts().sort_index()
    axes[0, 1].bar(qty_counts.index, qty_counts.values, edgecolor='black', alpha=0.7, color='#2ecc71')
    axes[0, 1].set_title('Distribution of Quantity Sold', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Quantity')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].grid(True, alpha=0.3)
    
    axes[1, 0].hist(df['DiscountPct'], bins=30, edgecolor='black', alpha=0.7, color='#e74c3c')
    axes[1, 0].set_title('Distribution of Discount Percentage', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Discount %')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].axvline(df['DiscountPct'].mean(), color='darkred', linestyle='--', linewidth=2, label=f"Mean: {df['DiscountPct'].mean():.1f}%")
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].hist(df['ConversionPct'], bins=30, edgecolor='black', alpha=0.7, color='#9b59b6')
    axes[1, 1].set_title('Distribution of Conversion Rate', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Conversion %')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].axvline(df['ConversionPct'].mean(), color='purple', linestyle='--', linewidth=2, label=f"Mean: {df['ConversionPct'].mean():.1f}%")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '01_univariate_distributions.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved: 01_univariate_distributions.png")

def chart2_category_revenue(df, output_dir):
    """Category revenue analysis"""
    print("\n2. Creating category revenue analysis...")
    
    category_revenue = df.groupby('Category')['NETAMT'].sum().sort_values(ascending=False)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    bars = axes[0].bar(category_revenue.index, category_revenue.values, edgecolor='black', alpha=0.8, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
    axes[0].set_title('Total Revenue by Category', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Category', fontsize=12)
    axes[0].set_ylabel('Revenue ($)', fontsize=12)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    for i, (cat, v) in enumerate(category_revenue.items()):
        axes[0].text(i, v, f'${v/1e9:.2f}B', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    explode = [0.05 if i == 0 else 0 for i in range(len(category_revenue))]
    axes[1].pie(category_revenue.values, labels=category_revenue.index, autopct='%1.1f%%',
                startangle=90, colors=colors, explode=explode, textprops={'fontsize': 12, 'fontweight': 'bold'})
    axes[1].set_title('Revenue Share by Category', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '02_category_revenue_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved: 02_category_revenue_analysis.png")

def chart3_top_subcategories(df, output_dir):
    """Top subcategories"""
    print("\n3. Creating top subcategories chart...")
    
    subcategory_data = df.groupby(['Category', 'SubCategory']).agg({'NETAMT': 'sum'}).reset_index()
    top_subcategories = subcategory_data.nlargest(10, 'NETAMT')
    
    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(top_subcategories)))
    bars = plt.barh(range(len(top_subcategories)), top_subcategories['NETAMT'].values, alpha=0.8, color=colors, edgecolor='black')
    plt.yticks(range(len(top_subcategories)), 
               [f"{row['Category']}-{row['SubCategory']}" for _, row in top_subcategories.iterrows()], fontsize=11)
    plt.xlabel('Revenue ($)', fontsize=12, fontweight='bold')
    plt.title('Top 10 SubCategories by Revenue', fontsize=14, fontweight='bold', pad=20)
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3, axis='x')
    
    for i, v in enumerate(top_subcategories['NETAMT'].values):
        plt.text(v, i, f' ${v/1e9:.2f}B', va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '03_top_subcategories.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved: 03_top_subcategories.png")

def chart4_time_series(df, output_dir):
    """Time series analysis"""
    print("\n4. Creating time series analysis...")
    
    daily_revenue = df.groupby('Date')['NETAMT'].sum()
    monthly_revenue = df.groupby(['Year', 'MonthName', 'Month']).agg({'NETAMT': 'sum'}).reset_index().sort_values('Month')
    
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    
    axes[0].plot(daily_revenue.index, daily_revenue.values, linewidth=1, alpha=0.5, color='lightblue')
    axes[0].plot(daily_revenue.index, daily_revenue.rolling(window=7).mean(), 
                 linewidth=2.5, color='#e74c3c', label='7-Day Moving Average')
    axes[0].set_title('Daily Revenue Trend with 7-Day Moving Average', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Date', fontsize=12)
    axes[0].set_ylabel('Revenue ($)', fontsize=12)
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3)
    
    colors = plt.cm.plasma(np.linspace(0, 1, len(monthly_revenue)))
    bars = axes[1].bar(range(len(monthly_revenue)), monthly_revenue['NETAMT'].values, 
                       edgecolor='black', alpha=0.8, color=colors)
    axes[1].set_xticks(range(len(monthly_revenue)))
    axes[1].set_xticklabels(monthly_revenue['MonthName'], rotation=45, ha='right')
    axes[1].set_title('Monthly Revenue Performance', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Revenue ($)', fontsize=12)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    for i, v in enumerate(monthly_revenue['NETAMT'].values):
        axes[1].text(i, v, f'${v/1e9:.2f}B', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '04_time_series_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved: 04_time_series_analysis.png")

def chart5_day_of_week(df, output_dir):
    """Day of week analysis"""
    print("\n5. Creating day of week analysis...")
    
    dow_analysis = df.groupby('DayName').agg({'NETAMT': ['sum', 'count']}).reset_index()
    dow_analysis.columns = ['DayName', 'Total_Revenue', 'Transaction_Count']
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_analysis['DayName'] = pd.Categorical(dow_analysis['DayName'], categories=day_order, ordered=True)
    dow_analysis = dow_analysis.sort_values('DayName')
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    colors = ['#e74c3c' if day in ['Saturday', 'Sunday'] else '#3498db' for day in dow_analysis['DayName']]
    bars = axes[0].bar(dow_analysis['DayName'], dow_analysis['Total_Revenue'], 
                       color=colors, edgecolor='black', alpha=0.8)
    axes[0].set_title('Revenue by Day of Week', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Total Revenue ($)', fontsize=12)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    for i, v in enumerate(dow_analysis['Total_Revenue'].values):
        axes[0].text(i, v, f'${v/1e9:.2f}B', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    bars = axes[1].bar(dow_analysis['DayName'], dow_analysis['Transaction_Count'],
                       color=colors, edgecolor='black', alpha=0.8)
    axes[1].set_title('Transaction Count by Day of Week', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Number of Transactions', fontsize=12)
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    for i, v in enumerate(dow_analysis['Transaction_Count'].values):
        axes[1].text(i, v, f'{v:,.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '05_day_of_week_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved: 05_day_of_week_analysis.png")

def chart6_store_performance(df, output_dir):
    """Store performance"""
    print("\n6. Creating store performance analysis...")
    
    store_metrics = df.groupby('Store').agg({
        'NETAMT': ['sum', 'mean'],
        'Qty': 'sum',
        'ConversionPct': 'mean',
        'DiscountPct': 'mean'
    }).reset_index()
    store_metrics.columns = ['Store', 'Total_Revenue', 'Avg_Transaction', 'Total_Units', 'Avg_Conversion', 'Avg_Discount']
    store_metrics = store_metrics.sort_values('Total_Revenue', ascending=False)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(store_metrics)))
    bars = axes[0, 0].bar(store_metrics['Store'], store_metrics['Total_Revenue'], edgecolor='black', alpha=0.8, color=colors)
    axes[0, 0].set_title('Total Revenue by Store', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('Revenue ($)', fontsize=12)
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    for i, v in enumerate(store_metrics['Total_Revenue'].values):
        axes[0, 0].text(i, v, f'${v/1e9:.2f}B', ha='center', va='bottom', fontweight='bold')
    
    colors = plt.cm.Oranges(np.linspace(0.4, 0.9, len(store_metrics)))
    axes[0, 1].bar(store_metrics['Store'], store_metrics['Avg_Transaction'], 
                   color=colors, edgecolor='black', alpha=0.8)
    axes[0, 1].set_title('Average Transaction Value by Store', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('Avg Transaction ($)', fontsize=12)
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(store_metrics)))
    axes[1, 0].bar(store_metrics['Store'], store_metrics['Avg_Conversion'],
                   color=colors, edgecolor='black', alpha=0.8)
    axes[1, 0].set_title('Average Conversion Rate by Store', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('Conversion Rate (%)', fontsize=12)
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(store_metrics)))
    axes[1, 1].bar(store_metrics['Store'], store_metrics['Avg_Discount'],
                   color=colors, edgecolor='black', alpha=0.8)
    axes[1, 1].set_title('Average Discount by Store', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('Discount (%)', fontsize=12)
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '06_store_performance_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved: 06_store_performance_analysis.png")

def chart7_discount_impact(df, output_dir):
    """Discount impact"""
    print("\n7. Creating discount impact analysis...")
    
    discount_analysis = df.groupby('DiscountSegment').agg({
        'NETAMT': ['sum', 'mean'],
        'Qty': ['sum', 'mean']
    }).reset_index()
    discount_analysis.columns = ['DiscountSegment', 'Total_Revenue', 'Avg_Transaction', 'Total_Qty', 'Avg_Qty']
    
    segment_order = ['No Discount', 'Low Discount', 'Medium Discount', 'High Discount']
    discount_analysis['DiscountSegment'] = pd.Categorical(discount_analysis['DiscountSegment'], 
                                                           categories=segment_order, ordered=True)
    discount_analysis = discount_analysis.sort_values('DiscountSegment')
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    axes[0].bar(discount_analysis['DiscountSegment'], discount_analysis['Total_Revenue'],
                edgecolor='black', alpha=0.8, color=colors)
    axes[0].set_title('Total Revenue by Discount Segment', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Revenue ($)', fontsize=12)
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(True, alpha=0.3, axis='y')
    
    axes[1].bar(discount_analysis['DiscountSegment'], discount_analysis['Avg_Qty'],
                color=colors, edgecolor='black', alpha=0.8)
    axes[1].set_title('Average Quantity Sold by Discount Segment', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Average Quantity', fontsize=12)
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '07_discount_impact_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved: 07_discount_impact_analysis.png")

def chart8_correlation_matrix(df, output_dir):
    """Correlation matrix"""
    print("\n8. Creating correlation matrix...")
    
    numeric_cols = ['MRP', 'SellingPrice', 'Qty', 'NETAMT', 'DiscountPct', 
                    'ConversionPct', 'Footfall', 'AvgUnitPrice']
    correlation_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='RdYlBu_r', 
                center=0, square=True, linewidths=2, cbar_kws={'shrink': 0.8},
                annot_kws={'fontsize': 11, 'fontweight': 'bold'})
    plt.title('Correlation Matrix of Key Metrics', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '08_correlation_matrix.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved: 08_correlation_matrix.png")

def chart9_price_segment(df, output_dir):
    """Price segment analysis"""
    print("\n9. Creating price segment analysis...")
    
    price_segment_analysis = df.groupby('PriceSegment').agg({
        'NETAMT': ['sum', 'mean', 'count'],
        'Qty': 'sum',
        'DiscountPct': 'mean'
    }).reset_index()
    price_segment_analysis.columns = ['PriceSegment', 'Total_Revenue', 'Avg_Transaction', 
                                      'Transaction_Count', 'Total_Qty', 'Avg_Discount']
    
    segment_order = ['Budget', 'Economy', 'Mid-Range', 'Premium']
    price_segment_analysis['PriceSegment'] = pd.Categorical(price_segment_analysis['PriceSegment'],
                                                            categories=segment_order, ordered=True)
    price_segment_analysis = price_segment_analysis.sort_values('PriceSegment')
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    colors = ['#95a5a6', '#3498db', '#2ecc71', '#f39c12']
    axes[0, 0].bar(price_segment_analysis['PriceSegment'], price_segment_analysis['Total_Revenue'],
                   edgecolor='black', alpha=0.8, color=colors)
    axes[0, 0].set_title('Total Revenue by Price Segment', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('Revenue ($)', fontsize=12)
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    axes[0, 1].bar(price_segment_analysis['PriceSegment'], price_segment_analysis['Transaction_Count'],
                   color=colors, edgecolor='black', alpha=0.8)
    axes[0, 1].set_title('Transaction Count by Price Segment', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('Number of Transactions', fontsize=12)
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    axes[1, 0].bar(price_segment_analysis['PriceSegment'], price_segment_analysis['Avg_Transaction'],
                   color=colors, edgecolor='black', alpha=0.8)
    axes[1, 0].set_title('Average Transaction Value by Price Segment', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('Avg Transaction ($)', fontsize=12)
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    axes[1, 1].bar(price_segment_analysis['PriceSegment'], price_segment_analysis['Avg_Discount'],
                   color=colors, edgecolor='black', alpha=0.8)
    axes[1, 1].set_title('Average Discount by Price Segment', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('Discount (%)', fontsize=12)
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '09_price_segment_analysis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved: 09_price_segment_analysis.png")

def chart10_executive_dashboard(df, output_dir):
    """Executive dashboard summary"""
    print("\n10. Creating executive dashboard summary...")
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # KPI Cards
    kpi_data = [
        ('Total Revenue', f"${df['NETAMT'].sum()/1e9:.2f}B", '#3498db'),
        ('Transactions', f"{len(df):,}", '#2ecc71'),
        ('Avg Transaction', f"${df['NETAMT'].mean():,.0f}", '#f39c12'),
        ('Units Sold', f"{df['Qty'].sum():,}", '#e74c3c'),
        ('Avg Discount', f"{df['DiscountPct'].mean():.1f}%", '#9b59b6'),
        ('Conversion Rate', f"{df['ConversionPct'].mean():.1f}%", '#1abc9c')
    ]
    
    for i, (label, value, color) in enumerate(kpi_data):
        ax = fig.add_subplot(gs[i // 3, i % 3])
        ax.text(0.5, 0.6, value, ha='center', va='center', fontsize=32, fontweight='bold', color=color)
        ax.text(0.5, 0.3, label, ha='center', va='center', fontsize=14, color='#34495e')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.add_patch(plt.Rectangle((0.05, 0.1), 0.9, 0.8, fill=False, edgecolor=color, linewidth=3))
    
    # Category pie chart
    ax = fig.add_subplot(gs[2, :2])
    category_revenue = df.groupby('Category')['NETAMT'].sum().sort_values(ascending=False)
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    ax.pie(category_revenue.values, labels=category_revenue.index, autopct='%1.1f%%',
           startangle=90, colors=colors, textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_title('Revenue by Category', fontsize=12, fontweight='bold')
    
    # Top stores
    ax = fig.add_subplot(gs[2, 2])
    store_revenue = df.groupby('Store')['NETAMT'].sum().sort_values(ascending=False).head(5)
    ax.barh(range(len(store_revenue)), store_revenue.values, color='#3498db', alpha=0.7, edgecolor='black')
    ax.set_yticks(range(len(store_revenue)))
    ax.set_yticklabels(store_revenue.index, fontsize=10)
    ax.set_title('Top Stores', fontsize=12, fontweight='bold')
    ax.invert_yaxis()
    
    fig.suptitle('Retail Analytics - Executive Dashboard', fontsize=18, fontweight='bold', y=0.98)
    plt.savefig(os.path.join(output_dir, '10_executive_dashboard.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✓ Saved: 10_executive_dashboard.png")

def main():
    """Main execution"""
    print("="*60)
    print("GENERATING VISUALIZATIONS FOR RETAIL ANALYTICS")
    print("="*60)
    
    df = load_data()
    output_dir = create_output_dir()
    
    chart1_univariate_distributions(df, output_dir)
    chart2_category_revenue(df, output_dir)
    chart3_top_subcategories(df, output_dir)
    chart4_time_series(df, output_dir)
    chart5_day_of_week(df, output_dir)
    chart6_store_performance(df, output_dir)
    chart7_discount_impact(df, output_dir)
    chart8_correlation_matrix(df, output_dir)
    chart9_price_segment(df, output_dir)
    chart10_executive_dashboard(df, output_dir)
    
    print("\n" + "="*60)
    print("ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
    print("="*60)
    print(f"\nLocation: {output_dir}")
    print("\nGenerated 10 professional charts:")
    print("  1. Univariate Distributions")
    print("  2. Category Revenue Analysis")
    print("  3. Top SubCategories")
    print("  4. Time Series Analysis")
    print("  5. Day of Week Analysis")
    print("  6. Store Performance")
    print("  7. Discount Impact")
    print("  8. Correlation Matrix")
    print("  9. Price Segment Analysis")
    print(" 10. Executive Dashboard")

if __name__ == "__main__":
    main()
