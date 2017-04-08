import bottle

from .htmlvis import HTTPSniffer, Request, Response, Transaction


class BottleSniffer(HTTPSniffer):
    """
    An Bottle plugin than can be installed in a Bottle application to capture
    HTTP transactions.
    See https://bottlepy.org/docs/dev/api.html#bottle.Bottle.install
    """

    def __init__(self):
        super(BottleSniffer, self).__init__()
        self._transactions = []

    @property
    def transactions(self):
        return self._transactions

    def apply(self, callback, context):
        def decorator(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            finally:
                transaction = Transaction(
                    client_name='client name',
                    request=Request(
                        body=bottle.request.body.read(),
                        elapsed=None,
                        headers=None,
                        method=None,
                        url_path=None),
                    response=Response(
                        body=None, elapsed=None, headers=None, status=None),
                    server_name='server name')
                self.transactions.append(transaction)

        return decorator
