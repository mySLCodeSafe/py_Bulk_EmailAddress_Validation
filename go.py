__author__ = "shami.lakhani@argos.co.uk"
# Amendment-History: Introducing multithreading for MX validation
# Requirements: Input folder to hold source files; output folder to write results; log folder to write log files (see coreengine.py for more information)
# Execution map: Load dataset; Extract domains from email address; Validate domains for MX record; Create output file of dataset and results

# start section #################
import csv, traceback, threading
from coreengine import *
from user_dataStructure_class import digitalCustomer

# **script params:**
input_dataFile=ce_input_folder+"sampleAllDomains.csv"
output_dataFile=ce_output_folder+"custDataLoad_dump.csv"

cust_DataSet=[] # create list of dictionaries that will be used as customer dataset
validation_inValidMXDomains = set () # Using a set (to remove duplicates) to hold domains that have a invalid MX record; assumption is that invalid will be smaller than valid.


## Default run:
if __name__ == "__main__":
    try:
        ce_logging ("Main","Script STARTED under process id: " + str(threading.current_thread()),"INFO")

    ## LoadCustomerDataset :: load customer dataset for analysis using external data file:
        ce_logging ("LoadCustomerDataset","Generating customer dataset from input file:" + str(input_dataFile),"INFO")
        with open(input_dataFile, 'r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',') # uses: csv.reader
            for row in readCSV:
                emailAddress = row[0]
                #uniqueID = row[1] # DEBUG
                # cust_DataSet.append (digitalCustomer(uniqueID,emailAddress))
                cust_DataSet.append (digitalCustomer(emailAddress))

    ## ExtractDomainsFor_MX_Validation :: Extract domains from email addressess for validation:
        ce_logging ("ExtractDomainsFor_MX_Validation","Iterating through e-mail address in cust_dataset to extract domains for futher validation","DEBUG")
        for i in cust_DataSet:
            try:
               # cust_DataSet_EmailAddress = i.EmailAddress.split('@')[1] # split the domain out of the e-mail address  # DEBUG
                cust_DataSet_EmailAddress = i.EmailAddress
                validation_inValidMXDomains.add(cust_DataSet_EmailAddress) # add the domain to the invalid list for validation later
            except Exception:
                traceback_Message = traceback.format_exc()
                ce_logging ("ValidateDomains_MX","Error occured with " + str(i.EmailAddress) +" --> "+str(traceback_Message),"ERROR")
        len_inValidMXDomains = len(validation_inValidMXDomains) # how many unique domains were extracted from the input file
        ce_logging ("ExtractDomainsFor_MX_Validation","Completed extraction of domains. Identified "+ str(len_inValidMXDomains)+" unique domains","INFO")

    ## ValidateDomains_MX :: Validate a domain for a correct MX record ; building a list of domains that do not have a valid MX record
        ce_logging ("ValidateDomains_MX","Iterating through extracted unique domains and testing for a valid MX record","DEBUG")
        # validate each domain in the set validation_ValidMXdomains for a valid MX record:
        loopCounter_statusIndicator = 0
        for domain in validation_inValidMXDomains.copy(): # iterate over a copy of the set as cant change during a loop as it will produce an integrity error
            loopCounter_statusIndicator +=1
            ce_display_progress(loopCounter_statusIndicator,len_inValidMXDomains) # indicate progress on validation
            if ce_validateDomain_MX_viaLocal(domain): # validate domain for MX record
                validation_inValidMXDomains.remove(domain)   # remove domain from the invalid list as it contains a valid MX record
        ce_logging ("ValidateDomains_MX","Completed validation of domains for MX records. Identified "+ str(len_inValidMXDomains)+" domains with valid MX records","INFO")

    ## UpdateCustDS_InvalidMXDomains :: Reflect the customer dataset with e-mail addressess that have an incorrect MX record
        ce_logging("UpdateCustDS_InvalidMXDomains","Iterating through customer dataset and indicating e-mail address with incorrect MX record", "DEBUG")
        for i in cust_DataSet:
            try:
                cust_DataSet_EmailAddress = i.EmailAddress
                if cust_DataSet_EmailAddress in validation_inValidMXDomains:  # if the domain is in the invalid domain list
                    i.ValidMXdomain = False  # update customer dataset
            except Exception:
                    traceback_Message = traceback.format_exc()
                    ce_logging ("UpdateCustDS_InvalidMXDomains","Error occured with " + str(i.EmailAddress) + "--> "+str(traceback_Message),"ERROR")

    ## Export_CustDS :: export to output file:
        ce_logging ("Export_CustDS","Exporting customer dataset to file: "+str(output_dataFile),"DEBUG")
        with open (output_dataFile,'w') as f:
            writer = csv.writer(f, delimiter=',',lineterminator='\n')
            for i in cust_DataSet: # iterate through customer dataset
                try:
                    cust_DataSet_EmailAddress = i.EmailAddress # extract the email address
                    cust_DataSet_ValidMXDomain = i.ValidMXdomain # extract result of MX domain record check
                    outputElement = (str(cust_DataSet_EmailAddress),str(cust_DataSet_ValidMXDomain)) # write the results out to the file
                    writer.writerow (outputElement)
                except Exception:
                    traceback_Message = traceback.format_exc()
                    ce_logging ("Export_CustDS","Error occured with " + str(i.EmailAddress) + "--> "+str(traceback_Message),"ERROR")


        ce_logging ("Main","Script ENDED","INFO")
    except Exception:
        traceback_message = traceback.format_exc()
        ce_logging ("Main","Error occured  --> "+str(traceback_Message),"ERROR")
