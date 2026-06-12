from dataclasses import dataclass, field


@dataclass
class TaskProfile:
    intent: str
    confidence: float
    signals: list[str] = field(default_factory=list)
    needs_clarification: bool = False


class TaskClassifier:
    def classify(self, user_input: str) -> TaskProfile:
        text = user_input.lower().strip()
        signals = []

        joke_cues = ("joke", "funny", "laugh", "sunao", "sunao", "mazaak", "mazak", "hansao", "hansaoo")
        research_cues = ("research", "analyze", "analysis", "compare", "trend", "latest", "news", "find", "deep")

        if any(cue in text for cue in joke_cues) and not any(cue in text for cue in research_cues):
            return TaskProfile(
                intent="joke",
                confidence=0.95,
                signals=["joke"],
                needs_clarification=False,
            )

        intent_map = {
            "joke": ["joke", "make me laugh", "funny", "roast me", "say something funny", "tell me a joke"],
            "chat": ["hello", "hi ", "hey ", "how are you", "who are you", "what can you do"],
            "coding": ["code", "bug", "fix", "script", "api", "project", "debug", "refactor"],
            "automation": ["open ", "launch ", "start ", "screenshot", "record", "capture", "browser"],
            "research": ["research", "analyze", "compare", "trend", "latest", "find"],
            "youtube": ["youtube", "thumbnail", "seo", "video", "channel"],
            "social": ["instagram", "linkedin", "facebook", "twitter", "x ", "post", "caption"],
            "email": ["email", "mail", "inbox", "reply", "draft"],
            "security": ["password", "login", "security", "2fa", "otp", "alert"],
            "account_setup": ["account", "signup", "sign up", "register", "profile creation"],
            "finance": ["expense", "budget", "money", "finance", "spend"],
            "fitness": ["workout", "diet", "calorie", "gym", "fitness"],
        }

        for intent, keywords in intent_map.items():
            if any(keyword in text for keyword in keywords):
                signals.append(intent)

        if not signals:
            return TaskProfile(
                intent="general",
                confidence=0.35,
                needs_clarification=True,
            )

        if "joke" in signals and len(signals) == 1:
            return TaskProfile(
                intent="joke",
                confidence=0.9,
                signals=signals,
                needs_clarification=False,
            )

        primary = signals[0] if len(signals) == 1 else "multi_step"
        confidence = 0.72 if len(signals) == 1 else 0.86

        if len(signals) > 1:
            confidence = min(0.92, confidence + 0.08)

        needs_clarification = confidence < 0.75

        return TaskProfile(
            intent=primary,
            confidence=confidence,
            signals=signals,
            needs_clarification=needs_clarification,
        )
