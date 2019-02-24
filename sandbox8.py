
__author__ = "shamilakhani@hotmail.com"


from time import sleep
import csv, os
import random
from coreengine import *
from user_dataStructure_class import digitalCustomer

# cust_DataSet = []
# input_dataFile = "./input/sampleAllDomains.csv"

# with open(input_dataFile, 'r') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter=',') # uses: csv.reader
#     for row in readCSV:
#         emailAddress = row[0]
#                 #uniqueID = row[1] # DEBUG
#                 # cust_DataSet.append (digitalCustomer(uniqueID,emailAddress))
#         cust_DataSet.append (digitalCustomer(emailAddress))




#from urlparse import urlparse
from threading import Thread
import threading
import sys, os, re

from queue import Queue

concurrent = 2
success = 0
errors = 0

test = []

def doWork():
    while True:
        url = q.get()
        validatepls = ce_validateDomain_MX_viaLocal (url)
        doSomethingwithResult (url, validatepls)
        q.task_done()

def doSomethingwithResult(domain, result):
    test.append(domain+ " "+ str(result))
 #   print (domain)

start = time.time()

q = Queue(concurrent * 2)

for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
    sleep(6)
    print("wait")
#try:
 #   for url in open('./input/sampleAllDomains.csv'):  #Location of your CSV containing one domain per line
  #      q.put(url.strip())
   # q.join()
#except KeyboardInterrupt:
 #   sys.exit(1)

end = time.time()


print ("############################")
print ("execution time:", (end-start))
#sleep (2)
#for i in test:
 #   print (i)

















# mlist = []

# def task():
#     print("Executing our Task")
#     sleep (1)
#     result = 0
#     i = 0
#     for i in range(10):
#         result = result + i
#     list.append ("hello")
#     print("I: {}".format(result))
#     print("Task Executed {}".format(threading.current_thread()))

# def test_task():
#     print ("launched test_task:: ", threading.current_thread())
#     sleep (6)
#     return ("shami")
#     #return True


# def main():

#     with ThreadPoolExecutor(max_workers=10) as executor:
#         #task1 = executor.submit(task)
#        # task2 = executor.submit(task)
#         #task3 = executor.submit(test_task)
#         task3 = executor.submit(test_task)
#         task4 = executor.submit(test_task)
#         task5 = executor.submit(test_task)
#         task6 = executor.submit(test_task)
#         task7 = executor.submit(test_task)
#         task8 = executor.submit(test_task)
#         task9 = executor.submit(test_task)
#         #task3.add_done_callback(done)
#         result = task3.result()
#         print (str(result))



# if __name__ == '__main__':
#     main()
