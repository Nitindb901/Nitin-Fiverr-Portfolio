"""
Project 7: Sales Forecasting ML - Build 5 Advanced ML Models
==============================================================
This script builds and trains 5 different forecasting models:
1. ARIMA - Classical time series baseline
2. Prophet - Facebook's model with seasonality
3. LSTM - Deep learning neural network
4. XGBoost - Gradient boosting regressor
5. Ensemble - Combined predictions from all 4

Author: Nitin Dubey
Date: November 2025
"""

import os
import pandas as pd
import numpy as np
import warnings
import pickle
from datetime import datetime, timedelta
import json

# Suppress warnings
warnings.filterwarnings('ignore')

print("📦 Importing ML libraries...")
print("   This may take a moment...\n")

# Time series models
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
import seaborn as sns

# Prophet
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    print("⚠️  Prophet not available. Installing...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'prophet'])
    from prophet import Prophet
    PROPHET_AVAILABLE = True

# Deep Learning - Skipping LSTM (requires TensorFlow backend)
LSTM_AVAILABLE = False
print("⚠️  LSTM skipped (requires TensorFlow). Building 4 models: ARIMA, Prophet, XGBoost, Ensemble\n")

# XGBoost
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    print("⚠️  XGBoost not available. Installing...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'xgboost'])
    import xgboost as xgb
    XGBOOST_AVAILABLE = True

# Metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("✅ All libraries imported successfully!\n")

# Create output directories
os.makedirs('models', exist_ok=True)
os.makedirs('data/forecasts', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

# ============================================================================
# LOAD AND PREPARE DATA
# ============================================================================

print("🔄 Loading transaction data...")
df = pd.read_csv('data/raw/transactions.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

print(f"   ✅ Loaded {len(df):,} transactions")
print(f"   📅 Date Range: {df['date'].min()} to {df['date'].max()}\n")

# Aggregate daily revenue
print("📊 Aggregating daily revenue...")
daily_revenue = df.groupby('date')['final_revenue'].sum().reset_index()
daily_revenue.columns = ['date', 'revenue']
daily_revenue = daily_revenue.sort_values('date')

# Fill missing dates with 0
date_range = pd.date_range(start=daily_revenue['date'].min(), 
                           end=daily_revenue['date'].max(), 
                           freq='D')
daily_revenue = daily_revenue.set_index('date').reindex(date_range, fill_value=0).reset_index()
daily_revenue.columns = ['date', 'revenue']

print(f"   ✅ Aggregated to {len(daily_revenue)} daily records\n")

# Split data: Train (80%) / Test (20%)
train_size = int(len(daily_revenue) * 0.8)
train_data = daily_revenue[:train_size].copy()
test_data = daily_revenue[train_size:].copy()

print(f"📊 Data Split:")
print(f"   Train: {len(train_data)} days ({train_data['date'].min()} to {train_data['date'].max()})")
print(f"   Test:  {len(test_data)} days ({test_data['date'].min()} to {test_data['date'].max()})\n")

# Save processed data
daily_revenue.to_csv('data/processed/daily_revenue.csv', index=False)
print("✅ Saved processed data to data/processed/daily_revenue.csv\n")

# ============================================================================
# MODEL 1: ARIMA
# ============================================================================

print("="*70)
print("🔮 MODEL 1: ARIMA (AutoRegressive Integrated Moving Average)")
print("="*70)

def calculate_mape(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def calculate_metrics(y_true, y_pred):
    """Calculate all metrics"""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = calculate_mape(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {'MAE': mae, 'RMSE': rmse, 'MAPE': mape, 'R2': r2}

print("\n📈 Training ARIMA model...")
print("   Using order (5,1,2) - AR:5, Integrated:1, MA:2")

try:
    # Fit ARIMA model
    arima_model = ARIMA(train_data['revenue'], order=(5, 1, 2))
    arima_fit = arima_model.fit()
    
    # Predict on test set
    arima_pred = arima_fit.forecast(steps=len(test_data))
    
    # Calculate metrics
    arima_metrics = calculate_metrics(test_data['revenue'], arima_pred)
    
    print(f"   ✅ ARIMA trained successfully!")
    print(f"   📊 Test Metrics:")
    print(f"      MAPE: {arima_metrics['MAPE']:.2f}%")
    print(f"      RMSE: ₹{arima_metrics['RMSE']:,.2f}")
    print(f"      MAE:  ₹{arima_metrics['MAE']:,.2f}")
    print(f"      R²:   {arima_metrics['R2']:.4f}")
    
    # Save model
    with open('models/arima_model.pkl', 'wb') as f:
        pickle.dump(arima_fit, f)
    
    # Generate 90-day forecast
    future_forecast = arima_fit.forecast(steps=90)
    forecast_dates = pd.date_range(start=daily_revenue['date'].max() + timedelta(days=1), periods=90, freq='D')
    arima_forecast_df = pd.DataFrame({
        'date': forecast_dates,
        'arima_forecast': future_forecast
    })
    
    print("   ✅ Generated 90-day forecast\n")
    
    ARIMA_SUCCESS = True
    
except Exception as e:
    print(f"   ❌ ARIMA training failed: {e}\n")
    ARIMA_SUCCESS = False
    arima_metrics = {'MAE': 0, 'RMSE': 0, 'MAPE': 100, 'R2': 0}
    arima_forecast_df = pd.DataFrame()

# ============================================================================
# MODEL 2: PROPHET
# ============================================================================

print("="*70)
print("🔮 MODEL 2: PROPHET (Facebook's Time Series Model)")
print("="*70)

print("\n📈 Training Prophet model...")
print("   Adding seasonality: yearly, weekly")
print("   Adding holidays: Diwali, New Year, Christmas, Holi")

try:
    # Prepare data for Prophet
    prophet_train = train_data.copy()
    prophet_train.columns = ['ds', 'y']
    
    # Create holidays dataframe
    holidays = pd.DataFrame({
        'holiday': ['diwali', 'new_year', 'christmas', 'holi'] * 6,
        'ds': pd.to_datetime([
            '2020-11-14', '2021-01-01', '2020-12-25', '2020-03-10',
            '2021-11-04', '2022-01-01', '2021-12-25', '2021-03-29',
            '2022-10-24', '2023-01-01', '2022-12-25', '2022-03-18',
            '2023-11-12', '2024-01-01', '2023-12-25', '2023-03-08',
            '2024-11-01', '2025-01-01', '2024-12-25', '2024-03-25',
            '2025-10-20', '2026-01-01', '2025-12-25', '2025-03-14',
        ]),
        'lower_window': 0,
        'upper_window': 5,
    })
    
    # Initialize and train Prophet
    prophet_model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        holidays=holidays,
        seasonality_mode='multiplicative'
    )
    prophet_model.fit(prophet_train)
    
    # Predict on test set
    prophet_test = test_data.copy()
    prophet_test.columns = ['ds', 'y']
    prophet_pred = prophet_model.predict(prophet_test[['ds']])
    
    # Calculate metrics
    prophet_metrics = calculate_metrics(prophet_test['y'], prophet_pred['yhat'])
    
    print(f"   ✅ Prophet trained successfully!")
    print(f"   📊 Test Metrics:")
    print(f"      MAPE: {prophet_metrics['MAPE']:.2f}%")
    print(f"      RMSE: ₹{prophet_metrics['RMSE']:,.2f}")
    print(f"      MAE:  ₹{prophet_metrics['MAE']:,.2f}")
    print(f"      R²:   {prophet_metrics['R2']:.4f}")
    
    # Save model
    with open('models/prophet_model.pkl', 'wb') as f:
        pickle.dump(prophet_model, f)
    
    # Generate 90-day forecast
    future = prophet_model.make_future_dataframe(periods=90)
    prophet_forecast = prophet_model.predict(future)
    prophet_forecast_df = prophet_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(90)
    prophet_forecast_df.columns = ['date', 'prophet_forecast', 'prophet_lower', 'prophet_upper']
    
    print("   ✅ Generated 90-day forecast with confidence intervals\n")
    
    PROPHET_SUCCESS = True
    
except Exception as e:
    print(f"   ❌ Prophet training failed: {e}\n")
    PROPHET_SUCCESS = False
    prophet_metrics = {'MAE': 0, 'RMSE': 0, 'MAPE': 100, 'R2': 0}
    prophet_forecast_df = pd.DataFrame()

# ============================================================================
# MODEL 3: LSTM - SKIPPED (Requires TensorFlow)
# ============================================================================

print("="*70)
print("⚠️  MODEL 3: LSTM - SKIPPED")
print("="*70)
print("   Requires TensorFlow backend (not available in Python 3.14)")
print("   Continuing with 4 models: ARIMA, Prophet, XGBoost, Ensemble\n")

LSTM_SUCCESS = False
lstm_metrics = {'MAE': 0, 'RMSE': 0, 'MAPE': 100, 'R2': 0}
lstm_forecast_df = pd.DataFrame()

# ============================================================================
# MODEL 4: XGBOOST
# ============================================================================

print("="*70)
print("🔮 MODEL 4: XGBOOST (Extreme Gradient Boosting)")
print("="*70)

print("\n📈 Training XGBoost model...")
print("   Features: year, month, quarter, day_of_week, is_weekend, lags, rolling means")

try:
    # Create features
    def create_features(df):
        df = df.copy()
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['day_of_week'] = df['date'].dt.dayofweek
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        df['day_of_year'] = df['date'].dt.dayofyear
        
        # Lag features
        df['lag_7'] = df['revenue'].shift(7)
        df['lag_30'] = df['revenue'].shift(30)
        
        # Rolling means
        df['rolling_mean_7'] = df['revenue'].rolling(window=7).mean()
        df['rolling_mean_30'] = df['revenue'].rolling(window=30).mean()
        
        return df
    
    # Prepare train data
    train_features = create_features(train_data)
    train_features = train_features.dropna()
    
    feature_cols = ['year', 'month', 'quarter', 'day_of_week', 'is_weekend', 
                   'day_of_year', 'lag_7', 'lag_30', 'rolling_mean_7', 'rolling_mean_30']
    
    X_train_xgb = train_features[feature_cols]
    y_train_xgb = train_features['revenue']
    
    print(f"   📊 Training samples: {len(X_train_xgb)}")
    
    # Train model
    xgb_model = xgb.XGBRegressor(
        n_estimators=200,
        max_depth=7,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    
    xgb_model.fit(X_train_xgb, y_train_xgb)
    
    # Prepare test data
    all_data_xgb = pd.concat([train_data, test_data])
    all_features = create_features(all_data_xgb)
    test_features = all_features[len(train_data):].copy()
    test_features = test_features.dropna()
    
    X_test_xgb = test_features[feature_cols]
    y_test_xgb = test_features['revenue']
    
    # Predict
    xgb_pred = xgb_model.predict(X_test_xgb)
    
    # Calculate metrics
    xgb_metrics = calculate_metrics(y_test_xgb, xgb_pred)
    
    print(f"   ✅ XGBoost trained successfully!")
    print(f"   📊 Test Metrics:")
    print(f"      MAPE: {xgb_metrics['MAPE']:.2f}%")
    print(f"      RMSE: ₹{xgb_metrics['RMSE']:,.2f}")
    print(f"      MAE:  ₹{xgb_metrics['MAE']:,.2f}")
    print(f"      R²:   {xgb_metrics['R2']:.4f}")
    
    # Save model
    with open('models/xgboost_model.pkl', 'wb') as f:
        pickle.dump(xgb_model, f)
    
    # Generate 90-day forecast
    last_date = daily_revenue['date'].max()
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=90, freq='D')
    
    xgb_forecast_list = []
    forecast_df = all_data_xgb.copy()
    
    for future_date in future_dates:
        # Create future row
        future_row = pd.DataFrame({
            'date': [future_date],
            'revenue': [0]  # Placeholder
        })
        forecast_df = pd.concat([forecast_df, future_row], ignore_index=True)
        forecast_features = create_features(forecast_df)
        
        last_row = forecast_features.iloc[-1:][feature_cols]
        
        if not last_row.isnull().any().any():
            pred = xgb_model.predict(last_row)[0]
            xgb_forecast_list.append(pred)
            forecast_df.iloc[-1, forecast_df.columns.get_loc('revenue')] = pred
        else:
            xgb_forecast_list.append(forecast_df['revenue'].tail(30).mean())
    
    xgb_forecast_df = pd.DataFrame({
        'date': future_dates,
        'xgboost_forecast': xgb_forecast_list
    })
    
    print("   ✅ Generated 90-day forecast\n")
    
    XGBOOST_SUCCESS = True
    
except Exception as e:
    print(f"   ❌ XGBoost training failed: {e}\n")
    XGBOOST_SUCCESS = False
    xgb_metrics = {'MAE': 0, 'RMSE': 0, 'MAPE': 100, 'R2': 0}
    xgb_forecast_df = pd.DataFrame()

# ============================================================================
# MODEL 5: ENSEMBLE
# ============================================================================

print("="*70)
print("🔮 MODEL 5: ENSEMBLE (Weighted Average of All Models)")
print("="*70)

print("\n📈 Creating Ensemble model...")
print("   Combining: ARIMA + Prophet + XGBoost")
print("   Weights based on inverse MAPE (lower MAPE = higher weight)")

try:
    # Calculate ensemble weights (inverse MAPE)
    models_mape = {
        'ARIMA': arima_metrics['MAPE'] if ARIMA_SUCCESS else 100,
        'Prophet': prophet_metrics['MAPE'] if PROPHET_SUCCESS else 100,
        'LSTM': lstm_metrics['MAPE'] if LSTM_SUCCESS else 100,
        'XGBoost': xgb_metrics['MAPE'] if XGBOOST_SUCCESS else 100
    }
    
    # Inverse MAPE for weights
    inverse_mape = {k: 1/v if v > 0 else 0 for k, v in models_mape.items()}
    total_inverse = sum(inverse_mape.values())
    weights = {k: v/total_inverse for k, v in inverse_mape.items()}
    
    print(f"\n   📊 Model Weights:")
    for model, weight in weights.items():
        print(f"      {model}: {weight:.2%}")
    
    # Merge all forecasts
    ensemble_forecast_df = arima_forecast_df.copy() if ARIMA_SUCCESS else pd.DataFrame()
    
    if PROPHET_SUCCESS and not prophet_forecast_df.empty:
        if ensemble_forecast_df.empty:
            ensemble_forecast_df = prophet_forecast_df[['date', 'prophet_forecast']].copy()
        else:
            ensemble_forecast_df = ensemble_forecast_df.merge(
                prophet_forecast_df[['date', 'prophet_forecast']], on='date', how='outer'
            )
    
    if LSTM_SUCCESS and not lstm_forecast_df.empty:
        if ensemble_forecast_df.empty:
            ensemble_forecast_df = lstm_forecast_df.copy()
        else:
            ensemble_forecast_df = ensemble_forecast_df.merge(lstm_forecast_df, on='date', how='outer')
    
    if XGBOOST_SUCCESS and not xgb_forecast_df.empty:
        if ensemble_forecast_df.empty:
            ensemble_forecast_df = xgb_forecast_df.copy()
        else:
            ensemble_forecast_df = ensemble_forecast_df.merge(xgb_forecast_df, on='date', how='outer')
    
    # Calculate weighted ensemble
    ensemble_forecast_df['ensemble_forecast'] = 0
    
    if ARIMA_SUCCESS and 'arima_forecast' in ensemble_forecast_df.columns:
        ensemble_forecast_df['ensemble_forecast'] += weights['ARIMA'] * ensemble_forecast_df['arima_forecast']
    
    if PROPHET_SUCCESS and 'prophet_forecast' in ensemble_forecast_df.columns:
        ensemble_forecast_df['ensemble_forecast'] += weights['Prophet'] * ensemble_forecast_df['prophet_forecast']
    
    if LSTM_SUCCESS and 'lstm_forecast' in ensemble_forecast_df.columns:
        ensemble_forecast_df['ensemble_forecast'] += weights['LSTM'] * ensemble_forecast_df['lstm_forecast']
    
    if XGBOOST_SUCCESS and 'xgboost_forecast' in ensemble_forecast_df.columns:
        ensemble_forecast_df['ensemble_forecast'] += weights['XGBoost'] * ensemble_forecast_df['xgboost_forecast']
    
    print("   ✅ Ensemble forecast created!\n")
    
    ENSEMBLE_SUCCESS = True
    
except Exception as e:
    print(f"   ❌ Ensemble creation failed: {e}\n")
    ENSEMBLE_SUCCESS = False

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("="*70)
print("💾 SAVING RESULTS")
print("="*70)

# Save forecasts
if not ensemble_forecast_df.empty:
    # 30-day forecast
    forecast_30 = ensemble_forecast_df.head(30)
    forecast_30.to_csv('data/forecasts/forecast_30day.csv', index=False)
    print("✅ Saved 30-day forecast")
    
    # 60-day forecast
    forecast_60 = ensemble_forecast_df.head(60)
    forecast_60.to_csv('data/forecasts/forecast_60day.csv', index=False)
    print("✅ Saved 60-day forecast")
    
    # 90-day forecast
    forecast_90 = ensemble_forecast_df
    forecast_90.to_csv('data/forecasts/forecast_90day.csv', index=False)
    print("✅ Saved 90-day forecast")

# Save model comparison
comparison_data = {
    'Model': ['ARIMA', 'Prophet', 'LSTM', 'XGBoost'],
    'MAPE': [
        arima_metrics['MAPE'] if ARIMA_SUCCESS else None,
        prophet_metrics['MAPE'] if PROPHET_SUCCESS else None,
        lstm_metrics['MAPE'] if LSTM_SUCCESS else None,
        xgb_metrics['MAPE'] if XGBOOST_SUCCESS else None
    ],
    'RMSE': [
        arima_metrics['RMSE'] if ARIMA_SUCCESS else None,
        prophet_metrics['RMSE'] if PROPHET_SUCCESS else None,
        lstm_metrics['RMSE'] if LSTM_SUCCESS else None,
        xgb_metrics['RMSE'] if XGBOOST_SUCCESS else None
    ],
    'MAE': [
        arima_metrics['MAE'] if ARIMA_SUCCESS else None,
        prophet_metrics['MAE'] if PROPHET_SUCCESS else None,
        lstm_metrics['MAE'] if LSTM_SUCCESS else None,
        xgb_metrics['MAE'] if XGBOOST_SUCCESS else None
    ],
    'R2': [
        arima_metrics['R2'] if ARIMA_SUCCESS else None,
        prophet_metrics['R2'] if PROPHET_SUCCESS else None,
        lstm_metrics['R2'] if LSTM_SUCCESS else None,
        xgb_metrics['R2'] if XGBOOST_SUCCESS else None
    ],
    'Status': [
        'Success' if ARIMA_SUCCESS else 'Failed',
        'Success' if PROPHET_SUCCESS else 'Failed',
        'Success' if LSTM_SUCCESS else 'Failed',
        'Success' if XGBOOST_SUCCESS else 'Failed'
    ]
}

comparison_df = pd.DataFrame(comparison_data)
comparison_df.to_csv('data/forecasts/model_comparison.csv', index=False)
print("✅ Saved model comparison")

# Save ensemble weights
if ENSEMBLE_SUCCESS:
    weights_df = pd.DataFrame(list(weights.items()), columns=['Model', 'Weight'])
    weights_df.to_csv('data/forecasts/ensemble_weights.csv', index=False)
    print("✅ Saved ensemble weights")

print("\n" + "="*70)
print("📊 FINAL SUMMARY")
print("="*70)

print("\n🎯 Model Performance (Test Set):\n")
print(f"{'Model':<15} {'MAPE':<12} {'RMSE':<15} {'MAE':<15} {'R²':<10} {'Status':<10}")
print("-" * 75)

for _, row in comparison_df.iterrows():
    if row['Status'] == 'Success':
        print(f"{row['Model']:<15} {row['MAPE']:>6.2f}%     ₹{row['RMSE']:>12,.0f}  ₹{row['MAE']:>12,.0f}  {row['R2']:>8.4f}  ✅")
    else:
        print(f"{row['Model']:<15} {'Failed':<12} {'Failed':<15} {'Failed':<15} {'Failed':<10} ❌")

if ENSEMBLE_SUCCESS:
    print("\n🏆 ENSEMBLE MODEL:")
    print(f"   Combines all {sum([ARIMA_SUCCESS, PROPHET_SUCCESS, XGBOOST_SUCCESS])} successful models")
    print(f"   Best weight: {max(weights.items(), key=lambda x: x[1])[0]} ({max(weights.values()):.1%})")

print("\n📁 Output Files:")
print("   Models: models/ (4 model files + scalers)")
print("   Forecasts: data/forecasts/ (30/60/90 day forecasts)")
print("   Comparison: data/forecasts/model_comparison.csv")
print("   Weights: data/forecasts/ensemble_weights.csv")

print("\n" + "="*70)
print("✅ MODEL TRAINING COMPLETE!")
print("="*70)
print("\n🎯 Next Step: Create interactive dashboard with all forecasts!\n")
