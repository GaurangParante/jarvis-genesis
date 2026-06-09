class ApolloAgent:

    name = "APOLLO"

    description = """
    YouTube Management Agent.

    Responsibilities:
    - Topic Research
    - Script Writing
    - SEO Optimization
    - Thumbnail Planning
    - Video Publishing
    - Channel Analytics
    """

    capabilities = [
        "youtube",
        "youtube_seo",
        "script_writing",
        "thumbnail_creation",
        "video_publishing",
        "channel_management"
    ]

    def handle(self, task):

        return (
            f"APOLLO received task -> {task}"
        )