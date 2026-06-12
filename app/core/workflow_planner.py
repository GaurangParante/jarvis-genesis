from dataclasses import dataclass


@dataclass
class WorkflowPlan:
    name: str
    execution_plan: dict


class WorkflowPlanner:
    priority_agents = [
        ("research", "PHANTOM"),
        ("youtube", "APOLLO"),
        ("social", "NOVA"),
        ("email", "MERCURY"),
        ("automation", "ORBIT"),
        ("coding", "FORGE"),
        ("security", "SENTINEL"),
        ("account_setup", "ORBIT"),
        ("finance", "TITAN"),
        ("fitness", "ATHENA"),
    ]

    def build_plan(self, user_input: str, task_profile):
        signals = list(getattr(task_profile, "signals", []) or [])
        text = user_input.lower().strip()

        if "account_setup" in signals or self._needs_account_setup(text):
            return self._build_account_setup_plan(user_input)

        if "youtube" in signals and "social" in signals:
            return self._build_creator_plan(user_input, workflow_name="youtube_social")

        if "youtube" in signals:
            return self._build_youtube_plan(user_input)

        if "social" in signals:
            return self._build_social_plan(user_input)

        if len(signals) > 1 or getattr(task_profile, "intent", "") == "multi_step":
            return self._build_multi_step_plan(user_input, signals)

        return None

    def _build_youtube_plan(self, user_input: str):
        return {
            "agents": [
                {
                    "name": "PHANTOM",
                    "task": f"Research YouTube topic ideas, keywords, and references for: {user_input}",
                    "parallel_group": 1,
                },
                {
                    "name": "APOLLO",
                    "task": f"Create YouTube title, script, description, and SEO notes for: {user_input}",
                    "parallel_group": 2,
                },
                {
                    "name": "ORBIT",
                    "task": f"Prepare browser and local files for the YouTube workflow: {user_input}",
                    "parallel_group": 3,
                    "requires_confirmation": True,
                    "confirmation_reason": "Browser and upload actions may require your review.",
                },
            ],
            "meta": {
                "workflow": "youtube",
                "source": "workflow_planner",
            },
        }

    def _build_social_plan(self, user_input: str):
        return {
            "agents": [
                {
                    "name": "PHANTOM",
                    "task": f"Research the social topic, trend angle, and audience hook for: {user_input}",
                    "parallel_group": 1,
                },
                {
                    "name": "NOVA",
                    "task": f"Draft the social media post, caption, and hashtags for: {user_input}",
                    "parallel_group": 2,
                },
                {
                    "name": "ORBIT",
                    "task": f"Open the target social platform and prepare for posting workflow: {user_input}",
                    "parallel_group": 3,
                    "requires_confirmation": True,
                    "confirmation_reason": "Posting or account actions should be reviewed before execution.",
                },
            ],
            "meta": {
                "workflow": "social",
                "source": "workflow_planner",
            },
        }

    def _build_account_setup_plan(self, user_input: str):
        return {
            "agents": [
                {
                    "name": "SENTINEL",
                    "task": f"Review the account setup request for safety concerns: {user_input}",
                    "parallel_group": 1,
                },
                {
                    "name": "ORBIT",
                    "task": f"Open the browser and navigate to the account setup flow for: {user_input}",
                    "parallel_group": 2,
                    "requires_confirmation": True,
                    "confirmation_reason": "Account login or signup may need your password or OTP.",
                },
                {
                    "name": "MERCURY",
                    "task": f"Prepare any email verification or inbox follow-up steps for: {user_input}",
                    "parallel_group": 3,
                },
            ],
            "meta": {
                "workflow": "account_setup",
                "source": "workflow_planner",
            },
        }

    def _build_multi_step_plan(self, user_input: str, signals: list[str]):
        agents = []
        seen = set()

        for signal, agent_name in self.priority_agents:
            if signal not in signals or agent_name in seen:
                continue

            seen.add(agent_name)
            agents.append(
                {
                    "name": agent_name,
                    "task": self._build_agent_task(agent_name, user_input, signal),
                    "parallel_group": len(agents) + 1,
                    "requires_confirmation": agent_name in {"ORBIT", "SENTINEL"},
                    "confirmation_reason": self._confirmation_reason(agent_name, signal),
                }
            )

        if not agents:
            return None

        return {
            "agents": agents,
            "meta": {
                "workflow": "multi_step",
                "source": "workflow_planner",
                "signals": signals,
            },
        }

    def _build_creator_plan(self, user_input: str, workflow_name: str):
        return {
            "agents": [
                {
                    "name": "PHANTOM",
                    "task": f"Research the creator topic and audience angle for: {user_input}",
                    "parallel_group": 1,
                },
                {
                    "name": "APOLLO",
                    "task": f"Draft YouTube content for: {user_input}",
                    "parallel_group": 2,
                },
                {
                    "name": "NOVA",
                    "task": f"Adapt the content for social media promotion: {user_input}",
                    "parallel_group": 3,
                },
                {
                    "name": "ORBIT",
                    "task": f"Prepare browser workflow for account posting: {user_input}",
                    "parallel_group": 4,
                    "requires_confirmation": True,
                    "confirmation_reason": "Publishing actions should be confirmed before execution.",
                },
            ],
            "meta": {
                "workflow": workflow_name,
                "source": "workflow_planner",
            },
        }

    def _build_agent_task(self, agent_name: str, user_input: str, signal: str) -> str:
        if agent_name == "PHANTOM":
            return f"Research background details, references, and trends for: {user_input}"
        if agent_name == "APOLLO":
            return f"Create YouTube strategy and content for: {user_input}"
        if agent_name == "NOVA":
            return f"Create social media copy and distribution plan for: {user_input}"
        if agent_name == "MERCURY":
            return f"Prepare email communication for: {user_input}"
        if agent_name == "FORGE":
            return f"Create or modify code for: {user_input}"
        if agent_name == "ORBIT":
            return f"Execute the desktop/browser workflow for: {user_input}"
        if agent_name == "SENTINEL":
            return f"Review security and approval risks for: {user_input}"
        if agent_name == "TITAN":
            return f"Review finance-related details for: {user_input}"
        if agent_name == "ATHENA":
            return f"Review fitness-related details for: {user_input}"
        if agent_name == "ARCHIVE":
            return f"Collect and store supporting notes for: {user_input}"
        return f"Handle the {signal} portion of: {user_input}"

    def _confirmation_reason(self, agent_name: str, signal: str) -> str:
        if agent_name == "ORBIT":
            return "Desktop, browser, or upload actions should be reviewed before execution."
        if agent_name == "SENTINEL":
            return "Security-sensitive steps should be confirmed."
        return f"{signal} actions may need your approval."

    def _needs_account_setup(self, text: str) -> bool:
        phrases = ("create account", "make account", "set up account", "signup", "sign up", "register")
        return any(phrase in text for phrase in phrases)
