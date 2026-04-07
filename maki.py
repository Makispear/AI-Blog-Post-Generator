import os
import sys

from crewai import Agent, Crew, Process, Task

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_TOPIC = "AI in healthcare in 2026"


def load_environment() -> None:
    if os.getenv("OPENAI_API_KEY"):
        return

    if load_dotenv is not None:
        load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY is not set. In production, configure it as an environment variable "
            "or secret. For local development, add it to .env and install python-dotenv."
        )


def generate_blog_post(topic: str = DEFAULT_TOPIC, verbose: bool = True) -> str:
    load_environment()

    researcher = Agent(
        role="Senior Researcher Analyst",
        backstory="An expert analyst with a knack for finding hidden gems in data.",
        goal=f"Discover key trends in {topic}",
    )

    writer = Agent(
        role="Tech Content Strategist",
        backstory="A skilled writer who can distill complex topics into clear narratives.",
        goal="Create compelling content on technical advancements",
    )

    research_task = Task(
        description=f"Identify key trends in the use of {topic}.",
        agent=researcher,
        expected_output=(
            "A detailed summary highlighting the top 3 AI advancements, including their "
            "significance, impact, and potential future implications."
        ),
    )

    write_task = Task(
        description="Compose a 3-paragraph blog post summarizing the key trends found.",
        agent=writer,
        expected_output=(
            "A well-structured, engaging 3-paragraph blog post tailored for a general audience."
        ),
    )

    research_crew = Crew(
        name="ResearchCrew",
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=verbose,
    )

    return str(research_crew.kickoff())


if __name__ == "__main__":
    print(generate_blog_post())