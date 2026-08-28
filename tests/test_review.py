from app.github.client import get_pull_request
from app.github.parser import parse_pull_request
from app.llm.client import review_llm
from app.llm.prompts import SYSTEM_PROMPT


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


messages = [
    (
        "system",
        SYSTEM_PROMPT,
    ),
    (
        "human",
        f"""
Review the following GitHub pull request.

Title:
{pr_data["title"]}

Description:
{pr_data["description"]}

Changed code:

{diff}
""",
    ),
]


review = review_llm.invoke(messages)


print("\n========== SUMMARY ==========\n")
print(review.summary)

print("\n========== FINDINGS ==========\n")

if not review.findings:
    print("No issues found.")

for finding in review.findings:
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