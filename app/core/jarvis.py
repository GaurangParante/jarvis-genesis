from app.core.intent_router import IntentRouter
from app.core.semantic_router import SemanticRouter
from app.core.llm_router import LLMRouter
from app.core.planner import Planner
from app.core.executor import Executor
from app.core.task_classifier import TaskClassifier
from app.core.workflow_planner import WorkflowPlanner
from app.memory.command_cache import CommandCache
from app.voice.voice_output import VoiceOutput


class Jarvis:
    def __init__(self):
        self.intent_router = IntentRouter()
        self.semantic_router = SemanticRouter()
        self.llm_router = LLMRouter()
        self.planner = Planner()
        self.executor = Executor()
        self.cache = CommandCache()
        self.classifier = TaskClassifier()
        self.workflow_planner = WorkflowPlanner()
        self.voice = VoiceOutput(enabled=True)
        self.last_intent = None
        self.last_response_text = ""

    def _apply_followup_context(self, user_input: str, profile):
        text = user_input.lower().strip()
        followup_cues = ("aur ek", "or ek", "ek aur", "another one", "one more", "phir se", "again", "ek aur sunao")

        if any(cue in text for cue in followup_cues) and self.last_intent in {"joke", "chat"}:
            profile.intent = "joke"
            profile.confidence = 0.98
            profile.signals = ["joke"]
            profile.needs_clarification = False

        return profile

    def _extract_voice_text(self, output: str) -> str:
        lines = []
        for line in output.splitlines():
            if line.startswith("Result : "):
                value = line.replace("Result : ", "").strip()
                if value:
                    lines.append(value)

        if lines:
            return " ".join(lines)

        cleaned = output.replace("[JARVIS]", "").replace("Execution Results", "")
        return " ".join(part.strip() for part in cleaned.splitlines() if part.strip())

    def process(self, user_input):
        profile = self.classifier.classify(user_input)
        profile = self._apply_followup_context(user_input, profile)

        print("\n[STEP 1] Intent Router")
        print(
            f"[CLASSIFIER] intent={profile.intent} "
            f"confidence={profile.confidence:.2f} "
            f"needs_clarification={profile.needs_clarification}"
        )

        execution_plan = None
        workflow_plan = None

        if profile.intent in {"joke", "chat"} or (
            profile.intent == "general"
            and len(user_input.split()) <= 8
            and not any(
                keyword in user_input.lower()
                for keyword in ("research", "open ", "create ", "build ", "code", "youtube", "instagram", "email", "budget", "workout")
            )
        ):
            execution_plan = {
                "agents": [
                    {
                        "name": "CHAT",
                        "task": user_input,
                    }
                ]
            }

        if execution_plan is None and (profile.intent in {"youtube", "social", "account_setup", "multi_step"} or len(profile.signals) > 1):
            workflow_plan = self.workflow_planner.build_plan(user_input, profile)
            if workflow_plan:
                print("[WORKFLOW PLANNER] Workflow plan generated")
                execution_plan = workflow_plan

        matches = self.intent_router.detect_agents(user_input)

        if execution_plan is None and matches and len(matches) == 1:
            agent_name = list(matches.keys())[0]
            print(f"[ROUTER] Direct Route -> {agent_name}")

            execution_plan = {
                "agents": [
                    {
                        "name": agent_name,
                        "task": user_input,
                    }
                ]
            }

        elif execution_plan is None:
            if matches and len(matches) > 1:
                print(f"[ROUTER] Multiple Matches -> {list(matches.keys())}")
            else:
                print("[ROUTER] No Strict Match Found. Switching Pipeline...")

            cached_plan = self.cache.get(user_input)

            if cached_plan:
                print("[CACHE] Hit")
                execution_plan = cached_plan
            else:
                print("[CACHE] Miss")

                semantic_result = self.semantic_router.detect_agent(user_input)

                if semantic_result and semantic_result.get("matched"):
                    print("[SEMANTIC ROUTER] Match Found")
                    execution_plan = {
                        "agents": [
                            {
                                "name": semantic_result["agent"],
                                "task": user_input,
                            }
                        ]
                    }
                else:
                    print("[SEMANTIC ROUTER] No Match")
                    execution_plan = self.llm_router.create_execution_plan(
                        user_input,
                        task_profile=profile,
                    )

                self.cache.set(user_input, execution_plan)
                print("[CACHE] Plan Saved")

        queue = self.planner.build_queue(execution_plan)
        results = self.executor.execute(queue)

        output = "\n[JARVIS]\n\n"
        output += "Execution Results\n\n"

        for item in results:
            output += (
                f"Step   : {item['step']}\n"
                f"Agent  : {item['agent']}\n"
                f"Status : {item['status']}\n"
                f"Result : {item['result']}\n\n"
            )

        self.last_intent = profile.intent
        self.last_response_text = self._extract_voice_text(output)
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
            self.voice.speak(self.last_response_text)
