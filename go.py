__author__ = "shami.lakhani@argos.co.uk"

# start section #################
import csv, traceback, time, sys
from coreengine import *  # (ce_)
from validate_domain_MX_record import vdmr_main_processDataSet  # (vdmx_)
from user_dataStructure_class import Order

# **script params:**
projectName = "validateOrdersAgainstMX"
runID = time.strftime("%Y%m%d%H%M%S_") + projectName
input_dataFile=ce_input_folder+sys.argv[-1] # capture user input : File name
output_dataFile=ce_output_folder+runID+"_output.csv"
tempFile = ce_tmp_folder+"invalidDomainsList_"+runID +".tmp" # temp file to hold invalid domain list
cust_DataSet= set () # create a set of classes that will hold the order information; using a set to remove duplicate orders
inValidMXDomainsList = set()

## Default run:
if __name__ == "__main__":
    try:
        ce_logging ("Main","Script STARTED - Run ID: "+runID,"INFO")

    ## LoadCustomerDataset :: load customer dataset for analysis using external data file:
        ce_logging ("LoadCustomerDataset","Generating customer dataset from input file:" + str(input_dataFile),"INFO")
        with open(input_dataFile, 'r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',') # uses: csv.reader
            for row in readCSV:

                # mapping of extracting data:
                orderNo = row[0]
                orderStatus = [10]
                emailAddress = row[2]
                fastTrackOrder=row [7]

                # load data into class within set:
                cust_DataSet.add (Order(emailAddress,orderNo,orderStatus,fastTrackOrder))
        ce_logging ("LoadCustomerDataset", "Completed generating customer dataset. Loaded: " + str(len(cust_DataSet)) + " records.","INFO")

    ## Validate_CustomerEmailAddressMXRecord
        ce_logging ("Validate_CustomerEmailAddressMXRecord","Extracting domains to pass to validation module","INFO")
        allCustEmailDomains = set()

        for i in cust_DataSet:
                allCustEmailDomains.add (i.get_emailAddressDomain())

        inValidMXDomainsList = vdmr_main_processDataSet(allCustEmailDomains,True)

    ## Export_CustDS :: export to output file:
        ce_logging ("Export_CustDS","Exporting customer dataset to file: "+str(output_dataFile),"INFO")
        with open (output_dataFile,'w+') as f:
           # writer = csv.writer(f, delimiter=',',lineterminator='\n')
            for i in cust_DataSet: # iterate through customer dataset
                try:
                    delimiterchar=","
                    endlinechar="\n"
                    cust_DataSet_output = i.get_allDetails()
                    customData_validMX = str((i.get_emailAddressDomain() not in inValidMXDomainsList))
                    f.write  (cust_DataSet_output+delimiterchar+customData_validMX+endlinechar)
                except Exception:
                    traceback_Message = traceback.format_exc()
                    ce_logging ("Export_CustDS","Error occured with " + str(traceback_Message),"ERROR")

        ce_logging ("Main","Script ENDED","INFO") # as Bugs would...thats all folks !
    except Exception:
        traceback_message = traceback.format_exc()
        ce_logging ("Main","Error occured  --> "+str(traceback_Message),"ERROR") # Danger Will Robinson !

print ("## END ##")
