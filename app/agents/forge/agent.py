class ForgeAgent:

    name = "FORGE"

    description = """
    Software Development Agent.

    Responsibilities:
    - Python Development
    - Laravel Development
    - API Creation
    - Database Design
    - Debugging
    - Project Generation
    """

    capabilities = [
        "python",
        "laravel",
        "api",
        "database",
        "debugging",
        "coding",
        "project_creation",
        "software_development"
    ]

    def handle(self, task):

        return (
            f"FORGE received task -> {task}"
        )