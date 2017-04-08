import bottle
import webtest
from htmlvis import BottleSniffer, HTTPSniffer
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


def test_sniffer_does_not_interfere_with_a_successful_request():
    test_app = webtest.TestApp(app)
    app.install(BottleSniffer())
    assert test_app.get('/success').status == '200 OK'


def test_sniffer_does_not_interfere_with_an_explicit_error_response():
    test_app = webtest.TestApp(app)
    app.install(BottleSniffer())
    with raises(webtest.app.AppError) as excinfo:
        test_app.get('/error')
    assert '400 Bad Request' in str(excinfo.value)
    assert 'Object already exists with that name' in str(excinfo.value)


def test_does_not_interfere_with_an_error_due_to_an_exception():
    test_app = webtest.TestApp(app)
    app.install(BottleSniffer())
    with raises(webtest.app.AppError) as excinfo:
        test_app.get('/exception')
    assert '500 Internal Server Error' in str(excinfo.value)
