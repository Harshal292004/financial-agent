from dataclasses import dataclass
from typing import List, Annotated,Dict,Any
from pydantic import BaseModel, Field


class Utility(BaseModel):
    electricity: Annotated[str, Field(description="Electricity bills")]
    water: Annotated[str, Field(description="Water bills")]
    gas: Annotated[str, Field(description="Gas bills")]
    internet: Annotated[str, Field(description="Internet expenses")]
    phone_bills: Annotated[str, Field(description="Phone bills")]

class Food(BaseModel):
    groceries: Annotated[str, Field(description="Grocery shopping expenses")]
    dining_out: Annotated[str, Field(description="Dining out or restaurant expenses")]


class Transportation(BaseModel):
    fuel: Annotated[str, Field(description="Fuel expenses")]
    public_transit: Annotated[str, Field(description="Public transportation costs")]
    maintenance: Annotated[str, Field(description="Vehicle maintenance and repairs")]


class ExpenseCategories(BaseModel):
    housing: Annotated[str, Field(description="Housing-related expenses, like rent or mortgage")]
    utilities: Annotated[Utility, Field(description="Utility bills")]
    food: Annotated[Food, Field(description="Food-related expenses")]
    transportation: Annotated[Transportation, Field(description="Transportation costs")]
    entertainment: Annotated[str, Field(description="Leisure and entertainment expenses")]
    savings: Annotated[str, Field(description="Contributions to savings or investments")]
    miscellaneous: Annotated[List[str], Field(description="Other uncategorized expenses")]



@dataclass
class ProcessedChunk:
    """
    Class for processing the chunk 
    """
    url:str
    chunk_number:int
    title:str
    summary:str
    content:str
    metadata:Dict[str,Any]
    embedding:List[float]  