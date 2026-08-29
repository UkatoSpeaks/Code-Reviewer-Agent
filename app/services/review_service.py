from app.github.client import get_pull_request
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

    return graph.invoke(initial_state)