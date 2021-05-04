#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64 as b64
import urllib.parse


CODERS = ('ROT13', 'Vigenere', 'A1Z26', 'Base64', 'URL')
DECODERS = ('ROT13', 'Vigenere', 'A1Z26', 'Base64', 'URL')
KEY_NOKEY = 0
KEY_DECIMAL = 1
KEY_TEXT = 2


def is_key(method):
    if method == 'ROT13':
        return KEY_DECIMAL
    elif method == 'Vigenere':
        return KEY_TEXT
    else:
        return KEY_NOKEY


def encode(text, method, key=None):
    error = None
    try:
        if method == 'Base64':
            text = b64.b64encode(text.encode('utf-8')).decode('utf-8')
        elif method == 'URL':
            text = urllib.parse.quote(text)
    except Exception as ex:
        error = {'title': ex.__class__.__name__ , 'text': str(ex)}
    return error, text


def decode(text, method, key=None):
    error = None
    try:
        if method == 'Base64':
            text = b64.b64decode(text.encode('utf-8')).decode('utf-8')
        elif method == 'URL':
            text = urllib.parse.unquote(text)
    except Exception as ex:
        error = {'title': ex.__class__.__name__ , 'text': str(ex)}
    return error, text
