from fastapi import FastAPI

from app.api.routes import router
from app.api.webhook import router as webhook_router


app = FastAPI(
    title="Code Reviewer Agent",
    version="1.0.0",
)

app.include_router(router)
app.include_router(webhook_router)