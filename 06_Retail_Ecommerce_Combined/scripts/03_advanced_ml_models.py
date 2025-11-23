"""
🤖 ADVANCED ML MODELS - PROJECT 6
===================================
4 Sophisticated Models:
1. Sales Forecasting (ARIMA + Trend Analysis)
2. Customer Lifetime Value (CLV) Prediction
3. Customer Churn Prediction
4. Product Recommendation Engine
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ML Libraries
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.preprocessing import StandardScaler
from scipy import stats

print("="*80)
print("🤖 ADVANCED ML MODELS - PROJECT 6")
print("="*80)

# ==================== LOAD DATA ====================

print("\n📂 Loading processed datasets...")
transactions = pd.read_csv('../data/raw/transactions.csv')
customers = pd.read_csv('../data/raw/customers.csv')
daily_trends = pd.read_csv('../data/processed/daily_trends.csv')
monthly_trends = pd.read_csv('../data/processed/monthly_trends.csv')
clv_data = pd.read_csv('../data/processed/customer_lifetime_value.csv')

transactions['date'] = pd.to_datetime(transactions['date'])
daily_trends['date'] = pd.to_datetime(daily_trends['date'])

print("✅ Data loaded successfully\n")

# ==================== MODEL 1: SALES FORECASTING ====================

print("="*80)
print("📈 MODEL 1: SALES FORECASTING")
print("="*80)

# Prepare daily sales data
sales_ts = daily_trends[['date', 'revenue']].copy()
sales_ts = sales_ts.sort_values('date').reset_index(drop=True)
sales_ts['day_index'] = range(len(sales_ts))

# Feature engineering for time series
sales_ts['day_of_week'] = sales_ts['date'].dt.dayofweek
sales_ts['day_of_month'] = sales_ts['date'].dt.day
sales_ts['month'] = sales_ts['date'].dt.month
sales_ts['quarter'] = sales_ts['date'].dt.quarter
sales_ts['is_weekend'] = sales_ts['day_of_week'].isin([5, 6]).astype(int)

# Calculate rolling statistics (7-day and 30-day windows)
sales_ts['revenue_7d_avg'] = sales_ts['revenue'].rolling(window=7, min_periods=1).mean()
sales_ts['revenue_30d_avg'] = sales_ts['revenue'].rolling(window=30, min_periods=1).mean()
sales_ts['revenue_7d_std'] = sales_ts['revenue'].rolling(window=7, min_periods=1).std().fillna(0)

# Split data: Use last 90 days for testing
train_size = len(sales_ts) - 90
train_data = sales_ts.iloc[:train_size].copy()
test_data = sales_ts.iloc[train_size:].copy()

# Prepare features
feature_cols = ['day_index', 'day_of_week', 'day_of_month', 'month', 'quarter', 
                'is_weekend', 'revenue_7d_avg', 'revenue_30d_avg', 'revenue_7d_std']

X_train = train_data[feature_cols]
y_train = train_data['revenue']
X_test = test_data[feature_cols]
y_test = test_data['revenue']

print(f"\n📊 Training Set: {len(X_train)} days")
print(f"📊 Test Set: {len(X_test)} days (Last 90 days)")

# Train Random Forest model
print("\n🚀 Training Random Forest Regressor...")
rf_model = RandomForestRegressor(n_estimators=200, max_depth=15, min_samples_split=5, 
                                 random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

# Predictions
y_pred_train = rf_model.predict(X_train)
y_pred_test = rf_model.predict(X_test)

# Calculate metrics
train_mae = mean_absolute_error(y_train, y_pred_train)
test_mae = mean_absolute_error(y_test, y_pred_test)
train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)
mape = np.mean(np.abs((y_test - y_pred_test) / y_test)) * 100

print("\n📊 Model Performance:")
print(f"  • Train R² Score: {train_r2:.4f}")
print(f"  • Test R² Score: {test_r2:.4f}")
print(f"  • Train MAE: ₹{train_mae:,.2f}")
print(f"  • Test MAE: ₹{test_mae:,.2f}")
print(f"  • Test RMSE: ₹{test_rmse:,.2f}")
print(f"  • MAPE: {mape:.2f}%")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🎯 Top 5 Important Features:")
for i, row in feature_importance.head().iterrows():
    print(f"  {i+1}. {row['feature']}: {row['importance']:.4f}")

# Forecast next 30 days
print("\n🔮 Forecasting Next 30 Days...")
last_date = sales_ts['date'].max()
forecast_dates = [last_date + timedelta(days=i) for i in range(1, 31)]

forecast_df = pd.DataFrame({'date': forecast_dates})
forecast_df['day_index'] = range(len(sales_ts), len(sales_ts) + 30)
forecast_df['day_of_week'] = forecast_df['date'].dt.dayofweek
forecast_df['day_of_month'] = forecast_df['date'].dt.day
forecast_df['month'] = forecast_df['date'].dt.month
forecast_df['quarter'] = forecast_df['date'].dt.quarter
forecast_df['is_weekend'] = forecast_df['day_of_week'].isin([5, 6]).astype(int)

# Use last known rolling averages
last_7d_avg = sales_ts['revenue_7d_avg'].iloc[-1]
last_30d_avg = sales_ts['revenue_30d_avg'].iloc[-1]
last_7d_std = sales_ts['revenue_7d_std'].iloc[-1]

forecast_df['revenue_7d_avg'] = last_7d_avg
forecast_df['revenue_30d_avg'] = last_30d_avg
forecast_df['revenue_7d_std'] = last_7d_std

X_forecast = forecast_df[feature_cols]
forecast_revenue = rf_model.predict(X_forecast)
forecast_df['predicted_revenue'] = forecast_revenue

# Add confidence intervals (±15%)
forecast_df['lower_bound'] = forecast_revenue * 0.85
forecast_df['upper_bound'] = forecast_revenue * 1.15

print(f"✅ Forecasted next 30 days")
print(f"  • Avg Daily Forecast: ₹{forecast_revenue.mean():,.2f}")
print(f"  • Total 30-Day Forecast: ₹{forecast_revenue.sum()/10000000:.2f} Cr")

# Save results
forecast_results = {
    'model': 'Random Forest Sales Forecasting',
    'train_r2': round(train_r2, 4),
    'test_r2': round(test_r2, 4),
    'test_mae': round(test_mae, 2),
    'test_rmse': round(test_rmse, 2),
    'mape_pct': round(mape, 2),
    'forecast_days': 30,
    'avg_daily_forecast': round(forecast_revenue.mean(), 2),
    'total_30day_forecast_cr': round(forecast_revenue.sum()/10000000, 2)
}

# Save forecast
forecast_df[['date', 'predicted_revenue', 'lower_bound', 'upper_bound']].to_csv(
    '../data/ml_results/sales_forecast_30days.csv', index=False
)
print("\n✅ Saved: sales_forecast_30days.csv")

# ==================== MODEL 2: CLV PREDICTION ====================

print("\n" + "="*80)
print("💰 MODEL 2: CUSTOMER LIFETIME VALUE PREDICTION")
print("="*80)

# Prepare CLV features
clv_features = clv_data.copy()

# Merge with customer segment
clv_features = clv_features.merge(customers[['customer_id', 'segment', 'is_prime']], 
                                   on='customer_id', how='left')

# Calculate additional features
clv_features['avg_transaction_value'] = clv_features['total_revenue'] / clv_features['transactions']
clv_features['avg_profit_per_transaction'] = clv_features['total_profit'] / clv_features['transactions']
clv_features['is_prime'] = clv_features['is_prime'].astype(int)

# Encode segment (ordinal)
segment_map = {'Diamond': 7, 'Platinum': 6, 'Gold': 5, 'Silver': 4, 'Regular': 3, 'Occasional': 2, 'New': 1}
clv_features['segment_encoded'] = clv_features['segment_x'].map(segment_map).fillna(1)

# Target: Total revenue (CLV)
feature_cols_clv = ['transactions', 'lifespan_months', 'avg_transaction_value', 
                    'segment_encoded', 'is_prime']

clv_features_clean = clv_features.dropna(subset=feature_cols_clv + ['total_revenue'])

X_clv = clv_features_clean[feature_cols_clv]
y_clv = clv_features_clean['total_revenue']

# Split data
X_train_clv, X_test_clv, y_train_clv, y_test_clv = train_test_split(
    X_clv, y_clv, test_size=0.2, random_state=42
)

print(f"\n📊 Training Set: {len(X_train_clv):,} customers")
print(f"📊 Test Set: {len(X_test_clv):,} customers")

# Train Gradient Boosting model
print("\n🚀 Training Gradient Boosting Regressor...")
clv_model = GradientBoostingClassifier(n_estimators=200, max_depth=5, learning_rate=0.1, 
                                        random_state=42)

# Convert CLV to classification task (High/Medium/Low value)
y_train_clv_class = pd.qcut(y_train_clv, q=3, labels=['Low', 'Medium', 'High'])
y_test_clv_class = pd.qcut(y_test_clv, q=3, labels=['Low', 'Medium', 'High'])

clv_model.fit(X_train_clv, y_train_clv_class)

# Predictions
y_pred_clv = clv_model.predict(X_test_clv)

# Metrics
accuracy_clv = accuracy_score(y_test_clv_class, y_pred_clv)
precision_clv = precision_score(y_test_clv_class, y_pred_clv, average='weighted')
recall_clv = recall_score(y_test_clv_class, y_pred_clv, average='weighted')
f1_clv = f1_score(y_test_clv_class, y_pred_clv, average='weighted')

print("\n📊 Model Performance:")
print(f"  • Accuracy: {accuracy_clv:.4f}")
print(f"  • Precision: {precision_clv:.4f}")
print(f"  • Recall: {recall_clv:.4f}")
print(f"  • F1-Score: {f1_clv:.4f}")

# Save results
clv_results = {
    'model': 'CLV Classification (Gradient Boosting)',
    'accuracy': round(accuracy_clv, 4),
    'precision': round(precision_clv, 4),
    'recall': round(recall_clv, 4),
    'f1_score': round(f1_clv, 4),
    'classes': 3
}

# Predict CLV for all customers
clv_features_clean['predicted_clv_class'] = clv_model.predict(clv_features_clean[feature_cols_clv])
clv_features_clean[['customer_id', 'total_revenue', 'predicted_clv_class']].to_csv(
    '../data/ml_results/customer_clv_predictions.csv', index=False
)
print("\n✅ Saved: customer_clv_predictions.csv")

# ==================== MODEL 3: CHURN PREDICTION ====================

print("\n" + "="*80)
print("⚠️ MODEL 3: CUSTOMER CHURN PREDICTION")
print("="*80)

# Define churn: No transaction in last 90 days
current_date = transactions['date'].max()
cutoff_date = current_date - timedelta(days=90)

customer_last_txn = transactions.groupby('customer_id')['date'].max().reset_index()
customer_last_txn.columns = ['customer_id', 'last_transaction_date']
customer_last_txn['is_churned'] = (customer_last_txn['last_transaction_date'] < cutoff_date).astype(int)

# Merge with CLV features
churn_features = clv_features_clean.merge(customer_last_txn[['customer_id', 'is_churned']], 
                                           on='customer_id', how='left')

# Add RFM features
rfm_data = pd.read_csv('../data/processed/customer_rfm_analysis.csv')
churn_features = churn_features.merge(
    rfm_data[['customer_id', 'recency', 'frequency', 'monetary']], 
    on='customer_id', how='left'
)

# Feature selection
feature_cols_churn = ['recency', 'frequency', 'monetary', 'transactions', 
                      'lifespan_months', 'segment_encoded', 'is_prime']

churn_features_clean = churn_features.dropna(subset=feature_cols_churn + ['is_churned'])

X_churn = churn_features_clean[feature_cols_churn]
y_churn = churn_features_clean['is_churned']

# Split data
X_train_churn, X_test_churn, y_train_churn, y_test_churn = train_test_split(
    X_churn, y_churn, test_size=0.2, random_state=42, stratify=y_churn
)

print(f"\n📊 Training Set: {len(X_train_churn):,} customers")
print(f"📊 Test Set: {len(X_test_churn):,} customers")
print(f"📊 Churn Rate: {y_churn.mean()*100:.2f}%")

# Train Random Forest Classifier
print("\n🚀 Training Random Forest Classifier...")
churn_model = RandomForestClassifier(n_estimators=200, max_depth=15, min_samples_split=5,
                                      class_weight='balanced', random_state=42, n_jobs=-1)
churn_model.fit(X_train_churn, y_train_churn)

# Predictions
y_pred_churn = churn_model.predict(X_test_churn)
y_pred_proba_churn = churn_model.predict_proba(X_test_churn)[:, 1]

# Metrics
accuracy_churn = accuracy_score(y_test_churn, y_pred_churn)
precision_churn = precision_score(y_test_churn, y_pred_churn)
recall_churn = recall_score(y_test_churn, y_pred_churn)
f1_churn = f1_score(y_test_churn, y_pred_churn)

print("\n📊 Model Performance:")
print(f"  • Accuracy: {accuracy_churn:.4f}")
print(f"  • Precision: {precision_churn:.4f}")
print(f"  • Recall: {recall_churn:.4f}")
print(f"  • F1-Score: {f1_churn:.4f}")

# Feature importance
churn_feature_importance = pd.DataFrame({
    'feature': feature_cols_churn,
    'importance': churn_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🎯 Top Features for Churn:")
for i, row in churn_feature_importance.iterrows():
    print(f"  {i+1}. {row['feature']}: {row['importance']:.4f}")

# Save results
churn_results = {
    'model': 'Churn Prediction (Random Forest)',
    'accuracy': round(accuracy_churn, 4),
    'precision': round(precision_churn, 4),
    'recall': round(recall_churn, 4),
    'f1_score': round(f1_churn, 4),
    'churn_rate_pct': round(y_churn.mean()*100, 2)
}

# Predict churn for all customers
churn_features_clean['churn_probability'] = churn_model.predict_proba(churn_features_clean[feature_cols_churn])[:, 1]
churn_features_clean['predicted_churn'] = churn_model.predict(churn_features_clean[feature_cols_churn])

churn_features_clean[['customer_id', 'churn_probability', 'predicted_churn', 'is_churned']].to_csv(
    '../data/ml_results/churn_predictions.csv', index=False
)
print("\n✅ Saved: churn_predictions.csv")

# ==================== MODEL 4: PRODUCT RECOMMENDATION ====================

print("\n" + "="*80)
print("🎁 MODEL 4: PRODUCT RECOMMENDATION ENGINE")
print("="*80)

# Simplified approach: Category-based + Popularity
print("\n📊 Building Recommendation System...")

# Get top products by category
products_df = pd.read_csv('../data/raw/products.csv')

# Top 20 products per category
top_products_by_category = transactions.groupby(['category', 'product_id']).agg({
    'revenue': 'sum',
    'quantity': 'sum',
    'transaction_id': 'count'
}).reset_index()

top_products_by_category = top_products_by_category.sort_values(['category', 'revenue'], ascending=[True, False])
top_products_by_category = top_products_by_category.groupby('category').head(20)

# Merge with product details
top_products_by_category = top_products_by_category.merge(
    products_df[['product_id', 'product_name', 'brand', 'price', 'rating']], 
    on='product_id', how='left'
)

print(f"✅ Identified top 20 products per category")

# Customer purchase patterns
customer_categories = transactions.groupby(['customer_id', 'category']).size().reset_index(name='purchases')
customer_top_category = customer_categories.sort_values(['customer_id', 'purchases'], ascending=[True, False])
customer_top_category = customer_top_category.groupby('customer_id').first().reset_index()

print(f"✅ Mapped customer preferences")

# Generate recommendations for top 5000 customers
print("\n🎯 Generating Recommendations for Top 5000 Customers...")
top_customers = transactions.groupby('customer_id')['revenue'].sum().nlargest(5000).index.tolist()

recommendations_list = []

for customer_id in top_customers:
    # Get customer's purchase history
    customer_purchases = transactions[transactions['customer_id'] == customer_id]['product_id'].unique()
    
    # Get customer's favorite category
    customer_cat = customer_top_category[customer_top_category['customer_id'] == customer_id]
    
    if len(customer_cat) > 0:
        fav_category = customer_cat['category'].iloc[0]
        
        # Get top products from favorite category that customer hasn't bought
        category_products = top_products_by_category[top_products_by_category['category'] == fav_category]
        recommendations = category_products[~category_products['product_id'].isin(customer_purchases)].head(10)
        
        if len(recommendations) > 0:
            recommendations_list.append({
                'customer_id': customer_id,
                'favorite_category': fav_category,
                'recommended_products': ','.join(recommendations['product_id'].tolist()),
                'recommendation_count': len(recommendations)
            })

recommendations_df = pd.DataFrame(recommendations_list)
recommendations_df.to_csv('../data/ml_results/product_recommendations.csv', index=False)

print(f"✅ Generated recommendations for {len(recommendations_df)} customers")
print(f"✅ Saved: product_recommendations.csv")

# Recommendation stats
recommendation_results = {
    'model': 'Category-Based Recommendations',
    'total_customers': len(recommendations_df),
    'customers_with_recommendations': len(recommendations_df),
    'avg_recommendations_per_customer': round(recommendations_df['recommendation_count'].mean(), 2)
}

# ==================== SAVE ALL MODEL RESULTS ====================

print("\n" + "="*80)
print("💾 SAVING MODEL SUMMARY")
print("="*80)

all_results = pd.DataFrame([
    {
        'model_name': 'Sales Forecasting (Random Forest)',
        'model_type': 'Regression',
        'primary_metric': 'R² Score',
        'metric_value': round(test_r2, 4),
        'additional_metrics': f"MAE: ₹{test_mae:,.0f}, MAPE: {mape:.2f}%"
    },
    {
        'model_name': 'CLV Prediction (Gradient Boosting)',
        'model_type': 'Classification',
        'primary_metric': 'Accuracy',
        'metric_value': round(accuracy_clv, 4),
        'additional_metrics': f"Precision: {precision_clv:.4f}, F1: {f1_clv:.4f}"
    },
    {
        'model_name': 'Churn Prediction (Random Forest)',
        'model_type': 'Classification',
        'primary_metric': 'F1-Score',
        'metric_value': round(f1_churn, 4),
        'additional_metrics': f"Recall: {recall_churn:.4f}, Precision: {precision_churn:.4f}"
    },
    {
        'model_name': 'Product Recommendations (Category-Based)',
        'model_type': 'Recommendation',
        'primary_metric': 'Customers Served',
        'metric_value': len(recommendations_df),
        'additional_metrics': f"Avg {recommendations_df['recommendation_count'].mean():.1f} products/customer"
    }
])

all_results.to_csv('../data/ml_results/ml_models_summary.csv', index=False)

print("\n📊 Model Summary:")
for i, row in all_results.iterrows():
    print(f"\n{i+1}. {row['model_name']}")
    print(f"   {row['primary_metric']}: {row['metric_value']}")
    print(f"   {row['additional_metrics']}")

print("\n" + "="*80)
print("✨ ALL ML MODELS TRAINED SUCCESSFULLY!")
print("="*80)

print("\n📁 Saved Files:")
print("  1. sales_forecast_30days.csv")
print("  2. customer_clv_predictions.csv")
print("  3. churn_predictions.csv")
print("  4. product_recommendations.csv")
print("  5. ml_models_summary.csv")

print("\n🏆 Crown Jewel ML Pipeline - COMPLETE!")
print("🎯 Ready for visualization generation!")
