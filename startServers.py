import subprocess
import multiprocessing
from Backend.Core.APIServer import startAPIServer

# initialize Thread Array
threads = []


def startWebserver():
    # Start Webserver at address localhost:8080 with serving directory ./ISS_Pojekt
    subprocess.call("python3 -m http.server 8080 --bind 127.0.0.1 --directory ./ISS_Projekt/",
                    shell=True)


if __name__ == '__main__':
    # Append Thread Objects to Thread array
    threads.append(multiprocessing.Process(target=startAPIServer))
    threads.append(multiprocessing.Process(target=startWebserver))
    for thread in threads:
        # Start Threads
        thread.start()

