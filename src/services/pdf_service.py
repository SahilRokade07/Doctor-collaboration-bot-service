from typing import Dict, Any
import PyPDF2
from io import BytesIO
from src.schemas.pdf import PDFContent, PDFUploadResponse
from src.schemas.bot import QueryRequest
from src.services.bot_service import BotService
from src.db.handlers import JSONDBHandler
from src.core.config import settings

class PDFService:
    """Service for handling PDF document processing"""
    
    def __init__(self):
        self.bot_service = BotService()
        self.db_handler = JSONDBHandler(settings.JSON_DB_PATH)
    
    async def process_pdf(self, file_content: bytes) -> PDFUploadResponse:
        """Process an uploaded PDF file"""
        # Extract text and metadata from PDF
        pdf_content = self._extract_pdf_content(file_content)
        
        # Generate summary using LLM
        summary = await self._generate_summary(pdf_content)
        
        # Extract key topics
        topics = await self._extract_topics(pdf_content)
        
        # Create response
        response = PDFUploadResponse(
            filename=pdf_content["metadata"].get("title", "Untitled"),
            page_count=pdf_content["page_count"],
            summary=summary,
            topics=topics
        )
        
        # Store the summary
        self._store_summary(response)
        
        return response
    
    def _extract_pdf_content(self, file_content: bytes) -> Dict[str, Any]:
        """Extract text and metadata from a PDF file"""
        pdf_file = BytesIO(file_content)
        reader = PyPDF2.PdfReader(pdf_file)
        
        pages = []
        for i, page in enumerate(reader.pages):
            pages.append(PDFContent(
                text=page.extract_text(),
                page_number=i + 1,
                metadata={}
            ))
        
        return {
            "pages": pages,
            "page_count": len(pages),
            "metadata": reader.metadata if reader.metadata else {}
        }
    
    async def _generate_summary(self, pdf_content: Dict[str, Any]) -> str:
        """Generate a summary of the PDF content using the LLM"""
        # Combine text from all pages
        full_text = "\n".join(page.text for page in pdf_content["pages"])
        
        # Use the bot service to generate a summary
        request = QueryRequest(
            query="Please provide a concise summary of the following medical document:",
            context=full_text[:4000]  # Limit context length
        )
        response = await self.bot_service.process_query(request)
        
        return response.response
    
    async def _extract_topics(self, pdf_content: Dict[str, Any]) -> list[str]:
        """Extract key topics from the PDF content"""
        # Use the bot service to extract topics
        request = QueryRequest(
            query="Please extract the main medical topics from this document:",
            context="\n".join(page.text for page in pdf_content["pages"][:2])
        )
        response = await self.bot_service.process_query(request)
        
        # Process the response into a list of topics
        topics = [
            topic.strip()
            for topic in response.response.split("\n")
            if topic.strip()
        ]
        
        return topics[:5]  # Return top 5 topics
    
    def _store_summary(self, response: PDFUploadResponse):
        """Store the PDF summary in the JSON database"""
        self.db_handler.save_summary(response.dict())
