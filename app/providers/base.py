from dataclasses import dataclass
from typing import Any


@dataclass
class ChatRequest:
    messages: list[dict[str, Any]]
    model: str | None = None
    temperature: float = 0.0


class ProviderError(RuntimeError):
    """Raised when a provider cannot complete a request."""


class BaseChatProvider:
    name = "base"

    def chat(self, request: ChatRequest) -> str:
        raise NotImplementedError

