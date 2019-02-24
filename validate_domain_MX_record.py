__author__ = "shami.lakhani@homeretailgroup.com"

#from urlparse import urlparse
from threading import Thread
import threading
import sys, os, re
import traceback # checked
from coreengine import * # checked


from queue import Queue
q_validateDomains = Queue(8)
confirmed_invalidDomains = set ()

def vdmr_main(dataset):
    extractedDomains = __vdmr_ExtractDomains(dataset)

    for i in range(4):
        t = Thread(target=__vdmr_ValidateDomains)
        t.daemon = True
        t.start()

    for domain in extractedDomains:
        q_validateDomains.put (domain)
    q_validateDomains.join()


    return confirmed_invalidDomains



def __vdmr_ExtractDomains(ext_dataset):
    cust_DataSet = ext_dataset
    extractedDomains = set()
    ce_logging ("ExtractDomainsFor_MX_Validation","Iterating through e-mail address in cust_dataset to extract domains for futher validation","DEBUG")
    for i in cust_DataSet:
        try:
            # cust_DataSet_EmailAddress = i.EmailAddress.split('@')[1] # split the domain out of the e-mail address  # DEBUG
            cust_DataSet_EmailAddress = i.EmailAddress
            extractedDomains.add(cust_DataSet_EmailAddress) # add the domain to the invalid list for validation later
        except Exception:
            traceback_Message = traceback.format_exc()
            ce_logging ("ValidateDomains_MX","Error occured with " + str(i.EmailAddress) +" --> "+str(traceback_Message),"ERROR")
    len_inValidMXDomains = len(extractedDomains) # how many unique domains were extracted from the input file
    ce_logging ("ExtractDomainsFor_MX_Validation","Completed extraction of domains. Identified "+ str(len_inValidMXDomains)+" unique domains","INFO")
    return extractedDomains

def __vdmr_ValidateDomains():
    #ce_logging ("ValidateDomains_MX","Iterating through extracted unique domains and testing for a valid MX record","DEBUG")
    while True:
        domainToValidate = q_validateDomains.get()
        validateDomainResult= ce_validateDomain_MX_viaLocal(domainToValidate)
        if validateDomainResult == False:
            __vdmr_ValidateDomains_ManageResult(domainToValidate)
        q_validateDomains.task_done()

def __vdmr_ValidateDomains_ManageResult(ext_validationResult):
    confirmed_invalidDomains.add(ext_validationResult)


