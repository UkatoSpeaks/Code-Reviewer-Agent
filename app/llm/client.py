from langchain_mistralai import ChatMistralAI

from app.config.settings import settings
from app.models.review import CodeReview


llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    api_key=settings.mistral_api_key,
)

review_llm = llm.with_structured_output(CodeReview)