__author__ = "shami.lakhani@argos.co.uk"
__reference__ = "https://jira.sainsburysargos.io/browse/TTT-1611"

# Module to validate domains for MX records. Customised for program: validate-domain_MX_record.py

import traceback, time
from dns.resolver import query # __vdmr_processDataSet_validateDomains_validateMXrecord
from threading import Thread, current_thread
from queue import Queue
from coreengine import ce_logging, ce_tmp_folder

# Module parameters/variables:
domain_exclusionList = ('virginmedia.com','dhl.com') # these domains fail to correctly validate on the Argos network; they have been manually checked for a valid MX record
confirmed_invalidDomains = [] # list to hold all invalid domains to be RETURNED for further processing by main class
processThreads = 20
q_validateDomains = Queue(40) # FIFO queue; will be used by multithreads

# MAIN/START FUNCTION:
def vdmr_main_processDataSet(ext_dataset):   # start of class

    # Start validation of MX records:
    ce_logging ("vdmr_main_processDataSet", "Module STARTED. Starting process to validate MX records.", "INFO")

    # start threads to start processing...
    for _ in range(processThreads):  # number of processess to start
        t = Thread(target=__vdmr_processDataSet_validateDomains)
        t.daemon = True
        t.start()

    # put domain into queue for processing...
    ce_logging ("vdmr_main_processDataSet", "Number of domains to process: "+ str(len(ext_dataset)), "INFO")
    for domain in ext_dataset:
        q_validateDomains.put (domain) # add domain to queue for processing
    q_validateDomains.join()

    ce_logging ("vdmr_main_processDataSet", "Completed MX record validation.", "INFO")

    ce_logging ("vdmr_main_processDataSet", "Module COMPLETED. Sending results back to main script for further processing.", "INFO")
    return confirmed_invalidDomains  # return results back to the main class


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
        query(ext_domainToValidate, 'MX')
        print (ext_domainToValidate + ":: valid")
        return True # return positive as domain has a valid MX record
    except Exception:
        if ext_domainToValidate in domain_exclusionList:
            return True
        else:
            print (ext_domainToValidate + ":: INVALID")
            return False # return negative as domain has no valid MX record

def __vdmr_processDataSet_validateDomains_manageResult(ext_validationResult):
    confirmed_invalidDomains.append (ext_validationResult) # add the domain identified as invalid to a list that represents all domains of invalid MX records