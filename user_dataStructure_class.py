class digitalCustomer():
    def __init__(self, ext_WCS_ID, ext_email_ID):
        self.custID = ext_WCS_ID
        self.emailAddress = str(ext_email_ID).lower() # store the e-mail address in lower char set
        self.validMXdomain = None # default value is True - every domain has a valid MX record unless indicated otherwise

    def get_emailAddressDomain(self):  # return back the domain from the email address
        return self.emailAddress.split('@')[1]

    def get_validEmailAddress(self): # return back a boolean value to indicate if the email address structure is correct
        from validate_email import validate_email
        rtn_result = validate_email(self.emailAddress)
        return rtn_result