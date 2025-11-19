"""
Executive Summary & KPI Analysis Script
Generates high-level metrics and financial analysis for leadership
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("💼 Starting Executive Summary Analysis...")
print("=" * 60)

# Load datasets
print("\n📂 Loading datasets...")
df_transactions = pd.read_csv('data/raw/sales_transactions.csv')
df_products = pd.read_csv('data/raw/products.csv')
df_inventory = pd.read_csv('data/raw/inventory.csv')
df_customers = pd.read_csv('data/raw/customers.csv')

df_transactions['Date'] = pd.to_datetime(df_transactions['Date'])

print(f"✓ Loaded {len(df_transactions):,} transactions")
print(f"✓ Loaded {len(df_products):,} products")
print(f"✓ Loaded {len(df_inventory):,} inventory records")
print(f"✓ Loaded {len(df_customers):,} customers")

# Merge transactions with products
df_sales = df_transactions.merge(df_products[['ProductID', 'Cost', 'Category', 'Margin']], on='ProductID', how='left')

# ============================================================================
# 1. FINANCIAL OVERVIEW
# ============================================================================
print("\n💰 Calculating Financial Metrics...")

# Revenue metrics
total_revenue = df_sales['TotalAmount'].sum()
total_cogs = (df_sales['Quantity'] * df_sales['Cost']).sum()
gross_profit = total_revenue - total_cogs
gross_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0

# Operating expenses (estimated at 30% of revenue for retail)
operating_expenses = total_revenue * 0.30
operating_profit = gross_profit - operating_expenses
operating_margin = (operating_profit / total_revenue * 100) if total_revenue > 0 else 0

# Net profit (after 25% tax)
net_profit = operating_profit * 0.75
net_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0

# EBITDA (Operating Profit + Depreciation, assume 2% of revenue)
depreciation = total_revenue * 0.02
ebitda = operating_profit + depreciation

print(f"\n💵 Financial Overview:")
print(f"  Total Revenue: ${total_revenue:,.2f}")
print(f"  Cost of Goods Sold: ${total_cogs:,.2f}")
print(f"  Gross Profit: ${gross_profit:,.2f}")
print(f"  Gross Margin: {gross_margin:.2f}%")
print(f"  Operating Expenses: ${operating_expenses:,.2f}")
print(f"  Operating Profit: ${operating_profit:,.2f}")
print(f"  Operating Margin: {operating_margin:.2f}%")
print(f"  Net Profit: ${net_profit:,.2f}")
print(f"  Net Margin: {net_margin:.2f}%")
print(f"  EBITDA: ${ebitda:,.2f}")

# ============================================================================
# 2. KEY PERFORMANCE INDICATORS
# ============================================================================
print("\n📊 Calculating Key Performance Indicators...")

# Sales KPIs
total_transactions = len(df_sales)
total_units_sold = df_sales['Quantity'].sum()
avg_transaction_value = df_sales['TotalAmount'].mean()
unique_customers = df_sales[~df_sales['CustomerID'].str.startswith('GUEST')]['CustomerID'].nunique()

# Inventory KPIs
total_inventory_value = df_inventory['StockValue'].sum()
inventory_turnover = (total_cogs / total_inventory_value) if total_inventory_value > 0 else 0

# Customer KPIs
customer_acquisition_cost = operating_expenses * 0.15 / len(df_customers)  # 15% of opex on marketing
avg_clv = total_revenue / unique_customers if unique_customers > 0 else 0
clv_cac_ratio = avg_clv / customer_acquisition_cost if customer_acquisition_cost > 0 else 0

print(f"\n🎯 Key Performance Indicators:")
print(f"  Total Transactions: {total_transactions:,}")
print(f"  Total Units Sold: {total_units_sold:,}")
print(f"  Avg Transaction Value: ${avg_transaction_value:.2f}")
print(f"  Active Customers: {unique_customers:,}")
print(f"  Inventory Turnover: {inventory_turnover:.2f}x")
print(f"  Customer Acquisition Cost: ${customer_acquisition_cost:.2f}")
print(f"  Avg Customer Lifetime Value: ${avg_clv:.2f}")
print(f"  CLV/CAC Ratio: {clv_cac_ratio:.2f}x")

# ============================================================================
# 3. YEAR-OVER-YEAR COMPARISON
# ============================================================================
print("\n📈 Analyzing Year-over-Year Growth...")

df_sales['Year'] = df_sales['Date'].dt.year

yearly_comparison = df_sales.groupby('Year').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'nunique',
    'Quantity': 'sum'
}).reset_index()

yearly_comparison.columns = ['Year', 'Revenue', 'Transactions', 'UnitsSold']

# Calculate YoY growth
if len(yearly_comparison) > 1:
    revenue_2023 = yearly_comparison[yearly_comparison['Year'] == 2023]['Revenue'].values[0]
    revenue_2024 = yearly_comparison[yearly_comparison['Year'] == 2024]['Revenue'].values[0]
    revenue_growth = ((revenue_2024 - revenue_2023) / revenue_2023 * 100)
    
    trans_2023 = yearly_comparison[yearly_comparison['Year'] == 2023]['Transactions'].values[0]
    trans_2024 = yearly_comparison[yearly_comparison['Year'] == 2024]['Transactions'].values[0]
    trans_growth = ((trans_2024 - trans_2023) / trans_2023 * 100)
    
    print(f"\nYear-over-Year Performance:")
    print(f"  2023 Revenue: ${revenue_2023:,.2f}")
    print(f"  2024 Revenue: ${revenue_2024:,.2f}")
    print(f"  Revenue Growth: {revenue_growth:+.2f}%")
    print(f"  Transaction Growth: {trans_growth:+.2f}%")

# ============================================================================
# 4. QUARTERLY PERFORMANCE
# ============================================================================
print("\n📅 Analyzing Quarterly Performance...")

df_sales['Quarter'] = df_sales['Date'].dt.quarter
df_sales['YearQuarter'] = df_sales['Year'].astype(str) + '-Q' + df_sales['Quarter'].astype(str)

quarterly_performance = df_sales.groupby('YearQuarter').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'nunique',
    'Quantity': 'sum'
}).reset_index()

quarterly_performance.columns = ['Quarter', 'Revenue', 'Transactions', 'UnitsSold']

print(f"\nQuarterly Performance:")
for _, row in quarterly_performance.iterrows():
    print(f"  {row['Quarter']}: ${row['Revenue']:,.2f} | {row['Transactions']:,} transactions")

# ============================================================================
# 5. CATEGORY CONTRIBUTION
# ============================================================================
print("\n📦 Analyzing Category Contribution to Revenue...")

category_financial = df_sales.groupby('Category').agg({
    'TotalAmount': 'sum',
    'Cost': lambda x: (df_sales.loc[x.index, 'Quantity'] * x).sum(),
    'Quantity': 'sum'
}).reset_index()

category_financial.columns = ['Category', 'Revenue', 'COGS', 'UnitsSold']
category_financial['GrossProfit'] = category_financial['Revenue'] - category_financial['COGS']
category_financial['GrossMargin'] = (category_financial['GrossProfit'] / category_financial['Revenue'] * 100).round(2)
category_financial['RevenueShare'] = (category_financial['Revenue'] / total_revenue * 100).round(2)
category_financial = category_financial.sort_values('Revenue', ascending=False)

print(f"\nCategory Financial Performance:")
for _, row in category_financial.iterrows():
    print(f"  {row['Category']}: ${row['Revenue']:,.2f} ({row['RevenueShare']:.1f}%) | "
          f"Margin: {row['GrossMargin']:.1f}%")

# ============================================================================
# 6. CHANNEL CONTRIBUTION
# ============================================================================
print("\n🌐 Analyzing Channel Performance...")

channel_financial = df_sales.groupby('Channel').agg({
    'TotalAmount': 'sum',
    'TransactionID': 'nunique'
}).reset_index()

channel_financial.columns = ['Channel', 'Revenue', 'Transactions']
channel_financial['RevenueShare'] = (channel_financial['Revenue'] / total_revenue * 100).round(2)
channel_financial['AvgTransactionValue'] = (channel_financial['Revenue'] / channel_financial['Transactions']).round(2)

print(f"\nChannel Financial Performance:")
for _, row in channel_financial.iterrows():
    print(f"  {row['Channel']}: ${row['Revenue']:,.2f} ({row['RevenueShare']:.1f}%) | "
          f"ATV: ${row['AvgTransactionValue']:.2f}")

# ============================================================================
# 7. PROFITABILITY TRENDS
# ============================================================================
print("\n💹 Analyzing Profitability Trends...")

df_sales['YearMonth'] = df_sales['Date'].dt.to_period('M')

monthly_profitability = df_sales.groupby('YearMonth').agg({
    'TotalAmount': 'sum',
    'Cost': lambda x: (df_sales.loc[x.index, 'Quantity'] * x).sum()
}).reset_index()

monthly_profitability.columns = ['YearMonth', 'Revenue', 'COGS']
monthly_profitability['GrossProfit'] = monthly_profitability['Revenue'] - monthly_profitability['COGS']
monthly_profitability['GrossMargin'] = (monthly_profitability['GrossProfit'] / monthly_profitability['Revenue'] * 100).round(2)
monthly_profitability['YearMonth'] = monthly_profitability['YearMonth'].astype(str)

print(f"\n✓ Calculated monthly profitability for {len(monthly_profitability)} months")
print(f"  Avg Monthly Revenue: ${monthly_profitability['Revenue'].mean():,.2f}")
print(f"  Avg Monthly Gross Profit: ${monthly_profitability['GrossProfit'].mean():,.2f}")
print(f"  Avg Gross Margin: {monthly_profitability['GrossMargin'].mean():.2f}%")

# ============================================================================
# 8. FORECAST (Simple Linear Projection)
# ============================================================================
print("\n🔮 Generating Revenue Forecast...")

# Calculate average monthly growth rate
monthly_revenue = df_sales.groupby('YearMonth')['TotalAmount'].sum().reset_index()
monthly_revenue['MonthNum'] = range(len(monthly_revenue))

# Simple linear regression for forecast
from numpy import polyfit, poly1d
x = monthly_revenue['MonthNum'].values
y = monthly_revenue['TotalAmount'].values
z = polyfit(x, y, 1)
p = poly1d(z)

# Forecast next 6 months
forecast_months = []
for i in range(1, 7):
    next_month = len(monthly_revenue) + i
    forecasted_revenue = p(next_month)
    forecast_months.append({
        'Month': f'Forecast Month {i}',
        'ForecastedRevenue': round(forecasted_revenue, 2)
    })

df_forecast = pd.DataFrame(forecast_months)

print(f"\n6-Month Revenue Forecast:")
for _, row in df_forecast.iterrows():
    print(f"  {row['Month']}: ${row['ForecastedRevenue']:,.2f}")

total_forecast_6m = df_forecast['ForecastedRevenue'].sum()
print(f"  Total 6-Month Forecast: ${total_forecast_6m:,.2f}")

# ============================================================================
# 9. MARKET SHARE (Simulated)
# ============================================================================
print("\n📍 Estimating Market Position...")

# Simulate market size (assume we have 8-12% share)
estimated_market_size = total_revenue / 0.10  # Assume 10% market share
market_growth_rate = 12.5  # Industry growing at 12.5%

print(f"\nMarket Position Estimates:")
print(f"  Our Revenue: ${total_revenue:,.2f}")
print(f"  Estimated Market Size: ${estimated_market_size:,.2f}")
print(f"  Estimated Market Share: 10.0%")
print(f"  Industry Growth Rate: {market_growth_rate}%")

# ============================================================================
# 10. EXECUTIVE SCORECARD
# ============================================================================
print("\n🎯 Creating Executive Scorecard...")

def get_status(value, target, direction='higher'):
    """Determine status: Green (Good), Yellow (Warning), Red (Critical)"""
    if direction == 'higher':
        if value >= target:
            return 'Green'
        elif value >= target * 0.9:
            return 'Yellow'
        else:
            return 'Red'
    else:  # lower is better
        if value <= target:
            return 'Green'
        elif value <= target * 1.1:
            return 'Yellow'
        else:
            return 'Red'

scorecard = [
    {'KPI': 'Gross Margin %', 'Actual': gross_margin, 'Target': 45.0, 'Status': get_status(gross_margin, 45.0, 'higher')},
    {'KPI': 'Net Margin %', 'Actual': net_margin, 'Target': 15.0, 'Status': get_status(net_margin, 15.0, 'higher')},
    {'KPI': 'Inventory Turnover', 'Actual': inventory_turnover, 'Target': 5.0, 'Status': get_status(inventory_turnover, 5.0, 'higher')},
    {'KPI': 'CLV/CAC Ratio', 'Actual': clv_cac_ratio, 'Target': 5.0, 'Status': get_status(clv_cac_ratio, 5.0, 'higher')},
    {'KPI': 'Avg Transaction Value', 'Actual': avg_transaction_value, 'Target': 45.0, 'Status': get_status(avg_transaction_value, 45.0, 'higher')},
]

df_scorecard = pd.DataFrame(scorecard)

print(f"\nExecutive Scorecard:")
for _, row in df_scorecard.iterrows():
    status_icon = '🟢' if row['Status'] == 'Green' else ('🟡' if row['Status'] == 'Yellow' else '🔴')
    print(f"  {status_icon} {row['KPI']}: {row['Actual']:.2f} (Target: {row['Target']:.2f})")

# ============================================================================
# SAVE PROCESSED DATA
# ============================================================================
print("\n💾 Saving processed datasets...")

# Financial summary
financial_summary = pd.DataFrame({
    'Metric': ['Total Revenue', 'COGS', 'Gross Profit', 'Gross Margin %', 
               'Operating Expenses', 'Operating Profit', 'Operating Margin %',
               'Net Profit', 'Net Margin %', 'EBITDA'],
    'Value': [total_revenue, total_cogs, gross_profit, gross_margin,
              operating_expenses, operating_profit, operating_margin,
              net_profit, net_margin, ebitda]
})
financial_summary.to_csv('data/processed/financial_summary.csv', index=False)
print("✓ Saved financial_summary.csv")

# KPI summary
kpi_summary = pd.DataFrame({
    'KPI': ['Total Transactions', 'Total Units Sold', 'Avg Transaction Value',
            'Active Customers', 'Inventory Turnover', 'Customer Acquisition Cost',
            'Avg Customer Lifetime Value', 'CLV/CAC Ratio'],
    'Value': [total_transactions, total_units_sold, avg_transaction_value,
              unique_customers, inventory_turnover, customer_acquisition_cost,
              avg_clv, clv_cac_ratio]
})
kpi_summary.to_csv('data/processed/kpi_summary.csv', index=False)
print("✓ Saved kpi_summary.csv")

# Yearly comparison
yearly_comparison.to_csv('data/processed/yearly_comparison.csv', index=False)
print("✓ Saved yearly_comparison.csv")

# Quarterly performance
quarterly_performance.to_csv('data/processed/quarterly_performance.csv', index=False)
print("✓ Saved quarterly_performance.csv")

# Category financial
category_financial.to_csv('data/processed/category_financial.csv', index=False)
print("✓ Saved category_financial.csv")

# Channel financial
channel_financial.to_csv('data/processed/channel_financial.csv', index=False)
print("✓ Saved channel_financial.csv")

# Monthly profitability
monthly_profitability.to_csv('data/processed/monthly_profitability.csv', index=False)
print("✓ Saved monthly_profitability.csv")

# Revenue forecast
df_forecast.to_csv('data/processed/revenue_forecast.csv', index=False)
print("✓ Saved revenue_forecast.csv")

# Executive scorecard
df_scorecard.to_csv('data/processed/executive_scorecard.csv', index=False)
print("✓ Saved executive_scorecard.csv")

print("\n" + "=" * 60)
print("✅ Executive Summary Analysis Complete!")
print("=" * 60)
print(f"\n📊 Executive Summary:")
print(f"  • Total Revenue: ${total_revenue:,.2f}")
print(f"  • Gross Margin: {gross_margin:.2f}%")
print(f"  • Net Profit: ${net_profit:,.2f} ({net_margin:.2f}%)")
print(f"  • EBITDA: ${ebitda:,.2f}")
print(f"  • 6-Month Forecast: ${total_forecast_6m:,.2f}")
if len(yearly_comparison) > 1:
    print(f"  • YoY Revenue Growth: {revenue_growth:+.2f}%")
