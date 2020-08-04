import multiprocessing
from Backend.Core.polling import polling
from time import sleep

def checkThread():
    thread = multiprocessing.Process(target=polling)
    thread.start()

    while True:
        if not thread.is_alive():
            print("thrad started")
            thread.start()
        else:
            print("Thread still running")
            sleep(1)
