import multiprocessing
from Backend.Core.APIServer import startAPIServer
from Backend.Core.polling import polling

# initialize Thread Array
threads = []

if __name__ == '__main__':
    # Append Thread Objects to Thread array
    threads.append(multiprocessing.Process(target=startAPIServer))
    threads.append(multiprocessing.Process(target=polling))
    for thread in threads:
        # Start Threads
        thread.start()

