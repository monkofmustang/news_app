import feedparser
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()


def ok_en():
    rss_url = os.getenv("THE_HIMALAYAN_EN")
    try:
        ok_nep_feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in ok_nep_feeds.entries:
            news_items.append({
                "title": entry.title,
                "description": entry.title_detail.value,
                "content": entry.summary_detail.value,
                "link": entry.link,
                "pubDate": entry.published,
                "category": "News",
                "image": entry.media_thumbnail[0]['url'] if entry.media_thumbnail[0]['url'] else None,
                "publisher": 'THE HIMALAYAN TIMES'
            })
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
    # news_json = json.dumps(news_items, ensure_ascii=False, indent=4)
    # # print(news_json)
    # return news_json
