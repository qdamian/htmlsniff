from htmlvis import seqdiag
from htmlvis import plantuml
import pytest


@pytest.fixture
def sample_request():
    return seqdiag.Message(
        category=seqdiag.Category.request,
        src='Client',
        dst='Server',
        text='hi there',
        when=0.0,
        data='')


@pytest.fixture
def sample_response():
    return seqdiag.Message(
        category=seqdiag.Category.response,
        src='Server',
        dst='Client',
        text='hello',
        when=0.0,
        data='')


class TestSeqDiag(object):
    def test_source_is_mandatory(self, sample_request):
        with pytest.raises(ValueError):
            malformed_request = seqdiag.Message(
                category=seqdiag.Category.request,
                src='',
                dst='Server',
                text='hi there',
                when=0.0,
                data='')
            diag = plantuml.seqdiag([malformed_request])

    def test_sources_are_quoted(self, sample_request):
        diag = plantuml.seqdiag([sample_request])
        assert '"Client"' in diag

    def test_destinations_are_quoted(self, sample_request):
        diag = plantuml.seqdiag([sample_request])
        assert '"Server"' in diag

    def test_double_quotes_in_source_name_are_converted_to_single_quotes(self, sample_request):
        sample_request.src = 'This " contains quotes"'
        diag = plantuml.seqdiag([sample_request])
        assert r"This ' contains quotes'" in diag

    def test_a_request_is_drawn_with_solid_line(self, sample_request):
        diag = plantuml.seqdiag([sample_request])
        assert '"Client" -> "Server"' in diag

    def test_handles_two_messages(self, sample_request, sample_response):
        diag = plantuml.seqdiag([sample_request, sample_response])
        assert 'hi there' in diag
        assert 'hello' in diag
