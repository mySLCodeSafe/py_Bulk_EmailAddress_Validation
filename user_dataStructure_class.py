class Customer:
    def __init__(self, ext_custEmailAddress):
        self.emailAddress = ext_custEmailAddress

    def get_emailAddressDomain(self):
        __emailAddress = self.emailAddress
        __emailDomain = __emailAddress.split('@')[1].lower()
        return __emailDomain

class Order(Customer):
    def __init__(self, ext_custEmailAddress, ext_orderNo, ext_orderStatus, ext_isitFastTrack=None):
        self.orderNo = ext_orderNo
        self.orderStatus = ext_orderStatus
        self.isitFastTrackOrder = ext_isitFastTrack
        Customer.__init__(self,ext_custEmailAddress)

    # Override - set hash of class based on order number
    def __hash__(self):
        return (hash(self.orderNo))

    # Override - only keep DUPLICATE orders that have a 'collected' status
    def __eq__(self, other):
        if self.orderStatus == "3700.6" or other.orderStatus == "3700.6":
            self.orderStatus = "3700.6"
        else:
            self.orderStatus = "9000"
        return self.orderNo == other.orderNo

    def get_isitFastTrack(self):
        if (self.isitFastTrackOrder == 'N') or (self.isitFastTrackOrder == "(null") or (self.isitFastTrackOrder == None):
            return False
        else:
            return True

    def get_allDetails(self):
        delimiterchar=","
        return (str(self.orderNo)+delimiterchar+str(self.orderStatus)+delimiterchar+str(self.get_isitFastTrack())+delimiterchar+str(self.emailAddress))