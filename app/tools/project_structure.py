import json

tree_map = {
  "root": [
    ".gitignore",
    "main.py",
    "map_project.py",
    "map_project.py.bak",
    "README.md",
    "requirements.txt"
  ],
  "app": [
    "__init__.py"
  ],
  "app\\agents": [
    "__init__.py"
  ],
  "app\\agents\\apollo": [
    "agent.py",
    "prompts.py",
    "tools.py",
    "__init__.py"
  ],
  "app\\agents\\archive": [
    "agent.py",
    "prompts.py",
    "tools.py",
    "__init__.py"
  ],
  "app\\agents\\athena": [
    "agent.py",
    "prompts.py",
    "tools.py",
    "__init__.py"
  ],
  "app\\agents\\forge": [
    "agent.py",
    "prompts.py",
    "tools.py",
    "__init__.py"
  ],
  "app\\agents\\mercury": [
    "agent.py",
    "prompts.py",
    "tools.py",
    "__init__.py"
  ],
  "app\\agents\\nova": [
    "agent.py",
    "prompts.py",
    "tools.py",
    "__init__.py"
  ],
  "app\\agents\\orbit": [
    "agent.py",
    "prompts.py",
    "tools.py",
    "__init__.py"
  ],
  "app\\agents\\phantom": [
    "agent.py",
    "prompts.py",
    "tools.py",
    "__init__.py"
  ],
  "app\\agents\\sentinel": [
    "agent.py",
    "prompts.py",
    "tools.py",
    "__init__.py"
  ],
  "app\\agents\\titan": [
    "agent.py",
    "prompts.py",
    "tools.py",
    "__init__.py"
  ],
  "app\\core": [
    "agent_registry.py",
    "config.py",
    "executor.py",
    "intent_router.py",
    "jarvis.py",
    "llm_router.py",
    "planner.py",
    "semantic_router.py",
    "__init__.py"
  ],
  "app\\data": [
    "apps.json",
    "app_aliases.json"
  ],
  "app\\data\\captures": [
    "webcam_20260610_012713.jpg",
    "webcam_20260610_015832.jpg",
    "webcam_20260610_015845.jpg",
    "webcam_20260610_015856.jpg"
  ],
  "app\\data\\recordings": [
    "screen_rec_20260610_015907.mp4",
    "screen_rec_20260610_015957.mp4",
    "screen_rec_20260610_020025.mp4",
    "webcam_rec_20260610_020048.mp4"
  ],
  "app\\data\\screenshots": [
    "screenshot_20260610_012701.png",
    "screenshot_20260610_015813.png",
    "screenshot_20260610_015822.png"
  ],
  "app\\data\\temp": [],
  "app\\embeddings": [
    "embedding_service.py"
  ],
  "app\\intents": [
    "automation.py",
    "coding.py",
    "email.py",
    "finance.py",
    "fitness.py",
    "social.py",
    "__init__.py"
  ],
  "app\\memory": [
    "cache.json",
    "command_cache.py"
  ],
  "app\\rag": [],
  "app\\tools": [
    "apollo_tools.py",
    "app_discovery.py",
    "app_scanner.py",
    "browser_tools.py",
    "file_tools.py",
    "forge_tools.py",
    "mercury_tools.py",
    "orbit_tools.py",
    "run_scan.py",
    "sentinel_tools.py",
    "titan_tools.py",
    "tool_registry.py"
  ],
  "app\\vectorstore": [
    "agent_vectors.json",
    "build_index.py",
    "faiss_index.bin",
    "metadata.json"
  ],
  "app\\voice": [],
  "data": [],
  "data\\screenshots": [
    "screenshot_20260610_004015.png"
  ],
  "docs": [
    "how_it_works.md"
  ],
  "system_docs": [
    "ChatGPT Image Jun 9, 2026, 09_47_15 AM.png",
    "ChatGPT Image Jun 9, 2026, 09_53_52 AM.png",
    "ChatGPT Image Jun 9, 2026, 09_55_14 AM.png"
  ],
  "tests": [
    "test_cache.py",
    "test_semantic_router.py",
    "__init__.py"
  ]
}

print(json.dumps(tree_map, indent=4))