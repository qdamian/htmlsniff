from . import plantuml


def draw(messages):
    return plantuml.html_image(messages)
