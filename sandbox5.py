import time
import multiprocessing



PROCESSES = multiprocessing.cpu_count() - 1

result_set = []

def process_tasks(task_queue):
    print ("*** :: ", multiprocessing.current_process())
    while not task_queue.empty():
        results = task_queue.get()
        printman(results)
        #print (results)


def run_process():

    full_task_queue = multiprocessing.Queue()

    import csv
    input_dataFile = "./input./sampleSet.csv"
    with open(input_dataFile, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',') # uses: csv.reader
        for row in readCSV:
            full_task_queue.put(row[0])


    processes = []

    print(f'Running with {PROCESSES} processes!')

    for n in range(PROCESSES):
        p = multiprocessing.Process(target=process_tasks, args=(full_task_queue,))
        processes.append(p)
        p.daemon=True
        p.start()
    for p in processes:
        p.join()


if __name__ == '__main__':
    start = time.time()

    #run_process()

    full_task_queue = multiprocessing.Queue()

    import csv
    input_dataFile = "./input./sampleSet.csv"
    with open(input_dataFile, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',') # uses: csv.reader
        for row in readCSV:
            full_task_queue.put(row[0])


    processes = []

    print(f'Running with {PROCESSES} processes!')

    for n in range(PROCESSES):
        p = multiprocessing.Process(target=process_tasks, args=(full_task_queue,))
        processes.append(p)
        p.daemon=True
        p.start()


    for p in processes:
        p.join()


    print (result_set)



    print(f'Time taken = {time.time() - start:.10f}')
