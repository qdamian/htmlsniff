from collections import namedtuple

from attr import attrib, attrs

from . import plantuml


@attrs
class Request(object):
    url = attrib()
    elapsed = attrib()


@attrs
class Response(object):
    status = attrib()
    elapsed = attrib()


@attrs
class Transaction(object):
    client = attrib()
    server = attrib()
    request = attrib()
    response = attrib()


def seqdiag(output_file_path, sniffers):
    messages = []
    for sniffer in sniffers:
        for trans in sniffer.transactions:
            messages.append(
                plantuml.Message(
                    category='request',
                    src=trans.client,
                    dst=trans.server,
                    when=trans.request.elapsed,
                    data={'url': trans.request.url, }))
            messages.append(
                plantuml.Message(
                    category='response',
                    src=trans.server,
                    dst=trans.client,
                    when=trans.response.elapsed,
                    data={'status': trans.response.status, }))
    messages.sort(key=lambda msg: msg)
    plantuml.seqdiag(messages=messages)
