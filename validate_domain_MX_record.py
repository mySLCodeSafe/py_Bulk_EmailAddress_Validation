import traceback
from threading import Thread, current_thread
from queue import Queue
from coreengine import ce_logging, ce_tmp_folder

tempFile = ce_tmp_folder+"invalidDomainsList.tmp" # temp file to hold invalid domain list
confirmed_invalidDomains = [] # list to hold all invalid domains to be RETURNED for processing
q_validateDomains = Queue(50) # FIFO queue; will be used by multithreads

def vdmr_main_processDataSet(dataset):   # start of class
    ce_logging ("vdmr_main_processDataSet", "Module STARTED", "INFO")
    for _ in range(3):  # number of processess to start
        t = Thread(target=__vdmr_processDataSet_validateDomains) # function to launch as multithreaded
        t.daemon = True
        t.start()

    for domain in __vdmr_processDataSet_extractDomainsToProcess(dataset):
        q_validateDomains.put (domain) # add the domain to the queue
    q_validateDomains.join()

    ce_logging ("vdmr_main_processDataSet", "Updating customer dataset to indicate if valid MX domain", "INFO")
    __vdmr_updateCustomerDataSet(dataset)

    ce_logging ("vdmr_main_processDataSet", "Exporting invalid domains to temp file", "INFO")
    try:
        with open(tempFile, 'w') as f: # write out the invalid domain list to the temp folder
            for domain in confirmed_invalidDomains: f.write(str(domain) + '\n')
            ce_logging ("ValidateEmailDomainForMX","Stored invalid domains in location: "+tempFile,"INFO")
    except Exception:
        traceback_Message = traceback.format_exc()
        ce_logging ("vdmr_main_processDataSet", "Error occured: "+traceback_Message, "ERROR")

    ce_logging ("vdmr_main_processDataSet", "Module COMPLETED", "INFO")
    return confirmed_invalidDomains  # return results back to the main class

def __vdmr_processDataSet_extractDomainsToProcess(ext_dataset):
    __cust_DataSet = ext_dataset
    __extractedDomains = set () # insert domains from a valid e-mail address into a set; using set to automatically remove duplicate domains
    try:
        for i in __cust_DataSet:
            if i.get_emailAddress(): # if it is a valid email address
                __extractedDomains.add(i.get_emailAddressDomain()) # add the domain to the set
        ce_logging ("__vdmr_processDataSet_extractDomainsToProcess", "Total # unique domains identified: " + str(len(__extractedDomains)),"INFO")
    except Exception:
        traceback_Message = traceback.format_exc()
        ce_logging ("__vdmr_processDataSet_extractDomainsToProcess", "Error occured with " + str(i.EmailAddress) +" --> "+str(traceback_Message),"ERROR")
    return __extractedDomains

def __vdmr_processDataSet_validateDomains():
    ce_logging ("__vdmr_processDataSet_validateDomains","Started thread: "+str(current_thread()),"INFO")
    try:
        while True:
            domainToValidate = q_validateDomains.get() # get a domain from the queue
            validateDomainResult= __vdmr_processDataSet_validateDomains_validateMXrecord(domainToValidate) # send the domain to process for a valid MX record; return is Boolean
            if validateDomainResult == False: # the domain does not have a valid MX record
                __vdmr_processDataSet_validateDomains_manageResult(domainToValidate) # add the domain to a list of invalid domains
            q_validateDomains.task_done()
    except Exception:
        traceback_Message = traceback.format_exc()
        ce_logging ("__vdmr_processDataSet_extractDomains", "Error occured with " + str(domainToValidate) +" --> "+str(traceback_Message),"ERROR")

def __vdmr_processDataSet_validateDomains_validateMXrecord(ext_domainToValidate):  # function to validate domain for a valid MX record
    try:
        from dns.resolver import query
        domain = ext_domainToValidate
        query(domain, 'MX')
        print (domain + ":: valid")
        return True # return positive as domain has a valid MX record
    except Exception:
        print (domain + ":: INvalid")
        return False # return negative as domain has no valid MX record

def __vdmr_processDataSet_validateDomains_manageResult(ext_validationResult):
    confirmed_invalidDomains.append(ext_validationResult) # add the domain identified as invalid to a list that represents all domains of invalid MX records

def __vdmr_updateCustomerDataSet(ext_dataset):
    from validate_email import validate_email # check for a correctly constructed email address
    __cust_DataSet = ext_dataset
    try:
        for i in __cust_DataSet:
            cust_emailAddress = i.get_emailAddress()
            if validate_email (cust_emailAddress) == True:
                if i.get_emailAddressDomain() not in confirmed_invalidDomains:  # check if the domain is part of the invalid domain list
                        i.set_validMXDomain(True)
    except Exception:
        traceback_Message = traceback.format_exc()
        ce_logging ("__vdmr_updateCustomerDataSet","Error occured with " + str(cust_emailAddress) + " --> "+str(traceback_Message),"ERROR")