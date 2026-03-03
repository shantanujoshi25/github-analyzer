import sqlite3
from db.jobs import JOBS_DB_NAME, init_jobs_db

DUMMY_JOBS = [
    {
        "title": "Senior Backend Engineer",
        "company": "CloudScale Inc.",
        "description": (
            "We are looking for a Senior Backend Engineer to design and build scalable "
            "microservices and APIs.\n\n"
            "Requirements:\n"
            "- 5+ years of experience with Python or Go\n"
            "- Strong knowledge of distributed systems and message queues (Kafka, RabbitMQ)\n"
            "- Experience with cloud platforms (AWS, GCP) and containerization (Docker, Kubernetes)\n"
            "- Proficiency in SQL and NoSQL databases (PostgreSQL, Redis, MongoDB)\n"
            "- Familiarity with CI/CD pipelines and infrastructure as code\n"
            "- Understanding of RESTful API design and gRPC\n\n"
            "Nice to have:\n"
            "- Open source contributions\n"
            "- Experience with event-driven architectures\n"
            "- Knowledge of observability tools (Prometheus, Grafana)"
        ),
    },
    {
        "title": "Full Stack Developer",
        "company": "WebFlow Studios",
        "description": (
            "Join our team as a Full Stack Developer to build modern web applications "
            "from front to back.\n\n"
            "Requirements:\n"
            "- 3+ years of experience with React, TypeScript, and Node.js\n"
            "- Strong understanding of HTML, CSS, and responsive design\n"
            "- Experience with relational databases (PostgreSQL, MySQL)\n"
            "- Familiarity with REST APIs and GraphQL\n"
            "- Knowledge of version control (Git) and agile methodologies\n"
            "- Experience with testing frameworks (Jest, Cypress)\n\n"
            "Nice to have:\n"
            "- Experience with Next.js or Remix\n"
            "- Familiarity with cloud deployment (Vercel, AWS)\n"
            "- UI/UX design sensibility"
        ),
    },
    {
        "title": "Machine Learning Engineer",
        "company": "DeepMind Analytics",
        "description": (
            "We are seeking a Machine Learning Engineer to develop and deploy ML models "
            "for production systems.\n\n"
            "Requirements:\n"
            "- 3+ years of experience in machine learning and deep learning\n"
            "- Proficiency in Python, PyTorch or TensorFlow\n"
            "- Experience with NLP, computer vision, or recommendation systems\n"
            "- Strong foundation in statistics, linear algebra, and probability\n"
            "- Experience with ML pipelines and model deployment (MLflow, Kubeflow)\n"
            "- Familiarity with data processing tools (Pandas, Spark)\n\n"
            "Nice to have:\n"
            "- Published research or conference papers\n"
            "- Experience with LLMs and transformer architectures\n"
            "- Knowledge of GPU optimization and distributed training"
        ),
    },
]


def seed_jobs():
    init_jobs_db()
    conn = sqlite3.connect(JOBS_DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM job_descriptions")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='job_descriptions'")

    for job in DUMMY_JOBS:
        cursor.execute(
            "INSERT INTO job_descriptions (title, company, description) VALUES (?, ?, ?)",
            (job["title"], job["company"], job["description"]),
        )

    conn.commit()
    conn.close()
    print(f"Seeded {len(DUMMY_JOBS)} job descriptions into '{JOBS_DB_NAME}'.")


if __name__ == "__main__":
    seed_jobs()
