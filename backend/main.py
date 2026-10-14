import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(f"OPENAI_API_KEY is missing from {ENV_FILE}")

client = OpenAI(api_key=api_key)

app = FastAPI(title="A - Personal AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "name": "A",
        "status": "online",
        "message": "A is alive."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/chat")
def chat(data: dict):
    message = data.get("message", "").strip()

    if not message:
        return {
            "reply": "I didn't receive a message."
        }

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=(
            "You are A, a helpful personal AI assistant. "
            "Be concise, friendly, and practical."
        ),
        input=message
    )

    return {
        "reply": response.output_text
    }