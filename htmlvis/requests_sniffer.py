import re
import time

from .htmlvis import HTTPSniffer, Request, Response, Transaction

try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit


class RequestsSniffer(HTTPSniffer):
    """An HTTP sniffer than can be hooked to the requests library
    See http://docs.python-requests.org/en/master/user/advanced/
    """

    def __init__(self, client_name, server_name):
        super(RequestsSniffer, self).__init__()
        self._transactions = []
        self._client_name = client_name
        self._server_name = server_name
        self._start_time = time.time()

    @property
    def transactions(self):
        return self._transactions

    def restart(self):
        self._start_time = time.time()
        del self._transactions[:]

    def __call__(self, response, *args, **kwargs):
        transaction = Transaction(
            client_name=self._client_name,
            server_name=self._server_name,
            request=self._extract_request_info(response),
            response=self._extract_response_info(response))
        self._transactions.append(transaction)

    def _extract_request_info(self, response):
        request = response.request
        response_elapsed_time = time.time() - self._start_time
        request_elapsed_time = max(
            response_elapsed_time - response.elapsed.total_seconds(), 0)
        parsed_url = urlsplit(request.url)
        url_host = parsed_url.netloc
        url_path = re.sub('.*' + url_host, '', request.url)
        headers = {key: value for key, value in request.headers.items()}
        return Request(
            body=request.body,
            elapsed=request_elapsed_time,
            headers=headers,
            method=request.method,
            url_path=url_path)

    def _extract_response_info(self, response):
        response_elapsed_time = time.time() - self._start_time
        status_and_reason = str(response.status_code)
        if response.reason:
            status_and_reason += ' ' + response.reason
        headers = {key: value for key, value in response.headers.items()}
        return Response(
            body=response.text,
            elapsed=response_elapsed_time,
            headers=headers,
            status=status_and_reason)
