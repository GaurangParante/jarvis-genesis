import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from app.memory.command_cache import CommandCache


cache = CommandCache()

cache.set(
    "open vscode",
    {
        "agents": [
            {
                "name": "ORBIT",
                "task": "Open VS Code"
            }
        ]
    }
)

result = cache.get(
    "open vscode"
)

print(result)