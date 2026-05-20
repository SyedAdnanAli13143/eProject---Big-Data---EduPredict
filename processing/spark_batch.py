"""
Spark Batch Processing — reads CSV data and computes student analytics.
Run: python processing/spark_batch.py

Requires: PySpark installed (pip install pyspark)
Works locally on Windows — no Hadoop cluster needed for testing.
"""

import os
import sys

try:
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F
    from pyspark.sql.window import Window
except ImportError:
    print("ERROR: Install pyspark first ->  pip install pyspark")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_spark():
    """Create a local Spark session (works on Windows without Hadoop)."""
    return (
        SparkSession.builder
        .appName("EduPredict-BatchProcessing")
        .master("local[*]")
        .config("spark.driver.memory", "2g")
        .getOrCreate()
    )


def compute_student_features(spark):
    """
    Join all datasets and compute per-student features:
    - attendance_rate
    - avg_grade
    - avg_lms_time
    - assignments_rate
    These features feed directly into the ML models.
    """
    print("\n[1] Loading datasets...")
    students = spark.read.csv(os.path.join(DATA_DIR, "students.csv"), header=True, inferSchema=True)
    attendance = spark.read.csv(os.path.join(DATA_DIR, "attendance.csv"), header=True, inferSchema=True)
    academic = spark.read.csv(os.path.join(DATA_DIR, "academic_records.csv"), header=True, inferSchema=True)
    lms = spark.read.csv(os.path.join(DATA_DIR, "lms_activity.csv"), header=True, inferSchema=True)

    print(f"    Students: {students.count()} | Attendance: {attendance.count()} | "
          f"Academic: {academic.count()} | LMS: {lms.count()}")

    # --- Attendance rate per student ---
    print("[2] Computing attendance rates...")
    att_agg = (
        attendance
        .withColumn("is_present", F.when(F.col("status") == "present", 1).otherwise(0))
        .groupBy("student_id")
        .agg(
            F.mean("is_present").alias("attendance_rate"),
            F.count("*").alias("total_classes"),
        )
    )

    # --- Average grade per student ---
    print("[3] Computing average grades...")
    grade_agg = (
        academic
        .groupBy("student_id")
        .agg(
            F.mean("grade").alias("avg_grade"),
            F.count("*").alias("total_courses_taken"),
        )
    )

    # --- LMS engagement per student ---
    print("[4] Computing LMS engagement...")
    lms_agg = (
        lms
        .groupBy("student_id")
        .agg(
            F.mean("time_spent_minutes").alias("avg_lms_time"),
            F.mean("logins").alias("avg_weekly_logins"),
            F.mean("assignments_submitted").alias("avg_assignments"),
            F.mean("forum_posts").alias("avg_forum_posts"),
        )
    )

    # --- Join everything ---
    print("[5] Joining all features...")
    features = (
        students
        .join(att_agg, "student_id", "left")
        .join(grade_agg, "student_id", "left")
        .join(lms_agg, "student_id", "left")
        .fillna(0)
    )

    # Save as CSV
    output_path = os.path.join(OUTPUT_DIR, "student_features.csv")
    features.toPandas().to_csv(output_path, index=False)
    print(f"\n    Student features saved to: {output_path}")
    print(f"    Total students processed: {features.count()}")
    print(f"    Columns: {features.columns}")

    return features


def compute_course_analytics(spark):
    """Compute per-course enrollment trends for demand forecasting."""
    print("\n[6] Computing course analytics...")
    courses = spark.read.csv(os.path.join(DATA_DIR, "courses.csv"), header=True, inferSchema=True)

    # Enrollment trend per course
    course_trend = (
        courses
        .withColumn("period", F.concat(F.col("year"), F.lit("-"), F.col("semester")))
        .groupBy("course_id", "course_name", "department", "period")
        .agg(
            F.sum("enrolled_count").alias("total_enrolled"),
            F.avg("capacity").alias("avg_capacity"),
        )
        .orderBy("course_id", "period")
    )

    output_path = os.path.join(OUTPUT_DIR, "course_trends.csv")
    course_trend.toPandas().to_csv(output_path, index=False)
    print(f"    Course trends saved to: {output_path}")

    return course_trend


def main():
    print("=" * 60)
    print("EduPredict — Spark Batch Processing")
    print("=" * 60)

    spark = create_spark()
    spark.sparkContext.setLogLevel("WARN")

    try:
        compute_student_features(spark)
        compute_course_analytics(spark)
        print("\n" + "=" * 60)
        print("Batch processing complete!")
        print("=" * 60)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
