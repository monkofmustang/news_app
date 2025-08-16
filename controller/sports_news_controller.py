from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from db.db_connection import get_db
from models.news import News, NewsResponse
from service.sports_news_service import SportsNewsService, process_sports_news
from sqlalchemy import and_

router = APIRouter(
    prefix="/sports-news",
    tags=["Sports News"],
)


@router.post("/process", response_model=Dict[str, Any])
async def process_sports_news_endpoint(background_tasks: BackgroundTasks):
    """
    Process sports news: fetch from all sources and save to database
    This endpoint runs the processing in the background
    """
    try:
        # Run the processing in background
        background_tasks.add_task(process_sports_news)
        
        return {
            "status": "success",
            "message": "Sports news processing started in background",
            "note": "Check the logs for processing status"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting sports news processing: {str(e)}")


@router.post("/process-sync", response_model=Dict[str, Any])
async def process_sports_news_sync():
    """
    Process sports news synchronously: fetch and save
    This endpoint waits for the processing to complete
    """
    try:
        result = process_sports_news()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing sports news: {str(e)}")


@router.get("/", response_model=List[NewsResponse])
async def get_sports_news(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get sports news from database
    """
    try:
        news_items = db.query(News).filter(
            News.tag == "sports_news"
        ).order_by(
            News.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sports news: {str(e)}")


@router.get("/{news_id}", response_model=NewsResponse)
async def get_sports_news_by_id(
    news_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific sports news item by ID
    """
    try:
        news_item = db.query(News).filter(
            and_(
                News.id == news_id,
                News.tag == "sports_news"
            )
        ).first()
        
        if not news_item:
            raise HTTPException(status_code=404, detail="Sports news item not found")
        
        return news_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sports news: {str(e)}")


@router.delete("/{news_id}")
async def delete_sports_news(
    news_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific sports news item by ID
    """
    try:
        news_item = db.query(News).filter(
            and_(
                News.id == news_id,
                News.tag == "sports_news"
            )
        ).first()
        
        if not news_item:
            raise HTTPException(status_code=404, detail="Sports news item not found")
        
        db.delete(news_item)
        db.commit()
        
        return {"message": "Sports news item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting sports news: {str(e)}")


@router.get("/stats/summary")
async def get_sports_news_stats(db: Session = Depends(get_db)):
    """
    Get statistics about sports news in the database
    """
    try:
        total_news = db.query(News).filter(News.tag == "sports_news").count()
        
        return {
            "total_news": total_news,
            "tag": "sports_news"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sports news stats: {str(e)}")
