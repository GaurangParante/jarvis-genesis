class AthenaAgent:

    name = "ATHENA"

    description = """
    Health and Fitness Agent.

    Responsibilities:
    - Workout Planning
    - Diet Planning
    - Fitness Tracking
    - Sleep Monitoring
    - Health Analytics
    """

    capabilities = [
        "fitness",
        "workout",
        "diet",
        "calorie_tracking",
        "sleep_tracking",
        "health_analysis"
    ]

    def handle(self):
        return "Ready for fitness tasks."