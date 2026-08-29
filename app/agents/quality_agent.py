from app.llm.client import review_llm
from app.graph.state import ReviewState


QUALITY_AGENT_PROMPT = """
You are a senior software engineer specializing in code quality
and maintainability.

Analyze the provided GitHub pull request diff.

Focus ONLY on:

- Poor code structure
- Maintainability problems
- Excessive duplication
- Poor naming
- Unnecessary complexity
- Bad abstractions
- Poor separation of concerns
- Difficult-to-test code
- Error handling quality
- Performance problems caused by poor implementation choices

Do not report:

- Security vulnerabilities
- General bugs
- Documentation typos
- Formatting issues
- Minor stylistic preferences

Only report issues that meaningfully affect code quality,
maintainability, or performance.

Do not invent issues.
Every finding must be actionable.
"""


def quality_agent(state: ReviewState) -> dict:
    messages = [
        (
            "system",
            QUALITY_AGENT_PROMPT,
        ),
        (
            "human",
            f"""
Analyze this GitHub pull request for code quality
and maintainability problems.

Title:
{state["title"]}

Description:
{state["description"]}

Changed code:

{state["diff"]}
""",
        ),
    ]

    review = review_llm.invoke(messages)

    return {
        "quality_findings": review.findings,
    }