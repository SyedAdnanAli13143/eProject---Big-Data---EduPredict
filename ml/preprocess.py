"""
Data Preprocessing & Feature Engineering for ML models.
Reads raw CSVs (or Spark-processed features) and builds clean feature sets.

Run: python ml/preprocess.py
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "..", "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)


def load_raw_data():
    """Load all raw CSVs."""
    print("Loading raw data...")
    students = pd.read_csv(os.path.join(RAW_DIR, "students.csv"))
    academic = pd.read_csv(os.path.join(RAW_DIR, "academic_records.csv"))
    attendance = pd.read_csv(os.path.join(RAW_DIR, "attendance.csv"))
    lms = pd.read_csv(os.path.join(RAW_DIR, "lms_activity.csv"))
    courses = pd.read_csv(os.path.join(RAW_DIR, "courses.csv"))
    print(f"  Students: {len(students)} | Academic: {len(academic)} | "
          f"Attendance: {len(attendance)} | LMS: {len(lms)} | Courses: {len(courses)}")
    return students, academic, attendance, lms, courses


def build_student_features(students, academic, attendance, lms):
    """
    Build a single feature table per student for ML models.
    Returns DataFrame with columns ready for training.
    """
    print("\nBuilding student features...")

    # --- Attendance rate ---
    att = attendance.copy()
    att["is_present"] = (att["status"] == "present").astype(int)
    att_agg = att.groupby("student_id").agg(
        attendance_rate=("is_present", "mean"),
        total_classes=("is_present", "count"),
    ).reset_index()

    # --- Academic performance ---
    grade_agg = academic.groupby("student_id").agg(
        avg_grade=("grade", "mean"),
        total_courses=("grade", "count"),
        grade_std=("grade", "std"),
    ).reset_index()
    grade_agg["grade_std"] = grade_agg["grade_std"].fillna(0)

    # --- LMS engagement ---
    lms_agg = lms.groupby("student_id").agg(
        avg_lms_time=("time_spent_minutes", "mean"),
        avg_logins=("logins", "mean"),
        avg_assignments=("assignments_submitted", "mean"),
        avg_forum_posts=("forum_posts", "mean"),
    ).reset_index()

    # --- Merge all ---
    features = students.merge(att_agg, on="student_id", how="left")
    features = features.merge(grade_agg, on="student_id", how="left")
    features = features.merge(lms_agg, on="student_id", how="left")

    # Fill missing values
    features = features.fillna(0)

    # Encode department as numeric
    features["dept_encoded"] = features["department"].astype("category").cat.codes

    # Save
    output_path = os.path.join(PROCESSED_DIR, "student_features.csv")
    features.to_csv(output_path, index=False)
    print(f"  Saved {len(features)} rows to {output_path}")
    print(f"  Columns: {list(features.columns)}")

    return features


def build_course_demand_features(courses):
    """Build features for course demand forecasting."""
    print("\nBuilding course demand features...")

    df = courses.copy()
    # Create numeric period for time-series ordering
    df["period_num"] = df["year"] * 2 + (df["semester"] == "Spring").astype(int)
    df["dept_encoded"] = df["department"].astype("category").cat.codes
    df["course_encoded"] = df["course_id"].astype("category").cat.codes

    output_path = os.path.join(PROCESSED_DIR, "course_demand_features.csv")
    df.to_csv(output_path, index=False)
    print(f"  Saved {len(df)} rows to {output_path}")

    return df


def run_preprocessing():
    """Run the full preprocessing pipeline."""
    students, academic, attendance, lms, courses = load_raw_data()
    student_features = build_student_features(students, academic, attendance, lms)
    course_features = build_course_demand_features(courses)
    print("\nPreprocessing complete!")
    return student_features, course_features


if __name__ == "__main__":
    run_preprocessing()
