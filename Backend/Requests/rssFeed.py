import rssUtility

def rssFeed():
    # Feed URL
    url = "https://www.nasa.gov/rss/dyn/spacetoground_vodcast.rss"
    # Read Feed
    entry = rssUtility.getRssFeed(url)

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
