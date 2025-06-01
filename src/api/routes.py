from fastapi import APIRouter, UploadFile, File
from src.schemas.bot import QueryRequest, QueryResponse
from src.schemas.pdf import PDFUploadResponse
from src.services.bot_service import BotService
from src.services.pdf_service import PDFService

router = APIRouter()
bot_service = BotService()
pdf_service = PDFService()

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a medical query using the LLM"""
    return await bot_service.process_query(request)

@router.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process a medical PDF document"""
    contents = await file.read()
    return await pdf_service.process_pdf(contents)
