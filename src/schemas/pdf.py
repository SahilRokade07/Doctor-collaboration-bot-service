from typing import List, Dict
from pydantic import BaseModel, Field, constr, PositiveInt

class PDFContent(BaseModel):
    """Schema for extracted PDF content"""
    text: constr(strip_whitespace=True, min_length=10) = Field(
        ..., description="Extracted text content from PDF (minimum 10 characters)"
    )
    page_number: PositiveInt = Field(
        ..., description="Page number (must be positive integer)"
    )
    metadata: Dict[str, str] = Field(
        default_factory=dict, description="PDF metadata as key-value pairs"
    )

class PDFUploadResponse(BaseModel):
    """Schema for PDF upload response"""
    filename: constr(strip_whitespace=True, min_length=3) = Field(
        ..., description="Name of the uploaded file"
    )
    page_count: PositiveInt = Field(
        ..., description="Number of pages in the PDF (must be positive)"
    )
    summary: constr(strip_whitespace=True, min_length=10) = Field(
        ..., description="Generated summary of the PDF content"
    )
    topics: List[constr(strip_whitespace=True, min_length=2)] = Field(
        ..., description="Extracted key topics from the document"
    )
