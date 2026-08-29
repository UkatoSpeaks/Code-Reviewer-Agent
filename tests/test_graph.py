from app.github.client import get_pull_request
from app.github.parser import parse_pull_request
from app.graph.workflow import build_review_graph


OWNER = "pallets"
REPO = "flask"
PULL_NUMBER = 1234


pull_request = get_pull_request(
    OWNER,
    REPO,
    PULL_NUMBER,
)

pr_data = parse_pull_request(pull_request)


diff = ""

for file in pr_data["files"]:
    if file["patch"]:
        diff += f"""
File: {file["filename"]}
Status: {file["status"]}

Patch:
{file["patch"]}

--------------------------------
"""


initial_state = {
    "owner": OWNER,
    "repo": REPO,
    "pull_number": PULL_NUMBER,

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


print("\n========== BUG FINDINGS ==========\n")

for finding in result["bug_findings"]:
    print(f"""
Severity: {finding.severity}
File: {finding.file}
Line: {finding.line}
Issue: {finding.issue}

Explanation:
{finding.explanation}

Suggestion:
{finding.suggestion}

--------------------------------
""")

print("\n========== GRAPH RESULT ==========\n")

print(
    "Bug findings:",
    len(result["bug_findings"])
)

print(
    "Security findings:",
    len(result["security_findings"])
)


print("\n========== SECURITY FINDINGS ==========\n")

for finding in result["security_findings"]:
    print(f"""
Severity: {finding.severity}
File: {finding.file}
Line: {finding.line}
Issue: {finding.issue}

Explanation:
{finding.explanation}

Suggestion:
{finding.suggestion}

--------------------------------
""")