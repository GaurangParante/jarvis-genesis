class ForgeAgent:

    name = "FORGE"

    description = """
    Software Development Agent.

    Responsible for software engineering, coding,
    debugging, project generation, APIs,
    databases and development workflows.
    """

    capabilities = [
        "python",
        "laravel",
        "fastapi",
        "flask",
        "api_development",
        "database_design",
        "sql",
        "debugging",
        "project_creation",
        "software_development",
        "git",
        "automation_scripts"
    ]

    examples = [
        "create laravel project",
        "create laravel migration",
        "build rest api",
        "fix python bug",
        "debug my code",
        "create mysql table",
        "write flask api",
        "generate model",
        "generate controller",
        "create authentication system",
        "optimize sql query",
        "create ai chatbot",
        "setup fastapi project",
        "create node js api",
        "write python script"
    ]

    def handle(self, task):
        return f"FORGE received task -> {task}"