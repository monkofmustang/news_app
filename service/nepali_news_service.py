import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from db.db_connection import get_db
from models.news import News
from newsFeeds import nagarik_news, nepal_news, ob_news, online_khabar, the_himalayan, rajdhani_daily, news_of_nepal
import feedparser
import ssl

# Create a custom SSL context that doesn't verify certificates
# This is needed for some RSS feeds that have SSL certificate issues
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Configure feedparser to use the custom SSL context
feedparser.PARSE_SSL_CONTEXT = ssl_context


class NepaliNewsService:
    
    def __init__(self):
        self.tag_np = "nepaliNewsNp"
        self.tag_en = "nepaliNewsEn"
    
    def fetch_all_nepali_news(self) -> List[Dict[str, Any]]:
        """
        Fetch news from all Nepali news sources
        Returns list of news items with language information
        """
        all_news = []
        
        try:
            # Fetch English news
            print("📡 Fetching English Nepali news...")
            try:
                ok_en = online_khabar.ok_en()
                for item in ok_en:
                    item['language'] = 'en'
                    item['category'] = self.tag_en
                all_news.extend(ok_en)
                print(f"✓ Online Khabar English: {len(ok_en)} items")
            except Exception as e:
                print(f"✗ Error fetching Online Khabar English: {e}")
            
            try:
                nepal_news_en = nepal_news.ok_en()
                for item in nepal_news_en:
                    item['language'] = 'en'
                    item['category'] = self.tag_en
                all_news.extend(nepal_news_en)
                print(f"✓ Nepal News English: {len(nepal_news_en)} items")
            except Exception as e:
                print(f"✗ Error fetching Nepal News English: {e}")
            
            try:
                tht_en = the_himalayan.ok_en()
                for item in tht_en:
                    item['language'] = 'en'
                    item['category'] = self.tag_en
                all_news.extend(tht_en)
                print(f"✓ The Himalayan Times English: {len(tht_en)} items")
            except Exception as e:
                print(f"✗ Error fetching The Himalayan Times English: {e}")
            
            # Fetch Nepali news
            print("📡 Fetching Nepali language news...")
            try:
                ok_np = online_khabar.ok_np()
                for item in ok_np:
                    item['language'] = 'np'
                    item['category'] = self.tag_np
                all_news.extend(ok_np)
                print(f"✓ Online Khabar Nepali: {len(ok_np)} items")
            except Exception as e:
                print(f"✗ Error fetching Online Khabar Nepali: {e}")
            
            try:
                ob_np = ob_news.ob_news_np()
                for item in ob_np:
                    item['language'] = 'np'
                    item['category'] = self.tag_np
                all_news.extend(ob_np)
                print(f"✓ OB News Nepali: {len(ob_np)} items")
            except Exception as e:
                print(f"✗ Error fetching OB News Nepali: {e}")
            
            try:
                nagarik_np = nagarik_news.nagarik_np()
                for item in nagarik_np:
                    item['language'] = 'np'
                    item['category'] = self.tag_np
                all_news.extend(nagarik_np)
                print(f"✓ Nagarik News Nepali: {len(nagarik_np)} items")
            except Exception as e:
                print(f"✗ Error fetching Nagarik News Nepali: {e}")
            
            try:
                rajdhani_np = rajdhani_daily.rd_np()
                for item in rajdhani_np:
                    item['language'] = 'np'
                    item['category'] = self.tag_np
                all_news.extend(rajdhani_np)
                print(f"✓ Rajdhani Daily Nepali: {len(rajdhani_np)} items")
            except Exception as e:
                print(f"✗ Error fetching Rajdhani Daily Nepali: {e}")
            
            try:
                news_of_nepal_np = news_of_nepal.non_np()
                for item in news_of_nepal_np:
                    item['language'] = 'np'
                    item['category'] = self.tag_np
                all_news.extend(news_of_nepal_np)
                print(f"✓ News of Nepal Nepali: {len(news_of_nepal_np)} items")
            except Exception as e:
                print(f"✗ Error fetching News of Nepal Nepali: {e}")
            
            print(f"📊 Total Nepali news items fetched: {len(all_news)}")
            return all_news
            
        except Exception as e:
            print(f"✗ Error fetching Nepali news: {e}")
            return []
    
    def save_news_to_db(self, news_items: List[Dict[str, Any]], db: Session) -> List[News]:
        """
        Save news items to database
        Returns list of saved News objects
        """
        saved_news = []
        
        for news_item in news_items:
            try:
                # Determine tag based on language
                language = news_item.get('language', 'en')
                tag = self.tag_en if language == 'en' else self.tag_np
                
                # Check if news already exists (based on title and link)
                existing_news = db.query(News).filter(
                    and_(
                        News.title == news_item.get('title'),
                        News.link == news_item.get('link'),
                        News.tag == tag
                    )
                ).first()
                
                if existing_news:
                    print(f"⚠️  Nepali news already exists: {news_item.get('title')[:50]}...")
                    continue
                
                # Save the raw publication date as string
                pub_date = news_item.get('pubDate')
                if pub_date:
                    print(f"📅 Raw date: {pub_date}")
                else:
                    print(f"⚠️  No date found")
                
                # Create new news record
                db_news = News(
                    title=news_item.get('title', ''),
                    description=news_item.get('description'),
                    content=news_item.get('content'),
                    link=news_item.get('link'),
                    pub_date=pub_date,
                    category=news_item.get('category'),
                    image=news_item.get('image'),
                    publisher=news_item.get('publisher'),
                    tag=tag,
                    summary=None,
                    is_summarized=False
                )
                
                db.add(db_news)
                saved_news.append(db_news)
                print(f"✓ Saved Nepali news ({language}): {news_item.get('title')[:50]}...")
                
            except Exception as e:
                print(f"✗ Error saving news item: {e}")
                continue
        
        # Commit all changes
        try:
            db.commit()
            print(f"✓ Successfully saved {len(saved_news)} new Nepali news items to database")
        except Exception as e:
            db.rollback()
            print(f"✗ Error committing to database: {e}")
            return []
        
        return saved_news
    
    def process_nepali_news(self) -> Dict[str, Any]:
        """
        Main method to process Nepali news
        Fetches news from all sources and saves to database
        """
        print("🇳🇵 Starting Nepali News Processing")
        print("=" * 50)
        
        # Get database session
        db = next(get_db())
        
        try:
            # Step 1: Fetch all Nepali news
            print("\n📡 Step 1: Fetching Nepali news from all sources...")
            news_items = self.fetch_all_nepali_news()
            
            if not news_items:
                return {
                    "status": "error",
                    "message": "No Nepali news items fetched from any source",
                    "fetched": 0,
                    "saved": 0,
                    "total_in_database": 0
                }
            
            # Step 2: Save news to database
            print("\n💾 Step 2: Saving Nepali news to database...")
            saved_news = self.save_news_to_db(news_items, db)
            
            # Get total news count for both tags
            total_np_count = db.query(News).filter(News.tag == self.tag_np).count()
            total_en_count = db.query(News).filter(News.tag == self.tag_en).count()
            
            result = {
                "status": "success",
                "message": "Nepali news processing completed successfully",
                "fetched": len(news_items),
                "saved": len(saved_news),
                "total_in_database": {
                    "nepaliNewsNp": total_np_count,
                    "nepaliNewsEn": total_en_count
                }
            }
            
            print("\n" + "=" * 50)
            print("✅ Nepali News Processing Complete!")
            print(f"📊 Results: {result}")
            
            return result
            
        except Exception as e:
            print(f"✗ Error in Nepali news processing: {e}")
            return {
                "status": "error",
                "message": f"Error processing Nepali news: {str(e)}",
                "fetched": 0,
                "saved": 0,
                "total_in_database": 0
            }
        
        finally:
            db.close()


# Convenience function to run the service
def process_nepali_news() -> Dict[str, Any]:
    """
    Convenience function to process Nepali news
    """
    service = NepaliNewsService()
    return service.process_nepali_news()


if __name__ == "__main__":
    # Test the service
    result = process_nepali_news()
    print(f"\nFinal Result: {result}")
