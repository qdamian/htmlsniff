from collections import namedtuple

from attr import attrib, attrs

from . import plantuml


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


def seqdiag(output_file_path, sniffers):
    """Generate a sequence diagram based on the transactions captured
    by the given HTTP sniffers
    """
    messages = []
    for sniffer in sniffers:
        for trans in sniffer.transactions:
            messages += _split_transaction_into_messages(trans)
    messages.sort(key=lambda msg: msg)
    plantuml.seqdiag(messages=messages)


def _split_transaction_into_messages(transaction):
    msgs = []
    msgs += [
        plantuml.Message(
            category='request',
            src=transaction.client,
            dst=transaction.server,
            when=transaction.request.elapsed,
            data={
                'method': transaction.request.method,
                'url': transaction.request.url,
            })
    ]
    msgs += [
        plantuml.Message(
            category='response',
            src=transaction.server,
            dst=transaction.client,
            when=transaction.response.elapsed,
            data={'status': transaction.response.status})
    ]
    return msgs
