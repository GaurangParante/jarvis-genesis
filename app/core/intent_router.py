from app.agents.apollo import ApolloAgent
from app.agents.archive import ArchiveAgent
from app.agents.athena import AthenaAgent
from app.agents.forge import ForgeAgent
from app.agents.mercury import MercuryAgent
from app.agents.nova import NovaAgent
from app.agents.orbit import OrbitAgent
from app.agents.phantom import PhantomAgent
from app.agents.sentinel import SentinelAgent
from app.agents.titan import TitanAgent


class IntentRouter:
    def __init__(self):
        self.agent_map = {
            "coding": ForgeAgent(),
            "automation": OrbitAgent(),
            "research": PhantomAgent(),
            "knowledge": ArchiveAgent(),
            "documents": ArchiveAgent(),
            "finance": TitanAgent(),
            "fitness": AthenaAgent(),
            "email": MercuryAgent(),
            "social_media": NovaAgent(),
            "youtube": ApolloAgent(),
            "security": SentinelAgent(),
            "general": ForgeAgent(),
        }
        self.intent_keywords = {
            "coding": (
                "code",
                "coding",
                "laravel",
                "vs code",
                "vscode",
                "debug",
                "git",
                "project",
                "program",
                "module",
                "auth",
            ),
            "automation": (
                "chrome",
                "browser",
                "folder",
                "file",
                "script",
                "automation",
                "launch",
            ),
            "research": (
                "research",
                "latest",
                "news",
                "trend",
                "market",
                "analysis",
            ),
            "knowledge": (
                "note",
                "notes",
                "document",
                "docs",
                "knowledge",
            ),
            "documents": (
                "pdf",
                "document",
                "file",
            ),
            "finance": (
                "budget",
                "spending",
                "expense",
                "income",
                "tax",
                "gpay",
            ),
            "fitness": (
                "workout",
                "calorie",
                "diet",
                "gym",
                "sleep",
                "fitness",
            ),
            "email": (
                "email",
                "gmail",
                "mail",
                "draft",
                "reply",
            ),
            "social_media": (
                "linkedin",
                "instagram",
                "facebook",
                "twitter",
                "x ",
                "post",
                "social",
            ),
            "youtube": (
                "youtube",
                "video",
                "thumbnail",
                "seo",
                "upload",
                "script",
            ),
            "security": (
                "security",
                "cctv",
                "password",
                "alert",
                "suspicious",
                "login",
            ),
        }

    def detect_intent(self, user_input: str) -> str:
        text = user_input.lower()

        for intent, keywords in self.intent_keywords.items():
            if any(keyword in text for keyword in keywords):
                return intent

        return "general"

    def select_agent(self, intent: str):
        return self.agent_map.get(intent, self.agent_map["general"])

    def route(self, user_input: str):
        intent = self.detect_intent(user_input)
        return intent, self.select_agent(intent)
