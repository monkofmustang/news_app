import feedparser
import re
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()


def ok_en():
    rss_url = os.getenv("NEPAL_NEWS_EN")
    try:
        ok_nep_feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in ok_nep_feeds.entries:
            content_value = entry.content[0].value if hasattr(entry.content, '__getitem__') and len(
                entry.content) > 0 else None
            image_url_match = re.search(r'(https?://[^\s]+\.jpg)', content_value)
            image_url = image_url_match.group(0).replace("768", "1024") if image_url_match else None
            soup = BeautifulSoup(content_value, "html.parser")
            content_text = soup.get_text(separator="\n")
            news_items.append({
                "title": entry.title,
                "description": entry.description if entry.description != '' else entry.title,
                "content": content_text,
                "link": entry.link,
                "pubDate": entry.published,
                "category": entry.category,
                "image": image_url,
                "publisher": 'Nepal News'
            })
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
    # news_json = json.dumps(news_items, ensure_ascii=False, indent=4)
    # # print(news_json)
    # return news_json
