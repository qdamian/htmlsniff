import json
import pytest
from htmlvis import plantuml, plantuml_text_encoding, seqdiag_model


@pytest.fixture
def sample_request():
    return seqdiag_model.Message(
        category=seqdiag_model.Category.request,
        src='Client A',
        dst='Server A',
        text='hi there',
        when=0.0,
        note='multi\nline',
        data='')


@pytest.fixture
def sample_response():
    return seqdiag_model.Message(
        category=seqdiag_model.Category.response,
        src='Server A',
        dst='Client A',
        text='hello',
        when=0.0,
        note='multi\nline',
        data='')


@pytest.fixture(autouse=True)
def mock_plantuml(mocker):
    mocker.patch('htmlvis.plantuml_text_encoding.encode')


class TestTextualRepresentation(object):
    def test_source_is_mandatory(self, sample_request):
        with pytest.raises(ValueError):
            malformed_request = seqdiag_model.Message(
                category=seqdiag_model.Category.request,
                src='',
                dst='Server A',
                text='hi there',
                note='',
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

    def test_request_notes_are_drawn_at_the_right_of_the_destination(
            self, sample_request):
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert 'note right\n    multi\n    line\nend note' in text_repr

    def test_no_note_is_added_if_request_has_no_notes(self, sample_request):
        sample_request.note = None
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert 'note' not in text_repr

    def test_empty_notes_are_not_added(self, sample_request):
        sample_request.note = ''
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert 'note' not in text_repr

    def test_handles_two_messages(self, sample_request, sample_response):
        plantuml.html_image([sample_request, sample_response])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert 'hi there' in text_repr
        assert 'hello' in text_repr

    def test_request_syntax(self, sample_request):
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert '"Client A" -> "Server A": hi there\n' in text_repr

    def test_returns_an_img_element(self, sample_request):
        plantuml_text_encoding.encode.return_value = 'lalala'
        img_element = plantuml.html_image([sample_request])
        assert img_element == '<img src="http://www.plantuml.com/plantuml/svg/lalala">'


class TestFormatting(object):
    def test_a_request_is_drawn_with_solid_line(self, sample_request):
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert '"Client A" -> "Server A"' in text_repr

    def test_a_response_is_drawn_with_a_dotted_line(self, sample_response):
        plantuml.html_image([sample_response])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert '"Client A" <-- "Server A"' in text_repr

    def test_response_notes_are_drawn_at_the_left_of_the_destination(
            self, sample_response):
        plantuml.html_image([sample_response])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        assert 'note left\n    multi\n    line\nend note' in text_repr

    def test_json_notes_are_pretty_formatted(self, sample_request):
        sample_request.note = '{"name": "John", "age": 33}'
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        # json dumps adds a trailing space in Python 2. https://bugs.python.org/issue16333
        text_repr = text_repr.replace(' \n', '\n')
        assert '    {\n        "name": "John",\n        "age": 33\n    }' in text_repr

    @pytest.mark.parametrize('json_note, formatted_note', [
        ('{"a": 2, "b": 1}', '    {\n        "a": 2,\n        "b": 1\n    }'),
        ('{"b": 1, "a": 2}', '    {\n        "b": 1,\n        "a": 2\n    }')
    ])
    def test_json_formatting_preserves_items_order(self, sample_request,
                                                   json_note, formatted_note):
        sample_request.note = json_note
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        # json dumps adds a trailing space in Python 2. https://bugs.python.org/issue16333
        text_repr = text_repr.replace(' \n', '\n')
        assert formatted_note in text_repr

    @pytest.mark.parametrize(
        'json_note, formatted_note',
        [('{"This is a very long string": 2}',
          '    {\n        "This is a very ...": 2\n    }'),
         ('{"b": "This is a very long string"}',
          '    {\n        "b": "This is a very ..."\n    }')])
    def test_long_strings_are_truncated(self, sample_request, json_note,
                                        formatted_note):
        sample_request.note = json_note
        plantuml.html_image([sample_request])
        text_repr = plantuml_text_encoding.encode.call_args[0][0]
        # json dumps adds a trailing space in Python 2. https://bugs.python.org/issue16333
        text_repr = text_repr.replace(' \n', '\n')
        assert formatted_note in text_repr
