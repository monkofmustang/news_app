"""
RSS Feed Utilities
This module provides utilities for fetching RSS feeds with SSL handling
"""

import requests
import feedparser
from io import BytesIO
import warnings

# Suppress SSL warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

def fetch_rss_feed(url, timeout=10):
    """
    Fetch RSS feed using requests library with SSL verification disabled
    
    Args:
        url (str): The RSS feed URL
        timeout (int): Request timeout in seconds
        
    Returns:
        feedparser.FeedParserDict: Parsed RSS feed
    """
    try:
        # Fetch the RSS feed using requests with SSL verification disabled
        response = requests.get(url, verify=False, timeout=timeout)
        response.raise_for_status()
        
        # Parse the RSS content
        feed = feedparser.parse(BytesIO(response.content))
        
        return feed
        
    except Exception as e:
        print(f"Error fetching RSS feed {url}: {e}")
        # Return empty feed
        return feedparser.FeedParserDict()
