__author__ = "shami.lakhani@argos.co.uk"
# Amendment-History: Introducing multithreading for MX validation
# Requirements: Input folder to hold source files; output folder to write results; log folder to write log files (see coreengine.py for more information)
# Execution map: Load dataset; Extract domains from email address; Validate domains for MX record; Create output file of dataset and results

# start section #################
import csv, traceback, time
from coreengine import ce_input_folder, ce_output_folder, ce_logging, ce_tmp_folder  # (ce_)
from validate_domain_MX_record import vdmr_main_processDataSet  # (vdmx_)
from user_dataStructure_class import digitalCustomer

# **script params:**
runID = time.strftime("%Y%m%d%H%M%S")
input_dataFile=ce_input_folder+"WCS_DB_User_Data_Nov18.csv"
output_dataFile=ce_output_folder+"custDataLoad_dump_"+runID+".csv"

cust_DataSet=[] # create list of dictionaries that will be used as customer dataset
inValidMXDomainsList = [] # Using a set (to remove duplicates) to hold domains that have a invalid MX record; assumption is that invalid will be smaller than valid.

## Default run:
if __name__ == "__main__":
    try:
        ce_logging ("Main","Script STARTED - Run ID: "+runID,"INFO")

    ## LoadCustomerDataset :: load customer dataset for analysis using external data file:
        ce_logging ("LoadCustomerDataset","Generating customer dataset from input file:" + str(input_dataFile),"INFO")
        with open(input_dataFile, 'r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',') # uses: csv.reader
            for row in readCSV:
                emailAddress = row[0]
                #cust_DataSet.append (digitalCustomer(emailAddress))
                uniqueID = row[1]
                cust_DataSet.append (digitalCustomer(uniqueID,emailAddress))

    ## ValidateEmailDomainForMX :: process cust. email addressess and identify domains with invalid MX records:
        ce_logging ("ValidateEmailDomainForMX","Validating e-mail address domains for a MX reord","DEBUG")
        try:
            inValidMXDomainsList = vdmr_main_processDataSet(cust_DataSet)
            tempFile = ce_tmp_folder+"invalidDomainsList_"+runID+".tmp" # temp file to hold invalid domain list
            with open(tempFile, 'w') as f: # write out the invalid domain list to the temp folder
                for domain in inValidMXDomainsList:
                    f.write(str(domain) + '\n')
            ce_logging ("ValidateEmailDomainForMX","Stored invalid domains in location: "+tempFile,"INFO")
        except Exception:
            traceback_Message = traceback.format_exc()
            ce_logging ("ValidateEmailDomainForMX","Error occured --> "+str(traceback_Message),"ERROR")

    ## UpdateCustDS_InvalidMXDomains :: Reflect the customer dataset with e-mail addressess that have an incorrect MX record
        ce_logging("UpdateCustDS_InvalidMXDomains","Iterating through customer dataset and indicating e-mail address with incorrect MX record", "DEBUG")
        for i in cust_DataSet:
            try:
                cust_DataSet_EmailAddress = i.EmailAddress.split('@')[1]
                if cust_DataSet_EmailAddress in inValidMXDomainsList:  # if the domain is in the invalid domain list
                    i.ValidMXdomain = False  # update customer dataset
            except Exception:
                    traceback_Message = traceback.format_exc()
                    ce_logging ("UpdateCustDS_InvalidMXDomains","Error occured with " + str(i.EmailAddress) + " --> "+str(traceback_Message),"ERROR")

    ## Export_CustDS :: export to output file:
        ce_logging ("Export_CustDS","Exporting customer dataset to file: "+str(output_dataFile),"INFO")
        with open (output_dataFile,'w') as f:
            writer = csv.writer(f, delimiter=',',lineterminator='\n')
            for i in cust_DataSet: # iterate through customer dataset
                try:
                    cust_DataSet_EmailAddress = i.EmailAddress # extract the email address
                    cust_DataSet_ValidMXDomain = i.ValidMXdomain # extract result of MX domain record check
                    cust_DataSet_CustID = i.custID
                    outputElement = (str(cust_DataSet_CustID),str(cust_DataSet_EmailAddress),str(cust_DataSet_ValidMXDomain)) # write the results out to the file
                    writer.writerow (outputElement)
                except Exception:
                    traceback_Message = traceback.format_exc()
                    ce_logging ("Export_CustDS","Error occured with " + str(i.EmailAddress) + " --> "+str(traceback_Message),"ERROR")


        ce_logging ("Main","Script ENDED","INFO")
    except Exception:
        traceback_message = traceback.format_exc()
        ce_logging ("Main","Error occured  --> "+str(traceback_Message),"ERROR")
