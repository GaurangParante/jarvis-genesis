import unittest

from app.core.executor import Executor
from app.core.jarvis import Jarvis
from app.core.task_classifier import TaskClassifier


class ChatModeTests(unittest.TestCase):
    def test_joke_goes_to_chat_intent(self):
        profile = TaskClassifier().classify("tell me joke")
        self.assertEqual(profile.intent, "joke")

    def test_topic_joke_stays_in_chat_mode(self):
        profile = TaskClassifier().classify("hathi pe koi joke sunao")
        self.assertEqual(profile.intent, "joke")
        self.assertFalse(profile.needs_clarification)

    def test_followup_joke_stays_in_chat_mode(self):
        jarvis = Jarvis()
        jarvis.last_intent = "joke"
        profile = TaskClassifier().classify("or ek sunao")
        profile = jarvis._apply_followup_context("or ek sunao", profile)

        self.assertEqual(profile.intent, "joke")
        self.assertFalse(profile.needs_clarification)

    def test_executor_returns_chat_response_for_joke(self):
        executor = Executor()
        result = executor.run_task("CHAT", "tell me joke")

        self.assertIsInstance(result, str)
        self.assertNotIn("received task ->", result)


if __name__ == "__main__":
    unittest.main()
