
class BException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class TimeoutException(BException):
    def __init__(self, msg):
        BException.__init__(self, msg)