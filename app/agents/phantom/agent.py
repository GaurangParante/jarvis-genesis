class PhantomAgent:

    name = "PHANTOM"

    description = """
    Research Agent.

    Performs internet research,
    market analysis,
    competitor analysis,
    trend discovery and investigations.
    """

    capabilities = [
        "research",
        "web_search",
        "market_analysis",
        "trend_analysis",
        "competitor_analysis",
        "news_monitoring"
    ]

    examples = [
        "research raj shamani",
        "latest ai news",
        "market analysis",
        "competitor research",
        "company analysis",
        "product research",
        "find latest trends",
        "industry report",
        "web research",
        "startup analysis",
        "analyze competitors",
        "research elon musk",
        "latest technology news",
        "stock market trends",
        "deep research"
    ]

    def handle(self, task):
        return f"PHANTOM received task -> {task}"