import re

class IntentRouter:

    def __init__(self):
        # Variable ka naam strictly 'strict_overrides' rakha hai taaki loop crash na ho.
        # Saare generic single-words ko saaf karke strictly multi-word phrases bana diye hain.
        self.strict_overrides = {
            "FORGE": [
                "laravel migration", "laravel project", "fastapi project", 
                "mysql table", "git commit", "git push"
            ],
            "ORBIT": [
                "take screenshot", "capture webcam", "record screen", "take selfie"
            ],
            "PHANTOM": [
                "market analysis", "competitor research", "latest trend news"
            ],
            "ARCHIVE": [
                "knowledge base", "pdf document", "secure notes"
            ],
            "TITAN": [
                "expense tracker", "budget tax", "gpay history", "finance money"
            ],
            "ATHENA": [
                "workout routine", "gym diet", "calorie tracker"
            ],
            "MERCURY": [
                "gmail draft", "send email", "reply mail"
            ],
            "NOVA": [
                "linkedin post", "instagram story", "facebook page", "twitter tweet"
            ],
            "APOLLO": [
                "youtube seo", "youtube analytics", "channel optimization"
            ],
            "SENTINEL": [
                "password alert", "security login", "cctv footage"
            ]
        }

    def route(self, user_input):
        """
        Main routing function. 
        Agar strict pattern match nahi hota, toh yeh None return karega 
        taaki system automatic FAISS Semantic Search par switch ho sake.
        """
        return self.detect_agents(user_input)

    def detect_agents(self, user_input):
        text = user_input.lower().strip()
        scores = {}

        # 1. High Priority Code/File Extension Rule (Direct Route to FORGE)
        if re.search(r'\b\w+\.(py|js|php|html|css|json|sh|txt|csv)\b', text):
            print("[ROUTER] File extension detected -> Prioritizing FORGE")
            scores["FORGE"] = 5
            return scores

        # 2. Strict Phrase Matching (Using the correct 'strict_overrides' variable)
        for agent, phrases in self.strict_overrides.items():
            for phrase in phrases:
                if phrase in text:
                    print(f"[ROUTER] Strict phrase match found: '{phrase}' -> {agent}")
                    scores[agent] = 4
                    return scores

        # 3. Fallback: Agar kuch bhi match nahi hua, toh None return karo.
        # Isse aapka Jarvis fallback karke Semantic Router (FAISS) chalayega.
        return None