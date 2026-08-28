from app.llm.client import review_llm
from app.llm.prompts import SYSTEM_PROMPT
from app.graph.state import ReviewState


BUG_AGENT_PROMPT = """
You are a software engineer specializing in finding bugs.

Analyze the provided GitHub pull request diff.

Focus ONLY on:
- Incorrect logic
- Runtime errors
- Edge cases
- Incorrect assumptions
- Broken functionality
- Potential regressions

Do not report:
- Security issues
- Style issues
- Formatting issues
- Documentation issues

Only report genuine and actionable bugs.
"""


def bug_agent(state: ReviewState) -> dict:
    messages = [
        (
            "system",
            BUG_AGENT_PROMPT,
        ),
        (
            "human",
            f"""
Review this GitHub pull request for bugs.

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
        "bug_findings": review.findings,
    }