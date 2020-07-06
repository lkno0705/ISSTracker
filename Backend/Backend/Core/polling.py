from Backend.Requests.rssFeed import rssFeed
from Backend.Requests.issCurrPos import currPos
from Backend.Core.database import redisDB
from datetime import datetime
from time import sleep

def polling():
    i = 0
    rssFeed()
    print("Executed RSS-Feed poll at: ", datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    while True:
        iss_dict = currPos()
        redisDB().setData(data=iss_dict, requestname='ISSpos')
        i += 1
        sleep(5)
        if i == 500:
            rssFeed()
            print("Executed RSS-Feed poll at: ", datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
            i = 0
