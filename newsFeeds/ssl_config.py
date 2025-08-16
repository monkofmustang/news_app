"""
SSL Configuration for RSS feeds
This module configures feedparser to handle SSL certificate issues
"""

import ssl
import feedparser

# Create a custom SSL context that doesn't verify certificates
# This is needed for some RSS feeds that have SSL certificate issues
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Configure feedparser to use the custom SSL context
feedparser.PARSE_SSL_CONTEXT = ssl_context

def configure_feedparser():
    """Configure feedparser with SSL context"""
    feedparser.PARSE_SSL_CONTEXT = ssl_context
