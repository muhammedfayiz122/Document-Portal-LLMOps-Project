from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List

class ChangeFormat(BaseModel):
    """
    Model to represent a change format.
    """
    page: str
    changes: str
    
class SummaryResponse():
    """
    Model to represent a summary response.
    """
    summary: str
    changes: List[ChangeFormat] = Field(default_factory=list)
    
class PromptType(str, Enum):
    DOCUMENT_ANALYSIS = "document_analysis",
    DOCUMENT_COMPARISON = "document_comparison",
    CONTEXTUALIZE_QUESTION = "contextualize_question",
    CONTEXTUALIZE_QA = "context_qa",
    