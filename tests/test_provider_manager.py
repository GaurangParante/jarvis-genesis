import unittest

from app.core.task_classifier import TaskClassifier
from app.providers.provider_manager import ProviderManager


class DummyProvider:
    pass


class ProviderManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = ProviderManager.__new__(ProviderManager)
        self.manager.providers = {
            "nim": DummyProvider(),
            "groq": DummyProvider(),
        }
        self.manager.default_provider = "nim"

    def test_planning_prefers_nim(self):
        provider = self.manager.choose_provider("build a routing plan", purpose="planning")
        self.assertEqual(provider, "nim")

    def test_complex_code_prefers_groq(self):
        provider = self.manager.choose_provider("debug and refactor this architecture", purpose="general")
        self.assertEqual(provider, "groq")

    def test_order_contains_fallback_provider(self):
        order = self.manager.choose_order("simple task", purpose="general")
        self.assertEqual(order[0], "nim")
        self.assertIn("groq", order)


class TaskClassifierTests(unittest.TestCase):
    def test_multi_signal_intent(self):
        classifier = TaskClassifier()
        profile = classifier.classify("research a youtube strategy and create a post")

        self.assertEqual(profile.intent, "multi_step")
        self.assertGreaterEqual(profile.confidence, 0.86)
        self.assertIn("research", profile.signals)
        self.assertIn("youtube", profile.signals)
        self.assertIn("social", profile.signals)


if __name__ == "__main__":
    unittest.main()
