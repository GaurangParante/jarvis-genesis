from dataclasses import dataclass


@dataclass
class SafetyDecision:
    requires_confirmation: bool
    reason: str = ""
    risk_level: str = "low"


class SafetyManager:
    sensitive_keywords = (
        "password",
        "login",
        "sign in",
        "signin",
        "account",
        "signup",
        "sign up",
        "register",
        "publish",
        "post",
        "upload",
        "send",
        "delete",
        "remove",
        "payment",
        "purchase",
        "otp",
        "2fa",
        "captcha",
    )

    def evaluate(self, agent: str, task: str, requires_confirmation: bool = False) -> SafetyDecision:
        text = task.lower().strip()

        if requires_confirmation:
            return SafetyDecision(
                requires_confirmation=True,
                reason="This workflow was marked as requiring user approval.",
                risk_level="medium",
            )

        if any(keyword in text for keyword in self.sensitive_keywords):
            return SafetyDecision(
                requires_confirmation=True,
                reason=f"Sensitive action detected for {agent}.",
                risk_level="high",
            )

        return SafetyDecision(
            requires_confirmation=False,
            reason="No sensitive action detected.",
            risk_level="low",
        )
