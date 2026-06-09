from app.agents.forge import ForgeAgent
from app.agents.orbit import OrbitAgent
from app.agents.phantom import PhantomAgent
from app.agents.archive import ArchiveAgent
from app.agents.titan import TitanAgent
from app.agents.athena import AthenaAgent
from app.agents.mercury import MercuryAgent
from app.agents.nova import NovaAgent
from app.agents.apollo import ApolloAgent
from app.agents.sentinel import SentinelAgent


class AgentRegistry:

    def __init__(self):

        self.agents = {
            "FORGE": ForgeAgent,
            "ORBIT": OrbitAgent,
            "PHANTOM": PhantomAgent,
            "ARCHIVE": ArchiveAgent,
            "TITAN": TitanAgent,
            "ATHENA": AthenaAgent,
            "MERCURY": MercuryAgent,
            "NOVA": NovaAgent,
            "APOLLO": ApolloAgent,
            "SENTINEL": SentinelAgent,
        }

    def get_agent(self, name):

        agent_class = self.agents.get(name)

        if not agent_class:
            return None

        return agent_class()

    def get_all_agents_info(self):

        agents = []

        for name, agent_class in self.agents.items():

            agents.append({
                "name": name,
                "description": agent_class.description,
                "capabilities": agent_class.capabilities
            })

        return agents

    def get_agent_documents(self):

        docs = []
        examples = []

        for name, agent_class in self.agents.items():

            text = f"""
Agent: {name}

Description:
{agent_class.description}

Capabilities:
{", ".join(agent_class.capabilities)}

Examples:
{", ".join(agent_class.examples)}
"""

            docs.append(
                {
                    "name": name,
                    "text": text
                }
            )

        return docs