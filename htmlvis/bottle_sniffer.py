import time

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
        self.start_time = time.time()

    @property
    def transactions(self):
        return self._transactions

    def apply(self, callback, context):
        def decorator(*args, **kwargs):
            try:
                request = self._gather_request_info(context)
                return callback(*args, **kwargs)
            finally:
                transaction = Transaction(
                    client_name='client name',
                    request=request,
                    response=Response(
                        body=None, elapsed=None, headers=None, status=None),
                    server_name='server name')
                self.transactions.append(transaction)

        return decorator

    def _gather_request_info(self, context):
        elapsed_time = time.time() - self.start_time
        headers = {key: val for key, val in bottle.request.headers.items()}
        return Request(
            body=bottle.request.body.read(),
            elapsed=elapsed_time,
            headers=headers,
            method=context['method'],
            url_path=bottle.request.path)
