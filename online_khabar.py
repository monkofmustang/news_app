import feedparser
import re
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()


def ok_np():
    rss_url = os.getenv("ONLINE_KHABAR_NP")
    placeholder_image_url = os.getenv("NULL_IMAGES")
    try:
        ok_nep_feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in ok_nep_feeds.entries:
            content_value = entry.content[0].value if hasattr(entry.content, '__getitem__') and len(
                entry.content) > 0 else None
            image_url_match = re.search(r'(https?://\S+\.jpg)', content_value)
            image_url = image_url_match.group(0) if image_url_match else None
            news_items.append({
                "title": entry.title,
                "description": entry.description,
                "content": entry.content[0].value,
                "link": entry.link,
                "pubDate": entry.published,
                "category": entry.category,
                "image": image_url if image_url else placeholder_image_url
            })
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
    # news_json = json.dumps(news_items, ensure_ascii=False, indent=4)
    # # print(news_json)
    # return news_json


def ok_en():
    rss_url = os.getenv("ONLINE_KHABAR_EN")
    placeholder_image_url = os.getenv("NULL_IMAGES")
    try:
        ok_nep_feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in ok_nep_feeds.entries:
            content_value = entry.content[0].value if hasattr(entry.content, '__getitem__') and len(
                entry.content) > 0 else None
            image_url_match = re.search(r'(https?://\S+\.jpg)', content_value)
            image_url = image_url_match.group(0) if image_url_match else None
            news_items.append({
                "title": entry.title,
                "description": entry.description,
                "content": entry.content[0].value,
                "link": entry.link,
                "pubDate": entry.published,
                "category": entry.category,
                "image": image_url if image_url else placeholder_image_url
            })
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
    # news_json = json.dumps(news_items, ensure_ascii=False, indent=4)
    # # print(news_json)
    # return news_json
