import pytest

import htmlviz
from htmlviz import plantuml
from mock import Mock


class TestSeqDiag(object):
    def test_converts_sniffers_transactions_to_ordered_messages(self, mocker):
        mocker.patch('htmlviz.plantuml.seqdiag')
        sniffer = Mock()
        sniffer.transactions = [
            htmlviz.Transaction(
                client='The Client',
                server='The Server',
                request=htmlviz.Request(
                    url='/kindness', elapsed=0.01),
                response=htmlviz.Response(
                    status='200 OK', elapsed=0.05)),
            htmlviz.Transaction(
                client='The Client',
                server='The Server',
                request=htmlviz.Request(
                    url='/rudeness', elapsed=0.02),
                response=htmlviz.Response(
                    status='404 Not Found', elapsed=0.03)),
        ]
        htmlviz.seqdiag('/fake/path', [sniffer])
        messages = plantuml.seqdiag.call_args[1]['messages']
        assert messages[0].when == 0.01
        assert messages[1].when == 0.02
        assert messages[2].when == 0.03
        assert messages[3].when == 0.05
