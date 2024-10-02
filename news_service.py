import ob_news
import the_himalayan
import nepal_news
import online_khabar
import nagarik_news
from fastapi import HTTPException
import time
import random

cache = {}
CACHE_EXPIRY_TIME = 900


def cache_news_result(language: str, data):
    cache[language] = {
        "data": data,
        "expiry": time.time() + CACHE_EXPIRY_TIME
    }


def get_cached_news(language: str):
    if language in cache:
        cached_item = cache[language]
        # Check if cache item has expired
        if cached_item['expiry'] > time.time():
            return cached_item['data']
        else:
            del cache[language]  # Cache expired, remove it
    return None


def summarise_news(language: str = "en"):
    cached_news = get_cached_news(language)
    if cached_news:
        return cached_news
    combined_news = []
    try:
        if language == "en":
            ok_json = online_khabar.ok_en()
            nepal_news_json = nepal_news.ok_en()
            tht_json = the_himalayan.ok_en()
            combined_news.extend(ok_json)
            combined_news.extend(nepal_news_json)
            combined_news.extend(tht_json)
        elif language == "np":
            ok_json = online_khabar.ok_np()
            ob_json = ob_news.ob_news_np()
            nagarik_json = nagarik_news.nagarik_np()
            combined_news.extend(ok_json)
            combined_news.extend(ob_json)
            combined_news.extend(nagarik_json)
        else:
            raise HTTPException(status_code=400, detail="Language not supported")
        random.shuffle(combined_news)
        cache_news_result(language, combined_news)
        return combined_news
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarising news: {str(e)}")

# combined_news_items = summarise_news(language="en")
# print(json.dumps(combined_news_items, ensure_ascii=False, indent=4))
