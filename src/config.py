# encoding: utf-8
import os


class Config(object):
    # Number of results to fetch from API
    RESULT_COUNT = 20
    
    # How long to cache results for
    CACHE_MAX_AGE = 20  # seconds
    
    # Icon
    THREESIX_ICON = "icon.png"
    GOOGLE_ICON = "google.png"
    
    # Algolia credentials
    ALGOLIA_APP_ID = os.getenv('ALGOLIA_APP_ID')
    ALGOLIA_SEARCH_ONLY_API_KEY = os.getenv('ALGOLIA_SEARCH_ONLY_API_KEY')
    ALGOLIA_SEARCH_INDEX = os.getenv('ALGOLIA_SEARCH_INDEX')

    # Knowledge Base details
    ZENDESK_KB_NAME = os.getenv('ZENDESK_KB_NAME')
    ZENDESK_KB_SLUG = os.getenv('ZENDESK_KB_SLUG')

    # Language for displayed results
    LOCALE = os.getenv('LOCALE')
