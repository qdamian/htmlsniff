import attr
import json
import time

import requests
from pytest import fixture, mark, raises

import responses
from htmlvis import HTTPSniffer, SniffingRequestsPlugin


@fixture
def success_response():
    responses.add(
        responses.GET,
        'http://mysniffer.com/api/1/success',
        json={"greeting": "hi there!"}, )


@fixture
def error_response():
    responses.add(
        responses.GET,
        'http://mysniffer.com/api/1/notfound',
        json={"error": "not found"},
        status=404)


class TestHTTPSniffer:
    def test_requires_a_transactions_property_to_be_available(self):
        with raises(NotImplementedError):
            HTTPSniffer().transactions

    def test_exposes_a_restart_method(self):
        with raises(NotImplementedError):
            HTTPSniffer().restart()


class TestSniffingRequestsPlugin:
    def test_implements_http_sniffer(self):
        assert issubclass(SniffingRequestsPlugin, HTTPSniffer)

    @responses.activate
    def test_intercepts_one_request(self, success_response):
        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        response.raise_for_status()
        assert len(sniffing_hook.transactions) == 1

    @responses.activate
    def test_intercepts_two_requests(self, success_response):
        sniffing_hook = SniffingRequestsPlugin('', '')
        first_response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        first_response.raise_for_status()
        second_response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        second_response.raise_for_status()
        assert len(sniffing_hook.transactions) == 2

    @responses.activate
    def test_records_the_request_method(self, success_response):
        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        assert transaction.request.method == 'GET'

    @responses.activate
    def test_records_the_request_url_path(self, success_response):
        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        assert transaction.request.url_path == '/api/1/success'

    @responses.activate
    @mark.parametrize(
        "url, response_fixture",
        [('http://mysniffer.com/api/1/success', success_response),
         ('http://mysniffer.com/api/1/notfound', error_response)])
    def test_transactions_are_json_serializable(self, url, response_fixture):
        response_fixture()
        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(url, hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        json.dumps(attr.asdict(transaction))

    @responses.activate
    def test_records_the_request_headers(self, success_response):
        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            headers={
                'Accept': 'application/json',
                'Better-Safe': 'Than/Sorry'
            },
            hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        assert transaction.request.headers['Accept'] == 'application/json'
        assert transaction.request.headers['Better-Safe'] == 'Than/Sorry'

    @responses.activate
    def test_records_the_request_body_if_content_type_is_json(
            self, success_response):
        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            json={'Better safe': 'Than sorry'},
            hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        # FIXME: should be str instead of bytes?
        assert transaction.request.body == b'{"Better safe": "Than sorry"}'

    @responses.activate
    def test_records_the_request_body_if_content_is_plain_text(
            self, success_response):
        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            data='Better safe than sorry',
            hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        # FIXME: should be bytes instead of str?
        assert transaction.request.body == 'Better safe than sorry'

    @responses.activate
    def test_measures_elapsed_time_for_one_transaction(self, success_response):
        sniffing_hook = SniffingRequestsPlugin('', '')
        start_time = time.time()
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        elapsed_time = time.time() - start_time
        response.raise_for_status()
        transaction = sniffing_hook.transactions[0]
        assert 0 <= transaction.request.elapsed <= elapsed_time
        assert 0 <= transaction.response.elapsed <= elapsed_time
        assert 0 <= transaction.request.elapsed <= transaction.response.elapsed

    @responses.activate
    def test_measures_elapsed_time_for_two_transactions(self, mocker):
        mocker.patch('time.time')
        time.time.return_value = 0.1
        sniffing_hook = SniffingRequestsPlugin('', '')
        success_response()
        start_time = time.time()
        time.time.return_value = 0.5
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        success_response()
        first_elapsed_time = time.time() - start_time
        time.time.return_value = 2.2
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        second_elapsed_time = time.time() - start_time
        response.raise_for_status()
        first_transaction = sniffing_hook.transactions[0]
        second_transaction = sniffing_hook.transactions[1]
        assert first_elapsed_time <= second_transaction.request.elapsed <= second_elapsed_time
        assert first_elapsed_time <= second_transaction.response.elapsed <= second_elapsed_time
        assert first_elapsed_time <= second_transaction.request.elapsed <= second_transaction.response.elapsed

    @responses.activate
    def test_records_the_response_headers(self):
        responses.add(
            responses.GET,
            'http://mysniffer.com/api/1/success',
            adding_headers={
                'Better-Safe': 'Than/Sorry',
                'Content-Type': 'application/json'
            })

        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        assert transaction.response.headers[
            'Content-Type'] == 'application/json'
        assert transaction.response.headers['Better-Safe'] == 'Than/Sorry'

    @responses.activate
    def test_records_the_response_body_if_content_type_is_json(self):
        responses.add(
            responses.GET,
            'http://mysniffer.com/api/1/success',
            json={'Better safe': 'Than sorry'})
        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        assert transaction.response.body == '{"Better safe": "Than sorry"}'

    @responses.activate
    def test_records_the_response_body_if_content_is_plain_text(self):
        responses.add(
            responses.GET,
            'http://mysniffer.com/api/1/success',
            body='Better safe than sorry')
        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        assert transaction.response.body == 'Better safe than sorry'

    @responses.activate
    def test_records_the_response_status_for_a_success_response(
            self, success_response):
        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        assert transaction.response.status == '200'

    @responses.activate
    def test_records_the_response_status_for_an_error_response(self,
                                                               error_response):
        sniffing_hook = SniffingRequestsPlugin('', '')
        response = requests.get(
            'http://mysniffer.com/api/1/notfound',
            hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        assert transaction.response.status == '404'

    @responses.activate
    def test_transaction_includes_the_client_and_server_name(self,
                                                             success_response):
        sniffing_hook = SniffingRequestsPlugin('Client name', 'Server name')
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        transaction = sniffing_hook.transactions[0]
        assert transaction.client_name == 'Client name'
        assert transaction.server_name == 'Server name'

    @responses.activate
    def test_restart_resets_the_elapsed_time(self, mocker):
        mocker.patch('time.time')
        time.time.return_value = 0.1
        sniffing_hook = SniffingRequestsPlugin('', '')
        success_response()
        start_time = time.time()
        time.time.return_value = 0.5
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        time.time.return_value = 2.0
        success_response()
        first_elapsed_time = time.time() - start_time
        first_transaction = sniffing_hook.transactions[0]
        sniffing_hook.restart()
        time.time.return_value = 2.2
        response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        second_elapsed_time = time.time() - start_time
        response.raise_for_status()
        second_transaction = sniffing_hook.transactions[0]
        assert second_transaction.request.elapsed < first_transaction.response.elapsed

    @responses.activate
    def test_restart_resets_the_captured_transactions(self, success_response):
        sniffing_hook = SniffingRequestsPlugin('', '')
        first_response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        first_response.raise_for_status()
        sniffing_hook.restart()
        second_response = requests.get(
            'http://mysniffer.com/api/1/success',
            hooks={'response': sniffing_hook})
        second_response.raise_for_status()
        assert len(sniffing_hook.transactions) == 1


@fixture
def transactions_response():
    responses.add(
        responses.GET,
        'http://mysniffer.com/sniffer/transactions',
        json={
            "transactions": [{
                "client_name": "Client name",
                "server_name": "Server name",
                "request": {
                    "body": '{"a": 1, "b": 2}',
                    "elapsed": 1.2,
                    "headers": {
                        "Accept": "application/json"
                    },
                    "method": "POST",
                    "url_path": "/some/url",
                },
                "response": {
                    "body": "",
                    "elapsed": 1.4,
                    "headers": "",
                    "status": "",
                }
            }, {
                "client_name": "Client name",
                "server_name": "Server name",
                "request": {
                    "body": "",
                    "elapsed": 2.3,
                    "headers": [""],
                    "method": "GET",
                    "url_path": "/another/url",
                },
                "response": {
                    "body": "",
                    "elapsed": "",
                    "headers": "",
                    "status": "",
                }
            }]
        })
