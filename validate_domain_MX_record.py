__author__ = "shami.lakhani@homeretailgroup.com"
__version__ = "1 - base build"

import traceback
from threading import Thread, current_thread
from queue import Queue
from coreengine import ce_logging

confirmed_invalidDomains = []
q_validateDomains = Queue(20) # queue size for multithread (normal set double of process size)

def __vdmr_processDataSet_validateDomains():
    ce_logging ("__vdmr_processDataSet_validateDomains","Started thread: "+str(current_thread()),"INFO")
    try:
        while True:
            domainToValidate = q_validateDomains.get()
            validateDomainResult= __vdmr_validateDomain_slow(domainToValidate)
           # print ("vdmr_processDataSet: ", validateDomainResult)
            if validateDomainResult == False:
                __vdmr_processDataSet_validateDomains_manageResult(domainToValidate)
            q_validateDomains.task_done()
    except Exception:
        traceback_Message = traceback.format_exc()
        ce_logging ("__vdmr_processDataSet_extractDomains", "Error occured with " + str(domainToValidate) +" --> "+str(traceback_Message),"ERROR")

def __vdmr_processDataSet_validateDomains_manageResult(ext_validationResult):
    confirmed_invalidDomains.append(ext_validationResult)

def __vdmr_processDataSet_extractDomainsFromEmail(ext_dataset):
    __cust_DataSet = ext_dataset
    __extractedDomains = set ()
    try:
        for i in __cust_DataSet:
            __extractedDomains.add(__vdmr_extractDomain(i.EmailAddress))
        ce_logging ("__vdmr_processDataSet_extractDomains", "Total # unique domains identified: " + str(len(__extractedDomains)),"INFO")
    except Exception:
        traceback_Message = traceback.format_exc()
        ce_logging ("__vdmr_processDataSet_extractDomains", "Error occured with " + str(i.EmailAddress) +" --> "+str(traceback_Message),"ERROR")
    return __extractedDomains



def __vdmr_extractDomain(ext_emailAddress):
  #  print ("vdmr_extractDomain in:", ext_emailAddress)
    __emailDomain = ext_emailAddress.split('@')[1]
  #  print ("vdmr_extractDomain out:", ext_emailAddress)
    return __emailDomain

def __vdmr_validateDomain_slow(ext_domainToValidate):  # function performing under cache to reduce the number of calls
    try:
        from dns.resolver import query
        domain = ext_domainToValidate
        rtn_result = False
        query(domain, 'MX')
        print (domain, " : True")
        return True # return positive as domain has a valid MX record
    except Exception:
        print (domain, " : False")
        return rtn_result # return negative as domain has no valid MX record

def __vdmr_validateDomain_fast(ext_domainToValidate):
    import dns.query
    domainToValidate = ext_domainToValidate
    DNS_SERVERS = ['172.18.20.100', '172.30.21.96'] # Internal name servers to launch query against
    #DNS_SERVERS = ['1.1.1.1'] # External name servers to launch query against
    __validationResult = False
    dns_lookup_construct = dns.message.make_query(domainToValidate, dns.rdatatype.MX)
    dns_lookup_response = dns.query.udp(dns_lookup_construct, DNS_SERVERS[0], timeout=10)
    if (bool(dns_lookup_response.answer)):
        __validationResult = True
    return __validationResult

def vdmr_main_processDataSet(dataset):   # start of class
    for _ in range(100):  # number of processess to start
        t = Thread(target=__vdmr_processDataSet_validateDomains)
        t.daemon = True
        t.start()

    for domain in __vdmr_processDataSet_extractDomainsFromEmail(dataset):
        q_validateDomains.put (domain)
    q_validateDomains.join()

    return confirmed_invalidDomains  # return results back to the main class