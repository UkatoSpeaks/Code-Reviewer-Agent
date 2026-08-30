import hashlib
import hmac

from fastapi import APIRouter, Header, HTTPException, Request

from app.config.settings import settings
from app.services.review_service import review_pull_request


router = APIRouter()


def verify_signature(
    body: bytes,
    signature: str | None,
) -> bool:
    if not signature:
        return False

    expected = hmac.new(
        settings.github_webhook_secret.encode(),
        body,
        hashlib.sha256,
    ).hexdigest()

    expected_signature = f"sha256={expected}"

    return hmac.compare_digest(
        expected_signature,
        signature,
    )


@router.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_github_event: str | None = Header(default=None),
    x_hub_signature_256: str | None = Header(default=None),
):
    body = await request.body()

    if not verify_signature(
        body,
        x_hub_signature_256,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature",
        )

    payload = await request.json()

    if x_github_event != "pull_request":
        return {
            "status": "ignored",
            "reason": "Not a pull request event",
        }

    action = payload.get("action")

    if action not in {
        "opened",
        "synchronize",
        "reopened",
    }:
        return {
            "status": "ignored",
            "reason": f"Unsupported action: {action}",
        }

    repository = payload["repository"]
    pull_request = payload["pull_request"]

    owner = repository["owner"]["login"]
    repo = repository["name"]
    pull_number = pull_request["number"]

    result = review_pull_request(
        owner,
        repo,
        pull_number,
    )

    return {
        "status": "completed",
        "summary": result["final_summary"],
        "findings": [
            finding.model_dump()
            for finding in result["final_findings"]
        ],
    }