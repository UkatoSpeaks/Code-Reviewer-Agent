from app.services.review_service import review_pull_request


OWNER = "pallets"
REPO = "flask"
PULL_NUMBER = 1234


result = review_pull_request(
    OWNER,
    REPO,
    PULL_NUMBER,
)


print("\n========== AGENT RESULTS ==========\n")

print("Bug findings:", len(result["bug_findings"]))
print("Security findings:", len(result["security_findings"]))
print("Quality findings:", len(result["quality_findings"]))


print("\n========== FINAL REVIEW ==========\n")

print("Summary:")
print(result["final_summary"])


print("\nFindings:")

if not result["final_findings"]:
    print("No issues found.")

for finding in result["final_findings"]:
    print(
        f"""
Severity: {finding.severity}
File: {finding.file}
Line: {finding.line}
Issue: {finding.issue}

Explanation:
{finding.explanation}

Suggestion:
{finding.suggestion}

--------------------------------
"""
    )