from app.core.intent_router import IntentRouter
from app.core.llm_router import LLMRouter
from app.core.planner import Planner
from app.memory.command_cache import CommandCache


class Jarvis:

    def __init__(self):

        self.intent_router = IntentRouter()

        self.llm_router = LLMRouter()

        self.planner = Planner()

        self.cache = CommandCache()

    def process(self, user_input):

        print("\n[STEP 1] Intent Router")

        matches = self.intent_router.detect_agents(
            user_input
        )

        # ==========================
        # SINGLE AGENT MATCH
        # ==========================

        if len(matches) == 1:

            agent_name = list(matches.keys())[0]

            print(
                f"[ROUTER] Direct Route → {agent_name}"
            )

            execution_plan = {
                "agents": [
                    {
                        "name": agent_name,
                        "task": user_input
                    }
                ]
            }

        # ==========================
        # MULTIPLE OR NO MATCH
        # ==========================

        else:

            if len(matches) > 1:

                print(
                    f"[ROUTER] Multiple Matches → {list(matches.keys())}"
                )

            else:

                print(
                    "[ROUTER] No Match Found"
                )

            # ==========================
            # CACHE LOOKUP
            # ==========================

            cached_plan = self.cache.get(
                user_input
            )

            if cached_plan:

                print(
                    "[CACHE] Hit"
                )

                execution_plan = cached_plan

            else:

                print(
                    "[CACHE] Miss"
                )

                # ==========================
                # LLM ROUTER
                # ==========================

                execution_plan = (
                    self.llm_router.create_execution_plan(
                        user_input
                    )
                )

                # ==========================
                # SAVE TO CACHE
                # ==========================

                self.cache.set(
                    user_input,
                    execution_plan
                )

                print(
                    "[CACHE] Plan Saved"
                )

        # ==========================
        # PLANNER
        # ==========================

        queue = self.planner.build_queue(
            execution_plan
        )

        # ==========================
        # OUTPUT
        # ==========================

        output = "\n[JARVIS]\n\n"

        output += "Execution Queue\n\n"

        for item in queue:

            output += (
                f"Step {item['step']}\n"
                f"Agent : {item['agent']}\n"
                f"Task  : {item['task']}\n\n"
            )

        return output

    def run(self):

        print("JARVIS Genesis ready.")
        print("Type 'exit' to quit.\n")

        while True:

            user_input = input("You: ").strip()

            if user_input.lower() in {"exit", "quit"}:
                break

            print()
            print(self.process(user_input))
            print()