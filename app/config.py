import os
from dotenv import load_dotenv
from crewai import LLM

def get_llm():
    """
    Dynamically loads API keys from .env file or environment variables.
    Automatically detects OpenAI API Key or Gemini API Key.
    """
    # Reload environment variables to catch any runtime updates to .env
    load_dotenv(override=True)

    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    model_env = os.getenv("MODEL", "").strip()

    if openai_key and not openai_key.startswith("your_"):
        model_name = model_env if model_env else "gpt-4o-mini"
        print(f"[LLM] Using OpenAI Model: {model_name}")
        return LLM(
            model=model_name,
            api_key=openai_key,
            temperature=0.7
        )
    elif gemini_key and not gemini_key.startswith("your_"):
        model_name = model_env if model_env else "gemini/gemini-1.5-flash"
        print(f"[LLM] Using Gemini Model: {model_name}")
        return LLM(
            model=model_name,
            api_key=gemini_key,
            temperature=0.7
        )
    else:
        # Fallback default
        model_name = model_env if model_env else "gpt-4o-mini"
        print("[WARNING] No valid OPENAI_API_KEY or GEMINI_API_KEY found in .env file.")
        return LLM(
            model=model_name,
            api_key=openai_key or gemini_key or "",
            temperature=0.7
        )
