from kafka import KafkaProducer
import json
import time
import httpx

GRAPHQL_URL = "http://localhost:8002/graphql"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

candidate_ids = [1, 2]
job_id = 2

for cid in candidate_ids:
    query = """
    query ($id: Int!) {
        candidate(id: $id) {
            id
            firstName
            lastName
            githubUrl
        }
    }
    """
    response = httpx.post(GRAPHQL_URL, json={"query": query, "variables": {"id": cid}})
    data = response.json()
    candidate = data.get("data", {}).get("candidate")

    if candidate is None:
        print(f"Candidate id={cid} not found via GraphQL. Skipping.")
        continue

    github_url = candidate.get("githubUrl")
    if not github_url:
        print(f"Candidate id={cid} ({candidate['firstName']}) has no GitHub URL. Skipping.")
        continue

    message = {"candidate_id": cid, "github_url": github_url, "job_id": job_id}
    producer.send("github_analysis", value=message)
    print(f"Sent: {message}")
    time.sleep(1)

producer.flush()
producer.close()
print("Producer finished.")
