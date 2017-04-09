import time

import bottle
import pytest
import webtest
from htmlvis import BottleSniffer, HTTPSniffer, Transaction

app = bottle.Bottle()


@pytest.fixture(autouse=True)
def mock_time(mocker):
    mocker.patch('time.time')
    time.time.return_value = 10.123


@app.post('/success')
@app.get('/success')
def success():
    time.time.return_value = time.time() + 0.100
    return "To infinity and beyond!"


@app.post('/error')
@app.get('/error')
def expliciterror():
    time.time.return_value = time.time() + 0.200
    bottle.response.status = 400
    return 'Object already exists with that name'


@app.post('/exception')
@app.get('/exception')
def exceptionalerror():
    1 / 0


def test_bottle_sniffer_is_an_http_sniffer():
    assert isinstance(BottleSniffer(), HTTPSniffer)


class TestSuccessfulTransactions():
    def test_sniffer_does_not_interfere(self):
        test_app = webtest.TestApp(app)
        app.install(BottleSniffer())
        assert test_app.get('/success').status == '200 OK'

    def test_a_transaction_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        test_app.get('/success')
        assert len(sniffer.transactions) == 1
        assert isinstance(sniffer.transactions[0], Transaction)

    def test_the_request_body_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        test_app.post('/success', "Dreams + work")
        request = sniffer.transactions[0].request
        assert request.body == b"Dreams + work"

    def test_the_elapsed_time_is_captured(self):
        test_app = webtest.TestApp(app)
        time.time.return_value = 2.3
        sniffer = BottleSniffer()
        app.install(sniffer)
        time.time.return_value = 4.5
        test_app.get('/success')
        request = sniffer.transactions[0].request
        assert abs(request.elapsed - 2.2) < 0.0001

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


class TestErrorTransactions():
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
        time.time.return_value = 2.3
        sniffer = BottleSniffer()
        app.install(sniffer)
        time.time.return_value = 4.5
        with pytest.raises(webtest.app.AppError):
            test_app.get('/error')
        request = sniffer.transactions[0].request
        assert abs(request.elapsed - 2.2) < 0.0001

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
