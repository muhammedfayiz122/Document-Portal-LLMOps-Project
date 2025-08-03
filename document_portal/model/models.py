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