import traceback
from threading import Thread, current_thread
from queue import Queue
from coreengine import ce_logging

confirmed_invalidDomains = [] # list to hold all invalid domains to be RETURNED for processing
q_validateDomains = Queue(50) # FIFO queue; will be used by multithreads

def vdmr_main_processDataSet(dataset):   # start of class
    ce_logging ("vdmr_main_processDataSet", "Module STARTED", "INFO")
    for _ in range(25):  # number of processess to start
        t = Thread(target=__vdmr_processDataSet_validateDomains) # function to launch as multithreaded
        t.daemon = True
        t.start()

    for domain in __vdmr_processDataSet_extractDomainsToProcess(dataset):
        q_validateDomains.put (domain) # add the domain to the queue
    q_validateDomains.join()
    ce_logging ("vdmr_main_processDataSet", "Module COMPLETED", "INFO")
    return confirmed_invalidDomains  # return results back to the main class


def __vdmr_processDataSet_extractDomainsToProcess(ext_dataset):
    __cust_DataSet = ext_dataset
    __extractedDomains = set () # insert domains from a valid e-mail address into a set; using set to automatically remove duplicate domains
    try:
        for i in __cust_DataSet:
            if i.get_validEmailAddress(): # if it is a valid email address
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
            validateDomainResult= __vdmr_validateDomain_slow(domainToValidate) # send the domain to process for a valid MX record; return is Boolean
            if validateDomainResult == False: # the domain does not have a valid MX record
                __vdmr_processDataSet_validateDomains_manageResult(domainToValidate) # add the domain to a list of invalid domains
            q_validateDomains.task_done()
    except Exception:
        traceback_Message = traceback.format_exc()
        ce_logging ("__vdmr_processDataSet_extractDomains", "Error occured with " + str(domainToValidate) +" --> "+str(traceback_Message),"ERROR")

def __vdmr_processDataSet_validateDomains_manageResult(ext_validationResult):
    confirmed_invalidDomains.append(ext_validationResult) # add the domain identified as invalid to a list that represents all domains of invalid MX records

def __vdmr_validateDomain_slow(ext_domainToValidate):  # function performing under cache to reduce the number of calls
    try:
        from dns.resolver import query
        domain = ext_domainToValidate
        query(domain, 'MX')
        print (domain, " : True") # debug - comment/remove
        return True # return positive as domain has a valid MX record
    except Exception:
        print (domain, " : False") # debug - comment/remove
        return False # return negative as domain has no valid MX record