from htmlvis import HTTPSniffer
from pytest import fixture, mark, raises


class TestHTTPSniffer:
    def test_requires_a_transactions_property_to_be_available(self):
        with raises(NotImplementedError):
            HTTPSniffer().transactions

    def test_exposes_a_restart_method(self):
        with raises(NotImplementedError):
            HTTPSniffer().restart()
