#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64 as b64
import urllib.parse
from itertools import cycle


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
        elif method == 'ROT13':
            text = rot13(text, int(key))
        elif method == 'Vigenere':
            text = vigenere_encode(text, key)
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
        elif method == 'ROT13':
            text = rot13(text, int(key) * -1)
        elif method == 'Vigenere':
            text = vigenere_decode(text, key)
    except Exception as ex:
        error = {'title': ex.__class__.__name__ , 'text': str(ex)}
    return error, text


def rot13(text, shift=13):
    new_text = ''
    for char in text:
        char_num = ord(char)
        if 97 <= char_num <= 122:
            new_text += chr(97 + (char_num - 97 + shift) % 26)
        elif 65 <= char_num <= 90:
            new_text += chr(65 + (char_num - 65 + shift) % 26)
        elif 1040 <= char_num <= 1071:
            new_text += chr(1040 + (char_num - 1040 + shift) % 32)
        elif 1072 <= char_num <= 1103:
            new_text += chr(1072 + (char_num - 1072 + shift) % 32)
        else:
            new_text += char
    return new_text


def vigenere_encode(text, key):
    return text


def vigenere_decode(text, key):
    return text
