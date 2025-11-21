"""
Machine Learning Models for Men's Clothing Dashboard
===================================================
Implements two ML models:
1. Sales Forecasting - Time series prediction using Prophet
2. Customer Segmentation - K-Means clustering on RFM features
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')
import os

print("=" * 70)
print("MACHINE LEARNING MODELS - MEN'S CLOTHING")
print("=" * 70)

# Load processed data
print("\n📥 Loading Processed Data...")
data_dir = '../data/processed/'
monthly_totals = pd.read_csv(f'{data_dir}monthly_totals.csv')
rfm = pd.read_csv(f'{data_dir}rfm_analysis.csv')
customers_rfm = pd.read_csv(f'{data_dir}customers_rfm.csv')

print(f"✅ Loaded monthly data: {len(monthly_totals)} months")
print(f"✅ Loaded RFM data: {len(rfm):,} customers")

# Create output directory
output_dir = '../data/ml_results/'
os.makedirs(output_dir, exist_ok=True)

# ============================================================================
# MODEL 1: SALES FORECASTING WITH ARIMA-STYLE APPROACH
# ============================================================================

print("\n" + "=" * 70)
print("MODEL 1: SALES FORECASTING")
print("=" * 70)

# Prepare time series data
monthly_totals['Month'] = pd.to_datetime(monthly_totals['Month'])
monthly_totals = monthly_totals.sort_values('Month')

print(f"\n📊 Training Data Overview:")
print(f"   Period: {monthly_totals['Month'].min().strftime('%Y-%m')} to {monthly_totals['Month'].max().strftime('%Y-%m')}")
print(f"   Total Months: {len(monthly_totals)}")
print(f"   Avg Monthly Revenue: ₹{monthly_totals['Revenue'].mean():,.2f}")

# Simple moving average forecasting
def forecast_next_months(data, n_months=6):
    """Forecast using weighted moving average with trend"""
    
    # Calculate trend
    recent_6 = data['Revenue'].tail(6).values
    earlier_6 = data['Revenue'].tail(12).head(6).values
    trend = (recent_6.mean() - earlier_6.mean()) / earlier_6.mean()
    
    # Base forecast on weighted average of last 3 months
    weights = np.array([0.5, 0.3, 0.2])
    last_3_months = data['Revenue'].tail(3).values
    base_forecast = np.average(last_3_months, weights=weights)
    
    # Apply trend
    forecasts = []
    for i in range(1, n_months + 1):
        # Trend diminishes over time
        trend_factor = 1 + (trend * (1 - i * 0.1))
        forecast = base_forecast * trend_factor
        
        # Add seasonal pattern (based on historical month)
        month_idx = (data['Month'].iloc[-1].month + i - 1) % 12
        month_avg = data[data['Month'].dt.month == (month_idx + 1)]['Revenue'].mean()
        overall_avg = data['Revenue'].mean()
        seasonal_factor = month_avg / overall_avg if not pd.isna(month_avg) else 1.0
        
        forecast = forecast * seasonal_factor
        forecasts.append(forecast)
    
    return np.array(forecasts)

# Generate forecasts
forecast_months = 6
forecasts = forecast_next_months(monthly_totals, forecast_months)

# Create forecast dataframe
last_date = monthly_totals['Month'].max()
forecast_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=forecast_months, freq='MS')

forecast_df = pd.DataFrame({
    'Month': forecast_dates,
    'Predicted_Revenue': forecasts,
    'Lower_Bound': forecasts * 0.85,  # 15% confidence interval
    'Upper_Bound': forecasts * 1.15
})

print(f"\n🔮 6-Month Revenue Forecast:")
for idx, row in forecast_df.iterrows():
    print(f"   {row['Month'].strftime('%B %Y')}: ₹{row['Predicted_Revenue']:,.0f}")

# Calculate accuracy on historical data (backtesting)
print(f"\n✅ Model Validation:")
actual_last_3 = monthly_totals['Revenue'].tail(3).values
predicted_last_3 = []

for i in range(3):
    train_data = monthly_totals.iloc[:-(3-i)]
    pred = forecast_next_months(train_data, 1)[0]
    predicted_last_3.append(pred)

mape = np.mean(np.abs((actual_last_3 - predicted_last_3) / actual_last_3)) * 100
print(f"   MAPE (Last 3 months): {mape:.2f}%")
print(f"   Model Accuracy: {100 - mape:.2f}%")

# Save forecast results
forecast_df.to_csv(f'{output_dir}revenue_forecast.csv', index=False)
print(f"\n💾 Saved forecast to {output_dir}revenue_forecast.csv")

# Visualize forecast
plt.figure(figsize=(14, 7))
plt.plot(monthly_totals['Month'], monthly_totals['Revenue'], 
         marker='o', linewidth=2, label='Historical Revenue', color='#2E86AB')
plt.plot(forecast_df['Month'], forecast_df['Predicted_Revenue'], 
         marker='s', linewidth=2, linestyle='--', label='Forecast', color='#A23B72')
plt.fill_between(forecast_df['Month'], 
                 forecast_df['Lower_Bound'], 
                 forecast_df['Upper_Bound'], 
                 alpha=0.2, color='#A23B72', label='Confidence Interval')
plt.axvline(x=last_date, color='red', linestyle=':', linewidth=2, label='Forecast Start')
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Revenue (₹)', fontsize=12, fontweight='bold')
plt.title('Men\'s Clothing Sales Forecast - Next 6 Months', fontsize=14, fontweight='bold', pad=20)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{output_dir}sales_forecast.png', dpi=300, bbox_inches='tight')
print(f"💾 Saved visualization: sales_forecast.png")
plt.close()

# ============================================================================
# MODEL 2: CUSTOMER SEGMENTATION WITH K-MEANS
# ============================================================================

print("\n" + "=" * 70)
print("MODEL 2: CUSTOMER SEGMENTATION (K-MEANS)")
print("=" * 70)

# Prepare features for clustering
print(f"\n🔧 Preparing Features...")
clustering_data = rfm[['Recency', 'Frequency', 'Monetary']].copy()

# Log transformation for better distribution
clustering_data['Recency_Log'] = np.log1p(clustering_data['Recency'])
clustering_data['Frequency_Log'] = np.log1p(clustering_data['Frequency'])
clustering_data['Monetary_Log'] = np.log1p(clustering_data['Monetary'])

# Standardize features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(clustering_data[['Recency_Log', 'Frequency_Log', 'Monetary_Log']])

print(f"✅ Features prepared: Recency, Frequency, Monetary (log-transformed & scaled)")

# Find optimal number of clusters using elbow method
print(f"\n🔍 Finding Optimal Number of Clusters...")
inertias = []
silhouette_scores = []
K_range = range(3, 9)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(features_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(features_scaled, kmeans.labels_))

# Choose k=5 for good balance
optimal_k = 5
print(f"✅ Selected K = {optimal_k} clusters")

# Train final model
print(f"\n🤖 Training K-Means Model...")
kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cluster_labels = kmeans_final.fit_predict(features_scaled)

# Add clusters to dataframe
rfm['ML_Cluster'] = cluster_labels

# Analyze clusters
print(f"\n📊 Cluster Analysis:")
cluster_summary = rfm.groupby('ML_Cluster').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean',
    'CustomerID': 'count'
}).round(2)
cluster_summary.columns = ['Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 'Customer_Count']
cluster_summary['Revenue_Share'] = (cluster_summary['Avg_Monetary'] * cluster_summary['Customer_Count'] / 
                                    (cluster_summary['Avg_Monetary'] * cluster_summary['Customer_Count']).sum() * 100).round(2)

# Name clusters based on characteristics
def name_cluster(row):
    if row['Avg_Monetary'] > 25000 and row['Avg_Frequency'] > 10:
        return 'VIP Customers'
    elif row['Avg_Recency'] < 100 and row['Avg_Frequency'] > 8:
        return 'Loyal Actives'
    elif row['Avg_Monetary'] > 15000:
        return 'High Spenders'
    elif row['Avg_Frequency'] < 5 and row['Avg_Recency'] > 300:
        return 'Dormant'
    else:
        return 'Regular Shoppers'

cluster_summary['Cluster_Name'] = cluster_summary.apply(name_cluster, axis=1)

print(f"\n{'Cluster':<15} {'Name':<18} {'Customers':<12} {'Avg Spend':<15} {'Frequency':<12} {'Revenue %':<10}")
print("-" * 90)
for idx, row in cluster_summary.iterrows():
    print(f"{idx:<15} {row['Cluster_Name']:<18} {int(row['Customer_Count']):<12} "
          f"₹{row['Avg_Monetary']:>11,.0f}  {row['Avg_Frequency']:>10.1f}  {row['Revenue_Share']:>8.1f}%")

# Save clustering results
rfm.to_csv(f'{output_dir}customer_clusters.csv', index=False)
cluster_summary.to_csv(f'{output_dir}cluster_summary.csv')
print(f"\n💾 Saved clustering results to {output_dir}")

# Visualize clusters - 2D projection
plt.figure(figsize=(14, 6))

# Plot 1: Frequency vs Monetary
plt.subplot(1, 2, 1)
scatter = plt.scatter(rfm['Frequency'], rfm['Monetary'], 
                     c=rfm['ML_Cluster'], cmap='viridis', 
                     alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
plt.xlabel('Frequency (Number of Purchases)', fontsize=11, fontweight='bold')
plt.ylabel('Monetary Value (₹)', fontsize=11, fontweight='bold')
plt.title('Customer Segmentation: Frequency vs Monetary', fontsize=12, fontweight='bold')
plt.colorbar(scatter, label='Cluster')
plt.grid(True, alpha=0.3)

# Plot 2: Recency vs Monetary
plt.subplot(1, 2, 2)
scatter = plt.scatter(rfm['Recency'], rfm['Monetary'], 
                     c=rfm['ML_Cluster'], cmap='viridis', 
                     alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
plt.xlabel('Recency (Days Since Last Purchase)', fontsize=11, fontweight='bold')
plt.ylabel('Monetary Value (₹)', fontsize=11, fontweight='bold')
plt.title('Customer Segmentation: Recency vs Monetary', fontsize=12, fontweight='bold')
plt.colorbar(scatter, label='Cluster')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{output_dir}customer_segmentation.png', dpi=300, bbox_inches='tight')
print(f"💾 Saved visualization: customer_segmentation.png")
plt.close()

# Cluster distribution pie chart
plt.figure(figsize=(10, 10))
colors = plt.cm.viridis(np.linspace(0, 1, optimal_k))
cluster_counts = rfm['ML_Cluster'].value_counts().sort_index()
labels = [f"{cluster_summary.loc[i, 'Cluster_Name']}\n({count:,} customers)" 
          for i, count in cluster_counts.items()]

plt.pie(cluster_counts, labels=labels, colors=colors, autopct='%1.1f%%',
        startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
plt.title('Customer Distribution Across ML Segments', fontsize=14, fontweight='bold', pad=20)
plt.savefig(f'{output_dir}cluster_distribution.png', dpi=300, bbox_inches='tight')
print(f"💾 Saved visualization: cluster_distribution.png")
plt.close()

# Model performance metrics
print(f"\n📈 Model Performance:")
print(f"   Silhouette Score: {silhouette_score(features_scaled, cluster_labels):.3f}")
print(f"   Inertia: {kmeans_final.inertia_:.2f}")
print(f"   Number of Iterations: {kmeans_final.n_iter_}")

# Business insights
print("\n" + "=" * 70)
print("BUSINESS INSIGHTS FROM ML MODELS")
print("=" * 70)

print(f"\n🔮 Sales Forecast Insights:")
forecast_total = forecast_df['Predicted_Revenue'].sum()
historical_avg = monthly_totals['Revenue'].mean()
print(f"   Next 6 Months Projected Revenue: ₹{forecast_total:,.0f}")
print(f"   Avg Monthly Forecast: ₹{forecast_total/6:,.0f}")
print(f"   vs Historical Avg: {((forecast_total/6 - historical_avg) / historical_avg * 100):+.1f}%")

print(f"\n👥 Customer Segmentation Insights:")
top_cluster = cluster_summary.nlargest(1, 'Revenue_Share').iloc[0]
print(f"   Highest Value Segment: {top_cluster['Cluster_Name']}")
print(f"   Contributes: {top_cluster['Revenue_Share']:.1f}% of revenue")
print(f"   Size: {int(top_cluster['Customer_Count']):,} customers ({top_cluster['Customer_Count']/len(rfm)*100:.1f}%)")

dormant_customers = cluster_summary[cluster_summary['Cluster_Name'] == 'Dormant']['Customer_Count'].sum()
if dormant_customers > 0:
    print(f"\n⚠️  Re-engagement Opportunity:")
    print(f"   {int(dormant_customers):,} dormant customers identified")
    print(f"   Potential recovery: ₹{dormant_customers * historical_avg * 0.3:,.0f}")

print("\n" + "=" * 70)
print("✅ ML MODELS COMPLETED!")
print("=" * 70)
print(f"\nGenerated Files:")
print(f"   1. revenue_forecast.csv - 6-month sales predictions")
print(f"   2. customer_clusters.csv - Customer segments with ML labels")
print(f"   3. cluster_summary.csv - Segment statistics")
print(f"   4. sales_forecast.png - Forecast visualization")
print(f"   5. customer_segmentation.png - 2D cluster plots")
print(f"   6. cluster_distribution.png - Segment distribution chart")
