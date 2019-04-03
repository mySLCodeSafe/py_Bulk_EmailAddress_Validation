class sterlingCustomer(object):
    def __init__(self, ext_orderNo, ext_orderStatus, ext_email_ID, ext_fastTrack=None, ext_validMXdomain=None):
        self.orderNo = ext_orderNo
        self.orderStatus = ext_orderStatus
        self.fastTrackOrder = ext_fastTrack
        self.emailAddress = ext_email_ID
        self.validMXdomain = ext_validMXdomain

    def set_validMXDomain(self, ext_result):
        self.validMXdomain = ext_result

    def get_validMXDomain(self):
        if (self.validMXdomain == None) or (self.validMXdomain == False):
            return False
        else:
            return True

    def get_emailAddressDomain(self):
        __emailAddress = self.emailAddress
        __emailDomain = __emailAddress.split('@')[1].lower()
        return __emailDomain

    def get_emailAddress(self): # return back a boolean value to indicate if the email address structure is correct
        rtn_result = self.emailAddress.lower()
        return rtn_result

    def get_fastTrackOrder(self):
        if self.fastTrackOrder == 'N':
            return False
        else:
            return True

    def get_orderStatus(self):
        return self.get_orderStatus
