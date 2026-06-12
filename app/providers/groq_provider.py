from app.core.config import GROQ_API_KEY, GROQ_MODEL
from .base import BaseChatProvider, ChatRequest, ProviderError


class GroqProvider(BaseChatProvider):
    name = "groq"

    def __init__(self, api_key: str | None = None, default_model: str | None = None):
        api_key = api_key or GROQ_API_KEY
        if not api_key:
            raise ProviderError("GROQ_API_KEY is not configured.")

        try:
            from groq import Groq
        except ImportError as exc:
            raise ProviderError("groq package is not installed.") from exc

        self.client = Groq(api_key=api_key)
        self.default_model = default_model or GROQ_MODEL

    def chat(self, request: ChatRequest) -> str:
        model = request.model or self.default_model

        response = self.client.chat.completions.create(
            model=model,
            messages=request.messages,
            temperature=request.temperature,
        )

        content = response.choices[0].message.content
        if not content:
            raise ProviderError("Groq returned an empty response.")

        return content.strip()
