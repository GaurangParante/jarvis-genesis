import unittest

from app.core.planner import Planner
from app.core.task_classifier import TaskClassifier
from app.providers.provider_manager import ProviderManager


class ProjectHealthTests(unittest.TestCase):
    def test_classifier_detects_multi_step_workflow(self):
        classifier = TaskClassifier()
        profile = classifier.classify("research a youtube strategy and create a social post")

        self.assertEqual(profile.intent, "multi_step")
        self.assertTrue(profile.signals)
        self.assertIn("research", profile.signals)
        self.assertIn("youtube", profile.signals)
        self.assertIn("social", profile.signals)

    def test_planner_accepts_agents_and_steps(self):
        planner = Planner()

        queue_from_agents = planner.build_queue(
            {
                "agents": [
                    {"name": "PHANTOM", "task": "research the topic"},
                    {"name": "APOLLO", "task": "write the YouTube script"},
                ]
            }
        )

        queue_from_steps = planner.build_queue(
            {
                "steps": [
                    {"agent": "ORBIT", "task": "open the browser"},
                    {"agent": "FORGE", "task": "create the helper script"},
                ]
            }
        )

        self.assertEqual(queue_from_agents[0]["agent"], "PHANTOM")
        self.assertEqual(queue_from_agents[1]["agent"], "APOLLO")
        self.assertEqual(queue_from_steps[0]["agent"], "ORBIT")
        self.assertEqual(queue_from_steps[1]["agent"], "FORGE")

    def test_provider_manager_prefers_nim_for_planning(self):
        manager = ProviderManager.__new__(ProviderManager)
        manager.providers = {"nim": object(), "groq": object()}
        manager.default_provider = "nim"

        provider = manager.choose_provider("build a routing plan", purpose="planning")

        self.assertEqual(provider, "nim")

    def test_provider_manager_prefers_groq_for_complex_reasoning(self):
        manager = ProviderManager.__new__(ProviderManager)
        manager.providers = {"nim": object(), "groq": object()}
        manager.default_provider = "nim"

        provider = manager.choose_provider("debug and refactor this architecture", purpose="general")

        self.assertEqual(provider, "groq")


if __name__ == "__main__":
    unittest.main()
