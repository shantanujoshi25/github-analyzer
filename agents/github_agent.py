from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool
from dotenv import load_dotenv

load_dotenv()


def analyze_github(github_url: str, job_description: str):
    scrape_tool = ScrapeWebsiteTool()

    analyst = Agent(
        role="Technical Recruiter Analyst",
        goal="Evaluate candidate GitHub profiles against job descriptions to assess fit",
        backstory=(
            "You are a senior technical recruiter with deep software engineering knowledge. "
            "You evaluate candidates by examining their GitHub profiles — repositories, "
            "tech stack, contributions, and activity — and compare them against job requirements "
            "to determine how well a candidate matches a role."
        ),
        tools=[scrape_tool],
        verbose=True,
    )

    analysis_task = Task(
        description=(
            f"Analyze the GitHub profile at {github_url} and evaluate the candidate "
            f"against the following job description:\n\n"
            f"--- JOB DESCRIPTION ---\n{job_description}\n--- END ---\n\n"
            "Steps:\n"
            "1. Scrape the GitHub profile page\n"
            "2. Identify the candidate's tech stack, top repositories, and activity\n"
            "3. Compare their skills and experience against the job requirements\n"
            "4. Identify matching skills and skill gaps\n"
            "5. Provide a fit score (1-10) and a hiring recommendation\n"
        ),
        expected_output=(
            "A structured markdown report with these sections:\n"
            "- **Candidate Profile**: Name, GitHub stats, top repos\n"
            "- **Tech Stack**: Languages and technologies identified from repos\n"
            "- **Job Requirements Match**: For each requirement, state if the candidate meets it\n"
            "- **Matching Skills**: Skills that align with the job\n"
            "- **Skill Gaps**: Requirements the candidate does not appear to meet\n"
            "- **Fit Score**: X/10 with justification\n"
            "- **Recommendation**: Hire / Consider / Pass with reasoning\n"
        ),
        agent=analyst,
    )

    crew = Crew(
        agents=[analyst],
        tasks=[analysis_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("CANDIDATE FIT REPORT")
    print("=" * 60)
    print(result.raw)
    return result.raw
