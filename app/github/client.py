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