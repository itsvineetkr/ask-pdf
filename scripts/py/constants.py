import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

API_URL_WHISPER = (
    "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo"
)

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
