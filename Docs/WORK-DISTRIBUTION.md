# EduPredict — Work Distribution

**Project:** Big Data + Predictive Analytics for Education
**Duration:** 07-May-2026 to 28-May-2026

---

## Split Summary

| Role          | Member                    | Share | Focus Area                          |
|---------------|---------------------------|-------|-------------------------------------|
| Lead          | Nusrah Naeem              | 30%   | Data Pipeline + ML Models           |
| Lead          | Bilal Farooqui            | 30%   | API + Web Portal + Infrastructure   |
| Member        | Muhammad Kashif Akhtar    | 10%   | Data Storage + Database Setup       |
| Member        | Bilal Ahmed               | 10%   | Documentation + Video Demo          |
| Member        | Shah Azzam                | 10%   | Testing + Support Module            |
| Member (Buffer)| Syed Mohammad Ismail     | 10%   | Tableau Dashboards + Monitoring     |

> **Buffer rule:** Syed Mohammad Ismail's 10% covers Tableau dashboards and monitoring — these are enhancements only. The core project is fully functional without them so this 10% will not affect the project if incomplete.

---

## Detailed Breakdown

### Nusrah Naeem — 30% (Lead #1)

**Owns:** `ingestion/`, `processing/`, `ml/`

| # | Task | Folder | Requirement Covered |
|---|------|--------|---------------------|
| 1 | Kafka streaming setup (producer + consumer) | `ingestion/` | Data Ingestion, Real-time Data Processing |
| 2 | Batch ingestion scripts (CSV/JSON to HDFS) | `ingestion/` | Data Ingestion |
| 3 | Spark batch processing jobs | `processing/` | Data Processing |
| 4 | Spark streaming jobs (Kafka integration) | `processing/` | Real-time Data Processing |
| 5 | Data cleaning and feature engineering pipeline | `ml/` | Data Processing |
| 6 | ML model — Student performance prediction | `ml/` | Machine Learning Models |
| 7 | ML model — Dropout risk prediction | `ml/` | Machine Learning Models |
| 8 | ML model — Course demand forecasting | `ml/` | Machine Learning Models |
| 9 | Model evaluation, tuning, and serialization (.pkl) | `ml/` | Machine Learning Models |
| 10 | Anomaly detection algorithm in student data | `ml/` | Machine Learning Models |

---

### Bilal Farooqui — 30% (Lead #2)

**Owns:** `api/`, `web/`, `infrastructure/`

| # | Task | Folder | Requirement Covered |
|---|------|--------|---------------------|
| 1 | Backend API scaffolding (Flask/FastAPI) | `api/` | All backend requirements |
| 2 | User authentication & authorization (role-based: admin, teacher, student, analyst) | `api/` | User Authentication and Authorization |
| 3 | Prediction API endpoints (call ML models) | `api/` | Machine Learning Models integration |
| 4 | Notifications & alerts engine (threshold-based) | `api/` | Notifications and Alerts |
| 5 | Frontend web portal (React or similar) | `web/` | Data Visualization, Feedback and Support |
| 6 | Dashboard pages — student performance, dropout risk, course demand | `web/` | Data Visualization |
| 7 | Role-based access control on frontend | `web/` | User Authentication and Authorization |
| 8 | Feedback & support page (contact form, issue reporting) | `web/` | Feedback and Support |
| 9 | Docker Compose — full stack (Hadoop, Spark, Kafka, MongoDB, API, Web) | `infrastructure/` | All infrastructure |
| 10 | System integration — connect all modules end to end | root | All requirements |

---

### Muhammad Kashif Akhtar — 10%

**Owns:** `data/`, database layer

| # | Task | Folder | Requirement Covered |
|---|------|--------|---------------------|
| 1 | HDFS setup & data partitioning strategy | `infrastructure/` | Data Storage |
| 2 | MongoDB schema design (students, courses, predictions, alerts) | `api/` or `infrastructure/` | Data Storage |
| 3 | Generate synthetic/sample datasets (academic records, demographics, LMS, attendance) | `data/` | Data Ingestion |
| 4 | Data format standardization (CSV, JSON compatibility) | `data/` | Data Ingestion |

---

### Bilal Ahmed — 10%

**Owns:** `Docs/`

| # | Task | Folder | Requirement Covered |
|---|------|--------|---------------------|
| 1 | Technical Specification Document (TSD) — architecture, workflows, model docs | `Docs/Technical Specification Document/` | Documentation |
| 2 | Flowcharts and Data Flow Diagrams | `Docs/Technical Specification Document/` | Documentation |
| 3 | How to Run Project guide (installation, setup, usage) | `Docs/How to Run Project/` | Documentation |
| 4 | Video demonstration of complete working application | `Docs/` | Documentation (Video) |

---

### Shah Azzam — 10%

**Owns:** testing, support integration

| # | Task | Folder | Requirement Covered |
|---|------|--------|---------------------|
| 1 | Test data preparation and validation datasets | `data/` | Test Data |
| 2 | API endpoint testing (unit + integration tests) | `api/` | Performance, Data Integrity |
| 3 | ML model validation (accuracy, precision, recall reports) | `ml/` | Machine Learning Models |
| 4 | Presentation slides | `Docs/Presentation/` | Documentation |

---

### Syed Mohammad Ismail — 10% (Buffer — Non-Critical)

**Owns:** visualization enhancements, monitoring

| # | Task | Folder | Requirement Covered |
|---|------|--------|---------------------|
| 1 | Tableau dashboards (student performance, trends, anomalies) | external (Tableau) | Data Visualization |
| 2 | Performance monitoring dashboard (system metrics, resource utilization) | `web/` or external | Performance Monitoring |
| 3 | UI/UX polish and additional visual charts on web portal | `web/` | Data Visualization |

> **Why this is buffer:** Basic dashboards are built into the web portal by Bilal Farooqui. Tableau dashboards and extra monitoring are enhancements. If this 10% is not delivered, the project still has all core dashboards working through the web portal.

---

## Dependency Map

```
Kashif (data + DB setup)
        |
        v
Nusrah (ingestion -> processing -> ML models)
        |
        v
Bilal F. (API consumes models -> Web portal displays results -> Docker ties it all)
        |
        v
Shah Azzam (testing across all modules)
        |
        v
Bilal Ahmed (documentation + video after features are done)

Ismail (Tableau dashboards — independent, can plug in anytime)
```

---

## Milestones

| Week | Date Range           | Target                                                |
|------|----------------------|-------------------------------------------------------|
| 1    | 07 May – 13 May      | Data setup (Kashif), Ingestion + Spark jobs (Nusrah), API scaffolding + Auth (Bilal F.) |
| 2    | 14 May – 20 May      | ML models ready (Nusrah), Web portal + alerts (Bilal F.), Testing starts (Shah Azzam) |
| 3    | 21 May – 28 May      | Integration, Documentation (Bilal A.), Video, Tableau (Ismail), Final testing + submission |
