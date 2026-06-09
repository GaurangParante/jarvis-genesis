class ApolloAgent:

    name = "APOLLO"

    description = """
    YouTube Growth Agent.

    Responsible for research,
    scripting, SEO,
    thumbnails, publishing
    and channel growth.
    """

    capabilities = [
        "youtube",
        "seo",
        "video_creation",
        "script_writing",
        "thumbnail_generation",
        "channel_management",
        "analytics"
    ]

    examples = [
        "create youtube script",
        "generate thumbnail",
        "youtube seo",
        "publish video",
        "upload video",
        "create faceless video",
        "generate youtube title",
        "write video description",
        "find trending topics",
        "youtube content strategy",
        "youtube analytics",
        "channel optimization",
        "create shorts script",
        "youtube keyword research",
        "viral video ideas"
    ]

    def handle(self, task):
        return f"APOLLO received task -> {task}"