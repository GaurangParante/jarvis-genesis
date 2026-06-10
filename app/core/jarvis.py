from app.core.intent_router import IntentRouter
from app.core.semantic_router import SemanticRouter
from app.core.llm_router import LLMRouter
from app.core.planner import Planner
from app.core.executor import Executor
from app.memory.command_cache import CommandCache


class Jarvis:

    def __init__(self):
        self.intent_router = IntentRouter()
        self.semantic_router = SemanticRouter()
        self.llm_router = LLMRouter()
        self.planner = Planner()
        self.executor = Executor()
        self.cache = CommandCache()

    def process(self, user_input):
        print("\n[STEP 1] Intent Router")
        
        # detect_agents ab strict rules par ya toh score dict dega ya fir None
        matches = self.intent_router.detect_agents(user_input)

        execution_plan = None

        # ==================================
        # SINGLE DIRECT MATCH (STRICT OVERRIDES)
        # ==================================
        if matches and len(matches) == 1:
            agent_name = list(matches.keys())[0]
            print(f"[ROUTER] Direct Route → {agent_name}")

            execution_plan = {
                "agents": [
                    {
                        "name": agent_name,
                        "task": user_input
                    }
                ]
            }

        # ==================================
        # MULTIPLE MATCHES OR NO STRIKT MATCH (FALLBACK TRIGGERED)
        # ==================================
        else:
            if matches and len(matches) > 1:
                print(f"[ROUTER] Multiple Matches → {list(matches.keys())}")
            else:
                print("[ROUTER] No Strict Match Found. Switching Pipeline...")

            # ==================================
            # CACHE CHECK
            # ==================================
            cached_plan = self.cache.get(user_input)

            if cached_plan:
                print("[CACHE] Hit")
                execution_plan = cached_plan
            else:
                print("[CACHE] Miss")

                # ==================================
                # SEMANTIC ROUTER (FAISS VECTOR SPACE)
                # ==================================
                semantic_result = self.semantic_router.detect_agent(user_input)

                if semantic_result and semantic_result.get("matched"):
                    print("[SEMANTIC ROUTER] Match Found")
                    execution_plan = {
                        "agents": [
                            {
                                "name": semantic_result["agent"],
                                "task": user_input
                            }
                        ]
                    }

                # ==================================
                # LLM ROUTER (FINAL FALLBACK)
                # ==================================
                else:
                    print("[SEMANTIC ROUTER] No Match")
                    execution_plan = self.llm_router.create_execution_plan(user_input)

                # Save the resolved plan to cache for future speedups
                self.cache.set(user_input, execution_plan)
                print("[CACHE] Plan Saved")

        # ==================================
        # PLANNER
        # ==================================
        queue = self.planner.build_queue(execution_plan)

        # ==================================
        # EXECUTOR
        # ==================================
        results = self.executor.execute(queue)

        # ==================================
        # OUTPUT FORMATTING
        # ==================================
        output = "\n[JARVIS]\n\n"
        output += "Execution Results\n\n"

        for item in results:
            output += (
                f"Step   : {item['step']}\n"
                f"Agent  : {item['agent']}\n"
                f"Status : {item['status']}\n"
                f"Result : {item['result']}\n\n"
            )

        return output

    def run(self):
        print("JARVIS Genesis ready.")
        print("Type 'exit' to quit.\n")

        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("\nJARVIS shutting down...")
                break

            print()
            result = self.process(user_input)
            print(result)