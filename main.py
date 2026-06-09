from app.core.jarvis import Jarvis
import os
import warnings

# Hugging Face warning aur dusre cleanups ke liye
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore", category=UserWarning, module="huggingface_hub")


def main():
    Jarvis().run()


if __name__ == "__main__":
    main()
