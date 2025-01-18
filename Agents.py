from pydantic_ai import Agent
from dotenv import load_dotenv
import asyncio

load_dotenv()

class Agents:
    def __init__(self):
        pass

    @staticmethod
    def processing_agent():
        processing_agent = Agent('google-gla:gemini-1.5-flash')
        return processing_agent