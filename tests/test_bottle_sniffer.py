import json
import time

import bottle
import pytest
import webtest
from htmlvis import BottleSniffer, HTTPSniffer, Transaction

app = bottle.Bottle()

CAPTURE_START_TIME = 0.123
SUCCESS_PROCESSING_TIME = 0.100
ERROR_PROCESSING_TIME = 0.050


@pytest.fixture(autouse=True)
def mock_time(mocker):
    mocker.patch('time.time')
    time.time.return_value = CAPTURE_START_TIME


@app.post('/success')
@app.get('/success')
def success():
    time.time.return_value = time.time() + SUCCESS_PROCESSING_TIME
    bottle.response.set_header('The-More', 'The-Merrier')
    return "To infinity and beyond!"


@app.post('/error')
@app.get('/error')
def expliciterror():
    time.time.return_value = time.time() + ERROR_PROCESSING_TIME
    bottle.response.status = 400
    bottle.response.set_header('Today-Is', 'No-Way')
    return 'Object already exists with that name'


@app.get('/http-response')
def httpresponse():
    body = json.dumps({'hello': 'world'})
    raise bottle.HTTPResponse(status=300, body=body)


@app.get('/http-error')
def httperror():
    raise bottle.HTTPError(status=404)


@app.post('/exception')
@app.get('/exception')
def exceptionalerror():
    time.time.return_value = time.time() + ERROR_PROCESSING_TIME
    1 / 0


def test_bottle_sniffer_is_an_http_sniffer():
    assert isinstance(BottleSniffer(), HTTPSniffer)


def test_bottle_sniffer_implements_api_version_2():
    # https://bottlepy.org/docs/dev/plugindev.html
    assert BottleSniffer().api == 2


def test_a_transaction_is_captured():
    test_app = webtest.TestApp(app)
    sniffer = BottleSniffer()
    app.install(sniffer)
    test_app.get('/success')
    assert len(sniffer.transactions) == 1
    assert isinstance(sniffer.transactions[0], Transaction)


def test_multiple_requests_are_captured():
    test_app = webtest.TestApp(app)
    sniffer = BottleSniffer()
    app.install(sniffer)
    for _ in range(100):
        test_app.get('/success').status
        with pytest.raises(webtest.app.AppError):
            test_app.get('/error').status
        with pytest.raises(webtest.app.AppError):
            test_app.get('/exception').status
    assert len(sniffer.transactions) == 300


class TestRequestDataCapturedInSuccessfulTransations():
    def test_sniffer_does_not_interfere(self):
        test_app = webtest.TestApp(app)
        app.install(BottleSniffer())
        assert test_app.get('/success').status == '200 OK'

    def test_the_request_body_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        test_app.post('/success', "Dreams + work")
        request = sniffer.transactions[0].request
        assert request.body == b"Dreams + work"

    def test_the_elapsed_time_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        REQUEST_TIME = 4.5
        time.time.return_value = REQUEST_TIME
        test_app.get('/success')
        request = sniffer.transactions[0].request
        expected_elapsed = REQUEST_TIME - CAPTURE_START_TIME
        assert abs(request.elapsed - expected_elapsed) < 0.0001

    def test_the_request_headers_are_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        test_app.get(
            '/success',
            headers={
                'Content-Type': 'application/json',
                'Some-Header': 'Some value'
            })
        request = sniffer.transactions[0].request
        # not comparing dictionaries because WebTest adds extra headers
        assert request.headers['Content-Type'] == 'application/json'
        assert request.headers['Some-Header'] == 'Some value'

    @pytest.mark.parametrize('method_call, method_name',
                             [('get', 'GET'), ('post', 'POST')])
    def test_the_request_method_is_captured(self, method_call, method_name):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        getattr(test_app, method_call)('/success')
        request = sniffer.transactions[0].request
        assert request.method == method_name

    def test_the_url_path_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        test_app.get('/success')
        request = sniffer.transactions[0].request
        assert request.url_path == '/success'


class TestRequestDataCapturedInFailedTransations():
    def test_sniffer_does_not_interfere(self):
        test_app = webtest.TestApp(app)
        app.install(BottleSniffer())
        with pytest.raises(webtest.app.AppError) as excinfo:
            test_app.get('/error')
        assert '400 Bad Request' in str(excinfo.value)
        assert 'Object already exists with that name' in str(excinfo.value)

    def test_sniffer_does_not_interfere_with_error_due_to_exceptions(self):
        test_app = webtest.TestApp(app)
        app.install(BottleSniffer())
        with pytest.raises(webtest.app.AppError) as excinfo:
            test_app.get('/exception')
        assert '500 Internal Server Error' in str(excinfo.value)

    @pytest.mark.parametrize('url', ['/error', '/exception'])
    def test_a_transaction_is_captured(self, url):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with pytest.raises(webtest.app.AppError):
            test_app.get(url)
        assert len(sniffer.transactions) == 1
        assert isinstance(sniffer.transactions[0], Transaction)

    @pytest.mark.parametrize('url', ['/error', '/exception'])
    def test_the_request_body_is_captured(self, url):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with pytest.raises(webtest.app.AppError):
            test_app.post(url, '2 + 2 = 5')
        request = sniffer.transactions[0].request
        assert request.body == b"2 + 2 = 5"

    def test_the_elapsed_time_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        REQUEST_TIME = 4.5
        time.time.return_value = REQUEST_TIME
        with pytest.raises(webtest.app.AppError):
            test_app.get('/error')
        request = sniffer.transactions[0].request
        expected_elapsed = REQUEST_TIME - CAPTURE_START_TIME
        assert abs(request.elapsed - expected_elapsed) < 0.0001

    @pytest.mark.parametrize('url', ['/error', '/exception'])
    def test_the_request_headers_are_captured(self, url):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with pytest.raises(webtest.app.AppError):
            test_app.get(
                url,
                headers={
                    'Content-Type': 'application/json',
                    'Some-Header': 'Some value'
                })
        request = sniffer.transactions[0].request
        # not comparing dictionaries because WebTest adds extra headers
        assert request.headers['Content-Type'] == 'application/json'
        assert request.headers['Some-Header'] == 'Some value'

    @pytest.mark.parametrize('method_call, method_name',
                             [('get', 'GET'), ('post', 'POST')])
    @pytest.mark.parametrize('url', ['/error', '/exception'])
    def test_the_request_method_is_captured(self, url, method_call,
                                            method_name):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with pytest.raises(webtest.app.AppError):
            getattr(test_app, method_call)('/error')
        request = sniffer.transactions[0].request
        assert request.method == method_name

    @pytest.mark.parametrize('url', ['/error', '/exception'])
    def test_the_url_path_is_captured(self, url):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with pytest.raises(webtest.app.AppError):
            test_app.get(url)
        request = sniffer.transactions[0].request
        assert request.url_path == url


class TestResponseDataCapturedInSuccessfulTransations():
    def test_the_response_body_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        test_app.post('/success')
        response = sniffer.transactions[0].response
        assert response.body == "To infinity and beyond!"

    def test_the_elapsed_time_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        REQUEST_TIME = 4.5
        time.time.return_value = REQUEST_TIME
        test_app.get('/success')
        response = sniffer.transactions[0].response
        expected_elapsed = (
            REQUEST_TIME - CAPTURE_START_TIME + SUCCESS_PROCESSING_TIME)
        assert abs(response.elapsed - expected_elapsed) < 0.0001

    def test_the_response_headers_are_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        test_app.post('/success')
        response = sniffer.transactions[0].response
        assert response.headers == {'The-More': 'The-Merrier'}

    def test_the_response_status_code_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        test_app.post('/success')
        response = sniffer.transactions[0].response
        assert response.status == '200 OK'


class TestResponsetDataCapturedInFailedTransations():
    def test_the_response_body_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with pytest.raises(webtest.app.AppError):
            test_app.get('/error')
        response = sniffer.transactions[0].response
        assert 'Object already exists with that name' in response.body

    @pytest.mark.parametrize('url', ['/error', '/exception'])
    def test_the_elapsed_time_is_captured(self, url):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        REQUEST_TIME = 4.5
        time.time.return_value = REQUEST_TIME
        with pytest.raises(webtest.app.AppError):
            test_app.get(url)
        response = sniffer.transactions[0].response
        expected_elapsed = (
            REQUEST_TIME - CAPTURE_START_TIME + ERROR_PROCESSING_TIME)
        assert abs(response.elapsed - expected_elapsed) < 0.0001

    def test_the_response_headers_are_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with pytest.raises(webtest.app.AppError):
            test_app.post('/error')
        response = sniffer.transactions[0].response
        assert response.headers == {'Today-Is': 'No-Way'}

    def test_the_response_status_code_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with pytest.raises(webtest.app.AppError):
            test_app.post('/error')
        response = sniffer.transactions[0].response
        assert response.status == '400 Bad Request'

    def test_status_code_is_captured_when_an_exception_is_raised(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with pytest.raises(webtest.app.AppError):
            test_app.post('/exception')
        response = sniffer.transactions[0].response
        assert response.status == '500 Internal Server Error'

    def test_status_code_is_captured_when_http_response_is_raised(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        test_app.get('/http-response')
        response = sniffer.transactions[0].response
        assert response.status == '300 Multiple Choices'

    def test_status_code_is_captured_when_http_error_is_raised(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with pytest.raises(webtest.app.AppError):
            test_app.get('/http-error')
        response = sniffer.transactions[0].response
        assert response.status == '404 Not Found'
