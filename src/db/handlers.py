import json
from typing import Any, Dict, List, Optional
from pathlib import Path

class JSONDBHandler:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create the database file if it doesn't exist"""
        if not self.db_path.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.db_path.write_text('{"queries": [], "summaries": []}')
    
    def read_all(self) -> Dict[str, List[Any]]:
        """Read all data from the JSON database"""
        return json.loads(self.db_path.read_text())
    
    def save_query(self, query: Dict[str, Any]):
        """Save a new query to the database"""
        data = self.read_all()
        data["queries"].append(query)
        self.db_path.write_text(json.dumps(data, indent=4))
    
    def save_summary(self, summary: Dict[str, Any]):
        """Save a new summary to the database"""
        data = self.read_all()
        data["summaries"].append(summary)
        self.db_path.write_text(json.dumps(data, indent=4))
    
    def get_queries(self) -> List[Dict[str, Any]]:
        """Get all queries from the database"""
        return self.read_all()["queries"]
    
    def get_summaries(self) -> List[Dict[str, Any]]:
        """Get all summaries from the database"""
        return self.read_all()["summaries"]
