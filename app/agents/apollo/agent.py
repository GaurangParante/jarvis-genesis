class ApolloAgent:

    name = "APOLLO"

    description = """
    YouTube Growth and Video Content Agent.
    Responsible for topic research, video_script_writing, YouTube SEO,
    thumbnails, publishing and channel growth analytics.
    Do NOT use this agent for programming, coding, or writing automated python/bash scripts.
    """

    capabilities = [
        "youtube",
        "seo",
        "video_creation",
        "video_script_writing",
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