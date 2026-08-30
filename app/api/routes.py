from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from app.services.review_service import review_pull_request


router = APIRouter()


class ReviewRequest(BaseModel):
    url: HttpUrl


@router.post("/review")
def review(request: ReviewRequest):
    url = str(request.url)

    parts = url.rstrip("/").split("/")

    if len(parts) < 5 or parts[-2] != "pull":
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub pull request URL",
        )

    owner = parts[-4]
    repo = parts[-3]
    pull_number = int(parts[-1])

    result = review_pull_request(
        owner,
        repo,
        pull_number,
    )

    return {
        "summary": result["final_summary"],
        "findings": [
            finding.model_dump()
            for finding in result["final_findings"]
        ],
    }