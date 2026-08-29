from app.llm.client import review_llm
from app.graph.state import ReviewState


AGGREGATOR_PROMPT = """
You are the lead code reviewer.

Combine the findings from specialized reviewers into one final review.

Rules:
- Remove duplicate findings.
- Ignore weak or invalid findings.
- Preserve only actionable issues.
- Keep severity accurate.
- Do not invent new issues.
- Provide a concise overall summary.
"""


def aggregator_agent(state: ReviewState) -> dict:
    all_findings = (
        state["bug_findings"]
        + state["security_findings"]
        + state["quality_findings"]
    )

    findings_text = "\n\n".join(
        str(finding.model_dump())
        for finding in all_findings
    )

    messages = [
        ("system", AGGREGATOR_PROMPT),
        (
            "human",
            f"""
Pull request:

Title:
{state["title"]}

Description:
{state["description"]}

Specialist findings:

{findings_text}
""",
        ),
    ]

    review = review_llm.invoke(messages)

    return {
        "final_summary": review.summary,
        "final_findings": review.findings,
    }