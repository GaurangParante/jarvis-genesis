class NovaAgent:

    name = "NOVA"

    description = """
    Social Media Agent.

    Handles posting,
    scheduling,
    engagement
    and analytics.
    """

    capabilities = [
        "social_media",
        "linkedin",
        "instagram",
        "facebook",
        "twitter",
        "content_management"
    ]

    examples = [
        "create linkedin post",
        "schedule instagram post",
        "write twitter thread",
        "facebook post",
        "social media strategy",
        "instagram content",
        "linkedin content",
        "schedule content",
        "social media analytics",
        "engagement report",
        "brand content",
        "social campaign",
        "content calendar",
        "viral post ideas",
        "social growth"
    ]

    def handle(self, task):
        return f"NOVA received task -> {task}"