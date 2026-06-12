import unittest

from app.core.safety_manager import SafetyManager
from app.core.task_classifier import TaskClassifier
from app.core.workflow_planner import WorkflowPlanner


class WorkflowPlannerTests(unittest.TestCase):
    def setUp(self):
        self.classifier = TaskClassifier()
        self.planner = WorkflowPlanner()
        self.safety = SafetyManager()

    def test_youtube_workflow_creates_multi_agent_plan(self):
        profile = self.classifier.classify("research a youtube strategy and create a video script")
        plan = self.planner.build_plan("research a youtube strategy and create a video script", profile)

        agents = [item["name"] for item in plan["agents"]]

        self.assertIn("PHANTOM", agents)
        self.assertIn("APOLLO", agents)
        self.assertIn("ORBIT", agents)

    def test_social_workflow_creates_multi_agent_plan(self):
        profile = self.classifier.classify("research and write an instagram post")
        plan = self.planner.build_plan("research and write an instagram post", profile)

        agents = [item["name"] for item in plan["agents"]]

        self.assertIn("PHANTOM", agents)
        self.assertIn("NOVA", agents)
        self.assertIn("ORBIT", agents)

    def test_account_setup_workflow_requires_confirmation(self):
        profile = self.classifier.classify("create account for youtube and instagram")
        plan = self.planner.build_plan("create account for youtube and instagram", profile)

        orbit_step = next(item for item in plan["agents"] if item["name"] == "ORBIT")

        self.assertTrue(orbit_step["requires_confirmation"])
        self.assertIn("password", orbit_step["confirmation_reason"].lower())

    def test_safety_manager_flags_password_tasks(self):
        decision = self.safety.evaluate("ORBIT", "log in with password")

        self.assertTrue(decision.requires_confirmation)
        self.assertEqual(decision.risk_level, "high")


if __name__ == "__main__":
    unittest.main()
