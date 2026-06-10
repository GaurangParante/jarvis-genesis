class ForgeAgent:

    name = "FORGE"

    description = """
    Software Development and Coding Agent.
    Responsible for writing scripts, software engineering, coding from scratch,
    debugging, project generation, APIs, databases, and automated backend development workflows.
    Use this agent whenever the user wants to write, create, generate, or modify any code, file, or script.
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
        "automation_scripts",
        "write_script",
        "create_file",
        "coding"
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
        "write python script",
        "create a script named test_bot.py",
        "generate automation script",
        "write a code to calculation"
    ]

    def handle(self, task):
        # Executor handles the direct logic in executor.py now
        return f"FORGE received task -> {task}"