"""
Multi-Category Retail ML Models
================================
Implements 3 powerful ML models:
1. Sales Forecasting - Predict future revenue (Prophet + Linear Regression)
2. Anomaly Detection - Identify unusual patterns in KPIs
3. Category Performance Classification - High/Medium/Low performers
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')
import os

# Create output directory
os.makedirs('../data/ml_results', exist_ok=True)

print("=" * 80)
print("MULTI-CATEGORY RETAIL ML MODELS")
print("=" * 80)

# ============================================================================
# 1. LOAD PROCESSED DATA
# ============================================================================

def load_processed_data():
    """Load all processed KPI datasets"""
    
    print("\n📂 Loading Processed Data...")
    
    daily_ts = pd.read_csv('../data/processed/daily_time_series.csv')
    monthly_ts = pd.read_csv('../data/processed/monthly_time_series.csv')
    category_kpis = pd.read_csv('../data/processed/category_kpis.csv')
    category_month = pd.read_csv('../data/processed/category_month_matrix.csv')
    
    # Convert dates
    daily_ts['date'] = pd.to_datetime(daily_ts['date'])
    
    print(f"  ✅ Daily time series: {len(daily_ts)} records")
    print(f"  ✅ Monthly time series: {len(monthly_ts)} records")
    print(f"  ✅ Category KPIs: {len(category_kpis)} categories")
    print(f"  ✅ Category-Month matrix: {len(category_month)} records")
    
    return daily_ts, monthly_ts, category_kpis, category_month

# ============================================================================
# 2. MODEL 1: SALES FORECASTING (Time Series)
# ============================================================================

def train_sales_forecasting_model(monthly_ts):
    """Train sales forecasting model using time series analysis"""
    
    print("\n🔮 MODEL 1: SALES FORECASTING")
    print("=" * 80)
    
    # Prepare data
    df = monthly_ts.copy()
    df['month_index'] = range(len(df))
    
    # Features for forecasting
    X = df[['month_index']].values
    y = df['revenue'].values
    
    # Create polynomial features (to capture trends)
    X_poly = np.column_stack([X, X**2, X**3])
    
    # Train-test split (last 6 months for testing)
    split_idx = len(df) - 6
    X_train, X_test = X_poly[:split_idx], X_poly[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    print(f"\n📊 Training Data:")
    print(f"  • Training samples: {len(X_train)}")
    print(f"  • Testing samples: {len(X_test)}")
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predictions on test set
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    accuracy = 100 - mape
    
    print(f"\n📈 Model Performance:")
    print(f"  • R² Score: {r2:.4f}")
    print(f"  • MAE: ₹{mae/10000000:.2f} Cr")
    print(f"  • MAPE: {mape:.2f}%")
    print(f"  • Accuracy: {accuracy:.2f}%")
    
    # Forecast next 12 months
    last_month_idx = len(df)
    future_months = np.arange(last_month_idx, last_month_idx + 12).reshape(-1, 1)
    future_months_poly = np.column_stack([future_months, future_months**2, future_months**3])
    future_predictions = model.predict(future_months_poly)
    
    # Create forecast dataframe
    forecast_df = pd.DataFrame({
        'month_index': range(last_month_idx, last_month_idx + 12),
        'forecasted_revenue': future_predictions,
        'forecast_period': [f'Month +{i+1}' for i in range(12)]
    })
    
    print(f"\n🔮 12-Month Revenue Forecast:")
    print(f"  • Next Quarter (3 months): ₹{future_predictions[:3].sum()/10000000:.2f} Cr")
    print(f"  • Next 6 months: ₹{future_predictions[:6].sum()/10000000:.2f} Cr")
    print(f"  • Next 12 months: ₹{future_predictions.sum()/10000000:.2f} Cr")
    print(f"  • Avg monthly forecast: ₹{future_predictions.mean()/10000000:.2f} Cr")
    
    # Calculate trend
    growth_rate = ((future_predictions[-1] - y[-1]) / y[-1]) * 100
    print(f"  • Projected growth: {growth_rate:+.2f}%")
    
    # Save results
    forecast_df.to_csv('../data/ml_results/revenue_forecast.csv', index=False)
    
    # Save model metrics
    metrics_df = pd.DataFrame([{
        'model': 'Sales Forecasting',
        'r2_score': r2,
        'mae': mae,
        'mape': mape,
        'accuracy': accuracy,
        'forecast_period': '12 months',
        'projected_revenue_12m': future_predictions.sum(),
        'growth_rate_pct': growth_rate
    }])
    metrics_df.to_csv('../data/ml_results/forecasting_metrics.csv', index=False)
    
    print(f"\n  ✅ Forecast saved: revenue_forecast.csv")
    print(f"  ✅ Metrics saved: forecasting_metrics.csv")
    
    return model, forecast_df, metrics_df

# ============================================================================
# 3. MODEL 2: ANOMALY DETECTION (Isolation Forest)
# ============================================================================

def train_anomaly_detection_model(daily_ts):
    """Detect anomalies in daily sales patterns"""
    
    print("\n\n🚨 MODEL 2: ANOMALY DETECTION")
    print("=" * 80)
    
    # Prepare features
    df = daily_ts.copy()
    
    # Create features for anomaly detection
    features = ['revenue', 'transactions', 'profit', 'avg_margin_pct', 'customers', 'quantity']
    X = df[features].values
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print(f"\n📊 Training Data:")
    print(f"  • Total days: {len(df)}")
    print(f"  • Features: {len(features)}")
    
    # Train Isolation Forest
    model = IsolationForest(
        contamination=0.05,  # Expect 5% anomalies
        random_state=42,
        n_estimators=100
    )
    
    # Predict anomalies (-1 for anomaly, 1 for normal)
    predictions = model.fit_predict(X_scaled)
    
    # Add predictions to dataframe
    df['is_anomaly'] = (predictions == -1).astype(int)
    df['anomaly_score'] = model.score_samples(X_scaled)
    
    # Analyze anomalies
    anomalies = df[df['is_anomaly'] == 1]
    normal_days = df[df['is_anomaly'] == 0]
    
    print(f"\n🔍 Anomaly Detection Results:")
    print(f"  • Normal days: {len(normal_days):,} ({len(normal_days)/len(df)*100:.1f}%)")
    print(f"  • Anomalous days: {len(anomalies):,} ({len(anomalies)/len(df)*100:.1f}%)")
    
    if len(anomalies) > 0:
        print(f"\n  Top 5 Anomalous Days:")
        top_anomalies = anomalies.nsmallest(5, 'anomaly_score')
        for idx, row in top_anomalies.iterrows():
            print(f"    • {row['date'].date()}: Revenue ₹{row['revenue']/100000:.2f}L, " +
                  f"Transactions: {row['transactions']}, Score: {row['anomaly_score']:.3f}")
        
        # Analyze anomaly characteristics
        print(f"\n  Anomaly Characteristics (vs Normal):")
        print(f"    • Avg Revenue: ₹{anomalies['revenue'].mean()/100000:.2f}L (Normal: ₹{normal_days['revenue'].mean()/100000:.2f}L)")
        print(f"    • Avg Transactions: {anomalies['transactions'].mean():.0f} (Normal: {normal_days['transactions'].mean():.0f})")
        print(f"    • Avg Margin: {anomalies['avg_margin_pct'].mean():.2f}% (Normal: {normal_days['avg_margin_pct'].mean():.2f}%)")
    
    # Save results
    anomaly_results = df[['date', 'revenue', 'transactions', 'profit', 'is_anomaly', 'anomaly_score']]
    anomaly_results.to_csv('../data/ml_results/anomaly_detection.csv', index=False)
    
    # Save anomaly summary
    anomaly_summary = pd.DataFrame([{
        'model': 'Anomaly Detection',
        'algorithm': 'Isolation Forest',
        'total_days': len(df),
        'normal_days': len(normal_days),
        'anomalous_days': len(anomalies),
        'anomaly_rate_pct': len(anomalies)/len(df)*100,
        'contamination': 0.05
    }])
    anomaly_summary.to_csv('../data/ml_results/anomaly_summary.csv', index=False)
    
    print(f"\n  ✅ Results saved: anomaly_detection.csv")
    print(f"  ✅ Summary saved: anomaly_summary.csv")
    
    return model, anomaly_results

# ============================================================================
# 4. MODEL 3: CATEGORY PERFORMANCE CLASSIFICATION
# ============================================================================

def train_category_classification_model(category_month):
    """Classify category-month combinations as High/Medium/Low performers"""
    
    print("\n\n🎯 MODEL 3: CATEGORY PERFORMANCE CLASSIFICATION")
    print("=" * 80)
    
    # Prepare data
    df = category_month.copy()
    
    # Create performance labels based on revenue
    revenue_percentiles = df['revenue'].quantile([0.33, 0.67])
    
    def classify_performance(revenue):
        if revenue >= revenue_percentiles[0.67]:
            return 'High'
        elif revenue >= revenue_percentiles[0.33]:
            return 'Medium'
        else:
            return 'Low'
    
    df['performance_class'] = df['revenue'].apply(classify_performance)
    
    print(f"\n📊 Training Data:")
    print(f"  • Total records: {len(df)}")
    print(f"  • Classes: {df['performance_class'].nunique()}")
    print(f"\n  Class Distribution:")
    print(df['performance_class'].value_counts().to_string())
    
    # Prepare features
    # One-hot encode category
    category_dummies = pd.get_dummies(df['category'], prefix='category')
    
    # Extract month number from year_month
    df['month_num'] = df['year_month'].str[-2:].astype(int)
    
    # Create feature matrix
    features = ['transactions', 'profit', 'avg_margin_pct', 'customers', 'month_num']
    X = pd.concat([df[features], category_dummies], axis=1)
    y = df['performance_class']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    print(f"\n  • Training samples: {len(X_train)}")
    print(f"  • Testing samples: {len(X_test)}")
    print(f"  • Features: {X.shape[1]}")
    
    # Train Random Forest Classifier
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = (y_pred == y_test).mean() * 100
    
    print(f"\n📈 Model Performance:")
    print(f"  • Accuracy: {accuracy:.2f}%")
    
    print(f"\n  Classification Report:")
    report = classification_report(y_test, y_pred, output_dict=True)
    for class_name in ['High', 'Medium', 'Low']:
        if class_name in report:
            print(f"    {class_name:8s} - Precision: {report[class_name]['precision']:.3f}, " +
                  f"Recall: {report[class_name]['recall']:.3f}, " +
                  f"F1: {report[class_name]['f1-score']:.3f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\n  Top 5 Important Features:")
    for idx, row in feature_importance.head(5).iterrows():
        print(f"    • {row['feature']}: {row['importance']:.4f}")
    
    # Predict on all data for insights
    df['predicted_class'] = model.predict(X)
    df['prediction_confidence'] = model.predict_proba(X).max(axis=1)
    
    # Save results
    classification_results = df[['year_month', 'category', 'revenue', 'performance_class', 
                                   'predicted_class', 'prediction_confidence']]
    classification_results.to_csv('../data/ml_results/category_classification.csv', index=False)
    
    feature_importance.to_csv('../data/ml_results/feature_importance.csv', index=False)
    
    # Save model metrics
    metrics_df = pd.DataFrame([{
        'model': 'Category Classification',
        'algorithm': 'Random Forest',
        'accuracy': accuracy,
        'n_classes': len(df['performance_class'].unique()),
        'n_features': X.shape[1],
        'high_precision': report.get('High', {}).get('precision', 0),
        'medium_precision': report.get('Medium', {}).get('precision', 0),
        'low_precision': report.get('Low', {}).get('precision', 0)
    }])
    metrics_df.to_csv('../data/ml_results/classification_metrics.csv', index=False)
    
    print(f"\n  ✅ Results saved: category_classification.csv")
    print(f"  ✅ Feature importance saved: feature_importance.csv")
    print(f"  ✅ Metrics saved: classification_metrics.csv")
    
    return model, classification_results, feature_importance

# ============================================================================
# 5. GENERATE ML INSIGHTS SUMMARY
# ============================================================================

def generate_ml_insights(forecast_df, anomaly_results, classification_results, category_kpis):
    """Generate comprehensive ML insights"""
    
    print("\n\n💡 GENERATING ML INSIGHTS")
    print("=" * 80)
    
    insights = []
    
    # Forecasting insights
    total_forecast = forecast_df['forecasted_revenue'].sum()
    insights.append(f"1. FORECASTING: Projected revenue for next 12 months is ₹{total_forecast/10000000:.2f} Crore")
    insights.append(f"   → Next quarter expected revenue: ₹{forecast_df.head(3)['forecasted_revenue'].sum()/10000000:.2f} Crore")
    
    # Anomaly insights
    anomaly_count = anomaly_results['is_anomaly'].sum()
    anomaly_rate = anomaly_count / len(anomaly_results) * 100
    insights.append(f"\n2. ANOMALY DETECTION: Identified {anomaly_count} anomalous days ({anomaly_rate:.1f}% of total)")
    
    if anomaly_count > 0:
        anomalous_days = anomaly_results[anomaly_results['is_anomaly'] == 1]
        avg_anomaly_revenue = anomalous_days['revenue'].mean()
        insights.append(f"   → Average revenue on anomalous days: ₹{avg_anomaly_revenue/100000:.2f} Lakhs")
    
    # Classification insights
    high_performers = classification_results[classification_results['predicted_class'] == 'High']
    if len(high_performers) > 0:
        top_category = high_performers['category'].value_counts().index[0]
        insights.append(f"\n3. CLASSIFICATION: {top_category} is the most consistent High performer")
        insights.append(f"   → {len(high_performers)} category-month combinations classified as High performance")
    
    # Category recommendations
    insights.append(f"\n4. RECOMMENDATIONS:")
    
    # Find underperforming categories
    low_performers = classification_results[classification_results['predicted_class'] == 'Low']
    if len(low_performers) > 0:
        underperforming_cat = low_performers['category'].value_counts().index[0]
        insights.append(f"   → Focus improvement efforts on {underperforming_cat} category")
    
    # Find growth opportunities
    category_growth = category_kpis.sort_values('avg_margin_pct', ascending=False)
    top_margin_cat = category_growth.iloc[0]['category']
    top_margin = category_growth.iloc[0]['avg_margin_pct']
    insights.append(f"   → {top_margin_cat} has highest margin ({top_margin:.2f}%) - expand inventory")
    
    # Revenue concentration risk
    top_cat_share = category_kpis.iloc[0]['revenue_share_pct']
    if top_cat_share > 60:
        insights.append(f"   → High revenue concentration ({top_cat_share:.1f}%) - diversify product mix")
    
    # Save insights
    insights_text = '\n'.join(insights)
    with open('../data/ml_results/ml_insights.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("MULTI-CATEGORY RETAIL ML INSIGHTS\n")
        f.write("=" * 80 + "\n\n")
        f.write(insights_text)
    
    print("\n" + insights_text)
    print(f"\n  ✅ Insights saved: ml_insights.txt")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\nStarting ML model training...\n")
    
    # Load data
    daily_ts, monthly_ts, category_kpis, category_month = load_processed_data()
    
    # Train models
    forecast_model, forecast_df, forecast_metrics = train_sales_forecasting_model(monthly_ts)
    anomaly_model, anomaly_results = train_anomaly_detection_model(daily_ts)
    classification_model, classification_results, feature_importance = train_category_classification_model(category_month)
    
    # Generate insights
    generate_ml_insights(forecast_df, anomaly_results, classification_results, category_kpis)
    
    print("\n" + "=" * 80)
    print("✨ ML MODEL TRAINING COMPLETE!")
    print("=" * 80)
    print("\n📁 Files saved in: ../data/ml_results/")
    print("  • revenue_forecast.csv")
    print("  • forecasting_metrics.csv")
    print("  • anomaly_detection.csv")
    print("  • anomaly_summary.csv")
    print("  • category_classification.csv")
    print("  • classification_metrics.csv")
    print("  • feature_importance.csv")
    print("  • ml_insights.txt")
    print("\n🎯 Ready for visualization and dashboard!")
