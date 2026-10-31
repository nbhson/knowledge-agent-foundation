class TokenOptimizer:
    """Optimize prompt for token efficiency"""
    
    @staticmethod
    def compress_context(context: str, max_tokens: int = 2000) -> str:
        """Compress context to fit token budget"""
        # Simple estimation: ~4 chars per token
        max_chars = max_tokens * 4
        
        if len(context) <= max_chars:
            return context
        
        # Strategy 1: Truncate from middle (keep start and end)
        keep_each = max_chars // 2
        return context[:keep_each] + "\n\n[...truncated...]\n\n" + context[-keep_each:]
    
    @staticmethod
    def deduplicate(text: str) -> str:
        """Remove duplicate lines"""
        seen = set()
        unique_lines = []
        for line in text.split('\n'):
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        return '\n'.join(unique_lines)
    
    @staticmethod
    def abbreviate(text: str, abbreviations: Dict[str, str] = None) -> str:
        """Replace common phrases with abbreviations"""
        default_abbr = {
            "for example": "e.g.",
            "that is": "i.e.",
            "and so on": "etc.",
            "versus": "vs.",
            "approximately": "≈",
        }
        abbr = abbreviations or default_abbr
        
        for long, short in abbr.items():
            text = text.replace(long, short)
        return text
