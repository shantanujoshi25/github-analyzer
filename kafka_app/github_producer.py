from kafka import KafkaProducer
import json
import sqlite3
import time
from db.candidates import DB_NAME

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

candidate_ids = [1, 2]

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

for cid in candidate_ids:
    cursor.execute("SELECT github_url FROM candidates WHERE id = ?", (cid,))
    row = cursor.fetchone()

    if row is None:
        print(f"Candidate id={cid} not found in database. Skipping.")
        continue

    github_url = row[0]
    if not github_url:
        print(f"Candidate id={cid} has no GitHub URL. Skipping.")
        continue

    message = {"candidate_id": cid, "github_url": github_url, "job_id": 2}
    producer.send("github_analysis", value=message)
    print(f"Sent: {message}")
    time.sleep(1)

conn.close()
producer.flush()
producer.close()
print("Producer finished.")
