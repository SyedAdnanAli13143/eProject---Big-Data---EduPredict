"""
Student Performance Prediction Model
Predicts a student's average grade based on attendance, LMS engagement, and demographics.

Run: python ml/train_performance.py
"""

import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

FEATURES = [
    "age", "dept_encoded", "attendance_rate", "total_classes",
    "avg_lms_time", "avg_logins", "avg_assignments", "avg_forum_posts",
]
TARGET = "avg_grade"


def train():
    """Train and save student performance model."""
    print("=" * 50)
    print("Student Performance Prediction Model")
    print("=" * 50)

    # Load data
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "student_features.csv"))
    print(f"\nDataset: {len(df)} students")

    X = df[FEATURES]
    y = df[TARGET]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Train: {len(X_train)} | Test: {len(X_test)}")

    # Train Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\nResults:")
    print(f"  MAE:  {mae:.4f}")
    print(f"  RMSE: {rmse:.4f}")
    print(f"  R2:   {r2:.4f}")

    # Feature importance
    importance = sorted(zip(FEATURES, model.feature_importances_), key=lambda x: x[1], reverse=True)
    print(f"\nFeature Importance:")
    for feat, imp in importance:
        print(f"  {feat:25s} {imp:.4f}")

    # Save model
    model_path = os.path.join(MODEL_DIR, "performance_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"\nModel saved to: {model_path}")

    return model, {"mae": mae, "rmse": rmse, "r2": r2}


if __name__ == "__main__":
    train()
