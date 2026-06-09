class MercuryAgent:

    name = "MERCURY"

    description = """
    Communication Agent.

    Responsibilities:
    - Gmail Management
    - Email Drafting
    - Email Replies
    - Communication Monitoring
    - Inbox Organization
    """

    capabilities = [
        "gmail",
        "email",
        "email_reply",
        "email_drafting",
        "communication",
        "inbox_management"
    ]

    def handle(self, task):

        return (
            f"MERCURY received task -> {task}"
        )