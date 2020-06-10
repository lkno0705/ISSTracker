import rssUtility

def rssFeed():
    
    # Feed URL
    url = "https://www.nasa.gov/rss/dyn/spacetoground_vodcast.rss"

    # Read Feed
    return rssUtility.getRssFeed(url)
