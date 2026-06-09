class Executor:

    def __init__(self, registry):
        self.registry = registry

    def execute(self, queue):

        results = []

        for item in queue:

            agent_name = item["agent"]
            task = item["task"]

            agent = self.registry.get_agent(
                agent_name
            )

            if not agent:

                results.append(
                    {
                        "step": item["step"],
                        "agent": agent_name,
                        "status": "FAILED",
                        "message": "Agent not found"
                    }
                )

                continue

            response = agent.handle(task)

            results.append(
                {
                    "step": item["step"],
                    "agent": agent_name,
                    "status": "SUCCESS",
                    "message": response
                }
            )

        return results