import ssl

import feedparser


def getRssFeed(url):
    # disable certificate check
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    # get RSS-Feed data
    rssFeed = feedparser.parse(url)

    list = []

    # create return values
    for e in rssFeed.entries:
        dict = {'title': e.title,
                'summary': e.summary,
                'published': e.published,
                'link': e.link}
        list.append(dict)
    # Return list of dictionaries with RSS-Feeds
    return list
