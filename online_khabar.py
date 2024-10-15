import feedparser
import re
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import requests

load_dotenv()


# def ok_np():
#     rss_url = os.getenv("ONLINE_KHABAR_NP")
#     try:
#         ok_nep_feeds = feedparser.parse(rss_url)
#         print(ok_nep_feeds)
#         news_items = []
#         for entry in ok_nep_feeds.entries:
#             content_value = entry.content[0].value if hasattr(entry.content, '__getitem__') and len(
#                 entry.content) > 0 else None
#             image_url_match = re.search(r'(https?://\S+\.jpg)', content_value)
#             image_url = image_url_match.group(0) if image_url_match else None
#             soup = BeautifulSoup(content_value, "html.parser")
#             content_text = soup.get_text(separator="\n")
#             news_items.append({
#                 "title": entry.title,
#                 "description": entry.description,
#                 "content": content_text,
#                 "link": entry.link,
#                 "pubDate": entry.published,
#                 "category": entry.category,
#                 "image": image_url,
#                 "publisher": 'Online Khabar'
#             })
#         return news_items
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
# news_json = json.dumps(news_items, ensure_ascii=False, indent=4)
# # print(news_json)
# return news_json


def ok_en():
    rss_url = os.getenv("ONLINE_KHABAR_EN")
    try:
        ok_nep_feeds = feedparser.parse(rss_url)
        news_items = []
        for entry in ok_nep_feeds.entries:
            content_value = entry.content[0].value if hasattr(entry.content, '__getitem__') and len(
                entry.content) > 0 else None
            image_url_match = re.search(r'(https?://\S+\.jpg)', content_value)
            image_url = image_url_match.group(0).replace("http", "https") if image_url_match else None
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
                "publisher": 'Online Khabar'
            })
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
    # news_json = json.dumps(news_items, ensure_ascii=False, indent=4)
    # # print(news_json)
    # return news_json


def ok_np():
    rss_url = os.getenv("ONLINE_KHABAR_NP")
    try:
        response = requests.get(rss_url)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        news_items = []

        for item in root.findall('./channel/item'):
            title = item.find('title').text
            description = item.find('description').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text

            image_url = item.find('image')
            image_url = image_url.text if image_url is not None else None

            content = item.find('{http://purl.org/rss/1.0/modules/content/}encoded')
            content_value = content.text if content is not None else ''

            if not image_url and content_value:
                soup = BeautifulSoup(content_value, "html.parser")
                image_tag = soup.find('img')
                if image_tag and 'src' in image_tag.attrs:
                    image_url = image_tag['src']

            content_text = BeautifulSoup(content_value, "html.parser").get_text(separator="\n")

            # Add the news item
            news_items.append({
                "title": title,
                "description": description,
                "content": content_text,
                "link": link,
                "pubDate": pub_date,
                "image": image_url,  # Image from <image> tag or <img> tag in content
                "publisher": 'Online Khabar'
            })
        return news_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")
