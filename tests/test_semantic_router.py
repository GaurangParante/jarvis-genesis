from app.core.semantic_router import SemanticRouter

router = SemanticRouter()

queries = [
    "take image of me",
    "capture webcam",
    "create laravel api",
    "analyze my expenses",
    "generate youtube video",
    "reply to email"
]

for query in queries:

    print("\n")
    print("=" * 50)
    print(query)

    result = router.detect_agent(
        query
    )

    print(result)