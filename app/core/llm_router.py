import json
import re

from groq import Groq

from app.core.config import GROQ_API_KEY
from app.core.agent_registry import AgentRegistry


class LLMRouter:

    def __init__(self):

        self.client = Groq(api_key=GROQ_API_KEY)
        self.registry = AgentRegistry()

    def create_execution_plan(self, user_input):

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

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()
        match = re.search(r"\{.*\}", content, re.DOTALL)

        if not match:
            raise ValueError(
                f"No JSON found in response:\n{content}"
            )

        json_text = match.group()

        try:

            execution_plan = json.loads(json_text)

            return execution_plan

        except json.JSONDecodeError as e:

            print("\n========== INVALID JSON ==========")
            print(json_text)
            print("==================================\n")

            raise e