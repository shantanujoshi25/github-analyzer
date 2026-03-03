from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from agents.github_graphql_tool import GitHubGraphQLTool

load_dotenv()


def analyze_github(github_url: str, job_description: str, leetcode_data: str = None):
    # Extract username from URL (e.g. "https://github.com/torvalds" -> "torvalds")
    username = github_url.rstrip("/").split("/")[-1]

    github_tool = GitHubGraphQLTool()

    backstory = (
        "You are a senior technical recruiter with deep software engineering knowledge. "
        "You evaluate candidates by examining their GitHub profiles — repositories, "
        "tech stack, contributions, and activity — and compare them against job requirements "
        "to determine how well a candidate matches a role."
    )
    if leetcode_data:
        backstory += (
            " You also evaluate candidates' LeetCode profiles — problem-solving stats, "
            "contest ratings, and language proficiency — to assess their algorithmic skills."
        )

    analyst = Agent(
        role="Technical Recruiter Analyst",
        goal="Evaluate candidate GitHub profiles against job descriptions to assess fit",
        backstory=backstory,
        tools=[github_tool],
        verbose=True,
    )

    task_description = (
        f"Use the GitHub GraphQL API tool to fetch the profile data for username '{username}'. "
        f"Then evaluate the candidate against the following job description:\n\n"
        f"--- JOB DESCRIPTION ---\n{job_description}\n--- END ---\n\n"
    )

    if leetcode_data:
        task_description += (
            f"The candidate also has a LeetCode profile. Here is their LeetCode data:\n\n"
            f"--- LEETCODE PROFILE ---\n{leetcode_data}\n--- END ---\n\n"
        )

    task_description += (
        "Steps:\n"
        f"1. Call the GitHub GraphQL API tool with username '{username}'\n"
        "2. Analyze the candidate's tech stack, top repositories, and contribution activity\n"
        "3. Compare their skills and experience against the job requirements\n"
        "4. Identify matching skills and skill gaps\n"
    )

    if leetcode_data:
        task_description += (
            "5. Evaluate the candidate's LeetCode performance — problem-solving breadth, "
            "difficulty distribution, contest rating, and language preferences\n"
            "6. Provide a fit score (1-10) and a hiring recommendation\n"
        )
    else:
        task_description += "5. Provide a fit score (1-10) and a hiring recommendation\n"

    expected_output = (
        "A structured markdown report with these sections:\n"
        "- **Candidate Profile**: Name, GitHub stats, top repos\n"
        "- **Tech Stack**: Languages and technologies identified from repos\n"
        "- **Job Requirements Match**: For each requirement, state if the candidate meets it\n"
        "- **Matching Skills**: Skills that align with the job\n"
        "- **Skill Gaps**: Requirements the candidate does not appear to meet\n"
    )

    if leetcode_data:
        expected_output += (
            "- **LeetCode Analysis**: Problems solved by difficulty, contest rating, "
            "language stats, and what this reveals about algorithmic ability\n"
        )

    expected_output += (
        "- **Fit Score**: X/10 with justification\n"
        "- **Recommendation**: Hire / Consider / Pass with reasoning\n"
    )

    analysis_task = Task(
        description=task_description,
        expected_output=expected_output,
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
    print("CANDIDATE FIT REPORT (GraphQL)")
    print("=" * 60)
    print(result.raw)
    return result.raw
