import feedparser
from fastapi import HTTPException
import os
from dotenv import load_dotenv
import html

load_dotenv()


def ok_en():
    rss_url = os.getenv("THE_HIMALAYAN_EN")
    try:
        ok_nep_feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in ok_nep_feeds.entries:
            news_title = clean_title(entry.title)
            news_items.append({
                "title": news_title,
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


def clean_title(news_item):
    # Decode HTML entities in a loop until all are unescaped
    while True:
        decoded_title = html.unescape(news_item)
        if decoded_title == news_item:  # Stop when no further decoding is needed
            break
        news_item = decoded_title
    return news_item
