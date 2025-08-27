from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from db.db_connection import get_db
from models.news import News, NewsResponse
from service.tech_news_service import TechNewsService, process_tech_news
from sqlalchemy import and_

router = APIRouter(
    prefix="/tech-news",
    tags=["Tech News"],
)


@router.post("/process", response_model=Dict[str, Any])
async def process_tech_news_endpoint(background_tasks: BackgroundTasks):
    """
    Process tech news: fetch from all sources and save to database
    This endpoint runs the processing in the background
    """
    try:
        # Run the processing in background
        background_tasks.add_task(process_tech_news)
        
        return {
            "status": "success",
            "message": "Tech news processing started in background",
            "note": "Check the logs for processing status"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting tech news processing: {str(e)}")


@router.post("/process-sync", response_model=Dict[str, Any])
async def process_tech_news_sync():
    """
    Process tech news synchronously: fetch and save
    This endpoint waits for the processing to complete
    """
    try:
        result = process_tech_news()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing tech news: {str(e)}")


@router.get("/", response_model=List[NewsResponse])
async def get_tech_news(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get tech news from database
    """
    try:
        news_items = db.query(News).filter(
            News.tag == "tech_news"
        ).order_by(
            News.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tech news: {str(e)}")


@router.get("/{news_id}", response_model=NewsResponse)
async def get_tech_news_by_id(
    news_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific tech news item by ID
    """
    try:
        news_item = db.query(News).filter(
            and_(
                News.id == news_id,
                News.tag == "tech_news"
            )
        ).first()
        
        if not news_item:
            raise HTTPException(status_code=404, detail="Tech news item not found")
        
        return news_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tech news: {str(e)}")


@router.delete("/{news_id}")
async def delete_tech_news(
    news_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific tech news item by ID
    """
    try:
        news_item = db.query(News).filter(
            and_(
                News.id == news_id,
                News.tag == "tech_news"
            )
        ).first()
        
        if not news_item:
            raise HTTPException(status_code=404, detail="Tech news item not found")
        
        db.delete(news_item)
        db.commit()
        
        return {"message": "Tech news item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting tech news: {str(e)}")


@router.get("/stats/summary")
async def get_tech_news_stats(db: Session = Depends(get_db)):
    """
    Get statistics about tech news in the database
    """
    try:
        total_news = db.query(News).filter(News.tag == "tech_news").count()
        
        return {
            "total_news": total_news,
            "tag": "tech_news"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tech news stats: {str(e)}")
