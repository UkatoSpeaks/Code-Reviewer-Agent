from github import Github

from app.config.settings import settings


github = Github(settings.github_token)


def get_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
):
    repository = github.get_repo(f"{owner}/{repo}")
    pull_request = repository.get_pull(pull_number)

    return pull_request


def post_pull_request_review(
    owner: str,
    repo: str,
    pull_number: int,
    body: str,
):
    repository = github.get_repo(f"{owner}/{repo}")
    pull_request = repository.get_pull(pull_number)

    review = pull_request.create_review(
        body=body,
        event="COMMENT",
    )

    return review


def post_inline_review(
    owner: str,
    repo: str,
    pull_number: int,
    body: str,
    commit_id: str,
    path: str,
    line: int,
):
    repository = github.get_repo(f"{owner}/{repo}")
    pull_request = repository.get_pull(pull_number)

    commit = repository.get_commit(commit_id)

    review = pull_request.create_review(
        body=body,
        event="COMMENT",
        commit=commit,
        comments=[
            {
                "path": path,
                "line": line,
                "side": "RIGHT",
                "body": body,
            }
        ],
    )

    return review