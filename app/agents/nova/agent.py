class NovaAgent:

    name = "NOVA"

    description = """
    Social Media Agent.

    Responsibilities:
    - Social Media Posting
    - Content Scheduling
    - Audience Engagement
    - Social Analytics
    - Brand Management
    """

    capabilities = [
        "social_media",
        "linkedin",
        "instagram",
        "facebook",
        "twitter",
        "content_scheduling",
        "social_analytics"
    ]

    def handle(self, task):

        return (
            f"NOVA received task -> {task}"
        )