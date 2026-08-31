def parse_pull_request(pull_request):
    files = []

    for file in pull_request.get_files():
        files.append(
            {
                "filename": file.filename,
                "status": file.status,
                "additions": file.additions,
                "deletions": file.deletions,
                "changes": file.changes,
                "patch": file.patch,
            }
        )

    return {
        "title": pull_request.title,
        "description": pull_request.body,
        "author": pull_request.user.login,
        "files": files,
        "commit_sha": pull_request.head.sha,
    }