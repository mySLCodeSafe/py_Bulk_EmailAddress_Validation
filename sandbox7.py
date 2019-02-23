from multiprocessing.pool import ThreadPool
import multiprocessing
import os, time
full_task_queue = multiprocessing.Queue()



def hello(x):
    return (False)

if __name__ == "__main__":

    import csv
    input_dataFile = "./input/sampleSet.csv"
    with open(input_dataFile, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',') # uses: csv.reader
        for row in readCSV:
            full_task_queue.put (row[0])
        full_task_queue.put('emptied')

    while not full_task_queue.empty():
        sendDomain = full_task_queue.get()
        if (sendDomain == 'emptied'):
            print ("done")
            break
        print (sendDomain)
