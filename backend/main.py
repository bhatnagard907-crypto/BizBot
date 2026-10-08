from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

app = FastAPI(title="FAQ Chatbot API")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"


def get_business_name() -> str:
    return os.getenv("BUSINESS_NAME") or "your business"


def get_mock_faqs() -> dict[str, str]:
    business_name = get_business_name()
    return {
        "what is your return policy": "You can return items within 30 days of purchase for a full refund.",
        "how do I contact support": f"Email us at support@{business_name}.com or call 1-800-555-0123.",
        "what are your business hours": "We're open Monday-Friday 9am-6pm EST.",
        "do you offer international shipping": "Yes, we ship to over 50 countries worldwide.",
        "how can I track my order": "Log into your account and go to 'My Orders' to see tracking info.",
    }


class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "qwen/qwen3.8-27b"

class ChatResponse(BaseModel):
    response: str
    source: str

def get_mock_response(message: str) -> str:
    message_lower = message.lower().strip()
    mock_faqs = get_mock_faqs()
    for question, answer in mock_faqs.items():
        if question in message_lower or message_lower in question:
            return answer
    q_words = set(message_lower.split())
    for question, answer in mock_faqs.items():
        question_words = set(question.split())
        common = q_words & question_words
        if len(common) >= 3 or (len(common) >= 2 and len(question_words) <= 5):
            return answer
    return "I don't have an answer for that. Please contact support for more help."

async def get_groq_response(message: str, model: str) -> str:
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Groq API key not configured")
    client = Groq(api_key=GROQ_API_KEY)
    business_name = get_business_name()
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a helpful FAQ assistant.Fetch the details of frequently asked customer questions the website of {business_name} and answer questions concisely as per user request. If the query is about any other business than the name provided, kindly tell the user that the bot is only used for the FAQs of {business_name}"
                ),
            },
            {"role": "user", "content": message}
        ],
        model=model,
        temperature=0.3,
        max_tokens=500,
    )
    return completion.choices[0].message.content

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if USE_MOCK:
        response = get_mock_response(request.message)
        source = "mock"
    else:
        response = await get_groq_response(request.message, request.model)
        source = "groq"
    return ChatResponse(response=response, source=source)

@app.get("/health")
async def health():
    return {"status": "healthy", "mode": "mock" if USE_MOCK else "groq", "use_mock_env": os.getenv("USE_MOCK"), "groq_key_set": bool(GROQ_API_KEY)}

@app.get("/debug")
async def debug():
    return {"USE_MOCK": USE_MOCK, "GROQ_API_KEY": GROQ_API_KEY, "env_USE_MOCK": os.getenv("USE_MOCK")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)