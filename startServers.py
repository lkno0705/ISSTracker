import subprocess
import multiprocessing

# initialize Thread Array
threads = []

def startAPI():
    while True:
        print("RUNNING")

def startWebserver():
    subprocess.call("python3 -m http.server 8080 --bind 127.0.0.1 --directory ./ISS_Projekt/",
                    shell=True)

if __name__ == '__main__':
    threads.append(multiprocessing.Process(target=startWebserver))
    threads.append(multiprocessing.Process(target=startAPI))
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

