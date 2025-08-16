import feedparser
from fastapi import HTTPException
import os
from dotenv import load_dotenv
import html

load_dotenv()


def un_news():
    rss_url = os.getenv("UN_NEWS")
    try:
        feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in feeds.entries:
            news_title = clean_title(entry.title)
            # Extract image from enclosure tag for UN News
            image_url = None
            if hasattr(entry, 'enclosures') and entry.enclosures:
                for enclosure in entry.enclosures:
                    if enclosure.get('type', '').startswith('image/'):
                        image_url = enclosure.get('url')
                        break
            
            news_items.append({
                "title": news_title,
                "description": entry.title_detail.value,
                "content": entry.summary_detail.value,
                "link": entry.link,
                "pubDate": entry.published,
                "category": "News",
                "image": image_url,
                "publisher": 'UN News'
            })
        print(news_items)
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching UN news: {str(e)}")


# def cnbc_news():
#     rss_url = os.getenv("CNBC_NEWS")
#     try:
#         feeds = feedparser.parse(rss_url)
#         news_items = []
#         for entry in feeds.entries:
#             news_title = clean_title(entry.title)
#             news_items.append({
#                 "title": news_title,
#                 "description": entry.title_detail.value,
#                 "content": entry.summary_detail.value,
#                 "link": entry.link,
#                 "pubDate": entry.published,
#                 "category": "Business",
#                 "image": entry.media_thumbnail[0]['url'] if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail else None,
#                 "publisher": 'CNBC'
#             })
#         print(news_items)
#         return news_items
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching CNBC news: {str(e)}")


def toi_news():
    rss_url = os.getenv("TOI_NEWS")
    try:
        feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in feeds.entries:
            news_title = clean_title(entry.title)
            # Extract image from enclosure tag for TOI News
            image_url = None
            if hasattr(entry, 'enclosures') and entry.enclosures:
                for enclosure in entry.enclosures:
                    if enclosure.get('type', '').startswith('image/'):
                        image_url = enclosure.get('url')
                        # Fix TOI image URL format: remove .cms and add .jpeg
                        if image_url and 'toiimg.com' in image_url:
                            base_url = image_url.split('.cms')[0]
                            image_url = f"{base_url}.jpeg"
                        break
            
            news_items.append({
                "title": news_title,
                "description": entry.title_detail.value,
                "content": entry.summary_detail.value,
                "link": entry.link,
                "pubDate": entry.published,
                "category": "News",
                "image": image_url,
                "publisher": 'Times of India'
            })
        print(news_items)
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching TOI news: {str(e)}")


def the_hindu_international():
    rss_url = os.getenv("THE_HINDU_INTERNATIONAL")
    try:
        feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in feeds.entries:
            news_title = clean_title(entry.title)
            # Extract image from media:content tag for The Hindu
            image_url = None
            if hasattr(entry, 'media_content') and entry.media_content:
                for media in entry.media_content:
                    if media.get('medium') == 'image':
                        image_url = media.get('url')
                        break
            
            news_items.append({
                "title": news_title,
                "description": entry.title_detail.value,
                "content": entry.summary_detail.value,
                "link": entry.link,
                "pubDate": entry.published,
                "category": "International",
                "image": image_url,
                "publisher": 'The Hindu International'
            })
        print(news_items)
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching The Hindu International news: {str(e)}")


def nyt_world():
    rss_url = os.getenv("NYT_WORLD")
    try:
        feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in feeds.entries:
            news_title = clean_title(entry.title)
            # Extract image from media:content tag for NYT
            image_url = None
            if hasattr(entry, 'media_content') and entry.media_content:
                for media in entry.media_content:
                    if media.get('medium') == 'image':
                        image_url = media.get('url')
                        break
            
            news_items.append({
                "title": news_title,
                "description": entry.title_detail.value,
                "content": entry.summary_detail.value,
                "link": entry.link,
                "pubDate": entry.published,
                "category": "World",
                "image": image_url,
                "publisher": 'The New York Times World'
            })
        print(news_items)
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching NYT World news: {str(e)}")


def clean_title(news_item):
    # Decode HTML entities in a loop until all are unescaped
    while True:
        decoded_title = html.unescape(news_item)
        if decoded_title == news_item:  # Stop when no further decoding is needed
            break
        news_item = decoded_title
    return news_item


nyt_world()
