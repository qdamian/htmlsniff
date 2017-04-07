"""
Collection of callables that (possibly) transform the messages
"""
import json
import re
from collections import OrderedDict

try:
    from contextlib import suppress
except ImportError:
    from contextlib2 import suppress


def prettify_json(msg):
    if not msg.note:
        return
    with suppress(ValueError):
        msg.note = json.dumps(
            json.loads(msg.note, object_pairs_hook=OrderedDict),
            indent=4,
            sort_keys=False)


def shorten_long_strings(msg):
    if not msg.note:
        return
    MAX_LEN = 15
    ANY_CHAR_BUT_QUOTE_OR_NEWLINE = '[^"\n]'
    MAX_LENGTH_STRING = '%s{%s}' % (ANY_CHAR_BUT_QUOTE_OR_NEWLINE, MAX_LEN)
    ANY_CHAR_NON_GREEDY = '.*?'
    REGEX = '"(' + MAX_LENGTH_STRING + ')' + ANY_CHAR_NON_GREEDY + '"'
    msg.note = re.sub(REGEX, r'"\1..."', msg.note)
