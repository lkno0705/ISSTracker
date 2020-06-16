from Backend.Requests import rssUtility


def rssFeed():
    # Feed URL
    url = "https://www.nasa.gov/rss/dyn/spacetoground_vodcast.rss"

    # set rssFeedName
    data = rssUtility.getRssFeed(url)
    data['rssFeedName'] = 'spacetoground'
    # Read Feed
    return data
