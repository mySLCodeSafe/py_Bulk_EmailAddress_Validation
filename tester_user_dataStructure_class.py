import os, csv, time

start = time.time()

from validate_domain_MX_record import vdmr_main_processDataSet
from user_dataStructure_class import digitalCustomer

cust_DataSet=[]
input_dataFile = "./input/sampleAllDomains.csv"

with open(input_dataFile, 'r') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',') # uses: csv.reader
    for row in readCSV:
        emailAddress = row[0]
                 #uniqueID = row[1] # DEBUG
        cust_DataSet.append (digitalCustomer(emailAddress))

returnedResult = vdmr_main_processDataSet(cust_DataSet)

for i in returnedResult:
    print (i)

end = time.time()
print ("#######################################################")
print ("Execution time: ", end - start)