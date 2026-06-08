class OrbitAgent:

    name = "ORBIT"

    description = """
    Desktop Automation Agent.

    Responsibilities:
    - Open Applications
    - Close Applications
    - File Management
    - Folder Management
    - Desktop Automation
    - Command Execution
    """

    capabilities = [
        "desktop_control",
        "open_application",
        "close_application",
        "file_management",
        "folder_management",
        "automation",
        "command_execution"
    ]

    def handle(self):
        return "Ready for desktop automation tasks."