from typing import TypedDict

from app.models.review import ReviewFinding


class ReviewState(TypedDict):
    # GitHub PR information
    owner: str
    repo: str
    pull_number: int

    title: str
    description: str
    diff: str

    # Agent findings
    bug_findings: list[ReviewFinding]
    security_findings: list[ReviewFinding]
    quality_findings: list[ReviewFinding]

    # Final result
    final_summary: str
    final_findings: list[ReviewFinding]