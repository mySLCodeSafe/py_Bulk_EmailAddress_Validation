__author__ = "shami.lakhani@argos.co.uk"
# Amendment-History: Introducing multithreading for MX validation
# Requirements: Input folder to hold source files; output folder to write results; log folder to write log files (see coreengine.py for more information)

# start section #################
import csv, traceback, time, sys
from coreengine import *  # (ce_)
from validate_domain_MX_record import vdmr_main_processDataSet  # (vdmx_)
from user_dataStructure_class import sterlingCustomer

# **script params:**
projectName = "validateOrdersAgainstMX"
runID = time.strftime("%Y%m%d%H%M%S_") + projectName
input_dataFile=ce_input_folder+sys.argv[-1] # Capture user input : File name
output_dataFile=ce_output_folder+runID+"_output.csv"
tempFile = ce_tmp_folder+"invalidDomainsList_"+runID +".tmp" # temp file to hold invalid domain list
cust_DataSet=[] # create list of classes that will be the customer dataset
cust_DataSet_index = {}

## Default run:
if __name__ == "__main__":
    try:
        ce_logging ("Main","Script STARTED - Run ID: "+runID,"INFO")

    ## LoadCustomerDataset :: load customer dataset for analysis using external data file:
        ce_logging ("LoadCustomerDataset","Generating customer dataset from input file:" + str(input_dataFile),"INFO")
        with open(input_dataFile, 'r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',') # uses: csv.reader
            for row in readCSV:
                orderNo = row[0]
                orderStatus = [10]
                emailAddress = row[2] # read first entry on row
                fastTrackOrder=row [7]
                cust_DataSet.append (sterlingCustomer(orderNo,orderStatus,emailAddress,fastTrackOrder))
                #print (cust_DataSet.index[-1]) # add records to the customer dataset
                cust_DataSet_index[orderNo] = len(cust_DataSet)-1
        ce_logging ("LoadCustomerDataset", "Completed generating customer dataset. Loaded: " + str(len(cust_DataSet)) + " records.","INFO")

    ## Validate_CustomerEmailAddressMXRecord
        ce_logging ("Validate_CustomerEmailAddressMXRecord","Generating customer dataset from input file:" + str(input_dataFile),"INFO")
        inValidMXDomainsList = vdmr_main_processDataSet(cust_DataSet)

    ## Export_CustDS :: export to output file:
        ce_logging ("Export_CustDS","Exporting customer dataset to file: "+str(output_dataFile),"INFO")
        with open (output_dataFile,'w') as f:
            writer = csv.writer(f, delimiter=',',lineterminator='\n')
            for i in cust_DataSet: # iterate through customer dataset
                try:
                    cust_DataSet_OrderNo = i.orderNo # extract the order number from the csutomer dataset
                    cust_DataSet_OrderStatus = i.get_orderStatus()
                    cust_DataSet_EmailAddress = i.emailAddress # extract the email address from the customer dataset
                    cust_validMX = i.get_validMXDomain()
                    cust_fastTrackOrder = i.get_fastTrackOrder()
                    outputElement = (str(cust_DataSet_OrderNo),str(cust_fastTrackOrder),str(cust_DataSet_EmailAddress),str(cust_validMX))
                    writer.writerow (outputElement) # write the results out to the file
                except Exception:
                    traceback_Message = traceback.format_exc()
                    ce_logging ("Export_CustDS","Error occured with " + str(i.EmailAddress) + " --> "+str(traceback_Message),"ERROR")

        ce_logging ("Main","Script ENDED","INFO") # as Bugs would...thats all folks !
    except Exception:
        traceback_message = traceback.format_exc()
        ce_logging ("Main","Error occured  --> "+str(traceback_Message),"ERROR") # Danger Will Robinson !

    print ("###")
    for key,val in cust_DataSet_index.items():
        print (key, "->", val)

    print (cust_DataSet[18].orderNo)