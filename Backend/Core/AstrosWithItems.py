import redis

import Backend.Requests.astrosOnISS as astrosOnIss

r = redis.StrictRedis(decode_responses=True)
# get List with names of Astros on ISS
astrosOnIss = astrosOnIss.getAstrosOnISS()


def get(DB, IssAstrps):
    astrosItems = {}
    items = {}
    for astro in IssAstrps:
        # get picture,flag and nation of current astro
        items['picture'] = DB.get("Astronaut:" + astro + ":" + 'picture')
        items['flag'] = DB.get("Astronaut:" + astro + ":" + 'flag')
        items['nation'] = DB.get("Astronaut:" + astro + ":" + 'nation')
        # assign these items to current astronaut
        astrosItems[astro] = items
    return astrosItems


get(r, astrosOnIss)
