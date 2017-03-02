from collections import namedtuple

from htmlviz import plantuml

Request = namedtuple('Request', 'url, elapsed')
Response = namedtuple('Response', 'status, elapsed')
Transaction = namedtuple('Transaction', 'client, server, request, response')


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
