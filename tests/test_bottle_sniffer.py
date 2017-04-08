import bottle
import webtest
from htmlvis import BottleSniffer, HTTPSniffer, Transaction
from pytest import raises

app = bottle.Bottle()


@app.route('/success')
def success():
    return "To infinity and beyond!"


@app.route('/error')
def expliciterror():
    bottle.response.status = 400
    return 'Object already exists with that name'


@app.route('/exception')
def exceptionalerror():
    1 / 0


@app.post('/name')
def name():
    return "Your name is %s" % bottle.request.body.read()


def test_bottle_sniffer_is_an_http_sniffer():
    assert isinstance(BottleSniffer(), HTTPSniffer)


class TestSucessfulTransactions():
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
        test_app.post('/name', 'Michael')
        request = sniffer.transactions[0].request
        assert request.body == "Michael"


class TestErrorTransactions():
    def test_sniffer_does_not_interfere(self):
        test_app = webtest.TestApp(app)
        app.install(BottleSniffer())
        with raises(webtest.app.AppError) as excinfo:
            test_app.get('/error')
        assert '400 Bad Request' in str(excinfo.value)
        assert 'Object already exists with that name' in str(excinfo.value)

    def test_a_transaction_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with raises(webtest.app.AppError):
            test_app.get('/error')
        assert len(sniffer.transactions) == 1
        assert isinstance(sniffer.transactions[0], Transaction)


class TestErrorTransactionsDueToExceptions():
    def test_does_not_interfere(self):
        test_app = webtest.TestApp(app)
        app.install(BottleSniffer())
        with raises(webtest.app.AppError) as excinfo:
            test_app.get('/exception')
        assert '500 Internal Server Error' in str(excinfo.value)

    def test_a_transaction_is_captured(self):
        test_app = webtest.TestApp(app)
        sniffer = BottleSniffer()
        app.install(sniffer)
        with raises(webtest.app.AppError):
            test_app.get('/exception')
        assert len(sniffer.transactions) == 1
        assert isinstance(sniffer.transactions[0], Transaction)
