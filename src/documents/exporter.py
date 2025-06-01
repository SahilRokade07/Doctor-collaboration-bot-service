from typing import List, Optional
import json
from pathlib import Path

class DocumentExporter:
    """Handles exporting of summaries and reports to various formats"""
    
    @staticmethod
    def export_to_json(data: dict, output_path: str):
        """Export data to a JSON file"""
        Path(output_path).write_text(json.dumps(data, indent=4))
    
    @staticmethod
    def export_to_txt(summaries: List[str], output_path: str):
        """Export summaries to a text file"""
        Path(output_path).write_text("\n\n".join(summaries))
    
    @staticmethod
    def create_report(
        title: str,
        summaries: List[str],
        metadata: Optional[dict] = None,
        output_path: str = "report.txt"
    ):
        """Create a formatted report from summaries"""
        content = [f"# {title}\n"]
        
        if metadata:
            content.append("## Metadata")
            for key, value in metadata.items():
                content.append(f"{key}: {value}")
            content.append("\n")
        
        content.append("## Summaries")
        for i, summary in enumerate(summaries, 1):
            content.append(f"\n{i}. {summary}")
        
        Path(output_path).write_text("\n".join(content))
