"""
Generate Professional EduPredict Presentation (.pptx)
Attractive design with R charts, metrics, and architecture
Run: python Docs/generate_ppt.py
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
OUTPUT_DIR = os.path.join(BASE_DIR, "Presentation")
PLOTS_DIR = os.path.join(PROJECT_DIR, "r-analytics", "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── Colors ──
BLUE = RGBColor(0x1E, 0x40, 0xAF)
DARK_BLUE = RGBColor(0x0F, 0x17, 0x2A)
LIGHT_BLUE = RGBColor(0xDB, 0xEA, 0xFE)
ACCENT = RGBColor(0x3B, 0x82, 0xF6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x1E, 0x29, 0x3B)
GRAY = RGBColor(0x94, 0xA3, 0xB8)
GREEN = RGBColor(0x10, 0xB9, 0x81)
RED = RGBColor(0xEF, 0x44, 0x44)
AMBER = RGBColor(0xF5, 0x9E, 0x0B)

def add_bg(slide, color=DARK_BLUE):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape_bg(slide, left, top, width, height, color):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_text(slide, text, left, top, width, height, size=18, color=WHITE, bold=False, align=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.alignment = align
    return txBox

def add_bullet_list(slide, items, left, top, width, height, size=16, color=WHITE):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"▸  {item}"
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(8)
    return txBox

def add_image(slide, filename, left, top, width):
    path = os.path.join(PLOTS_DIR, filename)
    if os.path.exists(path):
        slide.shapes.add_picture(path, left, top, width=width)
        return True
    return False

def add_metric_card(slide, left, top, value, label, color=ACCENT):
    w, h = Inches(2.8), Inches(1.6)
    shape = add_shape_bg(slide, left, top, w, h, RGBColor(0x1E, 0x29, 0x3B))
    # Top color bar
    add_shape_bg(slide, left, top, w, Inches(0.08), color)
    # Value
    add_text(slide, str(value), left + Inches(0.2), top + Inches(0.25), w - Inches(0.4), Inches(0.7),
             size=28, color=color, bold=True, align=PP_ALIGN.CENTER)
    # Label
    add_text(slide, label, left + Inches(0.2), top + Inches(0.95), w - Inches(0.4), Inches(0.5),
             size=12, color=GRAY, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════
# SLIDE 1: TITLE
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
add_bg(slide, DARK_BLUE)

# Accent line
add_shape_bg(slide, Inches(1), Inches(1.8), Inches(1.5), Inches(0.06), ACCENT)

add_text(slide, "EduPredict", Inches(1), Inches(2), Inches(10), Inches(1),
         size=52, color=WHITE, bold=True)
add_text(slide, "Big Data + Predictive Analytics for Education", Inches(1), Inches(3), Inches(10), Inches(0.7),
         size=24, color=ACCENT)
add_text(slide, "A complete data pipeline with ML predictions, R analytics,\nand interactive dashboard — all in Docker",
         Inches(1), Inches(3.8), Inches(10), Inches(0.8), size=16, color=GRAY)

add_text(slide, "eProject | Semester 6 | May 2026", Inches(1), Inches(5.5), Inches(5), Inches(0.5),
         size=14, color=GRAY)
add_text(slide, "Team: Nusrah Naeem · Bilal Farooqui · Kashif · Bilal A. · Shah Azzam · Ismail",
         Inches(1), Inches(6), Inches(10), Inches(0.5), size=13, color=GRAY)

# ══════════════════════════════════════════════════════════════
# SLIDE 2: PROBLEM
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "The Problem", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

problems = [
    "10-20% student dropout rates with NO early warning system",
    "Overcrowded or empty courses — no demand forecasting",
    "Massive data collected (grades, attendance, LMS) but never analyzed",
    "Reactive approach: problems found AFTER students fail",
    "No personalized insights for individual students",
]
add_bullet_list(slide, problems, Inches(1), Inches(1.8), Inches(11), Inches(4), size=20, color=WHITE)

add_text(slide, "Goal: Transform raw educational data into actionable predictions",
         Inches(1), Inches(6), Inches(11), Inches(0.6), size=18, color=ACCENT, bold=True)

# ══════════════════════════════════════════════════════════════
# SLIDE 3: SOLUTION
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "Our Solution — EduPredict", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

solutions = [
    "Collect & generate educational data (500 students, 5 datasets)",
    "Process with Big Data tools (Hadoop, Spark, Kafka, MongoDB)",
    "Predict using 4 Machine Learning models (scikit-learn)",
    "Analyze with R statistical computing (Plumber API + visualizations)",
    "Display on interactive web dashboard (Tailwind + Chart.js)",
    "Deploy with ONE command: docker compose up (10 services)",
]
add_bullet_list(slide, solutions, Inches(1), Inches(1.8), Inches(11), Inches(4.5), size=20, color=WHITE)

# ══════════════════════════════════════════════════════════════
# SLIDE 4: TECH STACK
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "Technology Stack", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

stack = [
    ("Storage", "MongoDB 7 + Hadoop HDFS", ACCENT),
    ("Streaming", "Apache Kafka + Zookeeper", GREEN),
    ("Processing", "Apache Spark 3.5.3", AMBER),
    ("ML", "scikit-learn (Python)", RED),
    ("Statistics", "R 4.3 + Plumber API", RGBColor(0x8B, 0x5C, 0xF6)),
    ("Backend", "FastAPI (Python)", ACCENT),
    ("Frontend", "HTML + Tailwind + Chart.js", GREEN),
    ("Deploy", "Docker Compose (10 containers)", RGBColor(0x06, 0xB6, 0xD4)),
]

for i, (layer, tech, color) in enumerate(stack):
    row = i // 4
    col = i % 4
    x = Inches(0.8 + col * 3.1)
    y = Inches(1.6 + row * 2.8)
    w, h = Inches(2.8), Inches(2.2)

    shape = add_shape_bg(slide, x, y, w, h, RGBColor(0x1E, 0x29, 0x3B))
    add_shape_bg(slide, x, y, w, Inches(0.06), color)
    add_text(slide, layer, x + Inches(0.2), y + Inches(0.3), w - Inches(0.4), Inches(0.5),
             size=14, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, tech, x + Inches(0.2), y + Inches(0.9), w - Inches(0.4), Inches(1),
             size=15, color=WHITE, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════
# SLIDE 5: ARCHITECTURE
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "System Architecture", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

arch_text = """Web Dashboard (Nginx:3001)  →  FastAPI Backend (:8000)  →  ML Models (Python)
                                    ↕                           ↕
                          R Analytics (:8787)         Spark Processing (:8080)
                                    ↕                           ↕
                          MongoDB (:27017)            Kafka (:9092) + HDFS (:9870)"""

add_text(slide, arch_text, Inches(0.8), Inches(1.8), Inches(11.5), Inches(3),
         size=16, color=WHITE)

add_text(slide, "10 Docker Containers — All orchestrated with docker compose up",
         Inches(0.8), Inches(5.5), Inches(11), Inches(0.5), size=18, color=ACCENT, bold=True)

containers = "MongoDB  •  Zookeeper  •  Kafka  •  HDFS NameNode  •  HDFS DataNode  •  Spark Master  •  Spark Worker  •  FastAPI  •  R Service  •  Nginx Web"
add_text(slide, containers, Inches(0.8), Inches(6.2), Inches(11), Inches(0.5), size=13, color=GRAY)

# ══════════════════════════════════════════════════════════════
# SLIDE 6: DATA PIPELINE
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "Data Pipeline", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

steps = [
    ("1", "Generate\nData", "500 students\n5 CSV files", ACCENT),
    ("2", "Ingest to\nMongoDB", "5 collections\nbatch load", GREEN),
    ("3", "Kafka\nStreaming", "Real-time\nevents", AMBER),
    ("4", "Spark\nProcessing", "Feature\nengineering", RED),
    ("5", "ML Model\nTraining", "4 models\ntrained", RGBColor(0x8B, 0x5C, 0xF6)),
    ("6", "API +\nDashboard", "16 endpoints\n9 sections", RGBColor(0x06, 0xB6, 0xD4)),
]

for i, (num, title, desc, color) in enumerate(steps):
    x = Inches(0.5 + i * 2.1)
    y = Inches(2)
    w, h = Inches(1.8), Inches(3.5)

    shape = add_shape_bg(slide, x, y, w, h, RGBColor(0x1E, 0x29, 0x3B))
    # Number circle
    add_shape_bg(slide, x + Inches(0.6), y + Inches(0.15), Inches(0.6), Inches(0.6), color)
    add_text(slide, num, x + Inches(0.6), y + Inches(0.2), Inches(0.6), Inches(0.5),
             size=20, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, title, x + Inches(0.1), y + Inches(0.9), w - Inches(0.2), Inches(0.8),
             size=14, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, desc, x + Inches(0.1), y + Inches(2), w - Inches(0.2), Inches(1),
             size=12, color=GRAY, align=PP_ALIGN.CENTER)

    # Arrow
    if i < len(steps) - 1:
        add_text(slide, "→", x + Inches(1.85), y + Inches(1.3), Inches(0.3), Inches(0.5),
                 size=24, color=ACCENT, bold=True)

# ══════════════════════════════════════════════════════════════
# SLIDE 7: ML RESULTS
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "ML Model Results", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

# Metric cards
add_metric_card(slide, Inches(0.8), Inches(1.6), "R² = 0.965", "Student Performance\nRandom Forest Regressor", GREEN)
add_metric_card(slide, Inches(3.9), Inches(1.6), "88.0%", "Dropout Risk Accuracy\nGradient Boosting", ACCENT)
add_metric_card(slide, Inches(7.0), Inches(1.6), "R² = 0.647", "Course Demand\nRandom Forest Regressor", AMBER)
add_metric_card(slide, Inches(10.1), Inches(1.6), "40 (8%)", "Anomalies Detected\nIsolation Forest", RED)

# Key findings
findings = [
    "Performance model predicts GPA with 96.5% accuracy (MAE = 0.11 GPA points)",
    "54 students (10.8%) flagged as dropout risk — avg GPA 1.75 vs 2.87 for active",
    "Course demand growing across all departments — CS has highest enrollment",
    "Anomalous students show significantly different behavioral patterns",
]
add_bullet_list(slide, findings, Inches(0.8), Inches(4), Inches(11), Inches(3), size=16, color=WHITE)

# ══════════════════════════════════════════════════════════════
# SLIDE 8: R ANALYTICS CHARTS
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "R Analytics — Visualizations", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

# Add R charts in a grid
charts_grid = [
    ("gpa_distribution.png", Inches(0.5), Inches(1.5)),
    ("department_comparison.png", Inches(4.5), Inches(1.5)),
    ("correlation_heatmap.png", Inches(8.8), Inches(1.5)),
    ("attendance_vs_grade.png", Inches(0.5), Inches(4.5)),
    ("department_dropout.png", Inches(4.5), Inches(4.5)),
    ("course_demand_trends.png", Inches(8.8), Inches(4.5)),
]

for filename, x, y in charts_grid:
    # Dark card background
    add_shape_bg(slide, x - Inches(0.1), y - Inches(0.1), Inches(4.2), Inches(2.9), RGBColor(0x1E, 0x29, 0x3B))
    add_image(slide, filename, x, y, Inches(4))

# ══════════════════════════════════════════════════════════════
# SLIDE 9: R STATISTICAL RESULTS
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "R Statistical Analysis Results", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

r_results = [
    "Descriptive Statistics: 500 students, mean GPA = 2.74, mean attendance = 77.3%",
    "ANOVA (GPA ~ Department): F=0.254, p=0.907 — No significant difference across depts",
    "T-test (Dropout vs Active GPA): t=-29.8, p<0.001 — HIGHLY SIGNIFICANT",
    "Correlation: Attendance ↔ Grade r=0.782, LMS Time ↔ Grade r=0.977",
    "Shapiro-Wilk: GPA distribution is non-normal (p<0.001)",
    "Dropout students: GPA 1.75, Attendance 66% vs Active: GPA 2.87, Attendance 79%",
]
add_bullet_list(slide, r_results, Inches(0.8), Inches(1.6), Inches(11.5), Inches(4), size=18, color=WHITE)

add_text(slide, "Key Insight: LMS engagement time is the strongest predictor of academic success (r=0.977)",
         Inches(0.8), Inches(6), Inches(11), Inches(0.6), size=16, color=ACCENT, bold=True)

# ══════════════════════════════════════════════════════════════
# SLIDE 10: DOCKER INFRA
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "Docker Infrastructure", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

containers_list = [
    ("MongoDB", ":27017", "NoSQL Database", ACCENT),
    ("Kafka", ":9092", "Event Streaming", GREEN),
    ("Zookeeper", ":2181", "Coordination", GRAY),
    ("HDFS NameNode", ":9870", "File Storage", AMBER),
    ("HDFS DataNode", "—", "Data Blocks", AMBER),
    ("Spark Master", ":8080", "Processing", RED),
    ("Spark Worker", "—", "Compute Node", RED),
    ("FastAPI", ":8000", "Backend API", ACCENT),
    ("R Service", ":8787", "R Analytics", RGBColor(0x8B, 0x5C, 0xF6)),
    ("Nginx Web", ":3001", "Dashboard", GREEN),
]

for i, (name, port, role, color) in enumerate(containers_list):
    row = i // 5
    col = i % 5
    x = Inches(0.5 + col * 2.5)
    y = Inches(1.6 + row * 2.5)
    w, h = Inches(2.2), Inches(2)

    add_shape_bg(slide, x, y, w, h, RGBColor(0x1E, 0x29, 0x3B))
    add_shape_bg(slide, x, y, w, Inches(0.06), color)
    add_text(slide, name, x + Inches(0.1), y + Inches(0.2), w - Inches(0.2), Inches(0.5),
             size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, port, x + Inches(0.1), y + Inches(0.8), w - Inches(0.2), Inches(0.4),
             size=18, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, role, x + Inches(0.1), y + Inches(1.4), w - Inches(0.2), Inches(0.4),
             size=11, color=GRAY, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════
# SLIDE 11: TEAM
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "Team Contribution", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

members = [
    ("Nusrah Naeem", "30%", "Lead", "Data Pipeline + ML Models", GREEN),
    ("Bilal Farooqui", "30%", "Lead", "API + Web + Docker", ACCENT),
    ("Kashif Akhtar", "10%", "Member", "Database & Storage", AMBER),
    ("Bilal Ahmed", "10%", "Member", "Documentation", RGBColor(0x8B, 0x5C, 0xF6)),
    ("Shah Azzam", "10%", "Member", "Testing & QA", RGBColor(0x06, 0xB6, 0xD4)),
    ("Syed M. Ismail", "10%", "Buffer", "Dashboards", GRAY),
]

for i, (name, share, role, focus, color) in enumerate(members):
    row = i // 3
    col = i % 3
    x = Inches(0.8 + col * 4)
    y = Inches(1.6 + row * 2.8)
    w, h = Inches(3.6), Inches(2.3)

    add_shape_bg(slide, x, y, w, h, RGBColor(0x1E, 0x29, 0x3B))
    add_shape_bg(slide, x, y, w, Inches(0.06), color)
    add_text(slide, name, x + Inches(0.2), y + Inches(0.2), w - Inches(0.4), Inches(0.5),
             size=18, color=WHITE, bold=True)
    add_text(slide, f"{share}  •  {role}", x + Inches(0.2), y + Inches(0.8), w - Inches(0.4), Inches(0.4),
             size=14, color=color, bold=True)
    add_text(slide, focus, x + Inches(0.2), y + Inches(1.4), w - Inches(0.4), Inches(0.6),
             size=13, color=GRAY)

# ══════════════════════════════════════════════════════════════
# SLIDE 12: FUTURE
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "Future Enhancements", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

future = [
    "Real student data integration (replace synthetic with institutional data)",
    "JWT authentication with role-based access (admin, faculty, student)",
    "Cloud deployment on AWS/Azure with auto-scaling Spark clusters",
    "Deep Learning: LSTM models for time-series grade prediction",
    "Tableau dashboard integration for non-technical stakeholders",
    "Automated email alerts when dropout risk exceeds threshold",
]
add_bullet_list(slide, future, Inches(0.8), Inches(1.6), Inches(11), Inches(4.5), size=20, color=WHITE)

# ══════════════════════════════════════════════════════════════
# SLIDE 13: LIVE DEMO
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
add_shape_bg(slide, Inches(0), Inches(0), Inches(13.333), Inches(1.2), BLUE)
add_text(slide, "Live Demo", Inches(0.8), Inches(0.25), Inches(10), Inches(0.7),
         size=32, color=WHITE, bold=True)

demo_steps = [
    "1.  git clone <repository-url>",
    "2.  cd eProject---Big-Data---EduPredict",
    "3.  docker compose up -d",
    "4.  Open http://localhost:3001  (Web Dashboard)",
    "5.  Open http://localhost:8000/docs  (API Swagger)",
    "6.  Open http://localhost:8080  (Spark UI)",
]
add_bullet_list(slide, demo_steps, Inches(1), Inches(1.8), Inches(11), Inches(4), size=22, color=WHITE)

add_text(slide, "That's it — everything runs with a single command!",
         Inches(1), Inches(6), Inches(11), Inches(0.6), size=20, color=GREEN, bold=True)

# ══════════════════════════════════════════════════════════════
# SLIDE 14: THANK YOU
# ══════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)

add_shape_bg(slide, Inches(3), Inches(1.5), Inches(7.333), Inches(0.06), ACCENT)

add_text(slide, "Thank You!", Inches(3), Inches(2), Inches(7.333), Inches(1.2),
         size=48, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
add_text(slide, "Questions & Discussion", Inches(3), Inches(3.5), Inches(7.333), Inches(0.8),
         size=24, color=ACCENT, align=PP_ALIGN.CENTER)

add_shape_bg(slide, Inches(3), Inches(4.8), Inches(7.333), Inches(0.06), ACCENT)

add_text(slide, "Dashboard:  http://localhost:3001\nAPI Docs:   http://localhost:8000/docs\nR Service:  http://localhost:8787",
         Inches(3), Inches(5.2), Inches(7.333), Inches(1.5), size=16, color=GRAY, align=PP_ALIGN.CENTER)

# ── Save ──
output_path = os.path.join(OUTPUT_DIR, "EduPredict-Presentation.pptx")
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
print(f"Slides: 14 | Dark theme | R charts included")
