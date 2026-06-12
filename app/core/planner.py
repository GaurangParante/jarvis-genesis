class Planner:

    def build_queue(self, execution_plan):

        queue = []

        agents = execution_plan.get("agents", [])
        steps = execution_plan.get("steps", [])
        plan_items = agents or steps

        for index, item in enumerate(plan_items, start=1):

            agent_name = item.get("name") or item.get("agent")
            task_text = item.get("task", "")

            queue.append({
                "step": index,
                "agent": agent_name,
                "task": task_text,
                "parallel_group": item.get("parallel_group"),
                "requires_confirmation": item.get("requires_confirmation", False),
                "confirmation_reason": item.get("confirmation_reason", ""),
                "workflow": item.get("workflow")
            })

        return queue
