import htmlvis
import pytest
from mock import Mock, mock_open


@pytest.fixture(autouse=True)
def patch_seqdiag_draw(mocker):
    mocker.patch('htmlvis.seqdiag.draw')


@pytest.fixture(autouse=True)
def patch_open(mocker):
    try:
        mocker.patch('builtins.open', mock_open())
    except ImportError:
        mocker.patch('__builtin__.open', mock_open())


@pytest.fixture
def successful_transaction():
    return htmlvis.Transaction(
        client_name='The Client',
        server_name='The Server',
        request=htmlvis.Request(
            body='',
            elapsed=0.1,
            headers={},
            method='PUT',
            url_path='/kindness'),
        response=htmlvis.Response(
            body='', elapsed=0.2, headers={}, status='200 OK'))


@pytest.fixture
def error_transaction():
    return htmlvis.Transaction(
        client_name='The Client',
        server_name='The Server',
        request=htmlvis.Request(
            body='',
            elapsed=1.1,
            headers={},
            method='GET',
            url_path='/rudeness'),
        response=htmlvis.Response(
            body='', elapsed=1.2, headers={}, status='404 Not Found'))


class TestRequestProcessingInSaveSeqDiag(object):
    def test_creates_a_request_message_from_the_transaction_request(
            self, mocker, successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][0]
        assert request_msg.category == htmlvis.seqdiag_model.Category.request

    def test_the_client_is_the_message_source(self, mocker,
                                              successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][0]
        assert request_msg.src == successful_transaction.client_name

    def test_the_server_is_the_message_destination(self, mocker,
                                                   successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][0]
        assert request_msg.dst == successful_transaction.server_name

    def test_the_url_is_passed_as_additional_data(self, mocker,
                                                  successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][0]
        assert request_msg.data[
            'url'] == successful_transaction.request.url_path

    @pytest.mark.parametrize(
        'transaction, expected_method',
        [(successful_transaction, 'PUT'), (error_transaction, 'GET')])
    def test_includes_the_http_method_as_message_data(self, transaction,
                                                      expected_method):
        sniffer = Mock()
        sniffer.transactions = [transaction()]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][0]
        assert request_msg.data['method'] == expected_method

    @pytest.mark.parametrize('transaction, expected_text',
                             [(successful_transaction, 'PUT /kindness'),
                              (error_transaction, 'GET /rudeness')])
    def test_combines_http_method_and_url_path_as_message_text(
            self, transaction, expected_text):
        sniffer = Mock()
        sniffer.transactions = [transaction()]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][0]
        assert request_msg.text == expected_text


class TestResponseProcessingInSaveSeqDiag(object):
    def test_creates_a_response_message_from_the_transaction_response(
            self, mocker, successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        response_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][1]
        assert response_msg.category == htmlvis.seqdiag_model.Category.response

    def test_the_server_is_the_message_source(self, mocker,
                                              successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        response_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][1]
        assert response_msg.src == successful_transaction.server_name

    def test_the_client_is_the_message_destination(self, mocker,
                                                   successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        response_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][1]
        assert response_msg.dst == successful_transaction.client_name

    def test_the_status_is_passed_as_additional_data(self, mocker,
                                                     successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        response_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][1]
        assert response_msg.data[
            'status'] == successful_transaction.response.status

    @pytest.mark.parametrize('transaction, expected_text',
                             [(successful_transaction, '200 OK'),
                              (error_transaction, '404 Not Found')])
    def test_uses_the_status_as_message_text(self, transaction, expected_text):
        sniffer = Mock()
        sniffer.transactions = [transaction()]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        request_msg = htmlvis.seqdiag.draw.call_args[1]['messages'][1]
        assert request_msg.text == expected_text


class TestTransactionProcessingInSaveSeqDiag(object):
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

    def test_gets_transactions_from_all_sniffers(self, successful_transaction,
                                                 error_transaction):
        sniffer_a = Mock()
        sniffer_a.transactions = [successful_transaction]
        sniffer_b = Mock()
        sniffer_b.transactions = [error_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer_a, sniffer_b])
        messages = htmlvis.seqdiag.draw.call_args[1]['messages']
        assert len(messages) == 4

    def test_opens_the_output_file_path_for_writing(self, mocker,
                                                    successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        open.assert_called_once_with('/fake/path', 'w')

    def test_writes_the_html_sequence_diagram_to_the_output_file(
            self, mocker, successful_transaction):
        sniffer = Mock()
        sniffer.transactions = [successful_transaction]
        htmlvis.save_seq_diag('/fake/path', [sniffer])
        open.return_value.write.assert_called_once_with(
            htmlvis.seqdiag.draw.return_value)
