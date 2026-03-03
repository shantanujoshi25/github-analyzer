import sqlite3
from db.candidates import DB_NAME, init_db

DUMMY_CANDIDATES = [
    {
        "user_id": "USR001",
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.johnson@example.com",
        "phone_number": "555-0101",
        "resume_url": "https://resumes.example.com/alice-johnson",
        "github_url": "https://github.com/torvalds",
        "leetcode_url": "https://leetcode.com/u/neal_wu",
        "portfolio_url": "https://linus.dev",
        "profile_summary": "Full-stack developer with 3 years of experience in React and Node.js.",
        "status": "actively_looking",
    },
    {
        "user_id": "USR002",
        "first_name": "Bob",
        "last_name": "Smith",
        "email": "bob.smith@example.com",
        "phone_number": "555-0102",
        "resume_url": "https://resumes.example.com/bob-smith",
        "github_url": "https://github.com/gvanrossum",
        "leetcode_url": None,
        "portfolio_url": None,
        "profile_summary": "Backend engineer specializing in Python and distributed systems.",
        "status": "casually_looking",
    },
    {
        "user_id": "USR003",
        "first_name": "Carol",
        "last_name": "Williams",
        "email": "carol.williams@example.com",
        "phone_number": None,
        "resume_url": "https://resumes.example.com/carol-williams",
        "github_url": "https://github.com/karpathy",
        "leetcode_url": "https://leetcode.com/u/votrubac",
        "portfolio_url": "https://karpathy.ai",
        "profile_summary": "ML engineer with expertise in NLP and computer vision.",
        "status": "actively_looking",
    },
    {
        "user_id": "USR004",
        "first_name": "David",
        "last_name": "Brown",
        "email": "david.brown@example.com",
        "phone_number": "555-0104",
        "resume_url": "https://resumes.example.com/david-brown",
        "github_url": None,
        "leetcode_url": None,
        "portfolio_url": None,
        "profile_summary": "DevOps engineer experienced with AWS, Kubernetes, and CI/CD pipelines.",
        "status": "not_looking",
    },
    {
        "user_id": "USR005",
        "first_name": "Eva",
        "last_name": "Martinez",
        "email": "eva.martinez@example.com",
        "phone_number": "555-0105",
        "resume_url": "https://resumes.example.com/eva-martinez",
        "github_url": "https://github.com/sindresorhus",
        "leetcode_url": "https://leetcode.com/u/lee215",
        "portfolio_url": "https://sindresorhus.com",
        "profile_summary": "Frontend developer passionate about accessibility and design systems.",
        "status": "actively_looking",
    },
]


def seed():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM candidates")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='candidates'")

    columns = [
        "user_id", "first_name", "last_name", "email", "phone_number",
        "resume_url", "github_url", "leetcode_url", "portfolio_url",
        "profile_summary", "status",
    ]
    placeholders = ", ".join(["?"] * len(columns))
    sql = f"INSERT INTO candidates ({', '.join(columns)}) VALUES ({placeholders})"

    for candidate in DUMMY_CANDIDATES:
        values = [candidate[col] for col in columns]
        cursor.execute(sql, values)

    conn.commit()
    conn.close()
    print(f"Seeded {len(DUMMY_CANDIDATES)} candidates into '{DB_NAME}'.")


if __name__ == "__main__":
    seed()
