from attr import attrib, attrs

from . import seqdiag
from . import seqdiag_model


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


@attrs
class Request(object):
    """Simplified representation of an HTTP request."""
    body = attrib()
    elapsed = attrib()
    headers = attrib()
    method = attrib()
    url_path = attrib()


@attrs
class Response(object):
    """Simplified representation of an HTTP response."""
    body = attrib()
    elapsed = attrib()
    headers = attrib()
    status = attrib()


@attrs
class Transaction(object):
    """Simplified representation of a request-response pair."""
    client_name = attrib()
    request = attrib()
    response = attrib()
    server_name = attrib()


def save_seq_diag(output_file_path, sniffers):
    """Generate a sequence diagram based on the transactions captured
    by the given HTTP sniffers
    """
    messages = []
    for sniffer in sniffers:
        for trans in sniffer.transactions:
            messages += _convert_to_seq_diag_messages(trans)
    messages.sort(key=lambda msg: msg.when)

    with open(output_file_path, 'w') as output_file:
        html_seqdiag = seqdiag.draw(messages=messages)
        print('html diagram: %s' % html_seqdiag)
        output_file.write(html_seqdiag)


def _convert_to_seq_diag_messages(transaction):
    request = transaction.request
    request_msg = seqdiag_model.Message(
        category=seqdiag_model.Category.request,
        src=transaction.client_name,
        dst=transaction.server_name,
        text='%s %s' % (request.method, request.url_path),
        when=request.elapsed,
        data={
            'method': request.method,
            'url': request.url_path,
        })
    response = transaction.response
    response_msg = seqdiag_model.Message(
        category=seqdiag_model.Category.response,
        src=transaction.server_name,
        dst=transaction.client_name,
        text=response.status,
        when=response.elapsed,
        data={'status': response.status})
    return [request_msg, response_msg]
