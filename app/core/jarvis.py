from app.core.intent_router import IntentRouter


class Jarvis:
    def __init__(self):
        self.router = IntentRouter()

    def process(self, user_input: str) -> str:
        intent, agent = self.router.route(user_input)
        response = agent.handle()
        return (
            "[JARVIS]\n"
            f"Intent: {intent}\n\n"
            "Agent Selected:\n"
            f"{agent.name}\n\n"
            f"{agent.name}:\n"
            f"{response}"
        )

    def run(self):
        print("JARVIS Genesis ready. Type 'exit' to quit.")
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("JARVIS: Goodbye.")
                break

            print()
            print(self.process(user_input))
            print()
