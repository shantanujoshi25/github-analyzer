# Kafka Agent - GitHub Profile Analyzer

A Kafka-based pipeline that analyzes GitHub profiles against job descriptions using AI agents (CrewAI).

## Architecture

```
Producer → Kafka (github_analysis topic) → Consumer → CrewAI Agent → Fit Report
```

- **Producer** reads candidate data from SQLite, sends GitHub URL + job ID to Kafka
- **Consumer** receives messages, looks up job description, triggers the AI agent
- **Agent** fetches GitHub profile data and evaluates candidate-job fit

## Project Structure

```
├── db/                     # Database layer
│   ├── candidates.py       # Candidates table schema
│   ├── jobs.py             # Job descriptions table schema
│   ├── seed_candidates.py  # Seed dummy candidates
│   └── seed_jobs.py        # Seed dummy job descriptions
├── agents/                 # AI agents
│   ├── github_agent.py           # Scrape-based agent
│   ├── github_agent_graphql.py   # GitHub GraphQL API agent
│   └── github_graphql_tool.py    # Custom CrewAI tool for GitHub API
├── kafka_app/              # Kafka producers & consumers
│   ├── github_producer.py    # Direct SQLite producer
│   ├── github_consumer.py    # Direct SQLite consumer
│   ├── graphql_producer.py   # GraphQL-based producer
│   ├── graphql_consumer.py   # GraphQL-based consumer
│   ├── test_producer.py      # Simple test producer
│   └── test_consumer.py      # Simple test consumer
├── graphql_api/            # GraphQL server
│   └── server.py           # Strawberry + FastAPI server
├── docker-compose.yml      # Kafka + Kafka UI
├── requirements.txt
└── .env.example
```

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # Add your API keys
docker compose up -d   # Start Kafka
python -m db.seed_candidates
python -m db.seed_jobs
```

## Usage

### Direct mode (SQLite + web scraping)
```bash
python -m kafka_app.github_consumer   # Terminal 1
python -m kafka_app.github_producer   # Terminal 2
```

### GraphQL mode (GitHub API + GraphQL server)
```bash
python -m graphql_api.server          # Terminal 1
python -m kafka_app.graphql_consumer  # Terminal 2
python -m kafka_app.graphql_producer  # Terminal 3
```

## Tech Stack

- **Kafka** - Message broker (via Docker)
- **CrewAI** - AI agent framework
- **OpenAI GPT-4o** - LLM for analysis
- **GitHub GraphQL API** - Structured profile data
- **Strawberry + FastAPI** - GraphQL server
- **SQLite** - Local database
