from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from db.db_connection import get_db
from models.news import News, NewsResponse
from service.international_news_service import InternationalNewsService, process_international_news
from sqlalchemy import and_

router = APIRouter(
    prefix="/international-news",
    tags=["International News"],
)


@router.post("/process", response_model=Dict[str, Any])
async def process_international_news_endpoint(background_tasks: BackgroundTasks):
    """
    Process international news: fetch from all sources, save to database, and summarize
    This endpoint runs the processing in the background
    """
    try:
        # Run the processing in background
        background_tasks.add_task(process_international_news)
        
        return {
            "status": "success",
            "message": "International news processing started in background",
            "note": "Check the logs for processing status"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting news processing: {str(e)}")


@router.post("/process-sync", response_model=Dict[str, Any])
async def process_international_news_sync():
    """
    Process international news synchronously: fetch, save, and summarize
    This endpoint waits for the processing to complete
    """
    try:
        result = process_international_news()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing news: {str(e)}")


@router.get("/", response_model=List[NewsResponse])
async def get_international_news(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get international news from database
    """
    try:
        news_items = db.query(News).filter(
            News.tag == "international_news"
        ).order_by(
            News.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@router.get("/summarized", response_model=List[NewsResponse])
async def get_summarized_international_news(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get only summarized international news from database
    """
    try:
        news_items = db.query(News).filter(
            and_(
                News.tag == "international_news",
                News.is_summarized == True
            )
        ).order_by(
            News.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching summarized news: {str(e)}")


@router.get("/{news_id}", response_model=NewsResponse)
async def get_international_news_by_id(
    news_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific international news item by ID
    """
    try:
        news_item = db.query(News).filter(
            and_(
                News.id == news_id,
                News.tag == "international_news"
            )
        ).first()
        
        if not news_item:
            raise HTTPException(status_code=404, detail="News item not found")
        
        return news_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@router.delete("/{news_id}")
async def delete_international_news(
    news_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific international news item by ID
    """
    try:
        news_item = db.query(News).filter(
            and_(
                News.id == news_id,
                News.tag == "international_news"
            )
        ).first()
        
        if not news_item:
            raise HTTPException(status_code=404, detail="News item not found")
        
        db.delete(news_item)
        db.commit()
        
        return {"message": "News item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting news: {str(e)}")


@router.post("/summarize/{news_id}")
async def summarize_specific_news(
    news_id: int,
    db: Session = Depends(get_db)
):
    """
    Manually trigger summarization for a specific news item
    """
    try:
        news_item = db.query(News).filter(
            and_(
                News.id == news_id,
                News.tag == "international_news"
            )
        ).first()
        
        if not news_item:
            raise HTTPException(status_code=404, detail="News item not found")
        
        if news_item.is_summarized and news_item.summary:
            return {"message": "News item already summarized", "summary": news_item.summary}
        
        # Prepare content for summarization
        content_to_summarize = ""
        if news_item.description:
            content_to_summarize += news_item.description + "\n\n"
        if news_item.content:
            content_to_summarize += news_item.content
        
        if not content_to_summarize.strip():
            raise HTTPException(status_code=400, detail="No content available to summarize")
        
        # Generate summary
        from service.llm_service import summarize_news
        from datetime import datetime
        
        summary = summarize_news(content_to_summarize)
        
        # Update the news item
        news_item.summary = summary
        news_item.is_summarized = True
        news_item.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "message": "News item summarized successfully",
            "summary": summary
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing news: {str(e)}")


@router.get("/stats/summary")
async def get_international_news_stats(db: Session = Depends(get_db)):
    """
    Get statistics about international news in the database
    """
    try:
        total_news = db.query(News).filter(News.tag == "international_news").count()
        summarized_news = db.query(News).filter(
            and_(
                News.tag == "international_news",
                News.is_summarized == True
            )
        ).count()
        
        return {
            "total_news": total_news,
            "summarized_news": summarized_news,
            "pending_summarization": total_news - summarized_news,
            "summarization_percentage": round((summarized_news / total_news * 100) if total_news > 0 else 0, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")
