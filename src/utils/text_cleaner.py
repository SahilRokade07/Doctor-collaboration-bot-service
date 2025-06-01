import re
from typing import Optional

class TextCleaner:
    """Utility class for cleaning and normalizing text"""
    
    @staticmethod
    def clean_medical_text(text: str) -> str:
        """Clean and normalize medical text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Normalize common medical abbreviations
        abbreviations = {
            r'\bpt\b': 'patient',
            r'\bDx\b': 'diagnosis',
            r'\bRx\b': 'prescription',
            r'\bTx\b': 'treatment',
            r'\bHx\b': 'history',
            r'\bsx\b': 'symptoms',
        }
        
        for abbr, full in abbreviations.items():
            text = re.sub(abbr, full, text, flags=re.IGNORECASE)
        
        return text
    
    @staticmethod
    def extract_medical_terms(text: str) -> list[str]:
        """Extract medical terms from text using simple pattern matching"""
        # This is a simplified example - in practice, you'd want to use a medical terminology database
        terms = []
        
        # Look for words ending in common medical suffixes
        medical_patterns = [
            r'\b\w+itis\b',  # inflammation
            r'\b\w+emia\b',  # blood condition
            r'\b\w+osis\b',  # condition/disease
            r'\b\w+pathy\b',  # disease
            r'\b\w+plasty\b',  # surgical repair
            r'\b\w+ectomy\b',  # surgical removal
        ]
        
        for pattern in medical_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            terms.extend(match.group(0) for match in matches)
        
        return list(set(terms))
    
    @staticmethod
    def format_medical_report(
        content: str,
        title: Optional[str] = None,
        section_headers: Optional[bool] = True
    ) -> str:
        """Format text as a medical report"""
        lines = []
        
        if title:
            lines.extend([title.upper(), "=" * len(title), ""])
        
        if section_headers:
            # Add common medical report sections if they appear to be present
            sections = {
                "HISTORY": r"\b(?:history|hx)\b.*?:",
                "EXAMINATION": r"\b(?:examination|exam)\b.*?:",
                "DIAGNOSIS": r"\b(?:diagnosis|dx)\b.*?:",
                "TREATMENT": r"\b(?:treatment|tx|plan)\b.*?:",
            }
            
            current_content = content
            for section, pattern in sections.items():
                match = re.search(pattern, current_content, re.IGNORECASE)
                if match:
                    start = match.start()
                    # Add section header
                    if start > 0:
                        lines.append("\n" + section + ":")
        
        lines.append(content)
        
        return "\n".join(lines)
