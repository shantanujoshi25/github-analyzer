from kafka import KafkaConsumer
import json
import sqlite3
from db.jobs import JOBS_DB_NAME
from agents.github_agent import analyze_github



consumer = KafkaConsumer(
    "github_analysis",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="github-analysis-group",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print("Listening on 'github_analysis' topic... (Ctrl+C to stop)")

for message in consumer:
    candidate_id = message.value.get("candidate_id")
    github_url = message.value.get("github_url")
    job_id = message.value.get("job_id")
    print(f"\nReceived candidate_id: {candidate_id}, github_url: {github_url}, job_id: {job_id}")

    conn = sqlite3.connect(JOBS_DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT title, description FROM job_descriptions WHERE id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        print(f"  Job id={job_id} not found in database. Skipping.")
        continue

    job_title, job_description = row
    print(f"  Matching against job: {job_title}")
    analyze_github(github_url, job_description)
