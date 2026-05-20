"""
Generate the comprehensive EduPredict Guide (layman + technical + Q&A) as a .docx file.
Run: python Docs/generate_guide.py
"""

import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
doc = Document()

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

def heading(text, level=1):
    doc.add_heading(text, level=level)

def para(text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    return p

def bullet(text):
    doc.add_paragraph(text, style="List Bullet")

def qa(question, answer):
    p = doc.add_paragraph()
    q_run = p.add_run(f"Q: {question}")
    q_run.bold = True
    q_run.font.color.rgb = RGBColor(37, 99, 235)
    doc.add_paragraph(f"A: {answer}")
    doc.add_paragraph("")

# ═══════════════════════════════════════════════════════
#  COVER
# ═══════════════════════════════════════════════════════
doc.add_paragraph("")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("EduPredict")
run.font.size = Pt(36)
run.bold = True
run.font.color.rgb = RGBColor(37, 99, 235)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("Complete Project Guide")
run.font.size = Pt(18)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("For Learners, Presenters, and Interviewees")
run.font.size = Pt(12)
run.italic = True

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("eProject — Semester 6 | May 2026")

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  PART 1: WHAT IS THIS PROJECT? (LAYMAN)
# ═══════════════════════════════════════════════════════
heading("Part 1: What is EduPredict? (Simple Explanation)")

para("Imagine you are the principal of a school with 500 students. Every day, you get mountains of data — attendance sheets, exam results, how much time students spend studying online, which courses they picked. But you have no time to read all of it.", bold=False)
para("")
para("What if a computer could read ALL of that data and tell you:", bold=True)
bullet('"Student #247 is likely to drop out next semester" — so you can intervene now')
bullet('"The Data Science course will have 95 students next semester, but the classroom only fits 60" — so you can plan ahead')
bullet('"Student #103 stopped attending classes and stopped logging into the online portal" — something unusual is happening')
bullet('"Students in the Business department have 15% lower attendance than Computer Science students" — you need to investigate')
para("")
para("That is exactly what EduPredict does.", bold=True)
para("")
para("It is a Big Data application that:")
bullet("Collects student data (grades, attendance, online activity, course enrollment)")
bullet("Stores it in powerful databases (MongoDB, Hadoop HDFS)")
bullet("Processes it using fast engines (Apache Spark, Apache Kafka)")
bullet("Uses AI/Machine Learning to make predictions (scikit-learn)")
bullet("Shows everything on a beautiful web dashboard")
para("")
para("And the best part? You just type ONE command to start everything:")
para('   docker compose up', bold=True)
para("")
para("That single command starts 10 different services (database, streaming, AI models, web dashboard, statistics engine, etc.) all at once. Like pressing one button to start an entire factory.")

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  PART 2: REAL-LIFE ANALOGY
# ═══════════════════════════════════════════════════════
heading("Part 2: Real-Life Analogy — The Hospital Comparison")

para("Think of EduPredict like a modern hospital system:", bold=True)
para("")

para("In a hospital:")
bullet("Patients → Students")
bullet("Medical records → Academic records + attendance + LMS data")
bullet("Lab tests → Machine Learning models running predictions")
bullet("Doctor's diagnosis → 'This student will likely drop out'")
bullet("Hospital dashboard → Our web dashboard showing all patient/student status")
bullet("Emergency alerts → Our anomaly detection flagging unusual behavior")
para("")

para("Technology Analogy:", bold=True)
bullet("MongoDB (Database) → The hospital's filing cabinet where all patient records are stored")
bullet("Kafka (Streaming) → The nurse's station receiving real-time vital sign updates")
bullet("Spark (Processing) → The lab that runs hundreds of blood tests in parallel, not one by one")
bullet("HDFS (Storage) → The hospital's archive warehouse storing decades of patient history")
bullet("FastAPI (Backend) → The receptionist connecting patients to doctors and lab results")
bullet("Web Dashboard → The doctor's monitor showing all patient vitals at a glance")
bullet("R Analytics → The specialist running advanced statistical tests")
bullet("Docker → The ambulance that carries the entire hospital setup — deploy it anywhere, and it works the same")

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  PART 3: TECHNICAL DEEP DIVE
# ═══════════════════════════════════════════════════════
heading("Part 3: Technical Deep Dive — Every Technology Explained")

heading("3.1 Apache Hadoop / HDFS", level=2)
para("What it is:", bold=True)
para("HDFS (Hadoop Distributed File System) is a storage system that splits large files into blocks and distributes them across multiple machines. Each block is replicated (default 3 copies) for fault tolerance.")
para("Why we use it:", bold=True)
para("Educational data grows exponentially — years of student records, millions of attendance entries. HDFS can store petabytes of data across commodity hardware.")
para("In our project:", bold=True)
para("We run a NameNode (the 'index/directory' of all files) and a DataNode (the actual storage) in Docker. The NameNode UI is accessible at port 9870.")
para("Real example:", bold=True)
para("If our school has 10 years of data for 10,000 students — that's millions of rows. A single computer's hard drive might struggle. HDFS splits this data across multiple machines, so reading is faster (parallel access) and data is safe (replicated).")

heading("3.2 Apache Kafka", level=2)
para("What it is:", bold=True)
para("Kafka is a distributed event streaming platform. It works like a message queue — producers send messages (events), and consumers read them. Messages are stored in 'topics'.")
para("Why we use it:", bold=True)
para("When a student scans their ID for attendance, that event needs to be captured instantly and processed in real time — not batch-processed at the end of the day.")
para("In our project:", bold=True)
para("We have two Kafka topics: 'student-attendance' and 'lms-activity'. The kafka_producer.py simulates real-time events every 2 seconds. The kafka_consumer.py reads these events and stores them in MongoDB.")
para("Real example:", bold=True)
para("A student scans their ID at 9:01 AM → Kafka receives the event → Consumer stores it in MongoDB → Spark Streaming detects this student has been absent 5 times this week → Dashboard shows an alert to the teacher.")

heading("3.3 Apache Spark", level=2)
para("What it is:", bold=True)
para("Spark is a distributed computing engine that processes data in parallel across multiple cores/machines. It is 100x faster than traditional MapReduce for in-memory workloads.")
para("Why we use it:", bold=True)
para("We need to join 5 different datasets (students + grades + attendance + LMS + courses) and compute features for 500 students. Spark does this in seconds by parallelizing the work.")
para("In our project:", bold=True)
para("spark_batch.py joins all CSV datasets and computes per-student features (attendance_rate, avg_grade, avg_lms_time). spark_streaming.py reads real-time Kafka events and detects attendance anomalies in 5-minute windows.")
para("Real example:", bold=True)
para("Computing the average grade for 500 students across 8500 academic records: a single-threaded program takes 10 seconds, Spark does it in 1 second by splitting the work across 4 CPU cores.")

heading("3.4 MongoDB", level=2)
para("What it is:", bold=True)
para("MongoDB is a NoSQL document database that stores data in flexible JSON-like documents. Unlike SQL databases, it does not require a fixed schema.")
para("Why we use it:", bold=True)
para("Student data is semi-structured — some students have extra fields, some courses have different attributes. MongoDB handles this naturally without ALTER TABLE migrations.")
para("In our project:", bold=True)
para("5 collections: students (500 docs), academic_records (8500 docs), attendance (21500 docs), lms_activity (10000 docs), courses (114 docs). The API reads from MongoDB for all dashboard queries.")

heading("3.5 scikit-learn (Machine Learning)", level=2)
para("What it is:", bold=True)
para("Python's most popular library for machine learning. Provides ready-to-use algorithms for classification, regression, clustering, and anomaly detection.")
para("Why we use it:", bold=True)
para("We need 4 different predictions, and scikit-learn provides the right algorithm for each.")
para("Our 4 models:", bold=True)
bullet("Random Forest Regressor → Predicts student GPA (R² = 0.965, meaning 96.5% of variance explained)")
bullet("Gradient Boosting Classifier → Predicts dropout risk (88% accuracy)")
bullet("Random Forest Regressor → Predicts course enrollment numbers (R² = 0.647)")
bullet("Isolation Forest → Detects anomalous students (flagged 40 out of 500 = 8%)")

heading("3.6 FastAPI", level=2)
para("What it is:", bold=True)
para("A modern, fast Python web framework for building APIs. Auto-generates interactive documentation (Swagger UI) at /docs.")
para("Why we use it:", bold=True)
para("FastAPI is 3-10x faster than Flask, has built-in data validation (Pydantic), and generates API docs automatically — perfect for a project that needs clear documentation.")
para("In our project:", bold=True)
para("16+ REST endpoints serving student data, predictions, pipeline management, service health, R analytics proxy, and team progress. The API auto-initializes on startup — generates data, trains models, and becomes ready to serve.")

heading("3.7 R Language (Statistical Computing)", level=2)
para("What it is:", bold=True)
para("R is a programming language designed for statistical computing. It has rich built-in functions for hypothesis testing, correlation, distribution analysis.")
para("Why we use it:", bold=True)
para("While Python/scikit-learn handles predictions, R handles formal statistical validation — ANOVA tests to check if GPA differences across departments are statistically significant, Shapiro-Wilk tests for normality, correlation matrices.")
para("In our project:", bold=True)
para("R Plumber API runs as a separate Docker container with endpoints: /summary, /correlation, /department-stats, /anova, /distribution/{variable}. The FastAPI backend proxies requests to R when needed.")

heading("3.8 Docker & Docker Compose", level=2)
para("What it is:", bold=True)
para("Docker packages applications into containers — lightweight, portable environments that include all dependencies. Docker Compose orchestrates multiple containers.")
para("Why we use it:", bold=True)
para("Our project has 10 services (MongoDB, Kafka, Spark, HDFS, API, Web, R, Zookeeper, NameNode, DataNode). Without Docker, installing and configuring all of these on Windows would take hours and break easily. With Docker Compose, one command starts everything.")
para("In our project:", bold=True)
para("docker-compose.yml defines all 10 services with their images, ports, environment variables, health checks, and volume mounts. 'docker compose up' pulls images, builds custom services, and starts the entire stack.")

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  PART 4: INTERVIEW / PRESENTATION Q&A
# ═══════════════════════════════════════════════════════
heading("Part 4: Interview & Presentation Q&A")
para("Common questions that may be asked during presentations or interviews, with detailed answers.", bold=True)
para("")

heading("General Questions", level=2)

qa("What is EduPredict?",
   "EduPredict is a Big Data application that helps educational institutions predict student performance, detect dropout risk, forecast course demand, and identify anomalous student behavior. It uses Hadoop for storage, Spark for processing, Kafka for real-time streaming, MongoDB for application data, scikit-learn for ML models, and a FastAPI + web dashboard for user interaction.")

qa("What problem does it solve?",
   "It solves 4 key problems: (1) Institutions can't identify at-risk students before they drop out — our Dropout Risk model predicts this. (2) Course planning is guesswork — our Demand Forecasting model predicts enrollment. (3) Large volumes of student data go unanalyzed — our Spark pipeline processes 40,000+ records efficiently. (4) Unusual student behavior goes unnoticed — our Anomaly Detection flags these students automatically.")

qa("Why is this a Big Data project?",
   "Because we use the 4 V's of Big Data: Volume (40,000+ data records across 5 datasets), Velocity (real-time Kafka streaming of attendance/LMS events), Variety (structured CSV data + semi-structured MongoDB documents + streaming events), and Veracity (anomaly detection to handle data quality issues). We use Big Data technologies: Hadoop HDFS, Apache Spark, Apache Kafka.")

qa("How do you run the project?",
   "Just clone the repository and run 'docker compose up'. This single command starts 10 Docker containers (MongoDB, Kafka, Zookeeper, HDFS NameNode, HDFS DataNode, Spark Master, Spark Worker, FastAPI API, R Analytics, Nginx Web). The API auto-initializes — generates data, trains models, and the dashboard is available at http://localhost:3000.")

heading("Machine Learning Questions", level=2)

qa("What ML algorithms did you use and why?",
   "We used 4 algorithms: (1) Random Forest Regressor for GPA prediction — it handles non-linear relationships well and doesn't overfit easily. (2) Gradient Boosting Classifier for dropout prediction — it builds models sequentially, correcting previous errors, which is great for imbalanced data (only 10% dropouts). (3) Random Forest Regressor for demand forecasting — robust to noisy enrollment data. (4) Isolation Forest for anomaly detection — it's unsupervised (no labels needed) and works well for finding outliers in multidimensional data.")

qa("What features did you engineer?",
   "From raw data, we computed: attendance_rate (% of classes attended), avg_grade (mean GPA across all courses), grade_std (grade consistency), avg_lms_time (weekly platform usage), avg_logins (LMS engagement), avg_assignments (completion rate), avg_forum_posts (participation), dept_encoded (numeric department code). These 8+ features feed into all models.")

qa("How accurate are your models?",
   "Student Performance: R²=0.965 (predicts 96.5% of GPA variance, MAE=0.11 grade points). Dropout Risk: 88% accuracy, 43% precision on dropout class (low because only 10% of students are dropouts — class imbalance). Course Demand: R²=0.647 (explains 65% of enrollment variance). Anomaly Detection: Flags 8% of students as anomalous — consistent with expected outlier rate.")

qa("What is Isolation Forest and how does it work?",
   "Isolation Forest detects anomalies by randomly partitioning data with decision trees. Normal data points need many splits to be isolated, while anomalies need few splits (they are 'easy to isolate'). We set contamination=0.08 (expecting 8% anomalies). Students with unusual combinations of low attendance + low grades + low LMS time get flagged.")

qa("Why not use deep learning?",
   "With 500 students, deep learning would overfit. Traditional ML algorithms (Random Forest, Gradient Boosting) work better on tabular data with small-to-medium datasets. Deep learning is better for images, text, or millions of data points. Our models achieve 96.5% R² — adding complexity would not improve this significantly.")

heading("Big Data Technology Questions", level=2)

qa("Why Kafka instead of direct database writes?",
   "Direct writes create tight coupling — if the database is slow or down, events are lost. Kafka decouples producers from consumers: events are written to Kafka first (very fast, durable), then consumed by multiple services at their own pace. This ensures no data loss and enables multiple consumers (e.g., MongoDB storage + Spark analytics + alert system) from the same event stream.")

qa("Why Spark instead of Pandas for processing?",
   "Pandas runs on a single machine and loads everything into memory. For 500 students, Pandas works fine. But when the institution grows to 50,000 students with millions of records, Pandas will run out of memory. Spark distributes processing across multiple machines and handles data that doesn't fit in memory. We built with Spark to ensure scalability.")

qa("What is HDFS and why include it?",
   "HDFS (Hadoop Distributed File System) stores large files by splitting them into blocks distributed across multiple machines with replication for fault tolerance. Even though MongoDB handles our current data, HDFS is essential for archiving years of historical data (terabytes) that would be too expensive to keep in MongoDB. It's the foundation of the Hadoop ecosystem.")

qa("How does Spark Streaming work with Kafka?",
   "Spark Structured Streaming reads from Kafka topics as a continuous stream. We define a 5-minute tumbling window to aggregate attendance events. If a student has >50% absence rate in any window, an alert is generated. Spark handles the windowing, watermarking (for late events), and aggregation automatically.")

heading("Architecture & Docker Questions", level=2)

qa("Why Docker? Can't you just install everything locally?",
   "Installing MongoDB, Kafka, Zookeeper, Hadoop, Spark, Python, and R on Windows with all their dependencies would take hours and frequently breaks due to version conflicts. Docker containerizes each service with its exact dependencies. 'docker compose up' starts everything in minutes, identically on any machine. This is also how real production systems are deployed.")

qa("How do the 10 Docker containers communicate?",
   "Docker Compose creates a shared network. Services reference each other by name: the API connects to 'mongodb://mongodb:27017', Kafka at 'kafka:29092', R at 'http://r-service:8787'. Nginx proxies web requests to the API at 'http://api:8000'. No hardcoded IPs — Docker handles DNS resolution.")

qa("What happens if one container crashes?",
   "Docker can be configured with restart policies (restart: always). MongoDB has a health check — the API waits for it to be healthy before starting. If Kafka crashes, events are buffered and replayed when it recovers (Kafka's durability guarantee). The web dashboard shows service status in real-time so administrators know immediately.")

qa("Why FastAPI instead of Flask?",
   "FastAPI is built on Starlette (async framework) making it 3-10x faster than Flask for I/O-bound operations. It has built-in Pydantic validation, auto-generates Swagger docs at /docs, and supports async/await natively — important for our service health checks that make HTTP calls to other containers.")

heading("R Analytics Questions", level=2)

qa("Why use R when you already have Python?",
   "R is the industry standard for statistical computing and is expected in academic Big Data projects. While Python handles ML predictions, R handles formal statistical tests: ANOVA (are GPA differences across departments statistically significant?), Shapiro-Wilk normality test, correlation analysis with p-values. R also shows we can use multiple languages in a microservice architecture.")

qa("How does the R service communicate with the rest of the system?",
   "R runs as a Plumber API (like Flask for R) in its own Docker container on port 8787. The FastAPI backend proxies requests to R (/api/r/summary → R service /summary). If R is unavailable, the API falls back to computing statistics in Python — ensuring the system works even without R.")

heading("Project Management Questions", level=2)

qa("How was the work distributed?",
   "Two leads (30% each) and four members (10% each). Nusrah Naeem handled the data pipeline + ML models. Bilal Farooqui handled the API + web dashboard + Docker infrastructure. Kashif handled data storage. Bilal Ahmed handled documentation. Shah Azzam handled testing. Ismail's 10% was buffer (Tableau dashboards) — project works without it.")

qa("What was the biggest challenge?",
   "Making 10 different technologies work together in Docker on Windows. Each service has its own configuration, networking, and dependencies. The key was using Docker Compose with health checks and environment variables for service discovery, plus building fallbacks (e.g., Python stats if R is unavailable).")

qa("How would you improve this project?",
   "Three improvements: (1) Add real student data instead of synthetic data. (2) Implement actual user authentication with JWT tokens. (3) Deploy on a cloud platform (AWS EMR for Spark, Amazon MSK for Kafka) for true distributed processing instead of single-machine Docker.")

doc.add_page_break()

# ═══════════════════════════════════════════════════════
#  PART 5: QUICK REFERENCE CARD
# ═══════════════════════════════════════════════════════
heading("Part 5: Quick Reference")

para("Start: ", bold=True)
para("   docker compose up --build -d")
para("Stop: ", bold=True)
para("   docker compose down")
para("Dashboard: ", bold=True)
para("   http://localhost:3000")
para("API Docs: ", bold=True)
para("   http://localhost:8000/docs")
para("HDFS UI: ", bold=True)
para("   http://localhost:9870")
para("Spark UI: ", bold=True)
para("   http://localhost:8080")

para("")
para("Run ML pipeline locally (no Docker): ", bold=True)
para("   python data/generate_data.py")
para("   python ml/run_all.py")

# ── Save ──
output_path = os.path.join(BASE_DIR, "EduPredict-Complete-Guide.docx")
doc.save(output_path)
print(f"Guide saved to: {output_path}")
