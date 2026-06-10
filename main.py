import os
from dotenv import load_dotenv

# 1. Load variables from .env file
load_dotenv()

# 2. Extract and strictly bind to OS environment for Hugging Face Hub
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    os.environ["HF_TOKEN"] = hf_token
    # Optional: system crash errors bypass karne ke liye symbols cache bhi optimize kar sakte ho
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from app.core.jarvis import Jarvis


def main():
    Jarvis().run()


if __name__ == "__main__":
    main()
