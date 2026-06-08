class SentinelAgent:

    name = "SENTINEL"

    description = """
    Security Agent.

    Responsibilities:
    - Security Monitoring
    - Login Detection
    - Threat Detection
    - Password Auditing
    - Alert Generation
    """

    capabilities = [
        "security",
        "threat_detection",
        "login_monitoring",
        "password_audit",
        "security_alerts",
        "system_monitoring"
    ]

    def handle(self):
        return "Ready for security tasks."