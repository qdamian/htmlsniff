"""
Generate http://plantuml.com/sequence-diagram
"""
import logging

from . import formatting, plantuml_text_encoding
from .seqdiag_model import Category

logger = logging.getLogger(__name__)

MSG_TO_TEXTUAL_REPR = {
    Category.request: '"{source}" -> "{destination}": {text}\n',
    Category.response: '"{destination}" <-- "{source}": {text}\n',
}
NOTE_LOCATION = {
    Category.request: 'right',
    Category.response: 'left',
}


def html_image(messages):
    """
    Generate an HTML img element with an SVG sequence diagram
    """
    logger.debug('Generating sequence diagram')
    textual_repr = _generate_textual_representation(messages)
    encoded_repr = plantuml_text_encoding.encode(textual_repr)
    html = '<img src="http://www.plantuml.com/plantuml/svg/%s">' % encoded_repr
    return html


def _generate_textual_representation(messages):
    textual_repr = ''
    for msg in messages:
        textual_repr += MSG_TO_TEXTUAL_REPR[msg.category].format(
            source=_sanitize(msg.src),
            destination=_sanitize(msg.dst),
            text=msg.text)
        formatters = [
            formatting.prettify_json, formatting.shorten_long_strings
        ]
        for fmt in formatters:
            fmt(msg)
        if msg.note:
            textual_repr += 'note ' + NOTE_LOCATION[
                msg.category] + '\n' + _indent(msg.note) + '\nend note'
    return textual_repr


def _sanitize(participant):
    return participant.replace('"', "'")


def _indent(text):
    return '    ' + '\n    '.join(text.splitlines())
