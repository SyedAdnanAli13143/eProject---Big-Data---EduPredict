"""
Generate the Technical Specification Document (TSD) as a .docx file.
Run: python Docs/generate_tsd.py
"""

import os
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "Technical Specification Document")
os.makedirs(OUTPUT_DIR, exist_ok=True)

doc = Document()

# ── Styles ──
style = doc.styles["Normal"]
font = style.font
font.name = "Calibri"
font.size = Pt(11)

def heading(text, level=1):
    h = doc.add_heading(text, level=level)
    return h

def para(text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    return p

def bullet(text):
    doc.add_paragraph(text, style="List Bullet")

def add_table(headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Light Grid Accent 1"
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
    for row_data in rows:
        row = table.add_row()
        for i, val in enumerate(row_data):
            row.cells[i].text = str(val)
    return table

# ═══════════════════════════════════════════════════════
#  COVER PAGE
# ═══════════════════════════════════════════════════════
doc.add_paragraph("")
doc.add_paragraph("")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("EduPredict")
run.font.size = Pt(36)
run.bold = True
run.font.color.rgb = RGBColor(37, 99, 235)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Big Data + Predictive Analytics for Education")
run.font.size = Pt(16)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Technical Specification Document (TSD)")
run.font.size = Pt(14)
run.bold = True

doc.add_paragraph("")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("eProject — Semester 6")
run.font.size = Pt(12)

doc.add_paragraph("")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Project Leads: ").bold = True
p.add_run("Nusrah Naeem (Student1477458) | Bilal Farooqui (Student1515247)")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Members: ").bold = True
p.add_run("Muhammad Kashif Akhtar | Bilal Ahmed | Shah Azzam | Syed Mohammad Ismail")

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Duration: ").bold = True
p.add_run("07 May 2026 – 28 May 2026")

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  TABLE OF CONTENTS (placeholder)
# ═══════════════════════════════════════════════════════
heading("Table of Contents")
contents = [
    "1. Acknowledgements",
    "2. eProject Synopsis",
    "3. eProject Analysis",
    "   3.1 Problem Statement",
    "   3.2 Functional Requirements",
    "   3.3 Non-Functional Requirements",
    "   3.4 Technology Stack",
    "4. eProject Design",
    "   4.1 System Architecture",
    "   4.2 Data Flow Diagrams (DFDs)",
    "   4.3 Process Flow / Flowcharts",
    "   4.4 Database Design / Structure",
    "   4.5 API Design",
    "5. Module Descriptions",
    "   5.1 Data Generation Module",
    "   5.2 Data Ingestion Module",
    "   5.3 Spark Processing Module",
    "   5.4 Machine Learning Module",
    "   5.5 FastAPI Backend Module",
    "   5.6 Web Dashboard Module",
    "   5.7 R Analytics Module",
    "   5.8 Docker Infrastructure Module",
    "6. Source Code with Comments",
    "7. User Guide",
    "8. Developer Guide",
    "9. Testing",
]
for item in contents:
    doc.add_paragraph(item)
doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  1. ACKNOWLEDGEMENTS
# ═══════════════════════════════════════════════════════
heading("1. Acknowledgements")
para("We would like to express our sincere gratitude to Aptech for providing us with the opportunity to work on this eProject. This project has been an invaluable learning experience that allowed us to apply the concepts of Big Data, Machine Learning, and Full-Stack development in a real-world context.")
para("We thank our faculty and mentors for their guidance and support throughout the development of EduPredict. Their expertise in Big Data technologies, data science, and software engineering helped shape the direction of this project.")
para("Special thanks to all team members who contributed their skills and dedication to make this project a success:")
bullet("Nusrah Naeem — Data Pipeline & Machine Learning (Lead)")
bullet("Bilal Farooqui — API, Web Portal & Infrastructure (Lead)")
bullet("Muhammad Kashif Akhtar — Data Storage & Database Setup")
bullet("Bilal Ahmed — Documentation & Video Demo")
bullet("Shah Azzam — Testing & QA")
bullet("Syed Mohammad Ismail — Visualization & Monitoring")
doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  2. EPROJECT SYNOPSIS
# ═══════════════════════════════════════════════════════
heading("2. eProject Synopsis")

para("Project Name: EduPredict — Big Data + Predictive Analytics for Education", bold=True)
para("")
para("EduPredict is a Big Data application designed to help educational institutions improve student retention, allocate resources effectively, and personalize learning experiences. The system collects and processes diverse educational data — including academic records, attendance, LMS (Learning Management System) activity, and course enrollment data — to generate actionable predictions and insights.")
para("")
para("Key Capabilities:", bold=True)
bullet("Student Performance Prediction — Predicts a student's GPA/grades using Random Forest Regression based on attendance patterns, LMS engagement, and demographics. Achieved R² = 0.965.")
bullet("Dropout Risk Detection — Identifies students at risk of dropping out using Gradient Boosting Classification. Analyzes attendance trends, grade patterns, and engagement levels.")
bullet("Course Demand Forecasting — Predicts future course enrollment numbers to help institutions plan resource allocation. Uses historical enrollment trends.")
bullet("Anomaly Detection — Flags students with unusual behavior patterns (sudden drops in attendance, abnormal LMS activity) using Isolation Forest algorithm.")
bullet("Real-time Streaming — Processes live student events (attendance scans, LMS logins) via Apache Kafka for immediate alerts.")
bullet("Interactive Dashboard — A web-based management portal showing all predictions, analytics, service health, and team progress.")
bullet("R Statistical Analysis — Dedicated R analytics service for statistical tests (ANOVA, correlation, distribution analysis).")

para("")
para("Technology Stack Summary:", bold=True)
add_table(
    ["Layer", "Technology", "Purpose"],
    [
        ["Data Storage", "MongoDB 7", "Primary database for application data"],
        ["Data Storage", "Hadoop HDFS", "Distributed file system for large datasets"],
        ["Streaming", "Apache Kafka", "Real-time event streaming"],
        ["Processing", "Apache Spark 3.5", "Batch and streaming data processing"],
        ["Machine Learning", "scikit-learn (Python)", "Predictive models and anomaly detection"],
        ["Backend API", "FastAPI (Python)", "REST API for all services"],
        ["Frontend", "HTML + Tailwind CSS + Chart.js", "Interactive web dashboard"],
        ["Analytics", "R + Plumber", "Statistical analysis service"],
        ["Infrastructure", "Docker Compose", "One-command deployment of full stack"],
    ],
)
doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  3. EPROJECT ANALYSIS
# ═══════════════════════════════════════════════════════
heading("3. eProject Analysis")

heading("3.1 Problem Statement", level=2)
para("Education institutions worldwide face critical challenges:")
bullet("Student Retention: High dropout rates lead to revenue loss and poor institutional reputation. Institutions struggle to identify at-risk students early enough to intervene.")
bullet("Resource Allocation: Courses are either over-enrolled (leading to poor quality) or under-enrolled (wasting faculty resources). Institutions lack data-driven tools to forecast demand.")
bullet("Personalization: Every student learns differently, but institutions apply one-size-fits-all approaches because they lack insights into individual student behavior.")
bullet("Data Overload: Institutions collect vast amounts of data (grades, attendance, LMS logs) but lack the tools to process and extract value from it.")
para("")
para("EduPredict addresses these challenges by leveraging Big Data technologies (Hadoop, Spark, Kafka) to process large educational datasets and Machine Learning to generate predictions that enable proactive decision-making.")

heading("3.2 Functional Requirements", level=2)

para("FR-1: User Authentication and Authorization", bold=True)
bullet("Secure login system with role-based access (Admin, Teacher, Student, Analyst)")
bullet("Access controls restricting data visibility based on roles")

para("FR-2: Data Ingestion", bold=True)
bullet("Batch ingestion: Load CSV files (academic records, demographics, attendance, LMS data) into MongoDB")
bullet("Stream ingestion: Real-time events via Kafka (attendance scans, LMS logins)")
bullet("Support for common formats: CSV, JSON")

para("FR-3: Data Storage", bold=True)
bullet("MongoDB for operational/application data")
bullet("HDFS for large-scale distributed storage")
bullet("Data partitioning strategies for optimized retrieval")

para("FR-4: Data Processing", bold=True)
bullet("Spark batch processing: Aggregate student features from raw data")
bullet("Spark streaming: Real-time processing of Kafka events")
bullet("Handle missing/incomplete data gracefully")

para("FR-5: Machine Learning Models", bold=True)
bullet("Student Performance Prediction (Random Forest Regressor)")
bullet("Dropout Risk Detection (Gradient Boosting Classifier)")
bullet("Course Demand Forecasting (Random Forest Regressor)")
bullet("Anomaly Detection (Isolation Forest)")
bullet("Models serialized as .pkl files for production use")

para("FR-6: Data Visualization", bold=True)
bullet("Interactive web dashboard with charts (Chart.js)")
bullet("Student tables with search, filter, pagination")
bullet("Department-wise analytics and course trends")

para("FR-7: Notifications and Alerts", bold=True)
bullet("Automated dropout risk alerts for flagged students")
bullet("Anomaly detection alerts for unusual behavior patterns")
bullet("Configurable thresholds")

para("FR-8: Feedback and Support", bold=True)
bullet("Support contact mechanism integrated into the dashboard")

heading("3.3 Non-Functional Requirements", level=2)
add_table(
    ["Requirement", "Description"],
    [
        ["Performance", "Handle 500+ students with sub-second API response times. Spark processes 40,000+ records efficiently."],
        ["Data Security", "Environment variables for secrets. No credentials in source code. MongoDB authentication ready."],
        ["Data Integrity", "Missing data handled with fillna(0) in preprocessing. Validation at API boundaries."],
        ["Reliability", "Docker health checks ensure service availability. Auto-restart on failure."],
        ["Scalability", "Docker Compose enables horizontal scaling. Kafka supports partitioning. Spark supports adding workers."],
        ["Monitoring", "Dashboard shows real-time service health. Pipeline step-by-step progress tracking."],
        ["Documentation", "TSD, User Guide, Developer Guide, Video Demo all provided."],
    ],
)

heading("3.4 Technology Stack — Detailed", level=2)

para("Why Hadoop / HDFS?", bold=True)
para("HDFS (Hadoop Distributed File System) is designed to store massive datasets across multiple machines. In education, student data grows every semester — grades, attendance logs, LMS interactions. HDFS provides fault-tolerant, scalable storage. Real-life analogy: Think of HDFS as a library with multiple copies of every book stored across different buildings. If one building burns down, the books are still available elsewhere.")

para("Why Apache Kafka?", bold=True)
para("Kafka is a distributed event streaming platform. It handles real-time data feeds — like a student scanning their ID card for attendance. That event is instantly published to Kafka and consumed by the system for processing. Real-life analogy: Kafka is like a post office that receives letters (events) and delivers them to the right mailboxes (consumers) in real time, never losing a letter.")

para("Why Apache Spark?", bold=True)
para("Spark processes large datasets much faster than traditional methods by distributing work across multiple cores/machines. It can process the same data in batch mode (historical analysis) and streaming mode (live events). Real-life analogy: Instead of one accountant processing all 500 student records, Spark is like having 10 accountants working in parallel, finishing 10x faster.")

para("Why MongoDB?", bold=True)
para("MongoDB is a NoSQL document database perfect for storing flexible, JSON-like educational data. Student records, predictions, and analytics results can have different structures — MongoDB handles this naturally. Real-life analogy: MongoDB is like a filing cabinet where each folder can contain different types of documents, unlike a rigid spreadsheet where every row must have the same columns.")

para("Why scikit-learn?", bold=True)
para("scikit-learn is Python's most popular ML library. It provides simple, efficient tools for data analysis and modeling. We use Random Forest (for regression/classification), Gradient Boosting (for dropout prediction), and Isolation Forest (for anomaly detection). Real-life analogy: scikit-learn is a toolbox — you pick the right tool (algorithm) for each job (prediction task).")

para("Why FastAPI?", bold=True)
para("FastAPI is a modern Python web framework that is fast, easy to code, and auto-generates API documentation. It serves as the backbone connecting the ML models to the web dashboard. Real-life analogy: FastAPI is like a receptionist who takes requests from visitors (web dashboard) and fetches information from the back office (ML models, database).")

para("Why R Language?", bold=True)
para("R is the gold standard for statistical computing. We use R for formal statistical tests (ANOVA, Shapiro-Wilk normality test, correlation analysis) that complement Python's ML predictions. Real-life analogy: If Python/scikit-learn is a doctor making diagnoses (predictions), R is the lab running precise medical tests (statistics) to confirm the findings.")

para("Why Docker?", bold=True)
para("Docker packages the entire application — all 10 services — into containers that run identically on any machine. One command (docker compose up) starts everything. Real-life analogy: Docker is like a shipping container — everything needed to run a restaurant (kitchen, ingredients, equipment) is packed inside. You can ship it anywhere and it works the same.")

para("Why Tailwind CSS + Chart.js?", bold=True)
para("Tailwind CSS provides utility-first CSS classes for rapid UI development without writing custom CSS. Chart.js renders interactive charts in the browser. Together they create a professional dashboard with minimal code.")

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  4. EPROJECT DESIGN
# ═══════════════════════════════════════════════════════
heading("4. eProject Design")

heading("4.1 System Architecture", level=2)
para("The system follows a layered Big Data architecture:")
para("")
para("""
┌─────────────────────────────────────────────────────────────────┐
│                        WEB DASHBOARD (:3000)                    │
│                  HTML + Tailwind CSS + Chart.js                  │
│                     (Nginx reverse proxy)                        │
├────────────────────────────┬────────────────────────────────────┤
│    FastAPI Backend (:8000)  │     R Analytics Service (:8787)    │
│  - REST API endpoints       │  - Statistical summary             │
│  - ML model serving         │  - Correlation matrix              │
│  - Pipeline management      │  - ANOVA tests                    │
│  - Service health checks    │  - Distribution analysis           │
├────────────────────────────┴────────────────────────────────────┤
│                     DATA PROCESSING LAYER                        │
│            Apache Spark (Batch + Structured Streaming)            │
├─────────────────────────────────────────────────────────────────┤
│                     STREAMING LAYER                              │
│              Apache Kafka + Zookeeper (:9092)                    │
│         Topics: student-attendance, lms-activity                 │
├──────────────────────┬──────────────────────────────────────────┤
│  MongoDB (:27017)    │        HDFS (NameNode :9870)             │
│  - students          │        - Large dataset storage            │
│  - academic_records  │        - Fault-tolerant replication       │
│  - attendance        │        DataNode                           │
│  - lms_activity      │                                          │
│  - courses           │                                          │
├──────────────────────┴──────────────────────────────────────────┤
│                    DOCKER COMPOSE (10 services)                  │
└─────────────────────────────────────────────────────────────────┘
""")

heading("4.2 Data Flow Diagrams (DFDs)", level=2)

para("Level 0 — Context Diagram", bold=True)
para("""
┌──────────┐    attendance,     ┌─────────────────┐    predictions,   ┌──────────────┐
│ Students │ ──grades, LMS───> │    EduPredict    │ ───alerts────> │ Admin/Teacher │
│          │    activity        │     System       │    dashboards    │              │
└──────────┘                   └─────────────────┘                  └──────────────┘
""")

para("Level 1 — Major Processes", bold=True)
para("""
┌────────────┐     ┌──────────────┐     ┌──────────────┐     ┌─────────────┐
│ 1. Data    │────>│ 2. Data      │────>│ 3. ML Model  │────>│ 4. API      │
│ Ingestion  │     │ Processing   │     │ Training     │     │ Serving     │
│ (Kafka +   │     │ (Spark)      │     │ (scikit-learn│     │ (FastAPI)   │
│  Batch)    │     │              │     │ + R)         │     │             │
└────────────┘     └──────────────┘     └──────────────┘     └─────────────┘
     │                                                              │
     │              ┌──────────────┐                                │
     └─────────────>│ 5. Data      │<───────────────────────────────┘
                    │ Storage      │
                    │ (MongoDB +   │
                    │  HDFS)       │
                    └──────────────┘
""")

para("Level 2 — ML Model Subprocess", bold=True)
para("""
┌────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ 3.1 Preprocess │────>│ 3.2 Train       │────>│ 3.3 Evaluate     │
│ - Clean data   │     │ - Performance   │     │ - Metrics (R2,   │
│ - Engineer     │     │ - Dropout       │     │   F1, MAE)       │
│   features     │     │ - Demand        │     │ - Serialize .pkl │
│ - Encode cats  │     │ - Anomaly       │     │                  │
└────────────────┘     └─────────────────┘     └──────────────────┘
""")

heading("4.3 Process Flowcharts", level=2)

para("Main Application Flow:", bold=True)
para("""
                    ┌──────────────────┐
                    │   docker compose │
                    │       up         │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Start all 10    │
                    │  containers      │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  API startup:    │
                    │  Generate data   │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Load data into  │
                    │  MongoDB         │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Run preprocess  │
                    │  (feature eng.)  │
                    └────────┬─────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
        ┌───────▼──┐  ┌─────▼────┐  ┌───▼────────┐
        │ Train    │  │ Train    │  │ Train      │
        │ Perf.    │  │ Dropout  │  │ Demand     │
        │ Model    │  │ Model    │  │ Model      │
        └───────┬──┘  └─────┬────┘  └───┬────────┘
                │            │            │
                └────────────┼────────────┘
                             │
                    ┌────────▼─────────┐
                    │  Run Anomaly     │
                    │  Detection       │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  API ready!      │
                    │  Dashboard at    │
                    │  localhost:3000   │
                    └──────────────────┘
""")

para("Dropout Risk Prediction Flow:", bold=True)
para("""
  Student Data ──> Aggregate Features ──> Scale/Encode ──> Gradient Boosting
       │                                                       │
       │          attendance_rate                          ┌────▼────┐
       │          avg_grade                                │ Risk:   │
       │          avg_lms_time                             │ High or │
       │          grade_std                                │ Low     │
       │          total_courses                            └────┬────┘
       │                                                       │
       └──────────────────> Dashboard Alert <──────────────────┘
""")

heading("4.4 Database Design / Structure", level=2)

para("MongoDB Collections:", bold=True)
para("")

para("1. students collection", bold=True)
add_table(
    ["Field", "Type", "Description"],
    [
        ["student_id", "String", "Unique ID (e.g., STU0001)"],
        ["age", "Integer", "Student age (18-28)"],
        ["gender", "String", "M or F"],
        ["department", "String", "Department name"],
        ["enrollment_year", "Integer", "Year of enrollment"],
        ["cumulative_gpa", "Float", "Overall GPA (0.0 - 4.0)"],
        ["is_active", "Integer", "1 = active, 0 = inactive"],
        ["is_dropout", "Integer", "1 = dropped out, 0 = enrolled"],
    ],
)
para("")

para("2. academic_records collection", bold=True)
add_table(
    ["Field", "Type", "Description"],
    [
        ["record_id", "Integer", "Unique record ID"],
        ["student_id", "String", "Reference to student"],
        ["course_id", "String", "Course code (e.g., CS101)"],
        ["course_name", "String", "Course name"],
        ["semester", "String", "Fall or Spring"],
        ["year", "Integer", "Academic year"],
        ["grade", "Float", "Grade point (0.0 - 4.0)"],
        ["credits", "Integer", "Course credits (3 or 4)"],
    ],
)
para("")

para("3. attendance collection", bold=True)
add_table(
    ["Field", "Type", "Description"],
    [
        ["student_id", "String", "Reference to student"],
        ["course_id", "String", "Course code"],
        ["date", "String", "Date (YYYY-MM-DD)"],
        ["status", "String", "present / absent / late"],
    ],
)
para("")

para("4. lms_activity collection", bold=True)
add_table(
    ["Field", "Type", "Description"],
    [
        ["student_id", "String", "Reference to student"],
        ["week_start", "String", "Week start date"],
        ["logins", "Integer", "Weekly login count"],
        ["time_spent_minutes", "Integer", "Minutes on platform"],
        ["assignments_submitted", "Integer", "Assignments completed"],
        ["forum_posts", "Integer", "Forum contributions"],
    ],
)
para("")

para("5. courses collection", bold=True)
add_table(
    ["Field", "Type", "Description"],
    [
        ["course_id", "String", "Course code"],
        ["course_name", "String", "Course name"],
        ["department", "String", "Department"],
        ["credits", "Integer", "Credit hours"],
        ["capacity", "Integer", "Max enrollment"],
        ["semester", "String", "Semester offered"],
        ["year", "Integer", "Year"],
        ["enrolled_count", "Integer", "Actual enrollment"],
    ],
)

doc.add_page_break()

heading("4.5 API Design", level=2)
para("RESTful API Endpoints (FastAPI):", bold=True)
add_table(
    ["Method", "Endpoint", "Description"],
    [
        ["GET", "/api/health", "Service health check"],
        ["GET", "/api/services", "Status of all Docker services"],
        ["GET", "/api/dashboard", "Dashboard summary (counts, metrics)"],
        ["GET", "/api/students?page=&limit=&search=", "Paginated student list with predictions"],
        ["GET", "/api/students/{student_id}", "Single student details"],
        ["GET", "/api/dropout-risk", "High-risk students list"],
        ["GET", "/api/anomalies", "Anomalous students"],
        ["GET", "/api/courses", "Course catalog with enrollment"],
        ["GET", "/api/courses/demand", "Course demand aggregated by dept"],
        ["GET", "/api/models", "ML model training metrics"],
        ["GET", "/api/pipeline", "Pipeline step-by-step status"],
        ["POST", "/api/pipeline/run", "Trigger pipeline re-run"],
        ["GET", "/api/r/summary", "R statistical summary"],
        ["GET", "/api/r/correlation", "R correlation matrix"],
        ["GET", "/api/r/department-stats", "R department comparison"],
        ["GET", "/api/team", "Team progress tracking"],
    ],
)

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  5. MODULE DESCRIPTIONS
# ═══════════════════════════════════════════════════════
heading("5. Module Descriptions")

modules = [
    ("5.1 Data Generation Module", "data/generate_data.py",
     "Generates 5 synthetic CSV datasets simulating a real educational institution with 500 students. Creates realistic correlations — students with higher GPA tend to have better attendance and more LMS engagement. Datasets: students.csv (500 rows), academic_records.csv (8500+ rows), attendance.csv (21500+ rows), lms_activity.csv (10000 rows), courses.csv (114 rows)."),

    ("5.2 Data Ingestion Module", "ingestion/",
     "Handles both batch and stream data ingestion. kafka_producer.py streams real-time attendance and LMS events to Kafka topics every 2 seconds. kafka_consumer.py reads from Kafka and stores events in MongoDB for persistence. batch_ingestion.py bulk-loads all CSV files into MongoDB collections. All scripts use environment variables for Docker/local compatibility."),

    ("5.3 Spark Processing Module", "processing/",
     "spark_batch.py uses PySpark to join all datasets and compute per-student features (attendance_rate, avg_grade, avg_lms_time, etc.) in parallel. spark_streaming.py uses Spark Structured Streaming to read from Kafka and generate real-time attendance alerts using 5-minute tumbling windows. Both run locally on Windows or in Docker."),

    ("5.4 Machine Learning Module", "ml/",
     "Contains 4 ML models: (1) Student Performance — Random Forest Regressor predicting GPA with R²=0.965; (2) Dropout Risk — Gradient Boosting Classifier with 88% accuracy; (3) Course Demand — Random Forest Regressor forecasting enrollment with R²=0.647; (4) Anomaly Detection — Isolation Forest flagging 8% of students as anomalous. All models saved as .pkl files."),

    ("5.5 FastAPI Backend Module", "api/main.py",
     "The central API serving 16+ endpoints. On startup, auto-runs the full pipeline (data generation, ingestion, preprocessing, model training). Provides REST endpoints for students, predictions, courses, anomalies, pipeline management, R analytics proxy, and team progress. Uses async httpx for inter-service communication."),

    ("5.6 Web Dashboard Module", "web/index.html",
     "Single-page application with 9 sections: Overview (stats + service health), Students (paginated table), Dropout Risk, Course Demand (line charts), Anomalies, ML Models (metrics with progress bars), Pipeline (step tracker + logs), R Analytics (summary + correlation tables), Team Progress (per-member task tracking). Uses Tailwind CSS and Chart.js."),

    ("5.7 R Analytics Module", "r-analytics/api.R",
     "R Plumber API providing 5 endpoints: /health, /summary (descriptive statistics with quartiles), /correlation (correlation matrix), /department-stats (per-department analysis), /anova (one-way ANOVA testing GPA differences across departments), /distribution/{variable} (Shapiro-Wilk normality test + histogram)."),

    ("5.8 Docker Infrastructure Module", "docker-compose.yml",
     "Orchestrates 10 containers: MongoDB, Zookeeper, Kafka, HDFS NameNode, HDFS DataNode, Spark Master, Spark Worker, FastAPI API, R Service, Nginx Web. Uses health checks, volume mounts for data persistence, and environment variables for service discovery. One command (docker compose up) starts everything."),
]

for title, files, desc in modules:
    heading(title, level=2)
    para(f"Files: {files}", bold=True)
    para(desc)
    para("")

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  6. SOURCE CODE WITH COMMENTS
# ═══════════════════════════════════════════════════════
heading("6. Source Code with Comments")
para("All source code files are included in the repository with inline comments explaining key logic. Below is the file structure:")
para("")

files = [
    ("data/generate_data.py", "Synthetic data generator — 5 CSV datasets"),
    ("ingestion/config.py", "Service configuration (env-variable based)"),
    ("ingestion/kafka_producer.py", "Kafka producer — streams real-time events"),
    ("ingestion/kafka_consumer.py", "Kafka consumer — stores events in MongoDB"),
    ("ingestion/batch_ingestion.py", "Batch CSV loader into MongoDB"),
    ("processing/spark_batch.py", "Spark batch analytics"),
    ("processing/spark_streaming.py", "Spark structured streaming from Kafka"),
    ("ml/preprocess.py", "Data cleaning and feature engineering"),
    ("ml/train_performance.py", "Student performance model (Random Forest)"),
    ("ml/train_dropout.py", "Dropout risk model (Gradient Boosting)"),
    ("ml/train_demand.py", "Course demand model (Random Forest)"),
    ("ml/anomaly_detection.py", "Anomaly detection (Isolation Forest)"),
    ("ml/run_all.py", "Full ML pipeline orchestrator"),
    ("api/main.py", "FastAPI backend (16+ endpoints)"),
    ("web/index.html", "Web dashboard (9 sections)"),
    ("r-analytics/api.R", "R Plumber statistical API"),
    ("docker-compose.yml", "Docker orchestration (10 services)"),
]
add_table(["File", "Description"], files)

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  7. USER GUIDE
# ═══════════════════════════════════════════════════════
heading("7. User Guide")

para("Prerequisites:", bold=True)
bullet("Windows 10/11 (64-bit)")
bullet("Docker Desktop installed and running")
bullet("Git (for cloning the repository)")
bullet("Minimum 16GB RAM, i5 processor")

para("")
para("Quick Start:", bold=True)
para("Step 1: Clone the repository")
para("   git clone <repository-url>")
para("   cd eProject---Big-Data---EduPredict")
para("")
para("Step 2: Start all services")
para("   docker compose up --build -d")
para("")
para("Step 3: Open the dashboard")
para("   Open browser → http://localhost:3000")
para("")
para("Step 4: Wait for pipeline to complete")
para("   The API automatically generates data, trains models, and loads everything. Watch the Pipeline page for progress.")
para("")

para("Dashboard Sections:", bold=True)
bullet("Overview — Key statistics (total students, dropout risk count, anomaly count, average attendance) and service health status")
bullet("Students — Browse all students with search by ID, filter by department, view GPA, attendance, LMS time, and risk level")
bullet("Dropout Risk — List of all students flagged as high dropout risk, sorted by GPA")
bullet("Course Demand — Line chart showing enrollment trends by department over time, plus course table with fill percentage")
bullet("Anomalies — Students flagged by Isolation Forest with unusual behavior patterns")
bullet("ML Models — Performance metrics for all 4 models with visual progress bars")
bullet("Pipeline — Step-by-step status of the data pipeline with live logs and re-run button")
bullet("R Analytics — Statistical summary, correlation matrix, and department comparison from the R service")
bullet("Team Progress — Track each team member's tasks and completion percentage")

para("")
para("Stopping the Application:", bold=True)
para("   docker compose down")

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  8. DEVELOPER GUIDE
# ═══════════════════════════════════════════════════════
heading("8. Developer Guide")

para("Project Structure:", bold=True)
para("""
eProject---Big-Data---EduPredict/
├── docker-compose.yml          ← Full stack orchestration
├── api/                        ← FastAPI backend
│   ├── Dockerfile
│   ├── main.py                 ← All API endpoints + pipeline
│   └── requirements.txt
├── web/                        ← Frontend dashboard
│   ├── Dockerfile
│   ├── nginx.conf              ← Reverse proxy config
│   └── index.html              ← Dashboard UI
├── r-analytics/                ← R statistical service
│   ├── Dockerfile
│   └── api.R                   ← Plumber API
├── data/                       ← Datasets
│   ├── generate_data.py        ← Data generator
│   ├── raw/                    ← Generated CSVs
│   └── processed/              ← Feature-engineered CSVs
├── ingestion/                  ← Data ingestion
│   ├── kafka_producer.py
│   ├── kafka_consumer.py
│   ├── batch_ingestion.py
│   └── config.py
├── processing/                 ← Spark jobs
│   ├── spark_batch.py
│   └── spark_streaming.py
├── ml/                         ← Machine Learning
│   ├── preprocess.py
│   ├── train_performance.py
│   ├── train_dropout.py
│   ├── train_demand.py
│   ├── anomaly_detection.py
│   ├── run_all.py
│   └── models/                 ← Saved .pkl models
├── infrastructure/             ← Additional configs
└── Docs/                       ← Documentation
""")

para("Local Development (Without Docker):", bold=True)
para("The ML pipeline can run standalone on Windows:")
para("   pip install pandas numpy scikit-learn")
para("   python data/generate_data.py")
para("   python ml/run_all.py")
para("")

para("Service Ports:", bold=True)
add_table(
    ["Service", "Port", "URL"],
    [
        ["Web Dashboard", "3000", "http://localhost:3000"],
        ["FastAPI", "8000", "http://localhost:8000/docs"],
        ["R Analytics", "8787", "http://localhost:8787"],
        ["MongoDB", "27017", "mongodb://localhost:27017"],
        ["Kafka", "9092", "localhost:9092"],
        ["HDFS NameNode UI", "9870", "http://localhost:9870"],
        ["Spark Master UI", "8080", "http://localhost:8080"],
    ],
)
para("")

para("Adding a New ML Model:", bold=True)
bullet("Create ml/train_newmodel.py following the pattern of existing models")
bullet("Add the training call to ml/run_all.py")
bullet("Add an API endpoint in api/main.py")
bullet("Add a dashboard section in web/index.html")

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  9. TESTING
# ═══════════════════════════════════════════════════════
heading("9. Testing")

para("Test Data:", bold=True)
para("500 synthetic students across 5 departments (Computer Science, Mathematics, Physics, Business, Engineering) with correlated academic records, attendance, and LMS activity data.")

para("")
para("Model Test Results:", bold=True)
add_table(
    ["Model", "Algorithm", "Metric", "Value"],
    [
        ["Student Performance", "Random Forest Regressor", "R² Score", "0.9653"],
        ["Student Performance", "Random Forest Regressor", "MAE", "0.1115"],
        ["Student Performance", "Random Forest Regressor", "RMSE", "0.1351"],
        ["Dropout Risk", "Gradient Boosting Classifier", "Accuracy", "0.8800"],
        ["Dropout Risk", "Gradient Boosting Classifier", "Precision", "0.4286"],
        ["Dropout Risk", "Gradient Boosting Classifier", "Recall", "0.2727"],
        ["Dropout Risk", "Gradient Boosting Classifier", "F1 Score", "0.3333"],
        ["Course Demand", "Random Forest Regressor", "R² Score", "0.6468"],
        ["Course Demand", "Random Forest Regressor", "MAE", "5.7971"],
        ["Anomaly Detection", "Isolation Forest", "Anomalies Found", "40 (8%)"],
    ],
)

para("")
para("API Testing:", bold=True)
para("All 16+ API endpoints tested for correct response format, status codes, and data integrity. FastAPI auto-generates interactive docs at http://localhost:8000/docs.")

para("")
para("Integration Testing:", bold=True)
bullet("Data generation → MongoDB ingestion → Preprocessing → Model training → API serving → Dashboard display: Full pipeline verified end-to-end.")
bullet("Service health checks confirm MongoDB, Kafka, HDFS, Spark, R, and API connectivity.")

# ── Save ──
output_path = os.path.join(OUTPUT_DIR, "EduPredict-TSD.docx")
doc.save(output_path)
print(f"TSD saved to: {output_path}")
