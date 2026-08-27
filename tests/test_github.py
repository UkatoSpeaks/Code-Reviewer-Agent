from app.github.client import get_pull_request
from app.github.parser import parse_pull_request


OWNER = "pallets"
REPO = "flask"
PULL_NUMBER = 1234


pull_request = get_pull_request(
    OWNER,
    REPO,
    PULL_NUMBER,
)

result = parse_pull_request(pull_request)

print("Title:", result["title"])
print("Author:", result["author"])
print("Files changed:", len(result["files"]))

for file in result["files"]:
    print("\nFile:", file["filename"])
    print("Status:", file["status"])
    print("Changes:", file["changes"])