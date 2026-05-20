"""
Dropout Risk Prediction Model
Binary classification: predicts whether a student is at risk of dropping out.

Run: python ml/train_dropout.py
"""

import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

FEATURES = [
    "age", "dept_encoded", "attendance_rate", "total_classes",
    "avg_grade", "grade_std", "total_courses",
    "avg_lms_time", "avg_logins", "avg_assignments", "avg_forum_posts",
]
TARGET = "is_dropout"


def train():
    """Train and save dropout risk model."""
    print("=" * 50)
    print("Dropout Risk Prediction Model")
    print("=" * 50)

    # Load data
    df = pd.read_csv(os.path.join(PROCESSED_DIR, "student_features.csv"))
    print(f"\nDataset: {len(df)} students")
    print(f"Dropout distribution:\n{df[TARGET].value_counts().to_string()}")

    X = df[FEATURES]
    y = df[TARGET]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"\nTrain: {len(X_train)} | Test: {len(X_test)}")

    # Train Gradient Boosting Classifier
    model = GradientBoostingClassifier(
        n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print(f"\nResults:")
    print(f"  Accuracy:  {acc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall:    {rec:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print(f"\nClassification Report:\n{classification_report(y_test, y_pred, zero_division=0)}")

    # Feature importance
    importance = sorted(zip(FEATURES, model.feature_importances_), key=lambda x: x[1], reverse=True)
    print(f"Feature Importance:")
    for feat, imp in importance:
        print(f"  {feat:25s} {imp:.4f}")

    # Save model
    model_path = os.path.join(MODEL_DIR, "dropout_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"\nModel saved to: {model_path}")

    return model, {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1}


if __name__ == "__main__":
    train()
