class digitalCustomer():
    #def __init__(self, ext_WCS_ID=0, ext_email_ID):
     #   self.WCSID = ext_WCS_ID
      #  self.EmailAddress = str(ext_email_ID).lower()

    def __init__(self, ext_email_ID, ext_validMX=True):
        self.EmailAddress = str(ext_email_ID).lower()
        self.ValidMXdomain = ext_validMX