import feedparser
import re
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()
def ob_news_np():
    rss_url = os.getenv("OUR_BIRATNAGAR_NP")
    try:
        feed = feedparser.parse(rss_url)
        news_items = []
        for entry in feed.entries:
            content_value = entry.content[0].value if hasattr(entry.content, '__getitem__') and len(
                entry.content) > 0 else None
            image_url_match = re.search(r'(https?://[^\s]+\.jpeg)', content_value)
            image_url = image_url_match.group(0) if image_url_match else None
            news_items.append({
                "title": entry.title,
                "description": entry.description,
                "content": entry.content[0].value,
                "link": entry.link,
                "pubDate": entry.published,
                "category": entry.category,
                "image": image_url
            })
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
    # news_json = json.dumps(news_items, ensure_ascii=False, indent=4)
    #
    # return news_json
