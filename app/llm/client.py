from langchain_mistralai import  ChatMistralAI
from app.config.settings import settings


llm=ChatMistralAI(
    model="mistral-small-2506",
    temperature=0,
    api_key=settings.mistral_api_key
)