import sqlite3

JOBS_DB_NAME = "jobs.db"


def init_jobs_db():
    conn = sqlite3.connect(JOBS_DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database '{JOBS_DB_NAME}' initialized with 'job_descriptions' table.")


if __name__ == "__main__":
    init_jobs_db()
