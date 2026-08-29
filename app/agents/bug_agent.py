from app.llm.client import review_llm
from app.llm.prompts import SYSTEM_PROMPT
from app.graph.state import ReviewState



BUG_AGENT_PROMPT = """
You are a senior software engineer specializing in detecting
real software bugs.

Analyze ONLY the actual code changes in the pull request.

A bug is a change that can cause:
- Incorrect program behavior
- Runtime errors
- Incorrect output
- Data corruption or loss
- Broken edge cases
- Regressions in existing functionality
- Incorrect state transitions
- Broken API behavior

IMPORTANT RULES:

1. Do NOT report documentation changes as bugs.
2. Do NOT report grammar or spelling corrections.
3. Do NOT report capitalization changes.
4. Do NOT report formatting changes.
5. Do NOT report comments or documentation-only changes.
6. Do NOT report subjective coding preferences.
7. If the changed file contains only documentation, return NO findings.
8. Only report a bug when you can explain a concrete way the
   software behavior could be incorrect.

For every genuine bug:
- Identify the file
- Identify the line if possible
- Explain the actual failure
- Explain why it happens
- Suggest a concrete fix

If there are no genuine bugs, return an empty findings list.

Never invent bugs.
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