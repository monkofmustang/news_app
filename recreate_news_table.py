#!/usr/bin/env python3
"""
Script to recreate the news table with correct schema
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def recreate_news_table():
    """Recreate the news table with correct schema"""
    try:
        from db.db_connection import engine
        from sqlalchemy import text
        
        print("🔄 Recreating news table...")
        print("=" * 50)
        
        # Connect to database
        with engine.connect() as conn:
            print("✓ Connected to database")
            
            # Drop the existing news table
            print("🗑️  Dropping existing news table...")
            conn.execute(text("DROP TABLE IF EXISTS news;"))
            print("✅ News table dropped")
            
            # Create the news table with correct schema
            print("🏗️  Creating news table with correct schema...")
            conn.execute(text("""
                CREATE TABLE news (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(500) NOT NULL,
                    description TEXT,
                    content TEXT,
                    link VARCHAR(1000),
                    pub_date VARCHAR(255),
                    category VARCHAR(100),
                    image VARCHAR(1000),
                    publisher VARCHAR(200),
                    tag VARCHAR(100) NOT NULL,
                    summary TEXT,
                    is_summarized BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
            
            # Create indexes
            print("📊 Creating indexes...")
            conn.execute(text("CREATE INDEX idx_news_title ON news(title);"))
            conn.execute(text("CREATE INDEX idx_news_tag ON news(tag);"))
            conn.execute(text("CREATE INDEX idx_news_pub_date ON news(pub_date);"))
            
            print("✅ News table created successfully")
            
            # Verify the table structure
            print("\n🔍 Verifying table structure...")
            result = conn.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'news' 
                ORDER BY ordinal_position;
            """))
            
            columns = result.fetchall()
            for column in columns:
                print(f"   📋 {column[0]}: {column[1]}")
            
            print("\n✅ News table recreation completed successfully!")
            return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("News Table Recreation")
    print("=" * 40)
    
    recreate_news_table()
