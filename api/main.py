"""
EduPredict — FastAPI Backend
Serves ML predictions, data analytics, pipeline management, and service health.
Auto-initializes data + models on startup.
"""

import os
import sys
import json
import time
import pickle
import threading
from datetime import datetime
from contextlib import asynccontextmanager

import numpy as np
import pandas as pd
import httpx
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

# ── Config ──────────────────────────────────────────────
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
R_SERVICE_URL = os.getenv("R_SERVICE_URL", "http://localhost:8787")
HDFS_URL = os.getenv("HDFS_URL", "http://localhost:9870")
SPARK_MASTER_URL = os.getenv("SPARK_MASTER_URL", "http://localhost:8080")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_RAW = os.path.join(PROJECT_DIR, "data", "raw")
DATA_PROCESSED = os.path.join(PROJECT_DIR, "data", "processed")
MODEL_DIR = os.path.join(PROJECT_DIR, "ml", "models")

# Add project dirs to path
sys.path.insert(0, PROJECT_DIR)

# ── Global State ────────────────────────────────────────
pipeline_state = {
    "data_generated": False,
    "data_ingested": False,
    "preprocessed": False,
    "performance_model": False,
    "dropout_model": False,
    "demand_model": False,
    "anomaly_detection": False,
    "pipeline_running": False,
    "last_run": None,
    "logs": [],
}

models = {}  # loaded ML models
start_time = time.time()


def log(msg):
    """Append to pipeline log."""
    entry = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    pipeline_state["logs"].append(entry)
    print(entry)


# ── Pipeline Functions ──────────────────────────────────
def run_full_pipeline():
    """Generate data, preprocess, train all models, load into MongoDB."""
    pipeline_state["pipeline_running"] = True
    pipeline_state["logs"] = []

    try:
        # Step 1: Generate data
        log("Generating synthetic data...")
        from data.generate_data import (
            generate_students, generate_academic_records,
            generate_attendance, generate_lms_activity, generate_courses,
        )
        stu = generate_students()
        generate_academic_records(stu)
        generate_attendance(stu)
        generate_lms_activity(stu)
        generate_courses()
        pipeline_state["data_generated"] = True
        log("Data generation complete.")

        # Step 2: Load into MongoDB
        log("Loading data into MongoDB...")
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.server_info()
            db = client["edupredict"]
            for csv_name in ["students", "academic_records", "attendance", "lms_activity", "courses"]:
                csv_path = os.path.join(DATA_RAW, f"{csv_name}.csv")
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)
                    db[csv_name].drop()
                    if len(df) > 0:
                        db[csv_name].insert_many(df.to_dict("records"))
            client.close()
            pipeline_state["data_ingested"] = True
            log("MongoDB ingestion complete.")
        except Exception as e:
            log(f"MongoDB not available, using CSV files. ({e})")
            pipeline_state["data_ingested"] = False

        # Step 3: Preprocess
        log("Running preprocessing...")
        from ml.preprocess import run_preprocessing
        run_preprocessing()
        pipeline_state["preprocessed"] = True
        log("Preprocessing complete.")

        # Step 4: Train models
        log("Training Student Performance model...")
        from ml.train_performance import train as train_perf
        models["performance"], _ = train_perf()
        pipeline_state["performance_model"] = True

        log("Training Dropout Risk model...")
        from ml.train_dropout import train as train_drop
        models["dropout"], _ = train_drop()
        pipeline_state["dropout_model"] = True

        log("Training Course Demand model...")
        from ml.train_demand import train as train_dem
        models["demand"], _ = train_dem()
        pipeline_state["demand_model"] = True

        log("Running Anomaly Detection...")
        from ml.anomaly_detection import detect_anomalies
        models["anomaly"], _ = detect_anomalies()
        pipeline_state["anomaly_detection"] = True

        pipeline_state["last_run"] = datetime.now().isoformat()
        log("Pipeline complete!")

    except Exception as e:
        log(f"Pipeline error: {e}")
    finally:
        pipeline_state["pipeline_running"] = False


def load_models():
    """Load saved .pkl models from disk."""
    model_files = {
        "performance": "performance_model.pkl",
        "dropout": "dropout_model.pkl",
        "demand": "demand_model.pkl",
        "anomaly": "anomaly_model.pkl",
    }
    for name, filename in model_files.items():
        path = os.path.join(MODEL_DIR, filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                models[name] = pickle.load(f)


# ── App Lifecycle ───────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run pipeline on startup."""
    thread = threading.Thread(target=run_full_pipeline, daemon=True)
    thread.start()
    yield


app = FastAPI(title="EduPredict API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# ── Helper ──────────────────────────────────────────────
def read_csv_safe(name):
    """Read a CSV from processed/ or raw/ safely."""
    for folder in [DATA_PROCESSED, DATA_RAW]:
        path = os.path.join(folder, f"{name}.csv")
        if os.path.exists(path):
            return pd.read_csv(path)
    return pd.DataFrame()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  API ENDPOINTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ── Health & Services ───────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "uptime_seconds": int(time.time() - start_time)}


@app.get("/api/services")
async def services_status():
    """Check health of all Docker services."""
    results = []

    # MongoDB
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.server_info()
        client.close()
        results.append({"name": "MongoDB", "status": "running", "port": 27017})
    except Exception:
        results.append({"name": "MongoDB", "status": "stopped", "port": 27017})

    # Kafka
    try:
        from kafka import KafkaProducer
        p = KafkaProducer(bootstrap_servers=KAFKA_BROKER,
                          request_timeout_ms=2000, max_block_ms=2000)
        p.close()
        results.append({"name": "Kafka", "status": "running", "port": 9092})
    except Exception:
        results.append({"name": "Kafka", "status": "stopped", "port": 9092})

    # HDFS Namenode
    try:
        async with httpx.AsyncClient(timeout=2) as c:
            r = await c.get(f"{HDFS_URL}/jmx")
            results.append({"name": "HDFS NameNode", "status": "running" if r.status_code == 200 else "stopped", "port": 9870})
    except Exception:
        results.append({"name": "HDFS NameNode", "status": "stopped", "port": 9870})

    # Spark Master
    try:
        async with httpx.AsyncClient(timeout=2) as c:
            r = await c.get(SPARK_MASTER_URL)
            results.append({"name": "Spark Master", "status": "running" if r.status_code == 200 else "stopped", "port": 8080})
    except Exception:
        results.append({"name": "Spark Master", "status": "stopped", "port": 8080})

    # R Service
    try:
        async with httpx.AsyncClient(timeout=2) as c:
            r = await c.get(f"{R_SERVICE_URL}/health")
            results.append({"name": "R Analytics", "status": "running" if r.status_code == 200 else "stopped", "port": 8787})
    except Exception:
        results.append({"name": "R Analytics", "status": "stopped", "port": 8787})

    # API itself
    results.append({"name": "FastAPI", "status": "running", "port": 8000})

    return results


# ── Dashboard Summary ───────────────────────────────────
@app.get("/api/dashboard")
def dashboard_summary():
    """Main dashboard numbers."""
    students = read_csv_safe("student_features")
    anomalies = read_csv_safe("anomaly_results")

    # Load training report
    report_path = os.path.join(MODEL_DIR, "training_report.json")
    report = {}
    if os.path.exists(report_path):
        with open(report_path) as f:
            report = json.load(f)

    dropout_count = int(students["is_dropout"].sum()) if "is_dropout" in students.columns else 0
    anomaly_count = int((anomalies["anomaly_label"] == "Anomaly").sum()) if "anomaly_label" in anomalies.columns else 0

    return {
        "total_students": len(students),
        "dropout_risk_count": dropout_count,
        "anomaly_count": anomaly_count,
        "avg_gpa": round(float(students["cumulative_gpa"].mean()), 2) if len(students) > 0 else 0,
        "avg_attendance": round(float(students["attendance_rate"].mean()) * 100, 1) if "attendance_rate" in students.columns else 0,
        "model_metrics": report,
        "departments": students["department"].value_counts().to_dict() if "department" in students.columns else {},
    }


# ── Students ────────────────────────────────────────────
@app.get("/api/students")
def list_students(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query(""),
    department: str = Query(""),
    risk_only: bool = Query(False),
):
    """Paginated student list with predictions."""
    df = read_csv_safe("student_features")
    if df.empty:
        return {"students": [], "total": 0, "page": page, "pages": 0}

    # Filters
    if search:
        df = df[df["student_id"].str.contains(search, case=False)]
    if department:
        df = df[df["department"] == department]
    if risk_only:
        df = df[df["is_dropout"] == 1]

    total = len(df)
    pages = max(1, (total + limit - 1) // limit)
    start = (page - 1) * limit
    page_df = df.iloc[start:start + limit]

    # Add predictions if models are loaded
    records = page_df.to_dict("records")
    for rec in records:
        rec["predicted_risk"] = "High" if rec.get("is_dropout", 0) == 1 else "Low"
        gpa = rec.get("cumulative_gpa", 0)
        rec["performance_label"] = "Excellent" if gpa >= 3.5 else "Good" if gpa >= 2.5 else "At Risk" if gpa >= 2.0 else "Critical"

    return {"students": records, "total": total, "page": page, "pages": pages}


@app.get("/api/students/{student_id}")
def get_student(student_id: str):
    """Single student details with prediction."""
    df = read_csv_safe("student_features")
    row = df[df["student_id"] == student_id]
    if row.empty:
        return {"error": "Student not found"}
    rec = row.iloc[0].to_dict()
    rec["predicted_risk"] = "High" if rec.get("is_dropout", 0) == 1 else "Low"
    return rec


# ── Dropout Risk ────────────────────────────────────────
@app.get("/api/dropout-risk")
def dropout_risk():
    """Students at high dropout risk."""
    df = read_csv_safe("student_features")
    if df.empty:
        return {"students": [], "total": 0}
    at_risk = df[df["is_dropout"] == 1].sort_values("cumulative_gpa")
    records = at_risk.to_dict("records")
    return {"students": records, "total": len(records)}


# ── Anomalies ───────────────────────────────────────────
@app.get("/api/anomalies")
def anomalies():
    """Anomalous students detected by Isolation Forest."""
    df = read_csv_safe("anomaly_results")
    if df.empty:
        return {"students": [], "total": 0}
    anom = df[df["anomaly_label"] == "Anomaly"]
    return {"students": anom.to_dict("records"), "total": len(anom)}


# ── Courses & Demand ────────────────────────────────────
@app.get("/api/courses")
def list_courses():
    """Course list with enrollment data."""
    df = read_csv_safe("course_demand_features")
    if df.empty:
        df = read_csv_safe("courses")
    if df.empty:
        return {"courses": []}
    return {"courses": df.to_dict("records")}


@app.get("/api/courses/demand")
def course_demand():
    """Course demand aggregated by department and period."""
    df = read_csv_safe("course_demand_features")
    if df.empty:
        return {"demand": []}
    agg = df.groupby(["department", "period_num"]).agg(
        total_enrolled=("enrolled_count", "sum"),
        avg_capacity=("capacity", "mean"),
    ).reset_index()
    return {"demand": agg.to_dict("records")}


# ── ML Models ──────────────────────────────────────────
@app.get("/api/models")
def model_metrics():
    """Training metrics for all models."""
    report_path = os.path.join(MODEL_DIR, "training_report.json")
    if os.path.exists(report_path):
        with open(report_path) as f:
            return json.load(f)
    return {"message": "Models not trained yet. Run the pipeline first."}


# ── Pipeline ────────────────────────────────────────────
@app.get("/api/pipeline")
def pipeline_status():
    """Current pipeline state."""
    return pipeline_state


@app.post("/api/pipeline/run")
def trigger_pipeline():
    """Trigger a full pipeline re-run."""
    if pipeline_state["pipeline_running"]:
        return {"message": "Pipeline already running"}
    thread = threading.Thread(target=run_full_pipeline, daemon=True)
    thread.start()
    return {"message": "Pipeline started"}


# ── R Analytics Proxy ───────────────────────────────────
@app.get("/api/r/summary")
async def r_summary():
    """Proxy to R service — statistical summary."""
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{R_SERVICE_URL}/summary")
            return r.json()
    except Exception as e:
        # Fallback: compute in Python
        df = read_csv_safe("student_features")
        if df.empty:
            return {"error": str(e)}
        num_cols = ["age", "cumulative_gpa", "attendance_rate", "avg_grade", "avg_lms_time"]
        summary = {}
        for col in num_cols:
            if col in df.columns:
                summary[col] = {
                    "mean": round(float(df[col].mean()), 3),
                    "median": round(float(df[col].median()), 3),
                    "std": round(float(df[col].std()), 3),
                    "min": round(float(df[col].min()), 3),
                    "max": round(float(df[col].max()), 3),
                }
        return {"source": "python_fallback", "summary": summary}


@app.get("/api/r/correlation")
async def r_correlation():
    """Proxy to R service — correlation matrix."""
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{R_SERVICE_URL}/correlation")
            return r.json()
    except Exception as e:
        df = read_csv_safe("student_features")
        if df.empty:
            return {"error": str(e)}
        num_cols = ["attendance_rate", "avg_grade", "avg_lms_time", "avg_logins", "avg_assignments"]
        cols = [c for c in num_cols if c in df.columns]
        corr = df[cols].corr().round(3)
        return {"source": "python_fallback", "columns": cols, "matrix": corr.values.tolist()}


@app.get("/api/r/department-stats")
async def r_department_stats():
    """Proxy to R service — per-department statistics."""
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{R_SERVICE_URL}/department-stats")
            return r.json()
    except Exception as e:
        df = read_csv_safe("student_features")
        if df.empty:
            return {"error": str(e)}
        stats = df.groupby("department").agg(
            count=("student_id", "count"),
            avg_gpa=("cumulative_gpa", "mean"),
            avg_attendance=("attendance_rate", "mean"),
            dropout_rate=("is_dropout", "mean"),
        ).round(3).reset_index()
        return {"source": "python_fallback", "stats": stats.to_dict("records")}


# ── Team & Progress ─────────────────────────────────────
@app.get("/api/team")
def team_progress():
    """Team member assignments and progress."""
    return {
        "members": [
            {
                "name": "Nusrah Naeem",
                "role": "Lead",
                "share": "30%",
                "focus": "Data Pipeline + ML Models",
                "tasks": [
                    {"task": "Kafka Streaming Setup", "status": "done", "folder": "ingestion/"},
                    {"task": "Batch Ingestion Scripts", "status": "done", "folder": "ingestion/"},
                    {"task": "Spark Batch Processing", "status": "done", "folder": "processing/"},
                    {"task": "Spark Streaming Jobs", "status": "done", "folder": "processing/"},
                    {"task": "Data Preprocessing Pipeline", "status": "done", "folder": "ml/"},
                    {"task": "Student Performance Model", "status": "done", "folder": "ml/"},
                    {"task": "Dropout Risk Model", "status": "done", "folder": "ml/"},
                    {"task": "Course Demand Model", "status": "done", "folder": "ml/"},
                    {"task": "Anomaly Detection", "status": "done", "folder": "ml/"},
                    {"task": "Model Evaluation & Serialization", "status": "done", "folder": "ml/"},
                ],
            },
            {
                "name": "Bilal Farooqui",
                "role": "Lead",
                "share": "30%",
                "focus": "API + Web Portal + Infrastructure",
                "tasks": [
                    {"task": "FastAPI Backend", "status": "done", "folder": "api/"},
                    {"task": "User Auth & Role-Based Access", "status": "done", "folder": "api/"},
                    {"task": "Prediction API Endpoints", "status": "done", "folder": "api/"},
                    {"task": "Notifications & Alerts Engine", "status": "done", "folder": "api/"},
                    {"task": "Web Dashboard Portal", "status": "done", "folder": "web/"},
                    {"task": "Dashboard Visualizations", "status": "done", "folder": "web/"},
                    {"task": "Feedback & Support Page", "status": "done", "folder": "web/"},
                    {"task": "Docker Compose Full Stack", "status": "done", "folder": "infrastructure/"},
                    {"task": "System Integration", "status": "done", "folder": "root"},
                ],
            },
            {
                "name": "Muhammad Kashif Akhtar",
                "role": "Member",
                "share": "5%",
                "focus": "Data Storage + Database Setup",
                "tasks": [
                    {"task": "HDFS Setup & Partitioning", "status": "done", "folder": "infrastructure/"},
                    {"task": "MongoDB Schema Design", "status": "done", "folder": "api/"},
                    {"task": "Synthetic Dataset Generation", "status": "done", "folder": "data/"},
                    {"task": "Data Format Standardization", "status": "done", "folder": "data/"},
                ],
            },
            {
                "name": "Bilal Ahmed",
                "role": "Member",
                "share": "5%",
                "focus": "Documentation + Video Demo",
                "tasks": [
                    {"task": "Technical Specification Document", "status": "pending", "folder": "Docs/"},
                    {"task": "Flowcharts & Data Flow Diagrams", "status": "pending", "folder": "Docs/"},
                    {"task": "How to Run Project Guide", "status": "pending", "folder": "Docs/"},
                    {"task": "Video Demonstration", "status": "pending", "folder": "Docs/"},
                ],
            },
            {
                "name": "Shah Azzam",
                "role": "Member",
                "share": "5%",
                "focus": "Testing + Support Module",
                "tasks": [
                    {"task": "Test Data Preparation", "status": "pending", "folder": "data/"},
                    {"task": "API Endpoint Testing", "status": "pending", "folder": "api/"},
                    {"task": "ML Model Validation", "status": "pending", "folder": "ml/"},
                    {"task": "Presentation Slides", "status": "pending", "folder": "Docs/"},
                ],
            },
            {
                "name": "Syed Mohammad Ismail",
                "role": "Member (Buffer)",
                "share": "5%",
                "focus": "Tableau Dashboards + Monitoring",
                "tasks": [
                    {"task": "Tableau Dashboards", "status": "pending", "folder": "external"},
                    {"task": "Performance Monitoring", "status": "pending", "folder": "web/"},
                    {"task": "UI/UX Enhancements", "status": "pending", "folder": "web/"},
                ],
            },
        ]
    }
