import json
from urllib import error, request

from app.core.config import NIM_API_KEY, NIM_BASE_URL, NIM_MODEL
from .base import BaseChatProvider, ChatRequest, ProviderError


class NIMProvider(BaseChatProvider):
    name = "nim"

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        default_model: str | None = None,
    ):
        api_key = api_key or NIM_API_KEY
        if not api_key:
            raise ProviderError("NIM_API_KEY is not configured.")

        self.api_key = api_key
        self.base_url = (base_url or NIM_BASE_URL).rstrip("/")
        self.default_model = default_model or NIM_MODEL

    def chat(self, request_payload: ChatRequest) -> str:
        model = request_payload.model or self.default_model
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": model,
            "messages": request_payload.messages,
            "temperature": request_payload.temperature,
        }

        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=data,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

        try:
            with request.urlopen(req, timeout=60) as response:
                raw = response.read().decode("utf-8")
        except error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="ignore")
            raise ProviderError(
                f"NIM request failed with HTTP {exc.code}: {details}"
            ) from exc
        except error.URLError as exc:
            raise ProviderError(f"NIM request failed: {exc.reason}") from exc

        try:
            content = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ProviderError(f"NIM returned invalid JSON: {raw}") from exc

        try:
            message = content["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError(f"NIM response missing content: {content}") from exc

        if not message:
            raise ProviderError("NIM returned an empty response.")

        return str(message).strip()

