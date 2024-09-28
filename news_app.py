from fastapi import FastAPI, Query, HTTPException
from typing import Optional
import news_service

app = FastAPI()


@app.get("/news/", status_code=200)
def get_news(language: Optional[str] = Query("en", description="Language of the news feed")):
    try:
        news = news_service.summarise_news(language)
        if not news:
            raise HTTPException(status_code=404, detail="No news found")
        return {"status": "success", "data": news}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
