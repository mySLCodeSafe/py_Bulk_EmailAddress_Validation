# Author: shamilakhani@hotmail.com
# Amendment-History: Introducing multithreading for MX validation

# start section #################
import csv, traceback
from coreengine import *
from classes_bucket import digitalCustomer

# **script params:**
input_dataFile=ce_input_folder+"sampleSet.csv"
output_dataFile=ce_output_folder+"custDataLoad_dump.csv"

cust_DataSet=[] # create list of dictionaries that will be used as customer dataset
validation_inValidMXDomains = set () # Using a set (to remove duplicates) to hold domains that have a invalid MX record; assumption is that invalid will be smaller than valid.

## Functions:
def validateEmailAddressForInvalidMXDomain(ext_customerEmailAddress):
    try:
        domainToValidate = ext_customerEmailAddress.split('@')[1]
        __MXValidationResult = True
        if domainToValidate in validation_inValidMXDomains:
            __MXValidationResult = False
        return __MXValidationResult
    except Exception:
        traceback_Message = traceback.format_exc()
        ce_logging ("validateEmailAddressForInvalidMXDomain","Error occured with " + str(ext_customerEmailAddress) +" --> "+str(traceback_Message),"ERROR")

## Default run:
if __name__ == "__main__":
    try:
        ce_logging ("Main","Script STARTED","INFO")

    ## GenerateCustomerDataset :: load customer dataset for analysis using external data file:
        ce_logging ("GenerateCustomerDataset","Generating customer dataset from input file:" + str(input_dataFile),"INFO")
        with open(input_dataFile, 'r') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',') # uses: csv.reader
            for row in readCSV:
                emailAddress = row[0]
                uniqueID = row[1]
                cust_DataSet.append (digitalCustomer(uniqueID,emailAddress))

    ## ValidateDomains_MX :: Validate a domain for a correct MX record
        # extract domains from customer addressess in the cust_dataset and hold in validation_inValidMXDomains:
        ce_logging ("ValidateDomains_MX","Iterating through e-mail address in cust_dataset to extract domains for futher validation","DEBUG")
        for i in cust_DataSet:
            try:
                cust_DataSet_EmailAddress = i.EmailAddress.split('@')[1] # split the domain out of the e-mail address
                validation_inValidMXDomains.add(cust_DataSet_EmailAddress) # add the domain to the invalid list for validation later
            except Exception:
                traceback_Message = traceback.format_exc()
                ce_logging ("ValidateDomains_MX","Error occured with " + str(i.EmailAddress) +" --> "+str(traceback_Message),"ERROR")

        len_inValidMXDomains = len(validation_inValidMXDomains) # how many unique domains were extracted from the input file
        ce_logging ("ValidateDomains_MX","Completed extraction of domains. Identified "+ str(len_inValidMXDomains)+" unique domains","INFO")

        ce_logging ("ValidateDomains_MX","Iterating through extracted unique domains and testing for a valid MX record","DEBUG")
        # validate each domain in the set validation_ValidMXdomains for a valid MX record:
        loopCounter_statusIndicator = 0
        for domain in validation_inValidMXDomains.copy(): # iterate over a copy of the set as cant change during a loop as it will produce an integrity error
            loopCounter_statusIndicator +=1
            ce_display_progress(loopCounter_statusIndicator,len_inValidMXDomains) # Indicate progress on validation
            if ce_validateDomain_MX_viaLocal(domain):
                validation_inValidMXDomains.remove(domain)   # remove domain from the invalid list as it contains a valid MX record
        ce_logging ("ValidateDomains_MX","Completed validation of domains for MX records. Identified "+ str(len_inValidMXDomains)+" domains with valid MX records","INFO")

    ## ValidateEmailAddressAndExport :: Validate customer email address against set of domains with invalid MX records and export to output file:
        ce_logging ("ValidateEmailAddressAndExport ","Validating MX records and exporting to file: "+str(output_dataFile),"DEBUG")
        with open (output_dataFile,'w') as f:
            writer = csv.writer(f, delimiter=',',lineterminator='\n')
            for i in cust_DataSet: # iterate through customer dataset
                try:
                    cust_DataSet_EmailAddress = i.EmailAddress # extract the email address
                    validationResult = validateEmailAddressForInvalidMXDomain(cust_DataSet_EmailAddress)
                    outputElement = (str(cust_DataSet_EmailAddress),str(validationResult)) # write the results out to the file
                    writer.writerow (outputElement)
                except Exception:
                    traceback_Message = traceback.format_exc()
                    ce_logging ("ValidateEmailAddressAndExport","Error occured with " + str(i.EmailAddress) + "--> "+str(traceback_Message),"ERROR")


        ce_logging ("Main","Script ENDED","INFO")
    except Exception:
        traceback_message = traceback.format_exc()
        ce_logging ("Main","Error occured  --> "+str(traceback_Message),"ERROR")

