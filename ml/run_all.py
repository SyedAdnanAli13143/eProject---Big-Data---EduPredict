"""
Run the complete ML pipeline: preprocess -> train all models -> anomaly detection.
Run: python ml/run_all.py

This runs entirely on Windows with just Python — no Docker needed.
"""

import os
import sys
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from preprocess import run_preprocessing
from train_performance import train as train_performance
from train_dropout import train as train_dropout
from train_demand import train as train_demand
from anomaly_detection import detect_anomalies

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


def main():
    print("=" * 60)
    print("  EduPredict — Full ML Pipeline")
    print("=" * 60)

    # Step 1: Preprocess
    print("\n>>> STEP 1: Data Preprocessing")
    print("-" * 40)
    run_preprocessing()

    # Step 2: Student Performance Model
    print("\n\n>>> STEP 2: Student Performance Model")
    print("-" * 40)
    _, perf_metrics = train_performance()

    # Step 3: Dropout Risk Model
    print("\n\n>>> STEP 3: Dropout Risk Model")
    print("-" * 40)
    _, dropout_metrics = train_dropout()

    # Step 4: Course Demand Model
    print("\n\n>>> STEP 4: Course Demand Model")
    print("-" * 40)
    _, demand_metrics = train_demand()

    # Step 5: Anomaly Detection
    print("\n\n>>> STEP 5: Anomaly Detection")
    print("-" * 40)
    _, anomalies = detect_anomalies()

    # Save summary report
    report = {
        "performance_model": perf_metrics,
        "dropout_model": dropout_metrics,
        "demand_model": demand_metrics,
        "anomalies_found": len(anomalies),
    }
    report_path = os.path.join(MODEL_DIR, "training_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    # Final summary
    print("\n\n" + "=" * 60)
    print("  PIPELINE COMPLETE — Summary")
    print("=" * 60)
    print(f"\n  Performance Model:  R2={perf_metrics['r2']:.4f}  MAE={perf_metrics['mae']:.4f}")
    print(f"  Dropout Model:      F1={dropout_metrics['f1']:.4f}  Acc={dropout_metrics['accuracy']:.4f}")
    print(f"  Demand Model:       R2={demand_metrics['r2']:.4f}  MAE={demand_metrics['mae']:.4f}")
    print(f"  Anomalies Detected: {len(anomalies)}")
    print(f"\n  Models saved to:    {MODEL_DIR}")
    print(f"  Report saved to:    {report_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
