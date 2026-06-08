class Planner:

    def build_queue(self, execution_plan):

        queue = []

        agents = execution_plan.get("agents", [])

        for index, item in enumerate(agents, start=1):

            queue.append({
                "step": index,
                "agent": item["name"],
                "task": item["task"]
            })

        return queue