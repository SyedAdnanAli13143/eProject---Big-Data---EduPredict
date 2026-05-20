"""
Kafka Producer — streams student attendance and LMS events to Kafka topics.
Run: python ingestion/kafka_producer.py

Requires: Kafka running (docker-compose up kafka)
"""

import json
import time
import random
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from config import KAFKA_BROKER, KAFKA_TOPIC_ATTENDANCE, KAFKA_TOPIC_LMS

try:
    from kafka import KafkaProducer
except ImportError:
    print("ERROR: Install kafka-python first ->  pip install kafka-python")
    sys.exit(1)


def create_producer():
    """Create Kafka producer with JSON serializer."""
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        retries=3,
    )


def generate_attendance_event():
    """Simulate a real-time attendance event."""
    return {
        "student_id": f"STU{random.randint(1, 500):04d}",
        "course_id": random.choice(["CS101", "CS201", "MT101", "PH101", "BU101"]),
        "status": random.choice(["present", "absent", "late"]),
        "timestamp": datetime.now().isoformat(),
    }


def generate_lms_event():
    """Simulate a real-time LMS activity event."""
    return {
        "student_id": f"STU{random.randint(1, 500):04d}",
        "action": random.choice(["login", "submit_assignment", "view_material", "forum_post"]),
        "course_id": random.choice(["CS101", "CS201", "MT101", "PH101", "BU101"]),
        "duration_minutes": random.randint(1, 60),
        "timestamp": datetime.now().isoformat(),
    }


def run_producer():
    """Main loop — sends events to Kafka every 2 seconds."""
    print(f"Connecting to Kafka at {KAFKA_BROKER}...")
    producer = create_producer()
    print("Connected! Streaming events (Ctrl+C to stop)...\n")

    count = 0
    try:
        while True:
            # Send attendance event
            att_event = generate_attendance_event()
            producer.send(KAFKA_TOPIC_ATTENDANCE, att_event)
            print(f"[Attendance] {att_event['student_id']} -> {att_event['status']}")

            # Send LMS event
            lms_event = generate_lms_event()
            producer.send(KAFKA_TOPIC_LMS, lms_event)
            print(f"[LMS]        {lms_event['student_id']} -> {lms_event['action']}")

            count += 2
            print(f"  Total events sent: {count}\n")

            producer.flush()
            time.sleep(2)

    except KeyboardInterrupt:
        print(f"\nStopped. Total events sent: {count}")
    finally:
        producer.close()


if __name__ == "__main__":
    run_producer()
