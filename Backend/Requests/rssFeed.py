from Backend.Requests import rssUtility


def rssFeed():
    # Feed URL
    url = "https://www.nasa.gov/rss/dyn/spacetoground_vodcast.rss"
    # set rssFeedName and read Feed into items
    data = {'rssFeedName': 'spacetoground', 'items': rssUtility.getRssFeed(url)}
    return data
