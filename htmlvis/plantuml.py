from . import plantuml_text_encoding


def html_image(messages):
    print('plantuml seqdiag called')
    if not messages[0].src:
        raise ValueError('Message with no source specified: %s' % messages)
    diag = ''
    for msg in messages:
        source = msg.src
        sanitized_source = source.replace('"', "'")
        diag += '"{source}" -> "Server"{text}\n'.format(
            source=sanitized_source, text=msg.text)
    encoded_repr = plantuml_text_encoding.encode(diag)
    return '<img src="http://www.plantuml.com/plantuml/svg/%s">' % encoded_repr
