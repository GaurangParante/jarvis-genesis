class TitanAgent:

    name = "TITAN"

    description = """
    Finance Agent.

    Responsibilities:
    - Expense Tracking
    - Income Tracking
    - Budget Management
    - Financial Reports
    - Tax Preparation
    """

    capabilities = [
        "finance",
        "expense_tracking",
        "income_tracking",
        "budgeting",
        "financial_reports",
        "tax_management"
    ]

    def handle(self):
        return "Ready for finance tasks."