class digitalCustomer():
    #def __init__(self, ext_WCS_ID, ext_email_ID):
    def __init__(self, ext_email_ID):
     #   self.WCSID = ext_WCS_ID
        self.EmailAddress = str(ext_email_ID).lower()
        self.ValidMXdomain = True # default value is True - every domain has a valid MX record unless indicated otherwise