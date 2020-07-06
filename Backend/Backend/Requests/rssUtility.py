import ssl
from Backend.Tools.rssFeedTimeConverter import convert
import feedparser


def getRssFeed(url):
    # disable certificate check
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context

    list = []
    # get RSS-Feed data
    for i in range(2):
        rssFeed = feedparser.parse(url[i])

        # create return values
        for e in rssFeed.entries:
            dict = {'title': e.title,
                    'summary': e.summary,
                    'published': convert(e.published),
                    'link': e.link}
            list.append(dict)
    # Return list of dictionaries with RSS-Feeds

    list = sorted(list, key=lambda x: (x['published']), reverse=True)
    return list
