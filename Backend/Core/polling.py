from Backend.Requests.rssFeed import rssFeed
from datetime import datetime
from time import sleep


def polling():
    while True:
        rssFeed()
        print("Executed RSS-Feed poll at: ", datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
        sleep(3600)  # Wait 1 hour
