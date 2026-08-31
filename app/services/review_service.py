from app.github.client import (
    get_pull_request,
    post_pull_request_review,
)
from app.github.parser import parse_pull_request
from app.graph.workflow import build_review_graph


def build_diff(files: list[dict]) -> str:
    diff = ""

    for file in files:
        if file.get("patch"):
            diff += f"""
File: {file["filename"]}
Status: {file["status"]}

Patch:
{file["patch"]}

--------------------------------
"""

    return diff


def build_review_body(result: dict) -> str:
    body = f"""## Code Review

### Summary

{result["final_summary"]}

### Findings

"""

    if not result["final_findings"]:
        body += "No issues found.\n"
        return body

    for finding in result["final_findings"]:
        body += f"""#### {finding.severity.upper()}

**File:** `{finding.file}`  
**Line:** {finding.line if finding.line else "N/A"}

**Issue:** {finding.issue}

**Explanation:**  
{finding.explanation}

**Suggestion:**  
{finding.suggestion}

---

"""

    return body


def review_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
):
    pull_request = get_pull_request(
        owner,
        repo,
        pull_number,
    )

    pr_data = parse_pull_request(pull_request)

    diff = build_diff(pr_data["files"])

    initial_state = {
        "owner": owner,
        "repo": repo,
        "pull_number": pull_number,
        "title": pr_data["title"],
        "description": pr_data["description"],
        "diff": diff,
        "bug_findings": [],
        "security_findings": [],
        "quality_findings": [],
        "final_summary": "",
        "final_findings": [],
    }

    graph = build_review_graph()

    result = graph.invoke(initial_state)

    review_body = build_review_body(result)

    post_pull_request_review(
        owner=owner,
        repo=repo,
        pull_number=pull_number,
        body=review_body,
    )

    return result