from enum import Enum

from attr import Factory, attrib, attrs

from . import plantuml

Category = Enum('Category', 'request response')


@attrs
class Message(object):
    category = attrib()
    src = attrib()
    dst = attrib()
    text = attrib()
    when = attrib()
    data = attrib(default=Factory(dict))


def draw(messages):
    print('draw called')
    return plantuml.html_image(messages)
