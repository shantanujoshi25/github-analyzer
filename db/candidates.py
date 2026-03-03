import sqlite3

DB_NAME = "candidates.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone_number TEXT,
            resume_url TEXT NOT NULL,
            github_url TEXT,
            leetcode_url TEXT,
            portfolio_url TEXT,
            profile_summary TEXT,
            status TEXT DEFAULT 'actively_looking'
                CHECK (status IN ('actively_looking', 'casually_looking', 'not_looking')),
            is_deleted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database '{DB_NAME}' initialized with 'candidates' table.")


if __name__ == "__main__":
    init_db()
