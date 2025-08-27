from fastapi import APIRouter, FastAPI, Query, HTTPException
from typing import Optional
from service import news_service, international_news_service, sports_news_service, tech_news_service

app = FastAPI()

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

@router.get("/international", status_code=200)
def get_international_news():
    print("Fetching international news directly from sources")
    try:
        service = international_news_service.InternationalNewsService()
        news = service.fetch_all_international_news()
        if not news:
            raise HTTPException(status_code=404, detail="No international news found")
        return {"status": "success", "data": news}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/sports", status_code=200)
def get_sports_news():
    print("Fetching sports news directly from sources")
    try:
        service = sports_news_service.SportsNewsService()
        news = service.fetch_all_sports_news()
        if not news:
            raise HTTPException(status_code=404, detail="No sports news found")
        return {"status": "success", "data": news}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/tech", status_code=200)
def get_tech_news():
    print("Fetching tech news directly from sources")
    try:
        service = tech_news_service.TechNewsService()
        news = service.fetch_all_tech_news()
        if not news:
            raise HTTPException(status_code=404, detail="No tech news found")
        # Sort news by pubDate descending, always using offset-aware datetimes
        from datetime import datetime, timezone
        def parse_pubdate(item):
            pubdate = item.get("pubDate", "")
            try:
                # Always parse as offset-aware
                return datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")
            except Exception:
                # Fallback: return a very old offset-aware datetime
                return datetime.min.replace(tzinfo=timezone.utc)
        news.sort(key=parse_pubdate, reverse=True)
        return {"status": "success", "data": news}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
