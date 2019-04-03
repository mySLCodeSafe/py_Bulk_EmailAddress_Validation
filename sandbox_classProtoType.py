class Customer:
    def __init__(self, ext_custEmailAddress, ext_isitValidMX = None):
        self.emailAddress = ext_custEmailAddress
        self.email_isitValidMX = ext_isitValidMX

    def get_emailAddressDomain(self):
        __emailAddress = self.emailAddress
        __emailDomain = __emailAddress.split('@')[1].lower()
        return __emailDomain

    def set_validMXDomain(self, ext_result):
        print ("set method: ", ext_result)
        self.email_isitValidMX = ext_result

    def get_validMXDomain(self):
        if (self.email_isitValidMX == None) or (self.email_isitValidMX == False):
            return False
        else:
            return True

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
        if self.orderNo == other.orderNo:
            self.orderStatus = "collected"
            return self.orderNo == other.orderNo
        else:
            return self.orderNo == other.orderNo

    def get_isitFastTrack(self):
        if (self.isitFastTrackOrder == 'N') or (self.isitFastTrackOrder == "(null") or (self.isitFastTrackOrder == None):
            return False
        else:
            return True

    def get_allDetails(self):
        return (":: " + str(self.emailAddress) +" , "+ str(self.get_emailAddressDomain()) +" , "+ str(self.get_validMXDomain()) +" , " + str(self.orderNo) +" , "+ str(self.orderStatus) + " , " + str(self.get_isitFastTrack()))

# load test data:

yo = set ()

yo.add (Order('first-first@first.com','0001','cancelled'))
yo.add (Order('first@first.com','0001','collected'))
yo.add (Order('second@second.com','0002','cancelled','Y'))
yo.add (Order('first@first.com','0001','cancelled'))
yo.add (Order('third@third.com','0003','collected'))
yo.add (Order('first@first.com','0001','collected'))
yo.add (Order('first-last@first.com','0001','cancelled'))

# print out test results:

print("output :: ")
for i in yo:
    if i.get_emailAddressDomain == "third.com":
        i.email_isitValidMX = True
     #   i.set_validMXDomain(True)
    print ("yo: ", i.get_allDetails())