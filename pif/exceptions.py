class PifException(Exception):
    """
    Any custom exception thrown by the Python Injection Framework (PIF).
    """

    msg: str

    def __init__(self, msg: str = None, *args):
        super().__init__(*args)
        self.msg = msg or self.__doc__

    def __str__(self):
        return self.msg

    def __repr__(self):
        return f"<{type(self)}({self.msg!r})>"


class BlankProviderException(PifException):
    """
    Attempted to evaluate a BlankProvider. Make sure to override this first!
    """
