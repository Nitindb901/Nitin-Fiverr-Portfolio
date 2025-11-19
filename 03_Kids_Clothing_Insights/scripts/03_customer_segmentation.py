"""
Customer Analytics & RFM Segmentation Script
Analyzes customer behavior and creates RFM segments
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("👥 Starting Customer Analytics & RFM Segmentation...")
print("=" * 60)

# Load datasets
print("\n📂 Loading datasets...")
df_customers = pd.read_csv('data/raw/customers.csv')
df_transactions = pd.read_csv('data/raw/sales_transactions.csv')

df_customers['SignupDate'] = pd.to_datetime(df_customers['SignupDate'])
df_transactions['Date'] = pd.to_datetime(df_transactions['Date'])

print(f"✓ Loaded {len(df_customers):,} customers")
print(f"✓ Loaded {len(df_transactions):,} transactions")

# Filter out guest purchases
df_transactions_registered = df_transactions[~df_transactions['CustomerID'].str.startswith('GUEST')]

print(f"✓ {len(df_transactions_registered):,} transactions from registered customers")

# ============================================================================
# 1. CUSTOMER PURCHASE BEHAVIOR
# ============================================================================
print("\n💳 Analyzing Customer Purchase Behavior...")

customer_behavior = df_transactions_registered.groupby('CustomerID').agg({
    'TransactionID': 'count',
    'TotalAmount': 'sum',
    'Date': ['min', 'max']
}).reset_index()

customer_behavior.columns = ['CustomerID', 'PurchaseCount', 'TotalSpend', 'FirstPurchase', 'LastPurchase']

# Merge with customer demographics
customer_behavior = customer_behavior.merge(df_customers[['CustomerID', 'City', 'State', 'SignupDate', 'Age', 'Gender']], 
                                            on='CustomerID', how='left')

# Calculate metrics
customer_behavior['AvgOrderValue'] = (customer_behavior['TotalSpend'] / customer_behavior['PurchaseCount']).round(2)
customer_behavior['CustomerTenure'] = ((datetime(2024, 12, 31) - customer_behavior['SignupDate']).dt.days).round(0)
customer_behavior['DaysSinceLastPurchase'] = ((datetime(2024, 12, 31) - customer_behavior['LastPurchase']).dt.days).round(0)

print(f"\n📊 Customer Behavior Summary:")
print(f"  Avg Purchase Count: {customer_behavior['PurchaseCount'].mean():.2f}")
print(f"  Avg Total Spend: ${customer_behavior['TotalSpend'].mean():,.2f}")
print(f"  Avg Order Value: ${customer_behavior['AvgOrderValue'].mean():.2f}")
print(f"  Avg Customer Tenure: {customer_behavior['CustomerTenure'].mean():.0f} days")

# ============================================================================
# 2. RFM ANALYSIS
# ============================================================================
print("\n🎯 Calculating RFM Scores...")

# Set analysis date
analysis_date = datetime(2024, 12, 31)

# Calculate RFM
rfm = df_transactions_registered.groupby('CustomerID').agg({
    'Date': lambda x: (analysis_date - x.max()).days,  # Recency
    'TransactionID': 'count',  # Frequency
    'TotalAmount': 'sum'  # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

print(f"\nRFM Statistics:")
print(f"  Avg Recency: {rfm['Recency'].mean():.1f} days")
print(f"  Avg Frequency: {rfm['Frequency'].mean():.2f} purchases")
print(f"  Avg Monetary: ${rfm['Monetary'].mean():,.2f}")

# Calculate RFM scores (1-5 scale)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])  # Lower recency = better
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

# Convert to numeric
rfm['R_Score'] = rfm['R_Score'].astype(int)
rfm['F_Score'] = rfm['F_Score'].astype(int)
rfm['M_Score'] = rfm['M_Score'].astype(int)

# Calculate RFM Score
rfm['RFM_Score'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']
rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

print(f"✓ Calculated RFM scores for {len(rfm):,} customers")

# ============================================================================
# 3. CUSTOMER SEGMENTATION
# ============================================================================
print("\n🏷️ Creating Customer Segments...")

def segment_customer(row):
    """Segment customers based on RFM scores"""
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    
    # Champions: High R, F, M
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    
    # Loyal Customers: High F, decent R and M
    elif f >= 4 and r >= 3 and m >= 3:
        return 'Loyal Customers'
    
    # Potential Loyalists: Recent customers with good frequency
    elif r >= 4 and f >= 2 and m >= 2:
        return 'Potential Loyalists'
    
    # Recent Customers: Very recent but low frequency
    elif r >= 4 and f <= 2:
        return 'Recent Customers'
    
    # Promising: Mid-level on all scores
    elif r >= 3 and f >= 2 and m >= 2:
        return 'Promising'
    
    # Need Attention: Declining engagement
    elif r >= 2 and f >= 2:
        return 'Need Attention'
    
    # At Risk: Used to be good, declining
    elif r <= 2 and f >= 3:
        return 'At Risk'
    
    # Cannot Lose: High spenders who haven't returned
    elif r <= 2 and m >= 4:
        return 'Cannot Lose Them'
    
    # Hibernating: Low recent activity but some history
    elif r <= 2 and f <= 2 and m >= 2:
        return 'Hibernating'
    
    # Lost: Very low engagement
    else:
        return 'Lost'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

# Segment statistics
segment_stats = rfm.groupby('Segment').agg({
    'CustomerID': 'count',
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean'
}).round(2)

segment_stats.columns = ['CustomerCount', 'AvgRecency', 'AvgFrequency', 'AvgMonetary']
segment_stats = segment_stats.reset_index()
segment_stats['CustomerShare'] = (segment_stats['CustomerCount'] / len(rfm) * 100).round(2)
segment_stats = segment_stats.sort_values('CustomerCount', ascending=False)

print(f"\n📊 Customer Segments:")
for _, row in segment_stats.iterrows():
    print(f"  {row['Segment']}: {row['CustomerCount']:,} customers ({row['CustomerShare']:.1f}%) | Avg Spend: ${row['AvgMonetary']:,.2f}")

# ============================================================================
# 4. CUSTOMER LIFETIME VALUE (CLV)
# ============================================================================
print("\n💰 Calculating Customer Lifetime Value...")

# Merge RFM with behavior data
customer_full = rfm.merge(customer_behavior, on='CustomerID', how='left')

# Calculate CLV components
customer_full['AvgPurchaseFrequency'] = customer_full['Frequency'] / (customer_full['CustomerTenure'] / 365)
customer_full['CustomerLifespan'] = 3.0  # Assume 3 years average lifespan
customer_full['CLV'] = (customer_full['AvgOrderValue'] * 
                        customer_full['AvgPurchaseFrequency'] * 
                        customer_full['CustomerLifespan']).round(2)

print(f"\nCLV Statistics:")
print(f"  Avg CLV: ${customer_full['CLV'].mean():,.2f}")
print(f"  Median CLV: ${customer_full['CLV'].median():,.2f}")
print(f"  Max CLV: ${customer_full['CLV'].max():,.2f}")

# CLV by segment
clv_by_segment = customer_full.groupby('Segment')['CLV'].agg(['mean', 'median', 'count']).round(2)
clv_by_segment.columns = ['AvgCLV', 'MedianCLV', 'CustomerCount']
clv_by_segment = clv_by_segment.reset_index().sort_values('AvgCLV', ascending=False)

print(f"\nCLV by Segment:")
for _, row in clv_by_segment.head(5).iterrows():
    print(f"  {row['Segment']}: ${row['AvgCLV']:,.2f}")

# ============================================================================
# 5. REPEAT PURCHASE ANALYSIS
# ============================================================================
print("\n🔄 Analyzing Repeat Purchase Behavior...")

# Identify repeat customers
customer_full['IsRepeatCustomer'] = customer_full['PurchaseCount'] > 1
repeat_rate = (customer_full['IsRepeatCustomer'].sum() / len(customer_full) * 100).round(2)

print(f"\nRepeat Purchase Rate: {repeat_rate:.2f}%")

# Repeat vs One-time customers
repeat_comparison = customer_full.groupby('IsRepeatCustomer').agg({
    'CustomerID': 'count',
    'TotalSpend': 'mean',
    'AvgOrderValue': 'mean',
    'CLV': 'mean'
}).round(2)

repeat_comparison.columns = ['CustomerCount', 'AvgTotalSpend', 'AvgOrderValue', 'AvgCLV']
repeat_comparison.index = ['One-time', 'Repeat']

print(f"\nOne-time vs Repeat Customers:")
for customer_type in repeat_comparison.index:
    row = repeat_comparison.loc[customer_type]
    print(f"  {customer_type}: {row['CustomerCount']:,} customers | Avg Spend: ${row['AvgTotalSpend']:,.2f} | CLV: ${row['AvgCLV']:,.2f}")

# ============================================================================
# 6. GEOGRAPHIC ANALYSIS
# ============================================================================
print("\n🗺️ Analyzing Geographic Distribution...")

geo_analysis = customer_full.groupby(['State', 'City']).agg({
    'CustomerID': 'count',
    'TotalSpend': 'sum',
    'CLV': 'mean'
}).round(2)

geo_analysis.columns = ['CustomerCount', 'TotalRevenue', 'AvgCLV']
geo_analysis = geo_analysis.reset_index().sort_values('TotalRevenue', ascending=False)

print(f"\nTop 10 Cities by Revenue:")
for idx, row in geo_analysis.head(10).iterrows():
    print(f"  {row['City']}, {row['State']}: {row['CustomerCount']:,} customers | ${row['TotalRevenue']:,.2f}")

# ============================================================================
# 7. DEMOGRAPHIC ANALYSIS
# ============================================================================
print("\n👤 Analyzing Customer Demographics...")

# Age group analysis
customer_full['AgeGroup'] = pd.cut(customer_full['Age'], 
                                   bins=[0, 25, 35, 45, 100], 
                                   labels=['18-25', '26-35', '36-45', '46+'])

age_analysis = customer_full.groupby('AgeGroup').agg({
    'CustomerID': 'count',
    'TotalSpend': 'mean',
    'PurchaseCount': 'mean',
    'CLV': 'mean'
}).round(2)

age_analysis.columns = ['CustomerCount', 'AvgSpend', 'AvgPurchases', 'AvgCLV']
age_analysis = age_analysis.reset_index()

print(f"\nAge Group Analysis:")
for _, row in age_analysis.iterrows():
    print(f"  {row['AgeGroup']}: {row['CustomerCount']:,} customers | Avg Spend: ${row['AvgSpend']:,.2f} | CLV: ${row['AvgCLV']:,.2f}")

# Gender analysis
gender_analysis = customer_full.groupby('Gender').agg({
    'CustomerID': 'count',
    'TotalSpend': 'mean',
    'PurchaseCount': 'mean',
    'CLV': 'mean'
}).round(2)

gender_analysis.columns = ['CustomerCount', 'AvgSpend', 'AvgPurchases', 'AvgCLV']
gender_analysis = gender_analysis.reset_index()

print(f"\nGender Analysis:")
for _, row in gender_analysis.iterrows():
    print(f"  {row['Gender']}: {row['CustomerCount']:,} customers | Avg Spend: ${row['AvgSpend']:,.2f}")

# ============================================================================
# 8. COHORT ANALYSIS
# ============================================================================
print("\n📅 Performing Cohort Analysis...")

# Create cohort based on signup month
customer_full['CohortMonth'] = customer_full['SignupDate'].dt.to_period('M')

# Calculate months since signup
cohort_data = []
for cohort in customer_full['CohortMonth'].unique():
    cohort_customers = customer_full[customer_full['CohortMonth'] == cohort]['CustomerID'].tolist()
    
    # Count active customers in each subsequent month
    for month_offset in range(0, 13):  # 12 months
        target_date = cohort.to_timestamp() + pd.DateOffset(months=month_offset)
        
        active = df_transactions_registered[
            (df_transactions_registered['CustomerID'].isin(cohort_customers)) &
            (df_transactions_registered['Date'].dt.to_period('M') == target_date.to_period('M'))
        ]['CustomerID'].nunique()
        
        cohort_data.append({
            'Cohort': str(cohort),
            'MonthOffset': month_offset,
            'ActiveCustomers': active
        })

df_cohort = pd.DataFrame(cohort_data)

# Calculate retention rates
cohort_sizes = df_cohort[df_cohort['MonthOffset'] == 0].set_index('Cohort')['ActiveCustomers']
df_cohort['CohortSize'] = df_cohort['Cohort'].map(cohort_sizes)
df_cohort['RetentionRate'] = (df_cohort['ActiveCustomers'] / df_cohort['CohortSize'] * 100).round(2)

print(f"✓ Calculated retention rates for {df_cohort['Cohort'].nunique()} cohorts")

# ============================================================================
# SAVE PROCESSED DATA
# ============================================================================
print("\n💾 Saving processed datasets...")

# RFM with segments
rfm_export = rfm.merge(customer_full[['CustomerID', 'City', 'State', 'Age', 'Gender', 'CLV', 'TotalSpend', 'PurchaseCount']], 
                       on='CustomerID', how='left')
rfm_export.to_csv('data/processed/customer_rfm.csv', index=False)
print("✓ Saved customer_rfm.csv")

# Segment statistics
segment_stats.to_csv('data/processed/customer_segments.csv', index=False)
print("✓ Saved customer_segments.csv")

# CLV analysis
clv_by_segment.to_csv('data/processed/clv_by_segment.csv', index=False)
print("✓ Saved clv_by_segment.csv")

# Geographic analysis
geo_analysis.to_csv('data/processed/customer_geography.csv', index=False)
print("✓ Saved customer_geography.csv")

# Demographic analysis
age_analysis.to_csv('data/processed/customer_demographics_age.csv', index=False)
gender_analysis.to_csv('data/processed/customer_demographics_gender.csv', index=False)
print("✓ Saved demographic analysis files")

# Cohort analysis
df_cohort.to_csv('data/processed/cohort_analysis.csv', index=False)
print("✓ Saved cohort_analysis.csv")

# Repeat customer analysis
repeat_comparison.to_csv('data/processed/repeat_customer_analysis.csv')
print("✓ Saved repeat_customer_analysis.csv")

print("\n" + "=" * 60)
print("✅ Customer Analytics Complete!")
print("=" * 60)
print(f"\n📊 Key Insights:")
print(f"  • Champions: {segment_stats[segment_stats['Segment']=='Champions']['CustomerCount'].values[0] if 'Champions' in segment_stats['Segment'].values else 0:,} customers")
print(f"  • Avg CLV: ${customer_full['CLV'].mean():,.2f}")
print(f"  • Repeat Purchase Rate: {repeat_rate:.1f}%")
print(f"  • Top City: {geo_analysis.iloc[0]['City']}, {geo_analysis.iloc[0]['State']}")
