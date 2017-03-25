from . import plantuml_text_encoding
import logging

logger = logging.getLogger(__name__)


def html_image(messages):
    logger.debug('Generating sequence diagram')
    textual_repr = _generate_textual_representation(messages)
    encoded_repr = plantuml_text_encoding.encode(textual_repr)
    html = '<img src="http://www.plantuml.com/plantuml/svg/%s">' % encoded_repr
    return html


def _generate_textual_representation(messages):
    textual_repr = ''
    for msg in messages:
        textual_repr += '"{source}" -> "{destination}"{text}\n'.format(
            source=_sanitize(msg.src),
            destination=_sanitize(msg.dst),
            text=msg.text)
    return textual_repr


def _sanitize(participant):
    return participant.replace('"', "'")
