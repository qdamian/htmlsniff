# -*- coding: utf-8 -*-

__author__ = """Damian Quiroga"""
__email__ = 'qdamian@gmail.com'
__version__ = '0.1.0'

import sys

# flake8: noqa: F401 imported but unused
from .htmlvis import save_seq_diag

if hasattr(sys, '_called_from_test'):
    from .htmlvis import Transaction, Request, Response
    from .htmlvis import seqdiag
