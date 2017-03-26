from . import plantuml_text_encoding
from .seqdiag_model import Category
import logging

logger = logging.getLogger(__name__)

MSG_TO_TEXTUAL_REPR = {
    Category.request: '"{source}" -> "{destination}": {text}\n',
    Category.response: '"{destination}" <-- "{source}": {text}\n',
}


def html_image(messages):
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
    return textual_repr


def _sanitize(participant):
    return participant.replace('"', "'")
