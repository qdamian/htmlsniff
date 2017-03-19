import pytest
from htmlvis import plantuml, seqdiag, plantuml_text_encoding


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


@pytest.fixture(autouse=True)
def mock_plantuml(mocker):
    mocker.patch('htmlvis.plantuml_text_encoding.encode')


class TestTextualRepresentation(object):
    def test_source_is_mandatory(self, sample_request):
        with pytest.raises(ValueError):
            malformed_request = seqdiag.Message(
                category=seqdiag.Category.request,
                src='',
                dst='Server',
                text='hi there',
                when=0.0,
                data='')
            plantuml.image([malformed_request])

    def test_sources_are_quoted(self, sample_request):
        plantuml.image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert '"Client"' in text_repr

    def test_destinations_are_quoted(self, sample_request):
        plantuml.image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert '"Server"' in text_repr

    def test_double_quotes_in_source_name_are_converted_to_single_quotes(
            self, sample_request):
        sample_request.src = 'This " contains quotes"'
        plantuml.image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert r"This ' contains quotes'" in text_repr

    def test_a_request_is_drawn_with_solid_line(self, sample_request):
        plantuml.image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert '"Client" -> "Server"' in text_repr

    def test_handles_two_messages(self, sample_request, sample_response):
        plantuml.image([sample_request, sample_response])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert 'hi there' in text_repr
        assert 'hello' in text_repr
