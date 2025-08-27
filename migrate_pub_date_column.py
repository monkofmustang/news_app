#!/usr/bin/env python3
"""
Migration script to change pub_date column from timestamp to varchar
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def migrate_pub_date_column():
    """Migrate pub_date column from timestamp to varchar"""
    try:
        from db.db_connection import engine
        
        print("🔄 Migrating pub_date column...")
        print("=" * 50)
        
        from sqlalchemy import text
        
        # Connect to database
        with engine.connect() as conn:
            print("✓ Connected to database")
            
            # Check if news table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'news'
                );
            """))
            
            if not result.scalar():
                print("❌ News table does not exist")
                return False
            
            print("✓ News table exists")
            
            # Check current column type
            result = conn.execute(text("""
                SELECT data_type 
                FROM information_schema.columns 
                WHERE table_name = 'news' AND column_name = 'pub_date';
            """))
            
            current_type = result.scalar()
            print(f"📊 Current pub_date column type: {current_type}")
            
            if current_type == 'character varying':
                print("✅ pub_date column is already varchar type")
                return True
            
            # Change column type from timestamp to varchar
            print("🔄 Changing pub_date column type from timestamp to varchar...")
            
            # First, drop the column if it exists
            conn.execute(text("ALTER TABLE news DROP COLUMN IF EXISTS pub_date;"))
            
            # Add the column as varchar
            conn.execute(text("ALTER TABLE news ADD COLUMN pub_date VARCHAR(255);"))
            
            print("✅ Successfully migrated pub_date column to varchar")
            
            # Verify the change
            result = conn.execute(text("""
                SELECT data_type 
                FROM information_schema.columns 
                WHERE table_name = 'news' AND column_name = 'pub_date';
            """))
            
            new_type = result.scalar()
            print(f"📊 New pub_date column type: {new_type}")
            
            if new_type == 'character varying':
                print("✅ Migration completed successfully!")
                return True
            else:
                print("❌ Migration failed - column type is not varchar")
                return False
                
    except Exception as e:
        print(f"❌ Migration error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Pub Date Column Migration")
    print("=" * 40)
    
    migrate_pub_date_column()
