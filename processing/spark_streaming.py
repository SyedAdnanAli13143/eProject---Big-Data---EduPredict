"""
Spark Structured Streaming — reads real-time events from Kafka and
computes running aggregates (attendance alerts, LMS summaries).
Run: python processing/spark_streaming.py

Requires: PySpark + Kafka running (docker-compose up kafka)
"""

import os
import sys

try:
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
except ImportError:
    print("ERROR: Install pyspark first ->  pip install pyspark")
    sys.exit(1)

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
CHECKPOINT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "checkpoints")
os.makedirs(CHECKPOINT_DIR, exist_ok=True)


# Schema for attendance events coming from Kafka
ATTENDANCE_SCHEMA = StructType([
    StructField("student_id", StringType()),
    StructField("course_id", StringType()),
    StructField("status", StringType()),
    StructField("timestamp", StringType()),
])


def create_spark():
    """Create Spark session with Kafka support."""
    return (
        SparkSession.builder
        .appName("EduPredict-Streaming")
        .master("local[*]")
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")
        .config("spark.driver.memory", "2g")
        .getOrCreate()
    )


def stream_attendance_alerts(spark):
    """
    Read attendance events from Kafka topic 'student-attendance'.
    Compute a 5-minute window aggregate and flag students with
    high absence rates in real time.
    """
    print("Reading from Kafka topic: student-attendance ...")

    # Read from Kafka
    raw_stream = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BROKER)
        .option("subscribe", "student-attendance")
        .option("startingOffsets", "latest")
        .load()
    )

    # Parse JSON value
    parsed = (
        raw_stream
        .select(F.from_json(F.col("value").cast("string"), ATTENDANCE_SCHEMA).alias("data"))
        .select("data.*")
        .withColumn("event_time", F.to_timestamp("timestamp"))
    )

    # 5-minute tumbling window — count absences per student
    windowed = (
        parsed
        .withWatermark("event_time", "10 minutes")
        .groupBy(
            F.window("event_time", "5 minutes"),
            "student_id",
        )
        .agg(
            F.count("*").alias("total_events"),
            F.sum(F.when(F.col("status") == "absent", 1).otherwise(0)).alias("absences"),
        )
        .withColumn("absence_rate", F.col("absences") / F.col("total_events"))
        .filter(F.col("absence_rate") > 0.5)  # Alert threshold
    )

    # Write alerts to console (in production, write to MongoDB or alert system)
    query = (
        windowed.writeStream
        .outputMode("update")
        .format("console")
        .option("truncate", False)
        .option("checkpointLocation", os.path.join(CHECKPOINT_DIR, "attendance_alerts"))
        .start()
    )

    return query


def main():
    print("=" * 60)
    print("EduPredict — Spark Structured Streaming")
    print("=" * 60)
    print(f"Kafka broker: {KAFKA_BROKER}")
    print("Waiting for events...\n")

    spark = create_spark()
    spark.sparkContext.setLogLevel("WARN")

    try:
        query = stream_attendance_alerts(spark)
        query.awaitTermination()
    except KeyboardInterrupt:
        print("\nStreaming stopped.")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
