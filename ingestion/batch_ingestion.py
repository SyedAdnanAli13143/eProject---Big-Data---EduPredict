"""
Batch Ingestion — loads CSV files from data/raw/ into MongoDB (and optionally HDFS).
Run: python ingestion/batch_ingestion.py

Requires: MongoDB running (docker-compose up mongodb)
"""

import os
import sys
import glob

sys.path.insert(0, os.path.dirname(__file__))
from config import MONGO_URI, MONGO_DB, DATA_DIR

try:
    import pandas as pd
except ImportError:
    print("ERROR: Install pandas first ->  pip install pandas")
    sys.exit(1)

try:
    from pymongo import MongoClient
except ImportError:
    print("ERROR: Install pymongo first ->  pip install pymongo")
    sys.exit(1)


def load_csv_to_mongo(csv_path, collection_name, db):
    """Read a CSV file and insert all rows into a MongoDB collection."""
    df = pd.read_csv(csv_path)
    records = df.to_dict("records")

    # Drop existing collection to avoid duplicates on re-run
    db[collection_name].drop()
    db[collection_name].insert_many(records)

    print(f"  {collection_name:25s} <- {len(records)} records from {os.path.basename(csv_path)}")


def run_batch_ingestion():
    """Load all CSV files from data/raw/ into MongoDB."""
    print(f"Data directory: {DATA_DIR}")
    print(f"Connecting to MongoDB at {MONGO_URI}...\n")

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]

    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    if not csv_files:
        print("No CSV files found! Run 'python data/generate_data.py' first.")
        return

    print(f"Found {len(csv_files)} CSV files. Loading into MongoDB '{MONGO_DB}'...\n")

    for csv_path in sorted(csv_files):
        filename = os.path.splitext(os.path.basename(csv_path))[0]
        collection_name = filename  # e.g., "students", "attendance"
        load_csv_to_mongo(csv_path, collection_name, db)

    print(f"\nBatch ingestion complete! All data loaded into MongoDB '{MONGO_DB}'.")
    client.close()


if __name__ == "__main__":
    run_batch_ingestion()
