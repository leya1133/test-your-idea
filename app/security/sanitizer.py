import re
from fastapi import HTTPException

# Blacklisted prompt injection patterns
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior)\s+instructions",
    r"override\s+(system\s+)?prompt",
    r"system\s*:",
    r"print\s+env(ironment)?\s+variables",
    r"show\s+(api\s+)?keys?",
    r"reveal\s+(api\s+)?keys?",
    r"eval\(",
    r"exec\("
]

def sanitize_user_input(text: str, max_length: int = 2000) -> str:
    """
    Sanitizes user input string against Prompt Injection, Command Injection, and buffer overflow attempts.
    """
    if not text:
        return ""
    
    # 1. Enforce length boundary
    cleaned = text.strip()[:max_length]

    # 2. Check for Prompt Injection Attack patterns
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            raise HTTPException(
                status_code=400,
                detail="Güvenlik Uyarısı: Girdinizde geçersiz veya potansiyel zararlı komut deseni tespit edildi (Prompt Injection Defense)."
            )

    # 3. Escape HTML control tags
    cleaned = cleaned.replace("<script>", "").replace("</script>", "")
    
    return cleaned
