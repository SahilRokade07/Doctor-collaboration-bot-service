import httpx
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import HTTPException
from src.core.config import settings
from src.schemas.bot import QueryRequest, QueryResponse
from src.db.handlers import JSONDBHandler

class BotService:
    """Service for interacting with medical LLMs via Ollama"""
    
    def __init__(self):
        self.api_url = f"{settings.OLLAMA_API_URL}/api/generate"
        self.model = settings.LLM_MODEL_NAME
        self.db_handler = JSONDBHandler(settings.JSON_DB_PATH)
    
    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """Process a medical query using the LLM"""
        # Prepare the prompt with medical context
        prompt = self._prepare_prompt(request.query, request.context)
        
        # Call Ollama API with timeout settings
        try:
            timeout_settings = httpx.Timeout(30.0, read=60.0)  # 30s for connection, 60s for read
            async with httpx.AsyncClient(timeout=timeout_settings) as client:
                response = await client.post(
                    self.api_url,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False
                    }
                )
                response.raise_for_status()
                llm_response = response.json()
        except httpx.TimeoutException as e:
            raise HTTPException(
                status_code=504,
                detail="Request to LLM service timed out. Please try again."
            ) from e
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Error communicating with LLM service: {str(e)}"
            ) from e
        
        # Process and store the response
        processed_response = self._process_response(llm_response)
        self._store_interaction(request, processed_response)
        
        return processed_response
    
    def _prepare_prompt(self, query: str, context: Optional[str] = None) -> str:
        """Prepare the prompt for the LLM"""
        base_prompt = (
            "You are a medical AI assistant. Please provide a detailed, "
            "accurate, and professional response to the following medical query. "
            "Base your response on established medical knowledge and research."
        )
        
        if context:
            return f"{base_prompt}\n\nContext: {context}\n\nQuery: {query}"
        return f"{base_prompt}\n\nQuery: {query}"
    
    def _process_response(self, llm_response: Dict[str, Any]) -> QueryResponse:
        """Process the LLM response into a structured format"""
        return QueryResponse(
            response=llm_response["response"],
            confidence=0.95,  # This should be calculated based on the model's output
            sources=[]  # This should be populated with relevant sources
        )
    
    def _store_interaction(self, request: QueryRequest, response: QueryResponse):
        """Store the interaction in the JSON database"""
        self.db_handler.save_query({
            "query": request.dict(),
            "response": response.dict(),
            "timestamp": str(datetime.now())
        })
