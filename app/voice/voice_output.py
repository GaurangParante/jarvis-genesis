from __future__ import annotations

try:
    import pyttsx3
except ImportError:  # pragma: no cover - optional dependency
    pyttsx3 = None


class VoiceOutput:
    def __init__(self, enabled: bool = True, rate: int = 175, volume: float = 1.0):
        self.enabled = enabled and pyttsx3 is not None
        self.rate = rate
        self.volume = volume
        self._engine = None

        if self.enabled:
            try:
                self._engine = pyttsx3.init()
                self._engine.setProperty("rate", self.rate)
                self._engine.setProperty("volume", self.volume)
            except Exception:
                self.enabled = False
                self._engine = None

    def speak(self, text: str):
        if not self.enabled or not text.strip():
            return

        cleaned = self._clean_text(text)
        if not cleaned:
            return

        self._speak_blocking(cleaned)

    def _speak_blocking(self, text: str):
        if not self._engine:
            return

        for chunk in self._chunk_text(text, 220):
            self._engine.say(chunk)
        self._engine.runAndWait()

    def _chunk_text(self, text: str, size: int):
        words = text.split()
        chunk = []
        length = 0

        for word in words:
            next_length = length + len(word) + 1
            if chunk and next_length > size:
                yield " ".join(chunk)
                chunk = [word]
                length = len(word)
            else:
                chunk.append(word)
                length = next_length

        if chunk:
            yield " ".join(chunk)

    def _clean_text(self, text: str) -> str:
        replacements = {
            "[JARVIS]": "",
            "Execution Results": "",
            "Step   :": "",
            "Agent  :": "",
            "Status :": "",
            "Result :": "",
        }

        cleaned = text
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)

        lines = [line.strip() for line in cleaned.splitlines()]
        lines = [line for line in lines if line]
        return " ".join(lines)
