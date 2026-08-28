from pydantic import BaseModel, Field


class ReviewFinding(BaseModel):
    severity: str = Field(
        description="Severity of the issue: critical, high, medium, low"
    )

    file: str = Field(
        description="File where the issue was found"
    )

    line: int | None = Field(
        default=None,
        description="Line number if identifiable"
    )

    issue: str = Field(
        description="Short description of the issue"
    )

    explanation: str = Field(
        description="Detailed explanation of why this is a problem"
    )

    suggestion: str = Field(
        description="Suggested fix"
    )


class CodeReview(BaseModel):
    summary: str
    findings: list[ReviewFinding]