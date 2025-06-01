from typing import Dict, Any
from db.handlers import JSONDBHandler
from core.config import settings

class JSONDBService:
    """Service for interacting with the JSON database"""
    
    def __init__(self):
        self.handler = JSONDBHandler(settings.JSON_DB_PATH)
    
    def get_all_queries(self) -> list[Dict[str, Any]]:
        """Get all stored queries"""
        return self.handler.get_queries()
    
    def get_all_summaries(self) -> list[Dict[str, Any]]:
        """Get all stored summaries"""
        return self.handler.get_summaries()
    
    def save_query(self, query_data: Dict[str, Any]):
        """Save a new query"""
        self.handler.save_query(query_data)
    
    def save_summary(self, summary_data: Dict[str, Any]):
        """Save a new summary"""
        self.handler.save_summary(summary_data)
