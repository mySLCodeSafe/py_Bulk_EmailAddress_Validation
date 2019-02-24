class digitalCustomer():
    #def __init__(self, ext_WCS_ID=0, ext_email_ID):
     #   self.WCSID = ext_WCS_ID
      #  self.EmailAddress = str(ext_email_ID).lower()

    def __init__(self, ext_email_ID):
        self.EmailAddress = str(ext_email_ID).lower()
        self.ValidMXdomain = True # default value is True - every domain has a valid MX record unless indicated otherwise
