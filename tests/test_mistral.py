from app.llm.client import llm


response = llm.invoke(
    "Explain in one sentence what a Python list is."
)

print(response.content)