import feedparser
import ssl

def rssFeed():
    
    #disable certificate check
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    #get RSS-Feed data
    rssFeed = feedparser.parse("https://www.nasa.gov/rss/dyn/spacetoground_vodcast.rss")

    entry = rssFeed.entries
    list = []

    #create return values
    for e in entry:
        dict = {'title': e.title,
                'summary': e.summary,
                'published': e.published,
                'link': e.link}
        list.append(dict)

    # Return dictionary with RSS list
    return { 'items': list }
