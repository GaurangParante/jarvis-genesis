from app.core.agent_registry import AgentRegistry
from app.providers.base import ProviderError
from app.providers.provider_manager import ProviderManager


class LLMRouter:

    def __init__(self):
        self.registry = AgentRegistry()
        self.providers = ProviderManager()

    def create_execution_plan(self, user_input, task_profile=None):

        agents = self.registry.get_all_agents_info()

        agent_text = ""

        for agent in agents:

            agent_text += f"""
Agent: {agent['name']}
Description: {agent['description']}
Capabilities: {', '.join(agent['capabilities'])}

"""

        prompt = f"""
You are JARVIS Agent Router.

Your job is to analyze the user request and decide which agent(s) should handle the task.

Available Agents:

{agent_text}

User Query:
{user_input}

Task Notes:
Intent: {getattr(task_profile, "intent", "general")}
Confidence: {getattr(task_profile, "confidence", 0.0)}

Rules:

1. Select one or more agents if required.
2. Assign a specific task to each selected agent.
3. Do not explain anything.
4. Do not add markdown.
5. Do not wrap response in ```json blocks.
6. Return VALID JSON ONLY.
7. If no suitable agent exists, return an empty agents list.

Output Format:

{{
  "agents": [
    {{
      "name": "AGENT_NAME",
      "task": "Task description"
    }}
  ]
}}

Example 1:

{{
  "agents": [
    {{
      "name": "FORGE",
      "task": "Create Laravel project"
    }}
  ]
}}

Example 2:

{{
  "agents": [
    {{
      "name": "ORBIT",
      "task": "Open VS Code"
    }},
    {{
      "name": "FORGE",
      "task": "Create Laravel project"
    }}
  ]
}}
"""
        signals = list(getattr(task_profile, "signals", []) or [])

        if len(signals) > 1:
            workflow_like = self._build_multi_signal_plan(user_input, signals)
            if workflow_like:
                return workflow_like

        try:
            _, execution_plan = self.providers.chat_json(
                prompt,
                task_text=user_input,
                purpose="planning"
            )

            if "agents" not in execution_plan and "steps" in execution_plan:
                execution_plan["agents"] = execution_plan["steps"]

            return execution_plan
        except ProviderError:
            return self._fallback_execution_plan(user_input, task_profile)

    def _fallback_execution_plan(self, user_input, task_profile=None):
        intent = getattr(task_profile, "intent", "general")
        signals = list(getattr(task_profile, "signals", []) or [])

        fallback_agent_map = {
            "coding": "FORGE",
            "automation": "ORBIT",
            "research": "PHANTOM",
            "youtube": "APOLLO",
            "social": "NOVA",
            "email": "MERCURY",
            "security": "SENTINEL",
            "finance": "TITAN",
            "fitness": "ATHENA",
        }

        if len(signals) > 1:
            agents = []
            seen = set()

            for signal in signals:
                agent_name = fallback_agent_map.get(signal)
                if not agent_name or agent_name in seen:
                    continue

                seen.add(agent_name)
                agents.append(
                    {
                        "name": agent_name,
                        "task": user_input
                    }
                )

            if agents:
                return {
                    "agents": agents,
                    "meta": {
                        "source": "fallback",
                        "intent": intent,
                        "signals": signals
                    }
                }

        agent_name = fallback_agent_map.get(intent, "PHANTOM")

        return {
            "agents": [
                {
                    "name": agent_name,
                    "task": user_input
                }
            ],
            "meta": {
                "source": "fallback",
                "intent": intent
            }
        }

    def _build_multi_signal_plan(self, user_input, signals):
        signal_agent_map = {
            "research": "PHANTOM",
            "youtube": "APOLLO",
            "social": "NOVA",
            "email": "MERCURY",
            "automation": "ORBIT",
            "coding": "FORGE",
            "security": "SENTINEL",
            "account_setup": "ORBIT",
            "finance": "TITAN",
            "fitness": "ATHENA",
        }

        seen = set()
        agents = []

        for signal in signals:
            agent_name = signal_agent_map.get(signal)
            if not agent_name or agent_name in seen:
                continue

            seen.add(agent_name)
            agents.append(
                {
                    "name": agent_name,
                    "task": user_input,
                    "parallel_group": len(agents) + 1,
                    "requires_confirmation": agent_name in {"ORBIT", "SENTINEL"},
                }
            )

        if not agents:
            return None

        return {
            "agents": agents,
            "meta": {
                "source": "llm_fallback",
                "signals": signals,
                "workflow": "multi_step",
            }
        }
