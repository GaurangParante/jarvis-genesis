class SentinelAgent:

    name = "SENTINEL"

    description = """
    Security Agent.

    Responsibilities:

    - CCTV monitoring
    - Security cameras
    - Surveillance
    - Motion detection
    - Intruder detection
    - Security recording
    - Camera feed monitoring
    - Webcam surveillance
    """

    capabilities = [
        "security",
        "cctv",
        "camera_monitoring",
        "threat_detection",
        "security_alerts"
    ]

    examples = [
        "check cctv",
        "show security feed",
        "monitor camera",
        "intruder detection",
        "security alert",
        "camera monitoring",
        "live camera feed",
        "motion detection",
        "security logs",
        "face detection",
        "security report",
        "check webcam feed",
        "camera activity",
        "surveillance",
        "security monitoring"
    ]

    def handle(self, task):
        return f"SENTINEL received task -> {task}"