"""
Configuration for ingestion services.
Uses environment variables so it works both locally and inside Docker.
"""

import os

# Kafka
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC_ATTENDANCE = "student-attendance"
KAFKA_TOPIC_LMS = "lms-activity"

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = "edupredict"

# HDFS
HDFS_URL = os.getenv("HDFS_URL", "http://localhost:9870")
HDFS_USER = os.getenv("HDFS_USER", "hadoop")

# Local data path (fallback when HDFS is not available)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
