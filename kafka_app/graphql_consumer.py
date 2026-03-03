from kafka import KafkaConsumer
import json
import httpx
from agents.github_agent_graphql import analyze_github

GRAPHQL_URL = "http://localhost:8002/graphql"

consumer = KafkaConsumer(
    "github_analysis",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="github-analysis-graphql-group",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

print("Listening on 'github_analysis' topic (GraphQL mode)... (Ctrl+C to stop)")

for message in consumer:
    candidate_id = message.value.get("candidate_id")
    github_url = message.value.get("github_url")
    job_id = message.value.get("job_id")
    print(f"\nReceived candidate_id: {candidate_id}, github_url: {github_url}, job_id: {job_id}")

    query = """
    query ($id: Int!) {
        job(id: $id) {
            title
            description
        }
    }
    """
    response = httpx.post(GRAPHQL_URL, json={"query": query, "variables": {"id": job_id}})
    data = response.json()
    job = data.get("data", {}).get("job")

    if job is None:
        print(f"  Job id={job_id} not found via GraphQL. Skipping.")
        continue

    print(f"  Matching against job: {job['title']}")
    analyze_github(github_url, job["description"])
