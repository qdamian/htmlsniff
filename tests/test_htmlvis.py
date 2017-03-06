import pytest

import htmlvis
from mock import Mock


@pytest.fixture(autouse=True)
def patch_seqdiag_draw(mocker):
    mocker.patch('htmlvis.seqdiag.draw')


@pytest.fixture
def successful_transaction():
    return htmlvis.Transaction(
        client='The Client',
        server='The Server',
        request=htmlvis.Request(
            method='PUT', url='/kindness', elapsed=0.1),
        response=htmlvis.Response(
            status='200 OK', elapsed=0.2))


@pytest.fixture
def error_transaction():
    return htmlvis.Transaction(
        client='The Client',
        server='The Server',
        request=htmlvis.Request(
            method='GET', url='/rudeness', elapsed=1.1),
        response=htmlvis.Response(
            status='404 Not Found', elapsed=1.2))


class TestSeqDiag(object):
    def test_creates_a_request_message_from_the_transaction_request(self, mocker,
                                                                    successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][0]
        assert request_msg.category == htmlvis.seqdiag.Category.request

    def test_the_client_is_the_message_source_in_requests(self, mocker, successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][0]
        assert request_msg.src == successful_transaction.client

    def test_the_server_is_the_message_destination_in_requests(self, mocker,
                                                               successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][0]
        assert request_msg.dst == successful_transaction.server

    def test_the_url_is_passed_as_additional_data_in_requests(self, mocker,
                                                              successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][0]
        assert request_msg.data['url'] == successful_transaction.request.url

    def test_creates_a_response_message_from_the_transaction_response(self, mocker,
                                                                      successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        response_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][1]
        assert response_msg.category == htmlvis.seqdiag.Category.response

    def test_the_server_is_the_message_source_in_responses(self, mocker, successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        response_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][1]
        assert response_msg.src == successful_transaction.server

    def test_the_client_is_the_message_destination_in_responses(self, mocker,
                                                                successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        response_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][1]
        assert response_msg.dst == successful_transaction.client

    def test_the_status_is_passed_as_additional_data_in_responses(self, mocker,
                                                                  successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        response_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][1]
        assert response_msg.data['status'] == successful_transaction.response.status

    def test_passes_both_request_and_response_to_the_sequence_diagram_generator(
            self, successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        messages = htmlvis.seqdiag.draw.call_args[1]['messages']
        assert len(messages) == 2

    def test_passes_multiple_transactions_to_the_sequence_diagram_generator(
            self, successful_transaction, error_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction, error_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        messages = htmlvis.seqdiag.draw.call_args[1]['messages']
        assert len(messages) == 4

    def test_converts_transactions_to_messages_ordered_by_elapsed_time(
            self, successful_transaction, error_transaction):
        successful_transaction.request.elapsed = 0.01
        successful_transaction.response.elapsed = 0.05
        error_transaction.request.elapsed = 0.02
        error_transaction.response.elapsed = 0.03
        sniffer = Mock()
        sniffer.transactions = [
            successful_transaction,
            error_transaction,
        ]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        messages = htmlvis.seqdiag.draw.call_args[1]['messages']
        msg_time = [msg.when for msg in messages]
        assert msg_time == [0.01, 0.02, 0.03, 0.05]

    def test_gets_transactions_from_all_sniffers(self, successful_transaction, error_transaction):
        sniffer_a = Mock()
        sniffer_a.transactions = [successful_transaction]
        sniffer_b = Mock()
        sniffer_b.transactions = [error_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer_a, sniffer_b])
        messages = htmlvis.seqdiag.draw.call_args[1]['messages']
        assert len(messages) == 4

    @pytest.mark.parametrize('transaction, expected_method',
                             [(successful_transaction, 'PUT'), (error_transaction, 'GET')])
    def test_includes_the_request_http_method_as_message_data(self, transaction, expected_method):
        sniffer = Mock()
        sniffer.transactions = [transaction()]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][0]
        assert request_msg.data['method'] == expected_method
