"""
Kafka Consumer — reads student events from Kafka and stores them in MongoDB.
Run: python ingestion/kafka_consumer.py

Requires: Kafka + MongoDB running (docker-compose up kafka mongodb)
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from config import KAFKA_BROKER, KAFKA_TOPIC_ATTENDANCE, KAFKA_TOPIC_LMS, MONGO_URI, MONGO_DB

try:
    from kafka import KafkaConsumer
except ImportError:
    print("ERROR: Install kafka-python first ->  pip install kafka-python")
    sys.exit(1)

try:
    from pymongo import MongoClient
except ImportError:
    print("ERROR: Install pymongo first ->  pip install pymongo")
    sys.exit(1)


def run_consumer():
    """Consume events from Kafka topics and insert into MongoDB."""
    print(f"Connecting to Kafka at {KAFKA_BROKER}...")
    consumer = KafkaConsumer(
        KAFKA_TOPIC_ATTENDANCE,
        KAFKA_TOPIC_LMS,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="edupredict-consumer",
    )

    print(f"Connecting to MongoDB at {MONGO_URI}...")
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]

    print("Listening for events (Ctrl+C to stop)...\n")

    count = 0
    try:
        for message in consumer:
            topic = message.topic
            data = message.value

            # Insert into the matching MongoDB collection
            if topic == KAFKA_TOPIC_ATTENDANCE:
                db.attendance_stream.insert_one(data)
                print(f"[Attendance] Saved: {data['student_id']} -> {data['status']}")
            elif topic == KAFKA_TOPIC_LMS:
                db.lms_stream.insert_one(data)
                print(f"[LMS]        Saved: {data['student_id']} -> {data['action']}")

            count += 1
            if count % 10 == 0:
                print(f"  Total events consumed: {count}\n")

    except KeyboardInterrupt:
        print(f"\nStopped. Total events consumed: {count}")
    finally:
        consumer.close()
        client.close()


if __name__ == "__main__":
    run_consumer()
