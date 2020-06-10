import feedparser
import ssl

def getRssFeed(url):

    #disable certificate check
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
        
    #get RSS-Feed data
    rssFeed = feedparser.parse(url)
    return rssFeed.entries
