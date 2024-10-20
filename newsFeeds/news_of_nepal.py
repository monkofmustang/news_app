import os
import feedparser
from fastapi import HTTPException
import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()


def non_np():
    rss_url = os.getenv("NEWS_OF_NEPAL")
    try:
        feed = feedparser.parse(rss_url)
        news_items = []
        for entry in feed.entries:
            content_value = entry.content[0].value if hasattr(entry.content, '__getitem__') and len(
                entry.content) > 0 else None
            image_url_match = re.search(r'(https?://[^\s]+(?:\.jpeg|\.jpg))', content_value)
            image_url = image_url_match.group(0).replace("-150x150","") if image_url_match else None
            soup = BeautifulSoup(content_value, "html.parser")
            content_text = soup.get_text(separator="\n")
            news_items.append({
                "title": entry.title,
                "description": entry.description,
                "content": content_text,
                "link": entry.link,
                "pubDate": entry.published,
                "category": entry.category,
                "image": image_url,
                "publisher": 'News Of Nepal'
            })
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
