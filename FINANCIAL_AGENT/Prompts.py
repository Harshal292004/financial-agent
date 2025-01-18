from langchain.prompts.chat import ChatPromptTemplate

class Prompts:
    def __init__():
        pass

    @staticmethod
    def EC_Prompt():
        """
        Prompt for Expense Categorization Agent.
        """
        return ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    """
                    You are an intelligent expense categorization assistant. Your job is to analyze, categorize, and label expenses based on provided descriptions and amounts.
                    Use the following categories: Housing, Food, Transportation, Entertainment, Healthcare, Utilities, Savings, and Others.
                    Be as specific as possible when categorizing expenses. If an expense doesn't fit a predefined category, classify it as "Others."
                    """,
                ),
                (
                    'human',
                    """
                    Analyze and categorize the following expenses:
                    {input}
                    Provide the output as a table with three columns: Expense Name, Amount, and Category.
                    """,
                ),
            ]
        )

    @staticmethod
    def PA_Prompt():
        """
        Prompt for Proactive Alert Agent.
        """
        return ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    """
                    You are an advanced financial assistant specializing in proactive alerts for budget management.
                    Your goal is to analyze spending patterns, identify anomalies, and provide early warnings or advice to avoid budget overruns.
                    Focus on overspending, unplanned expenses, and savings opportunities. Offer specific actions to address any issues.
                    """,
                ),
                (
                    'human',
                    """
                    Review the following financial data and provide proactive alerts for potential budget concerns:
                    {input}
                    Include clear explanations for each alert and suggest actionable recommendations to mitigate risks.
                    """,
                ),
            ]
        )

    @staticmethod
    def SAV_Prompt():
        """
        Prompt for Savings Agent.
        """
        return ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    """
                    You are a financial savings advisor. Your task is to analyze financial data, identify areas where savings can be optimized, and provide actionable tips to achieve short-term and long-term financial goals.
                    Consider factors like fixed expenses, discretionary spending, income, and potential investments.
                    """,
                ),
                (
                    'human',
                    """
                    Based on the following financial details:
                    {input}
                    Identify potential savings opportunities and provide tips to optimize spending while achieving financial goals.
                    Structure your response in two sections:
                    1. Areas for immediate savings.
                    2. Long-term strategies for financial growth.
                    """,
                ),
            ]
        )

    @staticmethod
    def FC_Prompt():
        """
        Prompt for Forecasting Agent.
        """
        return ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    """
                    You are a financial forecasting expert. Your job is to analyze past financial data, identify trends, and predict future spending patterns.
                    Focus on creating accurate forecasts based on historical data while accounting for seasonality, fixed costs, and variable expenses.
                    """,
                ),
                (
                    'human',
                    """
                    Using the following past financial data:
                    {input}
                    Forecast the monthly spending for the next 6 months. Include details about:
                    1. Total projected spending for each month.
                    2. Key categories contributing to spending.
                    3. Any notable trends or patterns observed in the forecast.
                    """,
                ),
            ]
        )
    def data_access_prompt():
        return ChatPromptTemplate.from_messages(
            [
                ("system", """
                You are an intelligent assistant. You have access to data provided in JSON format.
                Your task is to process user queries based on the data and return the relevant information.
                The JSON data looks like this:
                {
                    "expenses": [
                        {"date": "2025-01-01", "expense_name": "Groceries", "amount": 50, "category": "Food"},
                        {"date": "2025-01-02", "expense_name": "Car Fuel", "amount": 40, "category": "Transportation"},
                        {"date": "2025-01-03", "expense_name": "Netflix Subscription", "amount": 15, "category": "Entertainment"}
                    ]
                }
                """),
                ("human", "{user_query}")
            ]
        )
