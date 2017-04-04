"""
Collection of callables that (possibly) transform the messages
"""
import json
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
