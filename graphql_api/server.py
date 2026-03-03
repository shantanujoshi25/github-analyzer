import sqlite3
from typing import Optional
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from db.candidates import DB_NAME
from db.jobs import JOBS_DB_NAME


@strawberry.type
class Candidate:
    id: int
    user_id: str
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    resume_url: str
    github_url: Optional[str]
    leetcode_url: Optional[str]
    portfolio_url: Optional[str]
    profile_summary: Optional[str]
    status: str
    is_deleted: bool
    created_at: str
    updated_at: str


@strawberry.type
class JobDescription:
    id: int
    title: str
    company: str
    description: str
    created_at: str


def get_candidate_by_id(candidate_id: int) -> Optional[Candidate]:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return Candidate(**dict(row))


def get_all_candidates(limit: int = 10) -> list[Candidate]:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [Candidate(**dict(row)) for row in rows]


def get_job_by_id(job_id: int) -> Optional[JobDescription]:
    conn = sqlite3.connect(JOBS_DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_descriptions WHERE id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    return JobDescription(**dict(row))


def get_all_jobs(limit: int = 10) -> list[JobDescription]:
    conn = sqlite3.connect(JOBS_DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_descriptions LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [JobDescription(**dict(row)) for row in rows]


@strawberry.type
class Query:
    @strawberry.field
    def candidate(self, id: int) -> Optional[Candidate]:
        return get_candidate_by_id(id)

    @strawberry.field
    def candidates(self, limit: int = 10) -> list[Candidate]:
        return get_all_candidates(limit)

    @strawberry.field
    def job(self, id: int) -> Optional[JobDescription]:
        return get_job_by_id(id)

    @strawberry.field
    def jobs(self, limit: int = 10) -> list[JobDescription]:
        return get_all_jobs(limit)


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    print("Starting GraphQL server at http://localhost:8002/graphql")
    uvicorn.run(app, host="0.0.0.0", port=8002)
