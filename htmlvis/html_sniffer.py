class HTTPSniffer(object):
    """A class that captures network traffic at either client or server side and
    records information about each HTTP transaction, such as URLs, headers,
    bodies, etc
    """

    @property
    def transactions(self):
        """A list of Transaction objects"""
        raise NotImplementedError()

    def restart(self):
        """Clear the captured transactions and reset the capture clock"""
        raise NotImplementedError()
