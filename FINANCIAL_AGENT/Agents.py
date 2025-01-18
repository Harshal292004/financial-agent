from Prompts import Prompts
from pydantic_ai import Agent,RunContext

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
    def savings_agent():
        """
        Agent for saying agent
        """
        savings_agent= Prompts.SAV_Prompt() | llm 
        return  savings_agent
        
    @staticmethod     
    def forecasting_agent():
        """
        Agent for forecasting agent
        """
        forecasting_agent= Prompts.FC_Prompt() | llm 
        return forecasting_agent
        
    
    
    
    

