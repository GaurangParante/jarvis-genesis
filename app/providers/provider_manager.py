import json
import re

from app.core.config import DEFAULT_PROVIDER
from .base import ChatRequest, ProviderError
from .groq_provider import GroqProvider
from .nim_provider import NIMProvider


class ProviderManager:
    def __init__(self):
        self.providers = {}
        self.default_provider = DEFAULT_PROVIDER
        self._register_available_providers()

    def _register_available_providers(self):
        for provider_name, factory in (
            ("nim", NIMProvider),
            ("groq", GroqProvider),
        ):
            try:
                self.providers[provider_name] = factory()
            except ProviderError:
                continue

    def available(self):
        return list(self.providers.keys())

    def choose_provider(self, task_text: str, purpose: str = "general") -> str:
        text = task_text.lower().strip()

        high_frequency_terms = (
            "route", "plan", "json", "intent", "classify", "agent", "workflow"
        )
        heavy_reasoning_terms = (
            "refactor", "debug", "design", "analyze", "complex", "deep",
            "architecture", "write code", "generate code", "build system",
            "hard", "reason"
        )

        if purpose in {"routing", "planning", "classification"}:
            preferred = "nim"
        elif any(term in text for term in heavy_reasoning_terms):
            preferred = "groq"
        elif any(term in text for term in high_frequency_terms):
            preferred = "nim"
        else:
            preferred = self.default_provider or "nim"

        if preferred in self.providers:
            return preferred

        for fallback in ("nim", "groq"):
            if fallback in self.providers:
                return fallback

        raise ProviderError("No chat providers are configured.")

    def choose_order(self, task_text: str, purpose: str = "general"):
        primary = self.choose_provider(task_text, purpose)
        order = [primary]

        for candidate in ("nim", "groq"):
            if candidate not in order and candidate in self.providers:
                order.append(candidate)

        return order

    def chat(self, request: ChatRequest, task_text: str = "", purpose: str = "general") -> tuple[str, str]:
        errors = []

        for provider_name in self.choose_order(task_text, purpose):
            provider = self.providers.get(provider_name)
            if not provider:
                continue

            try:
                return provider_name, provider.chat(request)
            except ProviderError as exc:
                errors.append(f"{provider_name}: {exc}")

        raise ProviderError(" | ".join(errors) if errors else "No provider succeeded.")

    def chat_json(self, prompt: str, task_text: str = "", purpose: str = "planning") -> tuple[str, dict]:
        request_payload = ChatRequest(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        provider_name, content = self.chat(
            request_payload,
            task_text=task_text,
            purpose=purpose,
        )

        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise ProviderError(f"No JSON found in provider response: {content}")

        try:
            parsed = json.loads(match.group())
        except json.JSONDecodeError as exc:
            raise ProviderError(f"Invalid JSON from provider: {content}") from exc

        return provider_name, parsed
