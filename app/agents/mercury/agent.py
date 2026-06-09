class MercuryAgent:

    name = "MERCURY"

    description = """
    Email Management Agent.

    Reads, drafts,
    replies and manages
    email communication.
    """

    capabilities = [
        "email",
        "gmail",
        "email_reply",
        "email_drafting",
        "inbox_management"
    ]

    examples = [
        "read my emails",
        "check gmail",
        "reply to email",
        "draft email",
        "send email",
        "search inbox",
        "gmail summary",
        "latest emails",
        "find email",
        "email management",
        "reply professionally",
        "archive email",
        "important emails",
        "filter inbox",
        "mail search"
    ]

    def handle(self, task):
        return f"MERCURY received task -> {task}"