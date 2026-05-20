# How to Run EduPredict

## Prerequisites

1. **Windows 10/11 (64-bit)** — tested on Windows 11
2. **Docker Desktop** — [download here](https://www.docker.com/products/docker-desktop/)
   - After install, open Docker Desktop and wait for it to show "Engine Running"
3. **Git** — [download here](https://git-scm.com/downloads)
4. **Hardware**: Minimum i5 / 16GB RAM / 500GB SSD

---

## Option 1: Full Stack (Docker — Recommended)

### Step 1: Clone the project
```bash
git clone <repository-url>
cd eProject---Big-Data---EduPredict
```

### Step 2: Start everything
```bash
docker compose up --build -d
```
This starts **10 containers**: MongoDB, Kafka, Zookeeper, HDFS NameNode, HDFS DataNode, Spark Master, Spark Worker, FastAPI API, R Analytics, Web Dashboard.

First run will take time to download images (~5GB total).

### Step 3: Open the Dashboard
Open your browser and go to:
```
http://localhost:3001
```

### Step 4: Wait for pipeline
The API automatically:
1. Generates synthetic data (500 students)
2. Loads data into MongoDB
3. Runs preprocessing
4. Trains all 4 ML models
5. Runs anomaly detection

Watch progress on the **Pipeline** page in the dashboard.

### Step 5: Explore
- **Overview** — Stats and service health
- **Students** — Browse with search and filters
- **Dropout Risk** — High-risk students
- **Course Demand** — Enrollment trends
- **Anomalies** — Flagged students
- **ML Models** — Accuracy metrics
- **R Analytics** — Statistical analysis
- **Team Progress** — Work tracking

### Stopping
```bash
docker compose down
```

### Restarting
```bash
docker compose up -d
```

---

## Option 2: ML Pipeline Only (No Docker)

If you just want to run the ML models locally:

### Step 1: Install Python dependencies
```bash
pip install pandas numpy scikit-learn
```

### Step 2: Generate data
```bash
python data/generate_data.py
```

### Step 3: Run the complete ML pipeline
```bash
python ml/run_all.py
```

This trains all 4 models and saves them as `.pkl` files in `ml/models/`.

---

## Service URLs

| Service | URL | Description |
|---------|-----|-------------|
| Dashboard | http://localhost:3001 | Main web interface |
| API Docs | http://localhost:8000/docs | FastAPI Swagger docs |
| HDFS UI | http://localhost:9870 | Hadoop NameNode |
| Spark UI | http://localhost:8080 | Spark Master |
| R Service | http://localhost:8787 | R Analytics API |
| MongoDB | localhost:27017 | Database (use Compass) |
| Kafka | localhost:9092 | Message broker |

---

## Troubleshooting

**Docker Desktop not starting?**
- Make sure WSL2 is enabled: Settings → General → "Use WSL 2 based engine"
- Restart Docker Desktop

**Port already in use?**
- Check: `docker ps` to see running containers
- Stop all: `docker compose down`

**API not responding?**
- Check logs: `docker compose logs api`
- MongoDB might still be starting — wait for health check

**Images failing to pull?**
- Check internet connection
- Try: `docker compose pull` separately
