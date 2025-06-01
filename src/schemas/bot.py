from typing import Optional, List
from pydantic import BaseModel, Field, constr

class QueryRequest(BaseModel):
    """Schema for bot query requests"""
    query: constr(strip_whitespace=True, min_length=5) = Field(
        ..., description="The medical query to process (minimum 5 characters)"
    )
    context: Optional[constr(strip_whitespace=True, max_length=1000)] = Field(
        None, description="Additional context for the query (max 1000 characters)"
    )

class QueryResponse(BaseModel):
    """Schema for bot query responses"""
    response: constr(strip_whitespace=True, min_length=1) = Field(
        ..., description="The bot's response to the query"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score of the response (0.0 - 1.0)"
    )
    sources: Optional[List[constr(strip_whitespace=True, min_length=3)]] = Field(
        None, description="List of sources used for the response"
    )
