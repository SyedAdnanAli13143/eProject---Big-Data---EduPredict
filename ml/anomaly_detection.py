"""
Anomaly Detection in Student Data
Uses Isolation Forest to detect unusual student behavior patterns
(e.g., sudden drop in attendance, abnormal LMS activity).

Run: python ml/anomaly_detection.py
"""

import os
import pickle
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

FEATURES = [
    "attendance_rate", "avg_grade", "grade_std",
    "avg_lms_time", "avg_logins", "avg_assignments", "avg_forum_posts",
]


def detect_anomalies():
    """Train Isolation Forest and flag anomalous students."""
    print("=" * 50)
    print("Anomaly Detection — Isolation Forest")
    print("=" * 50)

    # Load data
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "student_features.csv"))
    print(f"\nDataset: {len(df)} students")

    X = df[FEATURES].copy()

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Isolation Forest (contamination = expected % of anomalies)
    model = IsolationForest(n_estimators=100, contamination=0.08, random_state=42)
    predictions = model.fit_predict(X_scaled)

    # -1 = anomaly, 1 = normal
    df["anomaly"] = predictions
    df["anomaly_label"] = df["anomaly"].map({1: "Normal", -1: "Anomaly"})

    # Results
    anomalies = df[df["anomaly"] == -1]
    print(f"\nAnomalies detected: {len(anomalies)} out of {len(df)} ({len(anomalies)/len(df)*100:.1f}%)")
    print(f"\nAnomaly students summary:")
    print(anomalies[["student_id", "attendance_rate", "avg_grade", "avg_lms_time", "is_dropout"]].to_string(index=False))

    # Save results
    output_path = os.path.join(PROCESSED_DIR, "anomaly_results.csv")
    df[["student_id", "anomaly_label"] + FEATURES].to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")

    # Save model + scaler
    model_path = os.path.join(MODEL_DIR, "anomaly_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump({"model": model, "scaler": scaler}, f)
    print(f"Model saved to: {model_path}")

    return model, anomalies


if __name__ == "__main__":
    detect_anomalies()
