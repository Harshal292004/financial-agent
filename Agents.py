from Prompts import Prompts
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
import json
import os


# Sample data (this could be loaded from an actual JSON file)
data = {
    "expenses": [
        {"date": "2025-01-01", "expense_name": "Groceries", "amount": 50, "category": "Food"},
        {"date": "2025-01-02", "expense_name": "Car Fuel", "amount": 40, "category": "Transportation"},
        {"date": "2025-01-03", "expense_name": "Netflix Subscription", "amount": 15, "category": "Entertainment"}
    ]
}

class Agents:
    def __init__(self):
        pass
    
    @staticmethod
    def  expense_categorization_agent(llm):
        """
        Agent for generating 
        """
        expense_categorization_agent=Prompts.EC_Prompt() |llm
        return expense_categorization_agent
    
    
    @staticmethod
    def proactive_alert_agent(llm):
        
        """
        Agent for proactive alert agent
        """
        
        proactive_alert_agent= Prompts.PA_Prompt() | llm     
        return proactive_alert_agent
    
    @staticmethod
    def savings_agent(llm):
        """
        Agent for saying agent
        """
        savings_agent= Prompts.SAV_Prompt() | llm 
        return  savings_agent
        
    @staticmethod     
    def forecasting_agent(llm):
        """
        Agent for forecasting agent
        """
        forecasting_agent= Prompts.FC_Prompt() | llm 
        return forecasting_agent


    @staticmethod
    def data_access_agent(llm):
        """
        Agent that will answer questions based on the data that has been provided by the user
        it will keep track of expenses and will answer the questions..
        """
        
        def data_query_tool(query: str):
            """
            Function to query the JSON data based on user input.
            """
            if 'expense' in query:
                expense_data = data['expenses']
                return json.dumps(expense_data)
            else:
                return "Sorry, I couldn't understand the query."

            tools = [
                Tool(
                    name="Data Query Tool",
                    func=data_query_tool,
                    description="Tool for querying expenses data"
                )
            ]
        
            prompt = Prompts.data_access_prompt()
            agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)

            return agent.run({"input": query, "prompt": prompt})
    


