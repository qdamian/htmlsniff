from enum import Enum

from attr import Factory, attrib, attrs

Category = Enum('Category', 'request response')


def assert_not_empty(message, attribute, value):
    if not value:
        raise ValueError(
            '{attribute} cannot be empty'.format(attribute=attribute.name))


@attrs
class Message(object):
    category = attrib()
    src = attrib(validator=assert_not_empty)
    dst = attrib()
    text = attrib()
    when = attrib()
    data = attrib(default=Factory(dict))
