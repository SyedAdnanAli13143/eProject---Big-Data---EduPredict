# EduPredict — Presentation Slides Outline

Use this outline to create PowerPoint/Google Slides.

---

## Slide 1: Title
**EduPredict — Big Data + Predictive Analytics for Education**
- eProject | Semester 6 | May 2026
- Team: Nusrah Naeem, Bilal Farooqui, Kashif Akhtar, Bilal Ahmed, Shah Azzam, Ismail

---

## Slide 2: Problem Statement
- Declining student retention rates
- Inefficient resource allocation (overcrowded/empty courses)
- No personalized learning insights
- Data overload — institutions collect but don't analyze
- **Goal: Data-driven decision making for education**

---

## Slide 3: Solution — EduPredict
- Collects educational data (grades, attendance, LMS, enrollment)
- Processes with Big Data tools (Hadoop, Spark, Kafka)
- Predicts using Machine Learning (4 models)
- Displays on interactive web dashboard
- One command deployment: `docker compose up`

---

## Slide 4: Technology Stack
| Layer | Technology |
|-------|-----------|
| Storage | MongoDB + Hadoop HDFS |
| Streaming | Apache Kafka |
| Processing | Apache Spark |
| ML | scikit-learn (Python) |
| Backend | FastAPI |
| Frontend | HTML + Tailwind + Chart.js |
| Statistics | R + Plumber |
| Deployment | Docker Compose (10 services) |

---

## Slide 5: System Architecture
- Show the layered architecture diagram
- Web Dashboard → FastAPI → ML Models → Spark → Kafka → MongoDB/HDFS
- All running in Docker containers

---

## Slide 6: Data Pipeline
1. Generate synthetic data (500 students, 5 datasets)
2. Batch ingestion into MongoDB
3. Real-time streaming via Kafka
4. Spark batch processing (feature engineering)
5. ML model training
6. API serving → Dashboard display

---

## Slide 7: ML Models — Results
| Model | Algorithm | Key Metric |
|-------|-----------|-----------|
| Student Performance | Random Forest | R² = 0.965 |
| Dropout Risk | Gradient Boosting | Accuracy = 88% |
| Course Demand | Random Forest | R² = 0.647 |
| Anomaly Detection | Isolation Forest | 40 flagged (8%) |

---

## Slide 8: Web Dashboard Demo
- Show screenshots of each section:
  - Overview (stats + service health)
  - Students table (search + filter)
  - Dropout Risk (highlighted students)
  - Course Demand (line charts)
  - ML Models (metric bars)
  - Pipeline (step tracker + logs)
  - Team Progress

---

## Slide 9: R Analytics
- Statistical summary (mean, median, quartiles)
- Correlation matrix
- ANOVA test across departments
- Distribution analysis with normality tests

---

## Slide 10: Docker Infrastructure
- 10 containers from 1 command
- MongoDB, Kafka, Zookeeper, HDFS, Spark, API, Web, R
- Health checks, volume persistence
- Works identically on any Windows machine

---

## Slide 11: Team Contribution
| Member | Share | Focus |
|--------|-------|-------|
| Nusrah Naeem (Lead) | 30% | Data Pipeline + ML |
| Bilal Farooqui (Lead) | 30% | API + Web + Docker |
| Kashif Akhtar | 10% | Storage + Database |
| Bilal Ahmed | 10% | Documentation + Video |
| Shah Azzam | 10% | Testing + QA |
| Ismail | 10% | Dashboards (Buffer) |

---

## Slide 12: Future Improvements
- Real student data (not synthetic)
- JWT authentication with role-based access
- Cloud deployment (AWS/Azure)
- Tableau integration for advanced visualization
- Mobile-responsive dashboard

---

## Slide 13: Live Demo
- Run `docker compose up`
- Open http://localhost:3000
- Show dashboard sections
- Show Pipeline running
- Show API docs at /docs

---

## Slide 14: Q&A
**Thank you!**
- Repository: [GitHub URL]
- Dashboard: http://localhost:3000
