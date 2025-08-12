from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from service import news_service

router = APIRouter(
    prefix="/news",  # All routes will be prefixed with /news
    tags=["News"],  # Tag for grouping in the documentation
)


@router.get("/", status_code=200)
def get_news(language: Optional[str] = Query("en", description="Language of the news feed")):
    print("Fetching news for language: ", language)
    try:
        news = news_service.summarise_news(language)
        if not news:
            raise HTTPException(status_code=404, detail="No news found")
        return {"status": "success", "data": news}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
