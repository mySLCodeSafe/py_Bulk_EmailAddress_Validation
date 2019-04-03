# Module to validate domains for MX records. Customised for program: validate-domain_MX_record.py

import traceback
from threading import Thread, current_thread
from queue import Queue
from coreengine import ce_logging, ce_tmp_folder

# Module parameters/variables:
confirmed_invalidDomains = set () # list to hold all invalid domains to be RETURNED for further processing by main class
processThreads = 5
q_validateDomains = Queue(10) # FIFO queue; will be used by multithreads


# MAIN/START FUNCTION:
def vdmr_main_processDataSet(ext_dataset, ext_exportToFileSwitch):   # start of class

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

    # Export invalid domains? :
    if ext_exportToFileSwitch == True:
        ce_logging("vdmr_main_processDataSet","Export to file switch was set to True. Starting export process.","INFO")
        __vdmr_exportToFileInvalidDomains()

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
        from dns.resolver import query
        domain = ext_domainToValidate
        query(domain, 'MX')
        print (domain + ":: valid")
        return True # return positive as domain has a valid MX record
    except Exception:
        print (domain + ":: INvalid")
        return False # return negative as domain has no valid MX record

def __vdmr_processDataSet_validateDomains_manageResult(ext_validationResult):
    confirmed_invalidDomains.add (ext_validationResult) # add the domain identified as invalid to a list that represents all domains of invalid MX records

def __vdmr_exportToFileInvalidDomains():
    import time
    tempFile = ce_tmp_folder+"invalidDomainsList_"+(time.strftime("%Y%m%d%H%M%S"))+".tmp" # temp file to hold invalid domain list
    try:
        with open(tempFile, 'w') as f: # write out the invalid domain list to the temp folder
            for domain in confirmed_invalidDomains: f.write(str(domain) + '\n')
            ce_logging ("vdmr_exportToFileInvalidDomains","Completed exporting invalid domains to file: "+tempFile,"INFO")
    except Exception:
        traceback_Message = traceback.format_exc()
        ce_logging ("vdmr_main_processDataSet", "Error occured: "+traceback_Message, "ERROR")