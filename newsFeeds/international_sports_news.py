import feedparser
from fastapi import HTTPException
import os
from dotenv import load_dotenv
import html

load_dotenv()


def the_hindu_sports():
    rss_url = os.getenv("THE_HINDU_SPORTS")
    try:
        feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in feeds.entries:
            image_url = None
            if hasattr(entry, 'media_content') and entry.media_content:
                for media in entry.media_content:
                    if media.get('medium') == 'image':
                        image_url = media.get('url')
                        break
            news_title = clean_title(entry.title)
            news_items.append({
                "title": news_title,
                "description": entry.title_detail.value,
                "content": entry.summary_detail.value,
                "link": entry.link,
                "pubDate": entry.published,
                "category": "Sports",
                "image": image_url,
                "publisher": 'The Hindu Sports'
            })
        print(news_items)
        return news_items
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching The Hindu Sports news: {str(e)}")


def the_himalayan_times_sports():
    rss_url = os.getenv("THE_HIMALAYAN_TIMES_SPORTS")
    try:
        feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in feeds.entries:
            news_title = clean_title(entry.title)
            news_items.append({
                "title": news_title,
                "description": entry.title_detail.value,
                "content": entry.summary_detail.value,
                "link": entry.link,
                "pubDate": entry.published,
                "category": "Sports",
                "image": entry.media_thumbnail[0]['url'] if hasattr(entry,
                                                                    'media_thumbnail') and entry.media_thumbnail else None,
                "publisher": 'The Himalayan Times Sports'
            })
        print(news_items)
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching The Himalayan Times Sports news: {str(e)}")


def clean_title(news_item):
    # Decode HTML entities in a loop until all are unescaped
    while True:
        decoded_title = html.unescape(news_item)
        if decoded_title == news_item:  # Stop when no further decoding is needed
            break
        news_item = decoded_title
    return news_item


the_himalayan_times_sports()
