#!/usr/bin/python
# encoding: utf-8

from __future__ import print_function, unicode_literals, absolute_import

import functools
import re
import sys
from textwrap import wrap
from urllib import quote_plus

from algoliasearch.search_client import SearchClient
from config import Config
from workflow import Workflow3, ICON_INFO

# Algolia client
client = SearchClient.create(Config.ALGOLIA_APP_ID, Config.ALGOLIA_SEARCH_ONLY_API_KEY)
index = client.init_index(Config.ALGOLIA_SEARCH_INDEX)


def cache_key(query):
    """Make filesystem-friendly cache key"""
    key = query
    key = key.lower()
    key = re.sub(r"[^a-z0-9-_;.]", "-", key)
    key = re.sub(r"-+", "-", key)
    return key


def handle_result(api_dict):
    """Extract relevant info from API result"""
    result = {}

    for key in {"title", "id", "body_safe", "locale", "section"}:
        result[key] = api_dict[key]

    return result

def filter_english_results(articles):
    """Filter articles that have locale en-us only"""
    return [article for article in articles if article["locale"]["locale"] == "en-us"]

def search(query=None, limit=Config.RESULT_COUNT):
    if query:
        results = index.search(query, {"page": 0, "hitsPerPage": limit})
        if results is not None and "hits" in results:
            return filter_english_results(results["hits"])
    return []


def main(wf):
    if wf.update_available:
        # Add a notification to top of Script Filter results
         wf.add_item(
             "New version available",
             "Action this item to install the update",
             autocomplete="workflow:update",
             icon=ICON_INFO,
         )

    query = wf.args[0].strip()

    if not query:
        wf.add_item("Search the " + Config.ZENDESK_KB_NAME + " docs...")
        wf.send_feedback()
        return 0

    key = cache_key(query)

    results = [
        handle_result(result)
        for result in wf.cached_data(
            key, functools.partial(search, query), max_age=Config.CACHE_MAX_AGE
        )
    ]

    # Show results
    if not results:
        url = "https://www.google.com/search?q={}".format(
            quote_plus(Config.ZENDESK_KB_NAME + " {}".format(query))
        )
        wf.add_item(
            "No matching answers found",
            "Shall I try and search Google?",
            valid=True,
            arg=url,
            copytext=url,
            quicklookurl=url,
            icon=Config.GOOGLE_ICON,
        )

    for result in results:
        # Use this value of subtitle if you want to display the contents of the article.
        subtitle = wrap(result["body_safe"], width=75)[0]
        if len(result["body_safe"]) > 75:
            subtitle += " ..."
        wf.add_item(
            uid=result["id"],
            title=result["title"],

            # Show the full path in the subtitle.
            subtitle=result["section"]["full_path"],
            arg=Config.ZENDESK_KB_SLUG+result["id"],
            valid=True,
            largetext=result["title"],
            copytext=Config.ZENDESK_KB_SLUG+result["id"],
            quicklookurl=Config.ZENDESK_KB_SLUG+result["id"],
            icon=Config.THREESIX_ICON,
        )

    wf.send_feedback()


if __name__ == "__main__":
    wf = Workflow3(
        update_settings={"github_slug": "saintsaens/alfred-zendesk-docs", "frequency": 7}
    )
    sys.exit(wf.run(main))
