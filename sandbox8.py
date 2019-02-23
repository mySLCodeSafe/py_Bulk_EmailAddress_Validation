__author__ = "shamilakhani@hotmail.com"

from concurrent.futures import ThreadPoolExecutor
from time import sleep
import threading
import random

mlist = []

def task():
    print("Executing our Task")
    sleep (1)
    result = 0
    i = 0
    for i in range(10):
        result = result + i
    list.append ("hello")
    print("I: {}".format(result))
    print("Task Executed {}".format(threading.current_thread()))

def test_task():
    print ("launched test_task:: ", threading.current_thread())
    sleep (6)
    return ("shami")
    #return True


def main():

    with ThreadPoolExecutor(max_workers=10) as executor:
        #task1 = executor.submit(task)
       # task2 = executor.submit(task)
        #task3 = executor.submit(test_task)
        task3 = executor.submit(test_task)
        task4 = executor.submit(test_task)
        task5 = executor.submit(test_task)
        task6 = executor.submit(test_task)
        task7 = executor.submit(test_task)
        task8 = executor.submit(test_task)
        task9 = executor.submit(test_task)
        #task3.add_done_callback(done)
        result = task3.result()
        print (str(result))



if __name__ == '__main__':
    main()
