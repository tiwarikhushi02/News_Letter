from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

model = init_chat_model(
    model="gemini-3-flash",
    model_provider="google-genai",
    api_key=GOOGLE_API_KEY
)