from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

from service.llm_service import chat_completion, ask_plaintext, summarize_news, detect_language


class SummarizeRequest(BaseModel):
    news_content: str
    model: Optional[str] = None


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.get("/ask")
def ask_ai(q: str = Query(..., description="Prompt to send to the model"), model: Optional[str] = None):
    try:
        content = ask_plaintext(q, model=model or "openai/gpt-oss-20b:fireworks-ai")
        return {"status": "success", "data": {"answer": content}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
def chat(messages: list[dict], model: Optional[str] = None):
    try:
        result = chat_completion(messages=messages, model=model or "openai/gpt-oss-20b:fireworks-ai")
        message = result.get("message")
        content = message.get("content", "") if isinstance(message, dict) else ""
        return {
            "status": "success",
            "data": {
                "answer": content,
                "raw": {
                    "id": result.get("id"),
                    "message": result.get("message"),
                    "model": result.get("model"),
                    "usage": result.get("usage"),
                },
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summarize")
def summarize_news_endpoint_post(request: SummarizeRequest):
    """Generate a 60-word news summary using the professional news summarizer."""
    try:
        detected_lang = detect_language(request.news_content)
        summary = summarize_news(request.news_content, model=request.model or "openai/gpt-oss-20b:fireworks-ai")
        return {
            "status": "success",
            "data": {
                "summary": summary,
                "word_count": len(summary.split()),
                "detected_language": detected_lang,
                "model": request.model or "openai/gpt-oss-20b:fireworks-ai"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summarize")
def summarize_news_endpoint_get(
    news_content: str = Query(..., description="News content to summarize"), 
    model: Optional[str] = Query(None, description="Model to use for summarization")
):
    """Generate a 60-word news summary using the professional news summarizer."""
    try:
        if not news_content or news_content.strip() == "":
            raise HTTPException(status_code=400, detail="news_content cannot be empty")
            
        detected_lang = detect_language(news_content)
        summary = summarize_news(news_content, model=model or "openai/gpt-oss-20b:fireworks-ai")
        return {
            "status": "success",
            "data": {
                "summary": summary,
                "word_count": len(summary.split()),
                "detected_language": detected_lang,
                "model": model or "openai/gpt-oss-20b:fireworks-ai"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


