"""
Generate synthetic educational datasets for EduPredict.
Run: python data/generate_data.py
Output: CSV files in data/raw/
"""

import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# --- Constants ---
DEPARTMENTS = ["Computer Science", "Mathematics", "Physics", "Business", "Engineering"]
COURSES = {
    "Computer Science": ["CS101-Intro to Programming", "CS201-Data Structures", "CS301-Databases", "CS401-Machine Learning", "CS501-Big Data"],
    "Mathematics": ["MT101-Calculus I", "MT201-Linear Algebra", "MT301-Statistics", "MT401-Discrete Math"],
    "Physics": ["PH101-Mechanics", "PH201-Electromagnetism", "PH301-Thermodynamics"],
    "Business": ["BU101-Accounting", "BU201-Marketing", "BU301-Finance", "BU401-Management"],
    "Engineering": ["EN101-Engineering Drawing", "EN201-Circuit Analysis", "EN301-Control Systems"],
}
SEMESTERS = ["Fall", "Spring"]
YEARS = [2023, 2024, 2025]

NUM_STUDENTS = 500


def generate_students():
    """Generate student demographics."""
    rows = []
    for i in range(1, NUM_STUDENTS + 1):
        dept = random.choice(DEPARTMENTS)
        enroll_year = random.choice([2021, 2022, 2023, 2024])
        age = random.randint(18, 28)
        gpa = round(random.uniform(1.5, 4.0), 2)
        is_dropout = 1 if gpa < 2.0 and random.random() < 0.6 else 0
        rows.append({
            "student_id": f"STU{i:04d}",
            "age": age,
            "gender": random.choice(["M", "F"]),
            "department": dept,
            "enrollment_year": enroll_year,
            "cumulative_gpa": gpa,
            "is_active": 0 if is_dropout else 1,
            "is_dropout": is_dropout,
        })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RAW_DIR, "students.csv"), index=False)
    print(f"  students.csv          -> {len(df)} rows")
    return df


def generate_academic_records(students_df):
    """Generate academic records (grades per course per semester)."""
    rows = []
    rid = 1
    for _, stu in students_df.iterrows():
        dept = stu["department"]
        course_list = COURSES[dept]
        for year in YEARS:
            for sem in SEMESTERS:
                num_courses = random.randint(2, 4)
                for course in random.sample(course_list, min(num_courses, len(course_list))):
                    base_grade = stu["cumulative_gpa"] + random.uniform(-0.8, 0.8)
                    grade = round(max(0.0, min(4.0, base_grade)), 2)
                    rows.append({
                        "record_id": rid,
                        "student_id": stu["student_id"],
                        "course_id": course.split("-")[0],
                        "course_name": course.split("-")[1],
                        "semester": sem,
                        "year": year,
                        "grade": grade,
                        "credits": random.choice([3, 4]),
                    })
                    rid += 1
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RAW_DIR, "academic_records.csv"), index=False)
    print(f"  academic_records.csv  -> {len(df)} rows")
    return df


def generate_attendance(students_df):
    """Generate attendance records."""
    rows = []
    start_date = datetime(2025, 1, 1)
    for _, stu in students_df.iterrows():
        # Each student has ~60 attendance entries
        attendance_rate = 0.5 + (stu["cumulative_gpa"] / 4.0) * 0.4  # higher GPA = better attendance
        for day_offset in range(0, 120, 2):  # every other day for ~60 entries
            date = start_date + timedelta(days=day_offset)
            if date.weekday() >= 5:
                continue
            status = np.random.choice(
                ["present", "absent", "late"],
                p=[attendance_rate, (1 - attendance_rate) * 0.7, (1 - attendance_rate) * 0.3],
            )
            dept = stu["department"]
            course = random.choice(COURSES[dept])
            rows.append({
                "student_id": stu["student_id"],
                "course_id": course.split("-")[0],
                "date": date.strftime("%Y-%m-%d"),
                "status": status,
            })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RAW_DIR, "attendance.csv"), index=False)
    print(f"  attendance.csv        -> {len(df)} rows")
    return df


def generate_lms_activity(students_df):
    """Generate LMS (Learning Management System) activity data."""
    rows = []
    start_date = datetime(2025, 1, 1)
    for _, stu in students_df.iterrows():
        engagement = stu["cumulative_gpa"] / 4.0  # 0 to 1
        for week in range(20):
            date = start_date + timedelta(weeks=week)
            rows.append({
                "student_id": stu["student_id"],
                "week_start": date.strftime("%Y-%m-%d"),
                "logins": max(0, int(engagement * 12 + random.randint(-3, 3))),
                "time_spent_minutes": max(0, int(engagement * 300 + random.randint(-60, 60))),
                "assignments_submitted": max(0, int(engagement * 5 + random.randint(-1, 1))),
                "forum_posts": max(0, int(engagement * 3 + random.randint(-1, 2))),
            })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RAW_DIR, "lms_activity.csv"), index=False)
    print(f"  lms_activity.csv      -> {len(df)} rows")
    return df


def generate_courses():
    """Generate course catalog with enrollment history (with growing trend)."""
    rows = []
    for dept, course_list in COURSES.items():
        for course in course_list:
            cid, cname = course.split("-")
            base_enrollment = random.randint(25, 60)
            capacity = random.choice([60, 80, 100])
            credits = random.choice([3, 4])
            for year in YEARS:
                for sem in SEMESTERS:
                    # Enrollment grows over time with some noise
                    period_idx = (year - 2023) * 2 + (1 if sem == "Spring" else 0)
                    trend = base_enrollment + period_idx * random.randint(2, 5)
                    noise = random.randint(-5, 5)
                    enrolled = max(10, min(capacity, trend + noise))
                    rows.append({
                        "course_id": cid,
                        "course_name": cname,
                        "department": dept,
                        "credits": credits,
                        "capacity": capacity,
                        "semester": sem,
                        "year": year,
                        "enrolled_count": enrolled,
                    })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(RAW_DIR, "courses.csv"), index=False)
    print(f"  courses.csv           -> {len(df)} rows")
    return df


if __name__ == "__main__":
    print("Generating synthetic data for EduPredict...\n")
    stu = generate_students()
    generate_academic_records(stu)
    generate_attendance(stu)
    generate_lms_activity(stu)
    generate_courses()
    print(f"\nAll files saved to: {RAW_DIR}")
