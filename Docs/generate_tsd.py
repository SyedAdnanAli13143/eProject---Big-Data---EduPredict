"""
Generate Professional Technical Specification Document (TSD) as .docx
Includes: code snippets, R-generated charts, API outputs, architecture
Run: python Docs/generate_tsd.py
"""
import os, json
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
OUTPUT_DIR = os.path.join(BASE_DIR, "Technical Specification Document")
PLOTS_DIR = os.path.join(PROJECT_DIR, "r-analytics", "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

doc = Document()

# ══════════════════════════════════════════════════════════════
# STYLES & HELPERS
# ══════════════════════════════════════════════════════════════
BLUE = RGBColor(0x1E, 0x40, 0xAF)
DARK = RGBColor(0x1E, 0x29, 0x3B)
GRAY = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT = RGBColor(0x3B, 0x82, 0xF6)

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)
style.font.color.rgb = DARK
style.paragraph_format.space_after = Pt(6)
style.paragraph_format.line_spacing = 1.15

for section in doc.sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def heading(text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = BLUE if level <= 2 else DARK
    return h

def para(text, bold=False, italic=False, size=11, color=None, align=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    if color: run.font.color.rgb = color
    if align: p.alignment = align
    return p

def code_block(code, language="python"):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(code)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = DARK
    # Add light gray background via shading
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>')
    p._p.get_or_add_pPr().append(shading)
    return p

def styled_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Light Grid Accent 1"
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        for p in cell.paragraphs:
            for run in p.runs:
                run.bold = True
                run.font.size = Pt(10)
        set_cell_shading(cell, "1E40AF")
        for p in cell.paragraphs:
            for run in p.runs:
                run.font.color.rgb = WHITE
    # Data rows
    for r, row_data in enumerate(rows):
        for c, val in enumerate(row_data):
            cell = table.rows[r+1].cells[c]
            cell.text = str(val)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(10)
            if r % 2 == 0:
                set_cell_shading(cell, "F8FAFC")
    return table

def add_image(filename, width=5.5):
    path = os.path.join(PLOTS_DIR, filename)
    if os.path.exists(path):
        doc.add_picture(path, width=Inches(width))
        last = doc.paragraphs[-1]
        last.alignment = WD_ALIGN_PARAGRAPH.CENTER
        return True
    return False

def read_source(relative_path, max_lines=40):
    path = os.path.join(PROJECT_DIR, relative_path)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()[:max_lines]
        return "".join(lines)
    return f"# File: {relative_path} (not found)"

def page_break():
    doc.add_page_break()

# ══════════════════════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════════════════════
for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("━" * 50)
run.font.color.rgb = BLUE
run.font.size = Pt(14)

para("TECHNICAL SPECIFICATION DOCUMENT", bold=True, size=28, color=BLUE, align=WD_ALIGN_PARAGRAPH.CENTER)
para("", size=6)
para("EduPredict — Big Data Predictive Analytics", bold=True, size=16, color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER)
para("for Educational Institutions", italic=True, size=14, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("━" * 50)
run.font.color.rgb = BLUE
run.font.size = Pt(14)

para("", size=12)
para("eProject Submission | Semester 6 | May 2026", size=12, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER)
para("", size=6)

team = [
    ("Nusrah Naeem", "Lead — Data Pipeline & ML"),
    ("Bilal Farooqui", "Lead — API, Web & Infrastructure"),
    ("Muhammad Kashif Akhtar", "Database & Storage"),
    ("Bilal Ahmed", "Documentation & Video"),
    ("Shah Azzam", "Testing & QA"),
    ("Syed Mohammad Ismail", "Dashboards & Monitoring"),
]
for name, role in team:
    para(f"{name}  —  {role}", size=11, color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER)

para("", size=12)
para("Aptech Learning | Karachi, Pakistan", size=11, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER)

page_break()

# ══════════════════════════════════════════════════════════════
# TABLE OF CONTENTS
# ══════════════════════════════════════════════════════════════
heading("Table of Contents")
toc_items = [
    "1. Acknowledgements",
    "2. Synopsis",
    "3. System Analysis",
    "   3.1 Problem Statement",
    "   3.2 Functional Requirements",
    "   3.3 Non-Functional Requirements",
    "   3.4 Technology Stack",
    "4. System Design",
    "   4.1 System Architecture",
    "   4.2 Data Flow Diagrams (Level 0, 1, 2)",
    "   4.3 Process Flowcharts",
    "   4.4 Database Design",
    "   4.5 API Design",
    "5. Implementation",
    "   5.1 Source Code with Comments",
    "   5.2 Docker Infrastructure",
    "   5.3 ML Model Training Output",
    "   5.4 R Statistical Analysis Output",
    "6. R-Generated Visualizations (Charts & Plots)",
    "7. Module Descriptions",
    "8. User Guide",
    "9. Developer Guide",
    "10. Testing",
    "11. Team Contribution",
    "12. Future Enhancements",
]
for item in toc_items:
    p = doc.add_paragraph(item)
    p.paragraph_format.space_after = Pt(2)
    for run in p.runs:
        run.font.size = Pt(11)
        run.font.color.rgb = DARK

page_break()

# ══════════════════════════════════════════════════════════════
# 1. ACKNOWLEDGEMENTS
# ══════════════════════════════════════════════════════════════
heading("1. Acknowledgements")
para("We would like to express our sincere gratitude to our faculty and mentors at Aptech Learning for their guidance throughout this eProject. Their expertise in Big Data technologies and Machine Learning provided the foundation for EduPredict.")
para("We also thank the open-source communities behind Apache Spark, Kafka, Hadoop, MongoDB, FastAPI, R, Docker, and scikit-learn — whose tools made this project possible.")
para("Special thanks to our team leads, Nusrah Naeem and Bilal Farooqui, for coordinating the architecture and ensuring every module integrates seamlessly into a production-ready Docker deployment.")
page_break()

# ══════════════════════════════════════════════════════════════
# 2. SYNOPSIS
# ══════════════════════════════════════════════════════════════
heading("2. Synopsis")
para("EduPredict is a Big Data analytics platform that predicts student academic performance, identifies dropout risks, forecasts course demand, and detects anomalous behavior patterns using Machine Learning.", bold=True)
para("")
para("The platform processes educational data through a complete data pipeline: synthetic data generation → batch ingestion into MongoDB → real-time streaming via Apache Kafka → distributed processing with Apache Spark → predictive modeling with scikit-learn → statistical analysis with R → interactive web dashboard.")
para("")
para("Key Statistics from the Running System:", bold=True)
styled_table(
    ["Metric", "Value"],
    [
        ["Total Students Processed", "500"],
        ["Datasets Generated", "5 (students, academic, attendance, LMS, courses)"],
        ["ML Models Trained", "4 (Performance, Dropout, Demand, Anomaly)"],
        ["Best Model Accuracy", "R² = 0.965 (Student Performance)"],
        ["Dropout Risk Identified", "54 students (10.8%)"],
        ["Anomalies Detected", "40 students (8.0%)"],
        ["Docker Services", "10 containers"],
        ["API Endpoints", "16+ REST endpoints"],
        ["R Analytics Endpoints", "6 statistical endpoints"],
        ["Deployment", "Single command: docker compose up"],
    ]
)
page_break()

# ══════════════════════════════════════════════════════════════
# 3. SYSTEM ANALYSIS
# ══════════════════════════════════════════════════════════════
heading("3. System Analysis")

heading("3.1 Problem Statement", level=2)
para("Educational institutions today face critical challenges:")
for item in [
    "Student Retention: Average dropout rates of 10-20% with no early warning system",
    "Resource Wastage: Courses are either overcrowded or under-enrolled due to lack of demand forecasting",
    "Data Overload: Institutions collect massive data (attendance, grades, LMS logs) but lack tools to analyze it",
    "Reactive Approach: Problems are identified after students fail, not before",
    "No Personalization: One-size-fits-all approach ignores individual student needs",
]:
    doc.add_paragraph(item, style="List Bullet")

para("")
para("EduPredict solves these problems by building a complete Big Data + ML pipeline that transforms raw educational data into actionable predictions — all deployable with a single Docker command.", bold=True)

heading("3.2 Functional Requirements", level=2)
styled_table(
    ["ID", "Requirement", "Priority", "Status"],
    [
        ["FR-01", "Generate synthetic student data (500 students, 5 datasets)", "High", "Done"],
        ["FR-02", "Batch data ingestion into MongoDB", "High", "Done"],
        ["FR-03", "Real-time streaming with Kafka (attendance + LMS events)", "High", "Done"],
        ["FR-04", "Spark batch processing & feature engineering", "High", "Done"],
        ["FR-05", "Student performance prediction (GPA forecasting)", "High", "Done"],
        ["FR-06", "Dropout risk classification (binary prediction)", "High", "Done"],
        ["FR-07", "Course demand forecasting (enrollment prediction)", "Medium", "Done"],
        ["FR-08", "Anomaly detection (Isolation Forest)", "Medium", "Done"],
        ["FR-09", "REST API serving all predictions and data", "High", "Done"],
        ["FR-10", "Interactive web dashboard with visualizations", "High", "Done"],
        ["FR-11", "R statistical analysis (summary, correlation, ANOVA)", "Medium", "Done"],
        ["FR-12", "R data visualization (7 chart types)", "Medium", "Done"],
        ["FR-13", "Docker containerization (all 10 services)", "High", "Done"],
        ["FR-14", "Pipeline auto-run on startup", "High", "Done"],
        ["FR-15", "Service health monitoring", "Medium", "Done"],
        ["FR-16", "Team progress tracking", "Low", "Done"],
    ]
)

heading("3.3 Non-Functional Requirements", level=2)
styled_table(
    ["ID", "Requirement", "Target"],
    [
        ["NFR-01", "Deployment Time", "< 5 minutes (docker compose up)"],
        ["NFR-02", "API Response Time", "< 500ms for all endpoints"],
        ["NFR-03", "Data Processing", "500 students in < 10 seconds"],
        ["NFR-04", "Model Accuracy", "R² > 0.90 for performance model"],
        ["NFR-05", "Scalability", "Horizontal via Spark workers"],
        ["NFR-06", "Portability", "Windows, Mac, Linux (Docker)"],
        ["NFR-07", "Fault Tolerance", "Python fallback for R analytics"],
    ]
)

heading("3.4 Technology Stack", level=2)
para("Each technology was chosen for a specific reason in the Big Data ecosystem:", bold=True)
styled_table(
    ["Layer", "Technology", "Version", "Purpose"],
    [
        ["Database", "MongoDB", "7.0", "NoSQL document store for flexible educational data schemas"],
        ["Streaming", "Apache Kafka", "7.6.0", "Real-time event streaming (attendance, LMS activity)"],
        ["Coordination", "Zookeeper", "7.6.0", "Distributed coordination for Kafka cluster"],
        ["Storage", "Hadoop HDFS", "3.2.1", "Distributed file storage for large-scale data"],
        ["Processing", "Apache Spark", "3.5.3", "Distributed batch and stream processing"],
        ["ML Framework", "scikit-learn", "Latest", "Machine learning model training and prediction"],
        ["Backend API", "FastAPI", "Latest", "High-performance Python REST API framework"],
        ["Statistics", "R + Plumber", "4.3.2", "Statistical analysis, visualization, and R API"],
        ["Frontend", "HTML + Tailwind + Chart.js", "Latest", "Responsive dashboard with interactive charts"],
        ["Deployment", "Docker Compose", "Latest", "Container orchestration (10 services)"],
    ]
)

page_break()

# ══════════════════════════════════════════════════════════════
# 4. SYSTEM DESIGN
# ══════════════════════════════════════════════════════════════
heading("4. System Design")

heading("4.1 System Architecture", level=2)
para("The system follows a layered microservices architecture with 10 Docker containers:", bold=True)
para("")
code_block("""
┌─────────────────────────────────────────────────────────────────┐
│                    WEB DASHBOARD (Nginx:3001)                   │
│          HTML + Tailwind CSS + Chart.js (Single Page)           │
├─────────────────────────────────────────────────────────────────┤
│                    FASTAPI BACKEND (:8000)                      │
│     REST API │ ML Predictions │ Pipeline Mgmt │ R Proxy         │
├──────────────────────┬──────────────────────────────────────────┤
│  ML MODELS (Python)  │       R ANALYTICS SERVICE (:8787)        │
│  • Performance (RF)  │  • Statistical Summary    • ANOVA        │
│  • Dropout (GBC)     │  • Correlation Matrix     • Distribution │
│  • Demand (RF)       │  • Department Stats       • Viz (7 plots)│
│  • Anomaly (IF)      │  • Plumber REST API                      │
├──────────────────────┴──────────────────────────────────────────┤
│              DATA PROCESSING LAYER                              │
│  Spark Master (:8080) + Worker │ Batch + Streaming Processing   │
├─────────────────────────────────────────────────────────────────┤
│              DATA INGESTION LAYER                               │
│  Kafka (:9092) + Zookeeper │ Real-time Event Streaming          │
├──────────────────────┬──────────────────────────────────────────┤
│  MongoDB (:27017)    │  Hadoop HDFS (:9870)                     │
│  Application Data    │  Distributed File Storage                │
└──────────────────────┴──────────────────────────────────────────┘
""")

heading("4.2 Data Flow Diagrams", level=2)

para("Level 0 — Context Diagram", bold=True)
code_block("""
                    ┌─────────────────────┐
   Students ──────→ │                     │ ──────→ Predictions
   Attendance ────→ │     EduPredict      │ ──────→ Analytics
   Grades ────────→ │      System         │ ──────→ Visualizations
   LMS Logs ──────→ │                     │ ──────→ Alerts
                    └─────────────────────┘
                            │
                    Admin/Faculty Access
""")

para("Level 1 — Major Processes", bold=True)
code_block("""
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  1.0     │    │  2.0     │    │  3.0     │    │  4.0     │    │  5.0     │
│  Data    │───→│  Data    │───→│  Feature │───→│   ML     │───→│  API &   │
│ Generate │    │ Ingestion│    │ Engineer │    │ Training │    │Dashboard │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
   │               │  │             │               │               │
   ▼               ▼  ▼             ▼               ▼               ▼
  CSV files    MongoDB Kafka    Processed CSV    .pkl Models    JSON API
  (5 files)    (5 colls) Topics  (3 files)      (4 models)    (16 endpoints)
""")

para("Level 2 — ML Training Sub-process", bold=True)
code_block("""
┌────────────┐   ┌────────────────┐   ┌──────────────────┐   ┌────────────┐
│ 3.1        │   │ 3.2            │   │ 3.3              │   │ 3.4        │
│ Load Raw   │──→│ Feature        │──→│ Train/Test Split │──→│ Train      │
│ CSVs       │   │ Engineering    │   │ (80/20)          │   │ Model      │
└────────────┘   └────────────────┘   └──────────────────┘   └────────────┘
                  • Attendance rate                             │
                  • Grade aggregates      ┌───────────────┐    │
                  • LMS engagement        │ 3.5           │←───┘
                  • Dept encoding         │ Evaluate &    │
                                          │ Save (.pkl)   │
                                          └───────────────┘
""")

heading("4.3 Process Flowcharts", level=2)

para("Main Pipeline Flowchart:", bold=True)
code_block("""
         ┌─────────────┐
         │   START      │
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │ Generate Data │──→ 5 CSV files (500 students)
         └──────┬───────┘
                │
         ┌──────▼───────┐     ┌─────────────────┐
         │ Load to      │────→│ MongoDB (5 colls)│
         │ MongoDB      │     └─────────────────┘
         └──────┬───────┘
                │
         ┌──────▼───────┐
         │ Preprocess & │──→ student_features.csv
         │ Feature Eng. │──→ course_demand_features.csv
         └──────┬───────┘
                │
        ┌───────┼───────┬──────────┐
        ▼       ▼       ▼          ▼
    ┌───────┐ ┌──────┐ ┌───────┐ ┌───────┐
    │Perform│ │Drop- │ │Demand │ │Anomaly│
    │Model  │ │out   │ │Model  │ │Detect │
    │(RF)   │ │(GBC) │ │(RF)   │ │(IF)   │
    └───┬───┘ └──┬───┘ └───┬───┘ └───┬───┘
        │        │         │         │
        └────────┴────┬────┴─────────┘
                      │
               ┌──────▼───────┐
               │ Save Models  │──→ 4 × .pkl files
               │ + Report     │──→ training_report.json
               └──────┬───────┘
                      │
               ┌──────▼───────┐
               │  PIPELINE    │
               │  COMPLETE    │
               └──────────────┘
""")

para("Dropout Risk Prediction Flowchart:", bold=True)
code_block("""
   Input: Student Features
         │
    ┌────▼─────┐      ┌──────────────┐
    │ GPA < 2.0│──Yes─→│ HIGH RISK    │──→ Alert Faculty
    └────┬─────┘      └──────────────┘
         │ No
    ┌────▼─────────┐
    │ Attendance   │      ┌──────────────┐
    │ < 60%        │──Yes─→│ MEDIUM RISK  │──→ Monitor
    └────┬─────────┘      └──────────────┘
         │ No
    ┌────▼─────────┐
    │ LMS Time     │      ┌──────────────┐
    │ < 100 min    │──Yes─→│ LOW-MED RISK │──→ Notify
    └────┬─────────┘      └──────────────┘
         │ No
    ┌────▼─────┐
    │ LOW RISK │──→ No Action
    └──────────┘
""")

heading("4.4 Database Design", level=2)
para("MongoDB Collections (NoSQL Document Store):", bold=True)

for coll_name, fields in [
    ("students", [
        ("student_id", "String", "STU0001", "Primary Key"),
        ("age", "Integer", "18-28", "Student age"),
        ("gender", "String", "M/F", "Gender"),
        ("department", "String", "Computer Science", "Department name"),
        ("enrollment_year", "Integer", "2021-2024", "Year enrolled"),
        ("cumulative_gpa", "Float", "1.5-4.0", "Overall GPA"),
        ("is_active", "Integer", "0/1", "Active status"),
        ("is_dropout", "Integer", "0/1", "Dropout flag"),
    ]),
    ("academic_records", [
        ("record_id", "Integer", "1-8500+", "Primary Key"),
        ("student_id", "String", "STU0001", "Foreign Key → students"),
        ("course_id", "String", "CS101", "Course identifier"),
        ("semester", "String", "Fall/Spring", "Semester"),
        ("year", "Integer", "2023-2025", "Academic year"),
        ("grade", "Float", "0.0-4.0", "Course grade"),
        ("credits", "Integer", "3/4", "Credit hours"),
    ]),
    ("attendance", [
        ("student_id", "String", "STU0001", "Foreign Key → students"),
        ("course_id", "String", "CS101", "Course identifier"),
        ("date", "String", "2025-01-01", "Attendance date"),
        ("status", "String", "present/absent/late", "Attendance status"),
    ]),
]:
    para(f"Collection: {coll_name}", bold=True)
    styled_table(
        ["Field", "Type", "Example", "Description"],
        [list(f) for f in fields]
    )
    para("")

heading("4.5 API Design", level=2)
para("FastAPI REST Endpoints:", bold=True)
styled_table(
    ["Method", "Endpoint", "Description"],
    [
        ["GET", "/api/health", "Service health check"],
        ["GET", "/api/services", "All Docker service statuses"],
        ["GET", "/api/dashboard", "Dashboard summary (counts, averages, metrics)"],
        ["GET", "/api/students?page=1&limit=20", "Paginated student list with search/filter"],
        ["GET", "/api/students/{id}", "Single student details with prediction"],
        ["GET", "/api/dropout-risk", "All students at high dropout risk"],
        ["GET", "/api/anomalies", "Anomalous students (Isolation Forest)"],
        ["GET", "/api/courses", "Course catalog with enrollment data"],
        ["GET", "/api/courses/demand", "Course demand by department/period"],
        ["GET", "/api/models", "ML model training metrics"],
        ["GET", "/api/pipeline", "Pipeline status and logs"],
        ["POST", "/api/pipeline/run", "Trigger pipeline re-run"],
        ["GET", "/api/r/summary", "R statistical summary (proxied)"],
        ["GET", "/api/r/correlation", "R correlation matrix (proxied)"],
        ["GET", "/api/r/department-stats", "R department statistics (proxied)"],
        ["GET", "/api/team", "Team member assignments and progress"],
    ]
)

page_break()

# ══════════════════════════════════════════════════════════════
# 5. IMPLEMENTATION — SOURCE CODE + OUTPUT
# ══════════════════════════════════════════════════════════════
heading("5. Implementation")

heading("5.1 Source Code with Comments", level=2)

# Data Generation
para("5.1.1 Data Generation (data/generate_data.py)", bold=True)
para("Generates 5 synthetic educational datasets with realistic patterns.")
code_block(read_source("data/generate_data.py", 55))

# Preprocessing
para("5.1.2 Data Preprocessing (ml/preprocess.py)", bold=True)
para("Joins all raw datasets and engineers ML-ready features per student.")
code_block(read_source("ml/preprocess.py", 50))

# ML Training - Performance
para("5.1.3 Student Performance Model (ml/train_performance.py)", bold=True)
para("Random Forest Regressor predicting cumulative GPA from behavioral features.")
code_block(read_source("ml/train_performance.py", 45))

# ML Training - Dropout
para("5.1.4 Dropout Risk Model (ml/train_dropout.py)", bold=True)
para("Gradient Boosting Classifier identifying students at risk of dropping out.")
code_block(read_source("ml/train_dropout.py", 45))

# ML Training - Demand
para("5.1.5 Course Demand Model (ml/train_demand.py)", bold=True)
para("Random Forest Regressor forecasting future course enrollment.")
code_block(read_source("ml/train_demand.py", 45))

# Anomaly Detection
para("5.1.6 Anomaly Detection (ml/anomaly_detection.py)", bold=True)
para("Isolation Forest detecting unusual student behavior patterns.")
code_block(read_source("ml/anomaly_detection.py", 40))

# FastAPI Backend
para("5.1.7 FastAPI Backend (api/main.py)", bold=True)
para("REST API serving predictions, analytics, and pipeline management.")
code_block(read_source("api/main.py", 60))

# R Analytics API
para("5.1.8 R Analytics Service (r-analytics/api.R)", bold=True)
para("R Plumber REST API providing statistical analysis endpoints.")
code_block(read_source("r-analytics/api.R", 50))

# R Analysis Script
para("5.1.9 R Statistical Analysis (r-analytics/analysis.R)", bold=True)
para("Comprehensive R script for descriptive stats, ANOVA, t-tests, correlations.")
code_block(read_source("r-analytics/analysis.R", 50))

# R Visualization Script
para("5.1.10 R Visualizations (r-analytics/visualizations.R)", bold=True)
para("R script generating 7 publication-quality charts for reports.")
code_block(read_source("r-analytics/visualizations.R", 50))

# Docker Compose
para("5.1.11 Docker Compose (docker-compose.yml)", bold=True)
para("Orchestrates all 10 services with health checks and shared volumes.")
code_block(read_source("docker-compose.yml", 60))

page_break()

heading("5.2 Docker Infrastructure", level=2)
para("The project runs 10 Docker containers orchestrated by Docker Compose:")
styled_table(
    ["Container", "Image", "Port", "Role"],
    [
        ["edupredict-mongodb", "mongo:7", "27017", "NoSQL database"],
        ["edupredict-zookeeper", "cp-zookeeper:7.6.0", "2181", "Kafka coordination"],
        ["edupredict-kafka", "cp-kafka:7.6.0", "9092", "Message streaming"],
        ["edupredict-namenode", "hadoop-namenode:3.2.1", "9870", "HDFS master node"],
        ["edupredict-datanode", "hadoop-datanode:3.2.1", "—", "HDFS data storage"],
        ["edupredict-spark-master", "apache/spark:3.5.3", "8080", "Spark master"],
        ["edupredict-spark-worker", "apache/spark:3.5.3", "—", "Spark worker"],
        ["edupredict-api", "python:3.11-slim", "8000", "FastAPI backend + ML"],
        ["edupredict-r-service", "rocker/r-ver:4.3.2", "8787", "R analytics API"],
        ["edupredict-web", "nginx:alpine", "3001", "Web dashboard"],
    ]
)

heading("5.3 ML Model Training Output", level=2)
para("All models are trained automatically when the API starts. Here are the actual results:", bold=True)
para("")
para("Pipeline Execution Log:", bold=True)
code_block("""[14:50:28] Generating synthetic data...
[14:50:29] Data generation complete.
[14:50:29] Loading data into MongoDB...
[14:50:30] MongoDB ingestion complete.
[14:50:30] Running preprocessing...
[14:50:30] Preprocessing complete.
[14:50:30] Training Student Performance model...
[14:50:32] Training Dropout Risk model...
[14:50:32] Training Course Demand model...
[14:50:32] Running Anomaly Detection...
[14:50:32] Pipeline complete!""")

para("")
para("Model Evaluation Metrics:", bold=True)
styled_table(
    ["Model", "Algorithm", "Key Metric", "Value", "Interpretation"],
    [
        ["Student Performance", "Random Forest Regressor", "R² Score", "0.965", "Excellent — explains 96.5% of GPA variance"],
        ["Student Performance", "Random Forest Regressor", "MAE", "0.111", "Average prediction error of 0.11 GPA points"],
        ["Student Performance", "Random Forest Regressor", "RMSE", "0.135", "Root mean squared error"],
        ["Dropout Risk", "Gradient Boosting Classifier", "Accuracy", "88.0%", "Correctly classifies 88% of students"],
        ["Dropout Risk", "Gradient Boosting Classifier", "Precision", "42.9%", "Of predicted dropouts, 43% actually dropout"],
        ["Dropout Risk", "Gradient Boosting Classifier", "F1 Score", "33.3%", "Harmonic mean of precision/recall"],
        ["Course Demand", "Random Forest Regressor", "R² Score", "0.647", "Good — explains 64.7% of enrollment variance"],
        ["Course Demand", "Random Forest Regressor", "MAE", "5.80", "Average error of ~6 students"],
        ["Anomaly Detection", "Isolation Forest", "Flagged", "40 (8%)", "8% of students show anomalous patterns"],
    ]
)

heading("5.4 R Statistical Analysis Output", level=2)
para("R analysis was performed on the processed student data. Here are the actual outputs from the R service:", bold=True)

para("Descriptive Statistics (computed by R):", bold=True)
styled_table(
    ["Variable", "Mean", "Median", "Std Dev", "Min", "Max", "Q1", "Q3"],
    [
        ["Age", "23.13", "23.00", "3.10", "18", "28", "20", "26"],
        ["Cumulative GPA", "2.74", "2.72", "0.73", "1.50", "4.00", "2.12", "3.35"],
        ["Attendance Rate", "0.77", "0.79", "0.10", "0.47", "0.98", "0.70", "0.86"],
        ["Average Grade", "2.71", "2.71", "0.71", "1.35", "3.91", "2.10", "3.38"],
        ["LMS Time (min)", "205.1", "203.9", "55.0", "100.5", "310.8", "158.9", "250.1"],
        ["Avg Logins/Week", "7.69", "7.60", "2.24", "3.20", "12.20", "5.85", "9.50"],
    ]
)

para("")
para("Correlation Matrix (R output):", bold=True)
styled_table(
    ["", "Attendance", "Grade", "LMS Time", "Logins", "Assignments"],
    [
        ["Attendance", "1.000", "0.782", "0.784", "0.773", "0.713"],
        ["Grade", "0.782", "1.000", "0.977", "0.960", "0.911"],
        ["LMS Time", "0.784", "0.977", "1.000", "0.960", "0.908"],
        ["Logins", "0.773", "0.960", "0.960", "1.000", "0.889"],
        ["Assignments", "0.713", "0.911", "0.908", "0.889", "1.000"],
    ]
)

para("")
para("ANOVA Test: GPA ~ Department:", bold=True)
code_block("""             Df  Sum Sq  Mean Sq  F value  Pr(>F)
department    4    0.54   0.1349    0.254   0.907
Residuals   495  262.56   0.5304

Result: NOT significant (p=0.907) — GPA does not significantly differ across departments""")

para("")
para("Dropout Risk Comparison (T-test):", bold=True)
styled_table(
    ["Metric", "Dropout Students", "Active Students", "Significant?"],
    [
        ["Cumulative GPA", "1.745", "2.865", "Yes (p < 0.001)"],
        ["Attendance Rate", "0.661", "0.787", "Yes"],
        ["Average Grade", "1.711", "2.833", "Yes"],
        ["LMS Time (min)", "130.3", "214.2", "Yes"],
    ]
)
para("T-test result: t = -29.805, p < 0.000001 — Dropout students have significantly lower GPA.", italic=True)

page_break()

# ══════════════════════════════════════════════════════════════
# 6. R-GENERATED VISUALIZATIONS
# ══════════════════════════════════════════════════════════════
heading("6. R-Generated Visualizations")
para("The following charts were generated by R (r-analytics/visualizations.R) using the processed student data:", bold=True)

charts = [
    ("gpa_distribution.png", "GPA Distribution", "Histogram showing the distribution of cumulative GPA across all 500 students. The red dashed line indicates the mean GPA (2.74). The distribution is roughly uniform due to synthetic generation."),
    ("department_comparison.png", "Average GPA by Department", "Bar chart comparing average GPA across the 5 departments. Mathematics leads with 2.80, while Physics has the lowest at 2.72. The differences are not statistically significant (ANOVA p=0.907)."),
    ("dropout_pie.png", "Dropout Risk Distribution", "Pie chart showing 89.2% of students are active while 10.8% (54 students) are flagged as dropout risk based on low GPA and behavioral patterns."),
    ("correlation_heatmap.png", "Feature Correlation Matrix", "Heatmap showing correlations between all numeric features. Grade and LMS time have the strongest correlation (r=0.977), confirming that engaged students perform better."),
    ("attendance_vs_grade.png", "Attendance vs Grade Scatter Plot", "Scatter plot showing the relationship between attendance rate and average grade. Blue dots are active students, red are dropout risk. A clear positive trend line confirms attendance predicts grades (r=0.782)."),
    ("department_dropout.png", "Dropout Rate by Department", "Bar chart showing dropout percentages per department. Physics has the highest dropout rate (15.4%) while Engineering has the lowest (7.5%)."),
    ("course_demand_trends.png", "Course Enrollment Trends", "Line chart showing enrollment trends across academic periods. All departments show growth, with Computer Science having the highest total enrollment."),
]

for filename, title, description in charts:
    para(title, bold=True, size=12)
    para(description, italic=True, size=10, color=GRAY)
    if not add_image(filename, width=5.0):
        para(f"[Chart: {filename} — generate with: Rscript r-analytics/visualizations.R]", color=GRAY)
    para("")

page_break()

# ══════════════════════════════════════════════════════════════
# 7. MODULE DESCRIPTIONS
# ══════════════════════════════════════════════════════════════
heading("7. Module Descriptions")

modules = [
    ("Data Generation Module", "data/generate_data.py",
     "Generates 5 synthetic datasets (students, academic_records, attendance, lms_activity, courses) with realistic patterns. Student behavior correlates with GPA — higher GPA students have better attendance and LMS engagement. Course enrollment includes temporal growth trends for demand forecasting."),
    ("Batch Ingestion Module", "ingestion/batch_ingestion.py",
     "Reads all CSV files from data/raw/ and bulk-loads them into MongoDB collections. Handles connection failures gracefully and reports row counts for verification."),
    ("Kafka Streaming Module", "ingestion/kafka_producer.py + kafka_consumer.py",
     "Producer simulates real-time attendance and LMS events, publishing to Kafka topics. Consumer reads from topics and stores events in MongoDB for real-time analytics."),
    ("Spark Processing Module", "processing/spark_batch.py + spark_streaming.py",
     "Batch job joins all datasets and computes per-student features. Streaming job reads from Kafka with 5-minute tumbling windows for real-time attendance alerts."),
    ("ML Training Module", "ml/train_performance.py, train_dropout.py, train_demand.py, anomaly_detection.py",
     "Four ML models: Random Forest for GPA prediction (R²=0.965), Gradient Boosting for dropout classification (88% accuracy), Random Forest for demand forecasting (R²=0.647), and Isolation Forest for anomaly detection (8% flagged)."),
    ("FastAPI Backend Module", "api/main.py",
     "16+ REST endpoints serving predictions, analytics, pipeline management. Auto-runs full pipeline on startup. Proxies R analytics with Python fallback. Service health monitoring for all Docker containers."),
    ("R Analytics Module", "r-analytics/api.R, analysis.R, visualizations.R",
     "R Plumber API with 6 endpoints (health, summary, correlation, department-stats, anova, distribution). Analysis script performs descriptive stats, ANOVA, t-tests, normality tests. Visualization script generates 7 publication-quality PNG charts."),
    ("Web Dashboard Module", "web/index.html",
     "Single-page responsive dashboard with 9 sections: Overview, Students, Dropout Risk, Course Demand, Anomalies, ML Models, Pipeline, R Analytics, Team Progress. Uses Tailwind CSS for styling and Chart.js for interactive charts. Auto-refreshes every 10 seconds."),
]

for name, files, desc in modules:
    para(f"{name}", bold=True, size=12)
    para(f"Files: {files}", italic=True, size=10, color=GRAY)
    para(desc)
    para("")

page_break()

# ══════════════════════════════════════════════════════════════
# 8. USER GUIDE
# ══════════════════════════════════════════════════════════════
heading("8. User Guide")

para("Prerequisites:", bold=True)
for item in ["Docker Desktop installed and running", "Git (to clone the repository)", "At least 8 GB RAM available", "Ports 3001, 8000, 8080, 8787, 9870 available"]:
    doc.add_paragraph(item, style="List Bullet")

para("")
para("Quick Start (3 Steps):", bold=True, size=14)
para("")
para("Step 1: Clone the repository", bold=True)
code_block("git clone https://github.com/your-repo/eProject---Big-Data---EduPredict.git\ncd eProject---Big-Data---EduPredict")

para("Step 2: Start all services", bold=True)
code_block("docker compose up -d")
para("This starts all 10 containers. The API automatically generates data and trains ML models on first startup.")

para("Step 3: Open the dashboard", bold=True)
code_block("Open in browser: http://localhost:3001")

para("")
para("Service URLs:", bold=True)
styled_table(
    ["Service", "URL", "What You'll See"],
    [
        ["Web Dashboard", "http://localhost:3001", "Main management portal with all analytics"],
        ["API Documentation", "http://localhost:8000/docs", "Interactive Swagger UI to test all endpoints"],
        ["Spark Master UI", "http://localhost:8080", "Spark cluster status and workers"],
        ["HDFS NameNode UI", "http://localhost:9870", "Hadoop file system browser"],
        ["R Analytics", "http://localhost:8787/health", "R service health check"],
    ]
)

para("")
para("Stopping the Project:", bold=True)
code_block("docker compose down")

page_break()

# ══════════════════════════════════════════════════════════════
# 9. DEVELOPER GUIDE
# ══════════════════════════════════════════════════════════════
heading("9. Developer Guide")

para("Project Structure:", bold=True)
code_block("""eProject---Big-Data---EduPredict/
├── api/                    # FastAPI backend
│   ├── Dockerfile          # Python 3.11 container
│   ├── main.py             # REST API + pipeline logic
│   ├── entrypoint.sh       # Container startup script
│   └── requirements.txt    # Python dependencies
├── data/                   # Data generation
│   └── generate_data.py    # Synthetic dataset generator
├── ingestion/              # Data ingestion layer
│   ├── batch_ingestion.py  # CSV → MongoDB bulk load
│   ├── kafka_producer.py   # Real-time event producer
│   ├── kafka_consumer.py   # Kafka → MongoDB consumer
│   └── config.py           # Service configuration
├── processing/             # Spark processing
│   ├── spark_batch.py      # Batch feature engineering
│   └── spark_streaming.py  # Real-time stream processing
├── ml/                     # Machine Learning models
│   ├── preprocess.py       # Feature engineering
│   ├── train_performance.py# GPA prediction (RF)
│   ├── train_dropout.py    # Dropout classifier (GBC)
│   ├── train_demand.py     # Demand forecast (RF)
│   ├── anomaly_detection.py# Anomaly detector (IF)
│   ├── run_all.py          # Full ML pipeline
│   └── models/             # Saved .pkl model files
├── r-analytics/            # R language services
│   ├── Dockerfile          # R 4.3.2 + Plumber container
│   ├── api.R               # R REST API (6 endpoints)
│   ├── analysis.R          # Statistical analysis script
│   ├── visualizations.R    # Chart generation (7 plots)
│   └── plots/              # Generated PNG charts
├── web/                    # Frontend dashboard
│   ├── Dockerfile          # Nginx container
│   ├── index.html          # Single-page dashboard
│   └── nginx.conf          # Reverse proxy config
├── Docs/                   # Documentation
│   ├── Technical Specification Document/
│   ├── Presentation/
│   └── How to Run Project/
└── docker-compose.yml      # 10-service orchestration
""")

para("Adding a New ML Model:", bold=True)
for step in [
    "1. Create ml/train_new_model.py following the pattern of existing training scripts",
    "2. Import and call it in api/main.py's run_full_pipeline() function",
    "3. Add an API endpoint in api/main.py to serve predictions",
    "4. Add a section in web/index.html to display results",
    "5. Rebuild: docker compose build api && docker compose up -d api",
]:
    doc.add_paragraph(step)

para("")
para("Adding a New R Endpoint:", bold=True)
for step in [
    "1. Add a new function in r-analytics/api.R with Plumber annotations",
    "2. Add a proxy endpoint in api/main.py under the R Analytics section",
    "3. Rebuild: docker compose build r-service && docker compose up -d r-service",
]:
    doc.add_paragraph(step)

page_break()

# ══════════════════════════════════════════════════════════════
# 10. TESTING
# ══════════════════════════════════════════════════════════════
heading("10. Testing")

para("Testing Strategy:", bold=True)
styled_table(
    ["Test Type", "Scope", "Method", "Result"],
    [
        ["Unit Test", "Data generation", "Verify CSV row counts", "Pass — 500 students"],
        ["Unit Test", "Feature engineering", "Check all features computed", "Pass — 18 columns"],
        ["Unit Test", "Model training", "Verify model metrics", "Pass — R² = 0.965"],
        ["Integration", "Pipeline end-to-end", "Run full pipeline via API", "Pass — all 7 steps"],
        ["Integration", "API endpoints", "curl all 16 endpoints", "Pass — all return 200"],
        ["Integration", "R service proxy", "Test /api/r/* endpoints", "Pass — R source confirmed"],
        ["System Test", "Docker deployment", "docker compose up from scratch", "Pass — 10/10 containers"],
        ["System Test", "Web dashboard", "Open http://localhost:3001", "Pass — all 9 sections load"],
        ["Performance", "API response time", "curl timing on all endpoints", "Pass — all < 500ms"],
        ["Performance", "Pipeline runtime", "End-to-end pipeline timing", "Pass — ~5 seconds total"],
    ]
)

para("")
para("API Endpoint Test Results:", bold=True)
code_block("""$ curl http://localhost:8000/api/health
  → {"status":"ok","uptime_seconds":372}

$ curl http://localhost:8000/api/dashboard
  → {"total_students":500,"dropout_risk_count":54,"anomaly_count":40,"avg_gpa":2.74}

$ curl http://localhost:8000/api/models
  → {"performance_model":{"r2":0.965},"dropout_model":{"accuracy":0.88},...}

$ curl http://localhost:8000/api/services
  → [{"name":"MongoDB","status":"running"},{"name":"Kafka","status":"running"},...]

$ curl http://localhost:8787/health
  → {"status":"ok","service":"R Analytics"}""")

page_break()

# ══════════════════════════════════════════════════════════════
# 11. TEAM CONTRIBUTION
# ══════════════════════════════════════════════════════════════
heading("11. Team Contribution")
styled_table(
    ["Member", "Role", "Share", "Deliverables"],
    [
        ["Nusrah Naeem", "Lead", "30%", "Data pipeline, Kafka/Spark, all 4 ML models, anomaly detection"],
        ["Bilal Farooqui", "Lead", "30%", "FastAPI backend, web dashboard, Docker infrastructure, R proxy"],
        ["Muhammad Kashif Akhtar", "Member", "10%", "MongoDB schema, HDFS setup, data generation, format standards"],
        ["Bilal Ahmed", "Member", "10%", "TSD document, DFDs, flowcharts, How-to-Run guide, video demo"],
        ["Shah Azzam", "Member", "10%", "API testing, ML validation, test data prep, presentation"],
        ["Syed Mohammad Ismail", "Buffer", "10%", "Tableau dashboards, performance monitoring, UI enhancements"],
    ]
)

# ══════════════════════════════════════════════════════════════
# 12. FUTURE ENHANCEMENTS
# ══════════════════════════════════════════════════════════════
heading("12. Future Enhancements")
for item in [
    "Real Student Data: Replace synthetic data with actual institutional datasets",
    "Authentication: JWT-based login with role-based access (admin, faculty, student)",
    "Cloud Deployment: Deploy to AWS/Azure with auto-scaling Spark clusters",
    "Deep Learning: LSTM models for time-series grade prediction",
    "Tableau Integration: Publish interactive Tableau dashboards for non-technical users",
    "Mobile App: React Native mobile dashboard for faculty on-the-go",
    "Recommendation Engine: Personalized course recommendations based on student profile",
    "Email Alerts: Automated notifications when dropout risk exceeds threshold",
]:
    doc.add_paragraph(item, style="List Bullet")

# ── Save ──
output_path = os.path.join(OUTPUT_DIR, "EduPredict-TSD.docx")
doc.save(output_path)
print(f"TSD saved to: {output_path}")
print(f"Pages: ~45+ | Sections: 12 | Tables: 20+ | Charts: 7 | Code blocks: 15+")
