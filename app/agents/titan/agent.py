class TitanAgent:

    name = "TITAN"

    description = """
    Finance Agent.

    Handles expenses,
    income tracking,
    budgeting,
    financial reports
    and spending analysis.
    """

    capabilities = [
        "finance",
        "expense_tracking",
        "income_tracking",
        "budgeting",
        "financial_reports",
        "spending_analysis"
    ]

    examples = [
        "show my expenses",
        "monthly spending report",
        "analyze spending",
        "budget planning",
        "track expenses",
        "track income",
        "show gpay transactions",
        "financial summary",
        "expense analysis",
        "monthly budget",
        "tax calculation",
        "money management",
        "expense dashboard",
        "cash flow report",
        "income report"
    ]

    def handle(self, task):
        return f"TITAN received task -> {task}"