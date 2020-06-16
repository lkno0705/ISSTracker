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

    rssFeedName = rssFeed.entries[0].title
    # Return dictionary with RSS list and its Name (whether "space to Ground" or ISS Daily Summary Report)
    return {'rssFeedName': rssFeedName, 'items': list}
