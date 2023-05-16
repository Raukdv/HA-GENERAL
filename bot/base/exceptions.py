class BOTException(Exception):
    def __init__(self, msg=None, logger=None):
        if logger:
            logger(instance=self, data=msg)
        return super().__init__(msg)

class CredentialInvalid(BOTException):
    pass
