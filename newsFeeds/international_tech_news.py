import feedparser
from fastapi import HTTPException
import os
from dotenv import load_dotenv
import html

load_dotenv()


def toi_tech():
    rss_url = os.getenv("TOI_TECH")
    try:
        feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in feeds.entries:
            news_title = clean_title(entry.title)
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
                "category": "Technology",
                "image": image_url,
                "publisher": 'Times of India Tech'
            })
        print(news_items)
        return news_items
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching TOI tech news: {str(e)}")


# def gadget_360_tech():
#     rss_url = os.getenv("GADGET_360_TECH")
#     try:
#         print(f"Fetching RSS from: {rss_url}")
#
#         # Add headers to avoid 403 Forbidden error
#         import urllib.request
#         import urllib.parse
#
#         # Create a request with browser-like headers
#         req = urllib.request.Request(
#             rss_url,
#             headers={
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#                 'Accept-Language': 'en-US,en;q=0.5',
#                 'Accept-Encoding': 'gzip, deflate',
#                 'Connection': 'keep-alive',
#                 'Upgrade-Insecure-Requests': '1',
#             }
#         )
#
#         # Open the URL with headers
#         with urllib.request.urlopen(req) as response:
#             rss_content = response.read()
#
#         # Parse the RSS content
#         feeds = feedparser.parse(rss_content)
#         print(f"Feed status: {feeds.status if hasattr(feeds, 'status') else 'No status'}")
#         print(f"Number of entries: {len(feeds.entries) if hasattr(feeds, 'entries') else 'No entries'}")
#
#         if hasattr(feeds, 'entries'):
#             print(f"First entry keys: {list(feeds.entries[0].keys()) if feeds.entries else 'No entries'}")
#
#         news_items = []
#         for entry in feeds.entries:
#             print(f"Processing entry: {entry.title if hasattr(entry, 'title') else 'No title'}")
#
#             news_title = clean_title(entry.title) if hasattr(entry, 'title') else 'No Title'
#             # Gadgets 360 RSS doesn't contain image tags, so set to None
#             image_url = None
#
#             # Extract description and content from the description field
#             description = getattr(entry, 'description', '')
#             content = getattr(entry, 'description', '')  # Use description as content since there's no separate summary
#
#             # Extract category from the category field
#             category = getattr(entry, 'category', 'Technology')
#
#             # Extract link and pubDate
#             link = getattr(entry, 'link', '')
#             pub_date = getattr(entry, 'published', '')
#
#             news_items.append({
#                 "title": news_title,
#                 "description": description,
#                 "content": content,
#                 "link": link,
#                 "pubDate": pub_date,
#                 "category": category,
#                 "image": image_url,
#                 "publisher": 'Gadgets 360'
#             })
#
#         print(f"Final news_items: {news_items}")
#         return news_items
#     except Exception as e:
#         print(f"Error in gadget_360_tech: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error fetching Gadgets 360 news: {str(e)}")


def tech_crunch():
    rss_url = os.getenv("TECH_CRUNCH")
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
                "category": "Technology",
                "image": entry.media_thumbnail[0]['url'] if hasattr(entry,
                                                                    'media_thumbnail') and entry.media_thumbnail else None,
                "publisher": 'TechCrunch'
            })
        print(news_items)
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching TechCrunch news: {str(e)}")


def clean_title(news_item):
    # Decode HTML entities in a loop until all are unescaped
    while True:
        decoded_title = html.unescape(news_item)
        if decoded_title == news_item:  # Stop when no further decoding is needed
            break
        news_item = decoded_title
    return news_item


tech_crunch()
