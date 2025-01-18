from dataclasses import dataclass
from typing import Dict,List,Any


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