# How JARVIS Genesis Works

This project is currently a small phase-1 demo:

`main.py` -> `Jarvis` -> `IntentRouter` -> Agent -> Response

## 1. Entry Point

The app starts in [`main.py`](../main.py).

```python
from app.core.jarvis import Jarvis


def main():
    Jarvis().run()


if __name__ == "__main__":
    main()
```

What this does:

- Imports the `Jarvis` controller.
- Creates a `Jarvis` instance.
- Starts the interactive loop with `Jarvis().run()`.

## 2. Jarvis Controller

The main runtime logic lives in [`app/core/jarvis.py`](../app/core/jarvis.py).

```python
class Jarvis:
    def __init__(self):
        self.router = IntentRouter()

    def process(self, user_input: str) -> str:
        intent, agent = self.router.route(user_input)
        response = agent.handle()
        return (
            "[JARVIS]\n"
            f"Intent: {intent}\n\n"
            "Agent Selected:\n"
            f"{agent.name}\n\n"
            f"{agent.name}:\n"
            f"{response}"
        )
```

What this does:

- Creates an `IntentRouter`.
- Takes the user's text input.
- Routes it to the correct agent.
- Calls the selected agent's `handle()` method.
- Formats the final output shown in the terminal.

## 3. Intent Routing

The routing logic is in [`app/core/intent_router.py`](../app/core/intent_router.py).

It works in two steps:

1. Detect the intent from the text.
2. Select the matching agent.

For example:

- `create laravel project` -> `coding` -> `FORGE`
- `open chrome` -> `automation` -> `ORBIT`
- `search latest AI news` -> `research` -> `PHANTOM`
- `create youtube script` -> `youtube` -> `APOLLO`

The router uses keyword matching.

```python
def detect_intent(self, user_input: str) -> str:
    text = user_input.lower()

    for intent, keywords in self.intent_keywords.items():
        if any(keyword in text for keyword in keywords):
            return intent

    return "general"
```

## 4. APOLLO Agent

The APOLLO agent is defined in [`app/agents/apollo/agent.py`](../app/agents/apollo/agent.py).

```python
class ApolloAgent:
    name = "APOLLO"

    def handle(self):
        return "Ready to help with YouTube tasks."
```

This means:

- If the router detects a YouTube-related intent,
- it selects `ApolloAgent`,
- and `handle()` returns:

`Ready to help with YouTube tasks.`

## 5. End-to-End Example

If the user types:

```text
create youtube script
```

The flow becomes:

1. `main.py` starts `Jarvis`.
2. `Jarvis.run()` reads the input.
3. `Jarvis.process()` sends the text to `IntentRouter`.
4. `IntentRouter.detect_intent()` matches `youtube`.
5. `IntentRouter.select_agent()` returns `ApolloAgent`.
6. `ApolloAgent.handle()` returns the response.
7. `Jarvis.process()` prints the final result.

Example output:

```text
[JARVIS]
Intent: youtube

Agent Selected:
APOLLO

APOLLO:
Ready to help with YouTube tasks.
```

## 6. Current Scope

This phase is intentionally small and simple:

- No AI model
- No tools
- No memory
- No voice
- No automation

It only does:

`Input -> Intent Detection -> Agent Selection -> Response`

