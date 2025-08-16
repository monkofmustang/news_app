#!/usr/bin/env python3
"""
Database initialization script for the News App.
This script creates the database tables and can be used for initial setup.
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

def init_database():
    """Initialize the database by creating all tables"""
    try:
        from db.db_connection import create_tables, engine
        from models.subscribers import Subscribers
        from models.news import News

        print("Connecting to database...")

        # Test connection
        with engine.connect() as conn:
            print("✓ Database connection successful")

        # Create tables
        print("Creating database tables...")
        create_tables()
        print("✓ Database tables created successfully")

        print("\nDatabase initialization completed successfully!")
        print("You can now start the application.")

    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error initializing database: {e}")
        print("Please check your database connection settings in .env file")
        sys.exit(1)

def check_environment():
    """Check if required environment variables are set"""
    print("Checking environment configuration...")

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("⚠  DATABASE_URL not found in environment variables")
        print("Please create a .env file with your database configuration")
        print("Example: DATABASE_URL=postgresql://user:password@localhost:5432/news_app")
        return False

    print("✓ DATABASE_URL found")
    return True

if __name__ == "__main__":
    print("News App Database Initialization")
    print("=" * 40)

    if check_environment():
        init_database()
    else:
        print("\nPlease configure your environment variables and try again.")
        sys.exit(1)
