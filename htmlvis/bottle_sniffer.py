"""
Bottle plugin to sniff HTTP transactions.
See https://bottlepy.org/docs/dev/plugindev.html
"""
import time

import bottle

from .htmlvis import HTTPSniffer, Request, Response, Transaction


class BottleSniffer(HTTPSniffer):
    """
    A Bottle plugin than can be installed in a Bottle application to capture
    HTTP transactions.
    See https://bottlepy.org/docs/dev/api.html#bottle.Bottle.install
    """
    api = 2

    def __init__(self):
        super(BottleSniffer, self).__init__()
        self._transactions = []
        self.start_time = time.time()

    @property
    def transactions(self):
        return self._transactions

    def apply(self, callback, context):
        """
        Transparently sniff a request, invoke the callback that processes it,
        and finally sniff the returned response
        """

        def decorator(*args, **kwargs):
            response_status = '500 Internal Server Error'
            handler_response = ''
            try:
                request = self._gather_request_info(context)
                handler_response = callback(*args, **kwargs)
                response_status = bottle.response.status
                return handler_response
            except bottle.HTTPResponse as http_error:
                response_status = http_error.status
                raise
            finally:
                response = self._gather_response_info(
                    context, handler_response, response_status)
                transaction = Transaction(
                    client_name='client name',
                    request=request,
                    response=response,
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
            method=context.method,
            url_path=bottle.request.path)

    def _gather_response_info(self, context, handler_response, status):
        elapsed_time = time.time() - self.start_time
        headers = {key: val for key, val in bottle.response.headers.items()}
        return Response(
            body=handler_response,
            elapsed=elapsed_time,
            headers=headers,
            status=status)
