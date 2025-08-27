import asyncio
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from db.db_connection import get_db
from models.news import News
from newsFeeds.international_news import un_news, toi_news, the_hindu_international, nyt_world
from service.llm_service import summarize_news


class InternationalNewsService:
    
    def __init__(self):
        self.tag = "international_news"
    
    def fetch_all_international_news(self) -> List[Dict[str, Any]]:
        """
        Fetch news from all international news sources
        Returns a list of all news items from different sources
        """
        all_news = []
        
        try:
            # Fetch from UN News
            print("Fetching UN News...")
            un_news_items = un_news()
            all_news.extend(un_news_items)
            print(f"✓ Fetched {len(un_news_items)} UN News items")
            
        except Exception as e:
            print(f"✗ Error fetching UN News: {e}")
        
        try:
            # Fetch from Times of India
            print("Fetching Times of India News...")
            toi_news_items = toi_news()
            all_news.extend(toi_news_items)
            print(f"✓ Fetched {len(toi_news_items)} TOI News items")
            
        except Exception as e:
            print(f"✗ Error fetching TOI News: {e}")
        
        try:
            # Fetch from The Hindu International
            print("Fetching The Hindu International News...")
            hindu_news_items = the_hindu_international()
            all_news.extend(hindu_news_items)
            print(f"✓ Fetched {len(hindu_news_items)} The Hindu News items")
            
        except Exception as e:
            print(f"✗ Error fetching The Hindu News: {e}")
        
        try:
            # Fetch from NYT World
            print("Fetching NYT World News...")
            nyt_news_items = nyt_world()
            all_news.extend(nyt_news_items)
            print(f"✓ Fetched {len(nyt_news_items)} NYT News items")
            
        except Exception as e:
            print(f"✗ Error fetching NYT News: {e}")
        
        print(f"\n📊 Total news items fetched: {len(all_news)}")
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
                    print(f"⚠️  News already exists: {news_item.get('title')[:50]}...")
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
                print(f"✓ Saved: {news_item.get('title')[:50]}...")
                
            except Exception as e:
                print(f"✗ Error saving news item: {e}")
                continue
        
        # Commit all changes
        try:
            db.commit()
            print(f"✓ Successfully saved {len(saved_news)} new news items to database")
        except Exception as e:
            db.rollback()
            print(f"✗ Error committing to database: {e}")
            return []
        
        return saved_news
    
    def summarize_and_update_news(self, news_items: List[News], db: Session) -> int:
        """
        Summarize news items and update them in database
        Returns number of successfully summarized items
        """
        summarized_count = 0
        
        for news_item in news_items:
            try:
                # Skip if already summarized
                if news_item.is_summarized and news_item.summary:
                    print(f"⚠️  Already summarized: {news_item.title[:50]}...")
                    continue
                
                # Prepare content for summarization
                content_to_summarize = ""
                if news_item.description:
                    content_to_summarize += news_item.description + "\n\n"
                if news_item.content:
                    content_to_summarize += news_item.content
                
                if not content_to_summarize.strip():
                    print(f"⚠️  No content to summarize for: {news_item.title[:50]}...")
                    continue
                
                # Generate summary using LLM
                print(f"🤖 Summarizing: {news_item.title[:50]}...")
                summary = summarize_news(content_to_summarize)
                
                # Update the news item
                news_item.summary = summary
                news_item.is_summarized = True
                news_item.updated_at = datetime.utcnow()
                
                summarized_count += 1
                print(f"✓ Summarized: {news_item.title[:50]}...")
                
            except Exception as e:
                print(f"✗ Error summarizing news item: {e}")
                continue
        
        # Commit all changes
        try:
            db.commit()
            print(f"✓ Successfully summarized {summarized_count} news items")
        except Exception as e:
            db.rollback()
            print(f"✗ Error committing summaries to database: {e}")
            return 0
        
        return summarized_count
    
    def process_international_news(self) -> Dict[str, Any]:
        """
        Main method to fetch, save, and summarize all international news
        Returns summary of the operation
        """
        print("🌍 Starting International News Processing...")
        print("=" * 50)
        
        # Get database session
        db = next(get_db())
        
        try:
            # Step 1: Fetch all international news
            print("\n📡 Step 1: Fetching news from all sources...")
            news_items = self.fetch_all_international_news()
            
            if not news_items:
                return {
                    "status": "error",
                    "message": "No news items fetched from any source",
                    "fetched": 0,
                    "saved": 0,
                    "summarized": 0
                }
            
            # Step 2: Save news to database
            print("\n💾 Step 2: Saving news to database...")
            saved_news = self.save_news_to_db(news_items, db)
            
            # Step 3: Summarize news
            print("\n🤖 Step 3: Summarizing news using LLM...")
            # summarized_count = self.summarize_and_update_news(saved_news, db)
            summarized_count = 0

            # Get total news count for this tag
            total_news_count = db.query(News).filter(News.tag == self.tag).count()

            result = {
                "status": "success",
                "message": "International news processing completed successfully",
                "fetched": len(news_items),
                "saved": len(saved_news),
                "summarized": summarized_count,
                "total_in_database": total_news_count
            }
            
            print("\n" + "=" * 50)
            print("✅ Processing Complete!")
            print(f"📊 Results: {result}")
            
            return result
            
        except Exception as e:
            print(f"✗ Error in international news processing: {e}")
            return {
                "status": "error",
                "message": f"Error processing international news: {str(e)}",
                "fetched": 0,
                "saved": 0,
                "summarized": 0
            }
        
        finally:
            db.close()


# Convenience function to run the service
def process_international_news() -> Dict[str, Any]:
    """
    Convenience function to process international news
    """
    service = InternationalNewsService()
    return service.process_international_news()
