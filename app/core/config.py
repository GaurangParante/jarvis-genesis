from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

NIM_API_KEY = os.getenv("NIM_API_KEY")
NIM_BASE_URL = os.getenv(
    "NIM_BASE_URL",
    "https://integrate.api.nvidia.com/v1"
)
NIM_MODEL = os.getenv("NIM_MODEL", "meta/llama-3.1-70b-instruct")

DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "nim").strip().lower()
