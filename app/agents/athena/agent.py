class AthenaAgent:

    name = "ATHENA"

    description = """
    Fitness and Health Agent.
    """

    capabilities = [
        "fitness",
        "diet",
        "workout",
        "sleep_tracking",
        "health_analysis"
    ]

    examples = [
        "create workout plan",
        "track calories",
        "diet plan",
        "sleep report",
        "fitness goals",
        "gym workout",
        "weight loss plan",
        "muscle gain plan",
        "track steps",
        "health analytics",
        "fitness progress",
        "weekly workout",
        "exercise routine",
        "nutrition plan",
        "calorie deficit"
    ]

    def handle(self, task):
        return f"ATHENA received task -> {task}"