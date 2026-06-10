from app.core.executor import Executor

class OrbitAgent:

    name = "ORBIT"

    description = """
    Desktop Automation Agent.
    Handles opening local system applications, system settings, capturing webcam/screenshots, 
    and general operating system tasks. Do NOT use this for writing code or generating programming scripts.
    """

    capabilities = [
        "browser_control",
        "application_control",
        "file_management",
        "folder_management",
        "camera_control",
        "automation",
        "camera_capture",
        "photo_capture",
        "webcam",
        "take_picture",
        "screenshot",
        "screen_recording",
        "desktop_control"
    ]

    examples = [
        "open vscode",
        "open chrome",
        "open downloads folder",
        "open file explorer",
        "launch spotify",
        "close chrome",
        "take screenshot",
        "capture screen",
        "record screen",
        "open camera",
        "take image of me",
        "capture webcam",
        "click photo",
        "record webcam video",
        "open notepad"
    ]

    def handle(self, task):
        executor = Executor()
        queue = [
            {
                "step": 1,
                "agent": "ORBIT",
                "task": task
            }
        ]
        return executor.execute(queue)