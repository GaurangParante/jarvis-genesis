from app.core.executor import Executor
class OrbitAgent:

    name = "ORBIT"

    description = """
    Desktop Automation Agent.

    Responsibilities:

    - Open applications
    - Open VS Code
    - Open Chrome
    - Open folders
    - Open files

    Camera Operations:

    - Open webcam
    - Capture image
    - Take photo
    - Take picture
    - Selfie capture
    - Webcam snapshot
    - Camera control

    Screen Operations:

    - Screenshot capture
    - Screen recording

    Desktop Control:

    - Launch programs
    - Browser automation
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