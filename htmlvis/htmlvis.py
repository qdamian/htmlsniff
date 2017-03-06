from attr import attrib, attrs

from . import seqdiag


@attrs
class Request(object):
    """Simplified representation of an HTTP request."""
    method = attrib()
    url = attrib()
    elapsed = attrib()


@attrs
class Response(object):
    """Simplified representation of an HTTP response."""
    status = attrib()
    elapsed = attrib()


@attrs
class Transaction(object):
    """Simplified representation of a request-response pair."""
    client = attrib()
    server = attrib()
    request = attrib()
    response = attrib()


def save_seq_diag(output_file_path, sniffers):
    """Generate a sequence diagram based on the transactions captured
    by the given HTTP sniffers
    """
    messages = []
    for sniffer in sniffers:
        for trans in sniffer.transactions:
            messages += _convert_html_transactions_to_seq_diag_msgs(trans)
    messages.sort(key=lambda msg: msg.when)
    seqdiag.draw(messages=messages)


def _convert_html_transactions_to_seq_diag_msgs(transaction):
    msgs = []
    msgs += [
        seqdiag.Message(
            category=seqdiag.Category.request,
            src=transaction.client,
            dst=transaction.server,
            text='',
            when=transaction.request.elapsed,
            data={
                'method': transaction.request.method,
                'url': transaction.request.url,
            })
    ]
    msgs += [
        seqdiag.Message(
            category=seqdiag.Category.response,
            src=transaction.server,
            dst=transaction.client,
            text='',
            when=transaction.response.elapsed,
            data={'status': transaction.response.status})
    ]
    return msgs
