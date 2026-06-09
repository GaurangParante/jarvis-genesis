import re

class IntentRouter:

    def __init__(self):

        self.intent_map = {

            "FORGE": [
                "code",
                "coding",
                "laravel",
                "python",
                "debug",
                "api",
                "function",
                "class",
                "project",
                "database",
                "migration",
            ],

            "ORBIT": [
                "open",
                "close",
                "launch",
                "folder",
                "application",
                "chrome",
                "browser",
                "vs code",
                "vscode",

                "search",
                "google",
                "youtube search",
                "youtube",
            ],

            "PHANTOM": [
                "research",
                "latest",
                "news",
                "trend",
                "analysis",
                "market",
                "competitor",
            ],

            "ARCHIVE": [
                "pdf",
                "docs",
                "notes",
                "knowledge",
            ],

            "TITAN": [
                "expense",
                "income",
                "budget",
                "tax",
                "finance",
                "money",
                "gpay",
            ],

            "ATHENA": [
                "gym",
                "workout",
                "fitness",
                "exercise",
                "diet",
                "sleep",
                "calories",
            ],

            "MERCURY": [
                "gmail",
                "email",
                "mail",
                "reply",
                "draft",
            ],

            "NOVA": [
                "linkedin",
                "instagram",
                "facebook",
                "twitter",
                "social",
                "post",
            ],

            "APOLLO": [
                "thumbnail",
                "video",
                "channel",
                "seo",
                "script",
            ],

            "SENTINEL": [
                "security",
                "password",
                "alert",
                "login",
                "cctv",
            ],
        }

    def route(self, user_input):

        result = self.detect_agents(user_input)

        return result

    def detect_agents(self, user_input):

        text = user_input.lower()

        scores = {}

        for agent, keywords in self.intent_map.items():

            score = 0
            matched_keywords = []

            for keyword in keywords:

                if re.search(
                    rf"\b{re.escape(keyword)}\b",
                    text
                ):
                    score += 1
                    matched_keywords.append(keyword)

            if score > 0:

                print(
                    f"{agent} -> {matched_keywords}"
                )

                scores[agent] = score

        return scores