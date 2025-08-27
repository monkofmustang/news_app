import asyncio
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from db.db_connection import get_db
from models.news import News
from newsFeeds.international_tech_news import toi_tech, tech_crunch


class TechNewsService:
    
    def __init__(self):
        self.tag = "tech_news"
    
    def fetch_all_tech_news(self) -> List[Dict[str, Any]]:
        """
        Fetch news from all tech news sources
        Returns a list of all news items from different sources
        """
        all_news = []
        
        try:
            # Fetch from Times of India Tech
            print("Fetching Times of India Tech News...")
            toi_tech_items = toi_tech()
            all_news.extend(toi_tech_items)
            print(f"✓ Fetched {len(toi_tech_items)} TOI Tech items")
            
        except Exception as e:
            print(f"✗ Error fetching TOI Tech News: {e}")
        
        try:
            # Fetch from TechCrunch
            print("Fetching TechCrunch News...")
            techcrunch_items = tech_crunch()
            all_news.extend(techcrunch_items)
            print(f"✓ Fetched {len(techcrunch_items)} TechCrunch items")
            
        except Exception as e:
            print(f"✗ Error fetching TechCrunch News: {e}")
        
        print(f"\n📊 Total tech news items fetched: {len(all_news)}")
        return all_news
    
    def save_news_to_db(self, news_items: List[Dict[str, Any]], db: Session) -> List[News]:
        """
        Save news items to database
        Returns list of saved News objects
        """
        saved_news = []
        
        for news_item in news_items:
            try:
                # Check if news already exists (based on title and link)
                existing_news = db.query(News).filter(
                    and_(
                        News.title == news_item.get('title'),
                        News.link == news_item.get('link'),
                        News.tag == self.tag
                    )
                ).first()
                
                if existing_news:
                    print(f"⚠️  Tech news already exists: {news_item.get('title')[:50]}...")
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
                    tag=self.tag,
                    summary=None,
                    is_summarized=False
                )
                
                db.add(db_news)
                saved_news.append(db_news)
                print(f"✓ Saved tech news: {news_item.get('title')[:50]}...")
                
            except Exception as e:
                print(f"✗ Error saving tech news item: {e}")
                continue
        
        # Commit all changes
        try:
            db.commit()
            print(f"✓ Successfully saved {len(saved_news)} new tech news items to database")
        except Exception as e:
            db.rollback()
            print(f"✗ Error committing to database: {e}")
            return []
        
        return saved_news
    
    def process_tech_news(self) -> Dict[str, Any]:
        """
        Main method to fetch and save all tech news
        Returns summary of the operation
        """
        print("💻 Starting Tech News Processing...")
        print("=" * 50)
        
        # Get database session
        db = next(get_db())
        
        try:
            # Step 1: Fetch all tech news
            print("\n📡 Step 1: Fetching tech news from all sources...")
            news_items = self.fetch_all_tech_news()
            
            if not news_items:
                return {
                    "status": "error",
                    "message": "No tech news items fetched from any source",
                    "fetched": 0,
                    "saved": 0,
                    "total_in_database": 0
                }
            
            # Step 2: Save news to database
            print("\n💾 Step 2: Saving tech news to database...")
            saved_news = self.save_news_to_db(news_items, db)
            
            # Get total news count for this tag
            total_news_count = db.query(News).filter(News.tag == self.tag).count()
            
            result = {
                "status": "success",
                "message": "Tech news processing completed successfully",
                "fetched": len(news_items),
                "saved": len(saved_news),
                "total_in_database": total_news_count
            }
            
            print("\n" + "=" * 50)
            print("✅ Tech News Processing Complete!")
            print(f"📊 Results: {result}")
            
            return result
            
        except Exception as e:
            print(f"✗ Error in tech news processing: {e}")
            return {
                "status": "error",
                "message": f"Error processing tech news: {str(e)}",
                "fetched": 0,
                "saved": 0,
                "total_in_database": 0
            }
        
        finally:
            db.close()


# Convenience function to run the service
def process_tech_news() -> Dict[str, Any]:
    """
    Convenience function to process tech news
    """
    service = TechNewsService()
    return service.process_tech_news()
