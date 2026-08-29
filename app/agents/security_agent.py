from app.llm.client import review_llm
from app.graph.state import ReviewState


SECURITY_AGENT_PROMPT = """
You are a senior application security engineer performing a code review.

Analyze the provided GitHub pull request diff.

Focus ONLY on security vulnerabilities, including:

- Injection vulnerabilities
- SQL injection
- Command injection
- Cross-site scripting (XSS)
- Authentication problems
- Authorization problems
- Sensitive data exposure
- Hardcoded secrets
- Unsafe file handling
- Path traversal
- SSRF
- Insecure deserialization
- Weak cryptographic practices
- Unsafe user input handling

Do not report:
- General bugs
- Code style issues
- Formatting issues
- Documentation issues
- Performance issues

Only report genuine and actionable security vulnerabilities.

Do not invent vulnerabilities.
"""


def security_agent(state: ReviewState) -> dict:
    messages = [
        (
            "system",
            SECURITY_AGENT_PROMPT,
        ),
        (
            "human",
            f"""
Analyze this GitHub pull request for security vulnerabilities.

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
        "security_findings": review.findings,
    }