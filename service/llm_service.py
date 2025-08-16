import os
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from openai import OpenAI


# Ensure .env is loaded for local/dev environments
load_dotenv()


_HF_TOKEN_ENV_KEY = "HF_TOKEN"
_HF_ROUTER_BASE_URL = "https://router.huggingface.co/v1"


def _get_openai_client(explicit_token: Optional[str] = None) -> OpenAI:
    token = explicit_token or os.getenv(_HF_TOKEN_ENV_KEY)
    if not token:
        raise RuntimeError(
            f"Environment variable '{_HF_TOKEN_ENV_KEY}' is required but was not found."
        )
    return OpenAI(base_url=_HF_ROUTER_BASE_URL, api_key=token)


def chat_completion(
    messages: List[Dict[str, str]],
    model: str = "openai/gpt-oss-20b:fireworks-ai",
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
    explicit_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Call the HF router using OpenAI SDK chat.completions API shape.

    Args:
        messages: List of {"role": "user|system|assistant", "content": str}
        model: Model identifier as expected by the HF router
        temperature: Sampling temperature
        max_tokens: Optional max tokens for the response
        top_p: Optional nucleus sampling
        explicit_token: Bypass env var and use this token instead

    Returns:
        Raw completion dict as returned by the OpenAI SDK.
    """
    try:
        client = _get_openai_client(explicit_token)
        
        params: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        if top_p is not None:
            params["top_p"] = top_p
        
        completion = client.chat.completions.create(**params)
        
        # Normalize to a convenient shape for callers in our app
        choice = completion.choices[0].message if completion and completion.choices else None
        
        result = {
            "id": getattr(completion, "id", None),
            "model": getattr(completion, "model", model),
            "usage": getattr(completion, "usage", None),
            "message": choice,
            "raw": completion,
        }
        return result
    except Exception as e:
        print(f"ERROR in chat_completion: {e}")
        raise


def ask_plaintext(prompt: str, model: str = "openai/gpt-oss-20b:fireworks-ai") -> str:
    """Convenience helper that returns assistant message content as string."""
    try:
        result = chat_completion(messages=[{"role": "user", "content": prompt}], model=model)
        message = result.get("message")
        
        # Handle both dict and ChatCompletionMessage objects
        if hasattr(message, 'content'):
            # It's a ChatCompletionMessage object
            return message.content
        elif isinstance(message, dict):
            # It's a dict
            return message.get("content", "")
        else:
            return ""
    except Exception as e:
        print(f"ERROR in ask_plaintext: {e}")
        raise


def detect_language(text: str) -> str:
    """Simple language detection based on character sets."""
    # Check for Nepali characters (Devanagari script)
    nepali_chars = set('अआइईउऊऋएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञड़ढ़')
    
    # Count Nepali characters
    nepali_count = sum(1 for char in text if char in nepali_chars)
    
    # If more than 30% of characters are Nepali, consider it Nepali
    if nepali_count > len(text) * 0.3:
        return "nepali"
    else:
        return "english"


def summarize_news(news_content: str, model: str = "openai/gpt-oss-20b:fireworks-ai") -> str:
    """Generate a 60-word news summary using the professional news summarizer system prompt."""
    system_prompt = """You are a master news summarizer and headline writer whose mission is to create exactly 60 words that are impossible to ignore for a user to open and read the full story. Your summaries must:

1. **HOOK the reader immediately** with a compelling opening that creates curiosity
2. **REVEAL the core story** with enough detail to inform but not satisfy completely
3. **CREATE urgency and intrigue** by hinting at consequences, implications, or shocking details
4. **USE emotional triggers** like "shocking," "unprecedented," "revolutionary," "controversial," "exclusive"
5. **END with a cliffhanger** that makes the reader desperate to know more
6. **MAINTAIN journalistic integrity** while being irresistibly clickable

**TECHNIQUES TO USE:**
- Start with action words: "BREAKING," "EXCLUSIVE," "SHOCKING," "REVOLUTIONARY"
- Include numbers, percentages, or specific impacts when possible
- Mention "what happens next" or "implications for everyone"
- Use phrases like "but that's not all," "here's why it matters," "the real story is..."
- End with questions or incomplete thoughts that demand answers

Your goal: Make every reader think "I MUST read the full story NOW!"

IMPORTANT: Detect the language of the input news content and respond in the SAME language. If the input is in Nepali (नेपाली), respond in Nepali. If the input is in English, respond in English. If the input is in any other language, respond in that language."""
    
    user_prompt = f"Transform this news article into exactly 60 words that will convince ANY reader to click and read the full story. Make it irresistible and impossible to ignore:\n\n{news_content}"
    
    try:
        result = chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=model
        )
        message = result.get("message")
        
        # Handle both dict and ChatCompletionMessage objects
        if hasattr(message, 'content'):
            return message.content
        elif isinstance(message, dict):
            return message.get("content", "")
        else:
            return ""
    except Exception as e:
        print(f"ERROR in summarize_news: {e}")
        raise


