"""
Convert Dashboard CSVs to JavaScript Data for Interactive Dashboard
"""

import pandas as pd
import json

print("=" * 60)
print("CONVERTING CSV TO JAVASCRIPT DATA")
print("=" * 60)
print()

# Load all dashboard CSVs
print("Loading dashboard data...")

# 1. Summary KPIs
kpis_df = pd.read_csv('dashboard/summary_kpis.csv')
kpis_data = dict(zip(kpis_df['Metric'], kpis_df['Value']))

# 2. Category Performance
category_df = pd.read_csv('dashboard/category_performance.csv')

# 3. Monthly Trends
monthly_df = pd.read_csv('dashboard/monthly_trends.csv')

# 4. Stock Ageing
stock_ageing_df = pd.read_csv('dashboard/stock_ageing_overall.csv')

# 5. POS Comparison
pos_df = pd.read_csv('dashboard/pos_comparison.csv')

# 6. SubCategory Performance
subcat_df = pd.read_csv('dashboard/subcategory_performance.csv')

# 7. Brand Performance
brand_df = pd.read_csv('dashboard/brand_performance.csv')

# 8. Margin Analysis
margin_df = pd.read_csv('dashboard/margin_analysis.csv')

print("✓ All data loaded")
print()

# Create JavaScript data file
js_content = """
// Grocery + Fashion Dashboard - Interactive Data
// Auto-generated from CSV files

const dashboardData = {
    
    // Key Performance Indicators
    kpis: {
"""

# Add KPIs
for metric, value in kpis_data.items():
    js_content += f'        "{metric}": "{value}",\n'

js_content += """    },
    
    // Category Performance
    categories: [
"""

for _, row in category_df.iterrows():
    js_content += f"""        {{
            name: "{row['Category']}",
            transactions: {row['Transactions']},
            revenue: {row['TotalRevenue']:.2f},
            avgRevenue: {row['AvgRevenue']:.2f},
            profit: {row['TotalProfit']:.2f},
            margin: {row['AvgMargin']:.2f},
            quantity: {row['TotalQuantity']},
            skus: {row['UniqueSKUs']}
        }},
"""

js_content += """    ],
    
    // Monthly Trends
    monthlyTrends: [
"""

for _, row in monthly_df.iterrows():
    js_content += f"""        {{
            month: "{row['YearMonth']}",
            category: "{row['Category']}",
            transactions: {row['Transactions']},
            revenue: {row['Revenue']:.2f},
            profit: {row['Profit']:.2f},
            quantity: {row['Quantity']}
        }},
"""

js_content += """    ],
    
    // Stock Ageing
    stockAgeing: [
"""

for _, row in stock_ageing_df.iterrows():
    js_content += f"""        {{
            category: "{row['StockAgeCategory']}",
            transactions: {row['Transactions']},
            revenue: {row['TotalRevenue']:.2f},
            quantity: {row['TotalQuantity']},
            avgAge: {row['AvgStockAge']:.2f}
        }},
"""

js_content += """    ],
    
    // POS Comparison
    posData: [
"""

for _, row in pos_df.iterrows():
    js_content += f"""        {{
            pos: "{row['POS_System']}",
            store: "{row['Store']}",
            transactions: {row['Transactions']},
            revenue: {row['TotalRevenue']:.2f},
            profit: {row['TotalProfit']:.2f},
            margin: {row['AvgMargin']:.2f},
            quantity: {row['TotalQuantity']},
            skus: {row['UniqueSKUs']}
        }},
"""

js_content += """    ],
    
    // SubCategory Performance
    subCategories: [
"""

for _, row in subcat_df.iterrows():
    js_content += f"""        {{
            category: "{row['Category']}",
            subCategory: "{row['SubCategory']}",
            transactions: {row['Transactions']},
            revenue: {row['TotalRevenue']:.2f},
            avgRevenue: {row['AvgRevenue']:.2f},
            profit: {row['TotalProfit']:.2f},
            margin: {row['AvgMargin']:.2f},
            quantity: {row['TotalQuantity']}
        }},
"""

js_content += """    ],
    
    // Top 10 Brands
    topBrands: [
"""

for _, row in brand_df.head(10).iterrows():
    js_content += f"""        {{
            category: "{row['Category']}",
            brand: "{row['Brand']}",
            transactions: {row['Transactions']},
            revenue: {row['TotalRevenue']:.2f},
            profit: {row['TotalProfit']:.2f},
            margin: {row['AvgMargin']:.2f},
            skus: {row['UniqueSKUs']}
        }},
"""

js_content += """    ],
    
    // Margin Analysis
    marginAnalysis: [
"""

for _, row in margin_df.iterrows():
    js_content += f"""        {{
            category: "{row['Category']}",
            subCategory: "{row['SubCategory']}",
            avgMargin: {row['AvgMargin']:.2f},
            minMargin: {row['MinMargin']:.2f},
            maxMargin: {row['MaxMargin']:.2f},
            profit: {row['TotalProfit']:.2f},
            revenue: {row['TotalRevenue']:.2f},
            profitMargin: {row['ProfitMargin%']:.2f}
        }},
"""

js_content += """    ]
};

// Export for use in HTML
if (typeof module !== 'undefined' && module.exports) {
    module.exports = dashboardData;
}
"""

# Save JavaScript file
with open('dashboard/dashboard_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("✓ Created: dashboard/dashboard_data.js")
print()
print("=" * 60)
print("CONVERSION COMPLETED!")
print("=" * 60)
print()
print("JavaScript data file ready for interactive dashboard!")
