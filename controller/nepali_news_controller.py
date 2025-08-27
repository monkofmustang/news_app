from fastapi import APIRouter, HTTPException
from typing import Optional
from service.nepali_news_service import process_nepali_news
from db.db_connection import get_db
from models.news import News
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/nepali-news",
    tags=["Nepali News"],
)


@router.post("/process", status_code=200)
def process_nepali_news_endpoint():
    """
    Process and save Nepali news from all sources to database
    """
    try:
        result = process_nepali_news()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing Nepali news: {str(e)}")


@router.get("/", status_code=200)
def get_nepali_news(language: Optional[str] = None, limit: Optional[int] = 50):
    """
    Get Nepali news from database
    language: 'np' for Nepali, 'en' for English, None for all
    limit: maximum number of news items to return
    """
    try:
        db = next(get_db())
        
        # Determine tag based on language
        if language == 'np':
            tag = "nepaliNewsNp"
        elif language == 'en':
            tag = "nepaliNewsEn"
        else:
            # Return all Nepali news (both languages)
            news_items = db.query(News).filter(
                News.tag.in_(["nepaliNewsNp", "nepaliNewsEn"])
            ).order_by(News.created_at.desc()).limit(limit).all()
            
            return {
                "status": "success",
                "data": [
                    {
                        "id": item.id,
                        "title": item.title,
                        "description": item.description,
                        "content": item.content,
                        "link": item.link,
                        "pub_date": item.pub_date,
                        "category": item.category,
                        "image": item.image,
                        "publisher": item.publisher,
                        "tag": item.tag,
                        "summary": item.summary,
                        "is_summarized": item.is_summarized,
                        "created_at": item.created_at,
                        "updated_at": item.updated_at
                    }
                    for item in news_items
                ],
                "count": len(news_items)
            }
        
        # Get news for specific language
        news_items = db.query(News).filter(
            News.tag == tag
        ).order_by(News.created_at.desc()).limit(limit).all()
        
        return {
            "status": "success",
            "data": [
                {
                    "id": item.id,
                    "title": item.title,
                    "description": item.description,
                    "content": item.content,
                    "link": item.link,
                    "pub_date": item.pub_date,
                    "category": item.category,
                    "image": item.image,
                    "publisher": item.publisher,
                    "tag": item.tag,
                    "summary": item.summary,
                    "is_summarized": item.is_summarized,
                    "created_at": item.created_at,
                    "updated_at": item.updated_at
                }
                for item in news_items
            ],
            "count": len(news_items),
            "language": language
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving Nepali news: {str(e)}")
    finally:
        db.close()


@router.get("/stats", status_code=200)
def get_nepali_news_stats():
    """
    Get statistics about Nepali news in database
    """
    try:
        db = next(get_db())
        
        # Count news by tag
        np_count = db.query(News).filter(News.tag == "nepaliNewsNp").count()
        en_count = db.query(News).filter(News.tag == "nepaliNewsEn").count()
        total_count = np_count + en_count
        
        # Get latest news dates
        latest_np = db.query(News).filter(News.tag == "nepaliNewsNp").order_by(News.created_at.desc()).first()
        latest_en = db.query(News).filter(News.tag == "nepaliNewsEn").order_by(News.created_at.desc()).first()
        
        return {
            "status": "success",
            "stats": {
                "total_news": total_count,
                "nepali_news": {
                    "count": np_count,
                    "latest_news_date": latest_np.created_at if latest_np else None
                },
                "english_news": {
                    "count": en_count,
                    "latest_news_date": latest_en.created_at if latest_en else None
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving Nepali news stats: {str(e)}")
    finally:
        db.close()
