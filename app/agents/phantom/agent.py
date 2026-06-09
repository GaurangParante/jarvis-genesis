class PhantomAgent:

    name = "PHANTOM"

    description = """
    Research Agent.

    Responsibilities:
    - Web Research
    - Market Analysis
    - Competitor Analysis
    - Trend Discovery
    - News Monitoring
    """

    capabilities = [
        "research",
        "web_search",
        "market_analysis",
        "competitor_analysis",
        "news_monitoring",
        "trend_analysis"
    ]

    def handle(self, task):

        return (
            f"PHANTOM received task -> {task}"
        )