import re

import pytest
from htmlvis import plantuml, plantuml_text_encoding, seqdiag


@pytest.fixture
def sample_request():
    return seqdiag.Message(
        category=seqdiag.Category.request,
        src='Client A',
        dst='Server A',
        text='hi there',
        when=0.0,
        data='')


@pytest.fixture
def sample_response():
    return seqdiag.Message(
        category=seqdiag.Category.response,
        src='Server A',
        dst='Client A',
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
                dst='Server A',
                text='hi there',
                when=0.0,
                data='')
            plantuml.html_image([malformed_request])

    def test_sources_are_quoted(self, sample_request):
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert '"Client A"' in text_repr

    def test_destinations_are_quoted(self, sample_request):
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert '"Server A"' in text_repr

    def test_double_quotes_in_source_name_are_converted_to_single_quotes(
            self, sample_request):
        sample_request.src = 'This " contains quotes"'
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert r"This ' contains quotes'" in text_repr

    def test_double_quotes_in_destination_name_are_converted_to_single_quotes(
            self, sample_request):
        sample_request.dst = 'This " contains quotes"'
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert r"This ' contains quotes'" in text_repr

    def test_a_request_is_drawn_with_solid_line(self, sample_request):
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert '"Client A" -> "Server A"' in text_repr

    def test_handles_two_messages(self, sample_request, sample_response):
        plantuml.html_image([sample_request, sample_response])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert 'hi there' in text_repr
        assert 'hello' in text_repr

    def test_returns_an_img_element(self, sample_request):
        img_element = plantuml.html_image([sample_request])
        assert re.match('<img.*>', img_element)

    def test_returns_an_img_element(self, sample_request):
        plantuml_text_encoding.encode.return_value = 'lalala'
        img_element = plantuml.html_image([sample_request])
        assert img_element == '<img src="http://www.plantuml.com/plantuml/svg/lalala">'
