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


def is_key(algorithm):
    """Key type function

    Args:
        algorithm: Text string defines algorithm.

    Returns:
        Constant - KEY_DECIMAL if algorithm required integer as key,
                   KEY_TEXT if algorithm required string as key,
                   KEY_NOKEY otherwise.

    """
    if algorithm == 'ROT13':
        return KEY_DECIMAL
    elif algorithm == 'Vigenere':
        return KEY_TEXT
    else:
        return KEY_NOKEY


def encode(text, algorithm, key=None):
    """Encode text function

    Args:
        text: Text string for encryption.
        algorithm: Text string defines algorithm.
        key: Text string or integer - encryption key.

    Returns:
        Error - None if encryption is ok,
                else dictionary with error title and error text.
        Text string - encrypted text.

    """
    error = None
    try:
        if algorithm == 'Base64':
            text = b64.b64encode(text.encode('utf-8')).decode('utf-8')
        elif algorithm == 'URL':
            text = urllib.parse.quote(text)
        elif algorithm == 'ROT13':
            text = rot13(text, int(key))
        elif algorithm == 'Vigenere':
            text = vigenere_encode(text, key)
        elif algorithm == 'A1Z26':
            text = a1z26_encode(text)
    except Exception as ex:
        error = {'title': ex.__class__.__name__, 'text': str(ex)}
    return error, text


def decode(text, algorithm, key=None):
    """Decode text function

    Args:
        text: Encrypted text string for decryption.
        algorithm: Text string defines algorithm.
        key: Text string or integer - decryption key.

    Returns:
        Error - None if decryption is ok,
                else dictionary with error title and error text.
        Text string - decrypted text.

    """
    error = None
    try:
        if algorithm == 'Base64':
            text = b64.b64decode(text.encode('utf-8')).decode('utf-8')
        elif algorithm == 'URL':
            text = urllib.parse.unquote(text)
        elif algorithm == 'ROT13':
            text = rot13(text, int(key) * -1)
        elif algorithm == 'Vigenere':
            text = vigenere_decode(text, key)
        elif algorithm == 'A1Z26':
            text = a1z26_decode(text)
    except Exception as ex:
        error = {'title': ex.__class__.__name__, 'text': str(ex)}
    return error, text


lat_range_1 = 65, 91, 26
lat_range_2 = 97, 123, 26
cyr_range_1 = 1040, 1072, 32
cyr_range_2 = 1072, 1104, 32


def rot13(text, shift=13):
    """Simple letter substitution cipher that replaces a letter
    with the 13th letter after it in the alphabet or use selected shift.

    Args:
        text: Text string for conversion.
        shift: Integer - custom alphabet shift.

    Returns:
        Text string - converted text.

    """
    new_text = ''
    for char in text:
        char_num = ord(char)
        start, len_ = 0, 1
        if char_num in range(*lat_range_1[:2]):
            start, len_ = lat_range_1[0], lat_range_1[2]
        elif char_num in range(*lat_range_2[:2]):
            start, len_ = lat_range_2[0], lat_range_2[2]
        elif char_num in range(*cyr_range_1[:2]):
            start, len_ = cyr_range_1[0], cyr_range_1[2]
        elif char_num in range(*cyr_range_2[:2]):
            start, len_ = cyr_range_2[0], cyr_range_2[2]
        else:
            start = char_num

        new_text += chr(start + (char_num - start + shift) % len_)
    return new_text


def vigenere_make_key(key, rev=False):
    """Generate key iterator for Vigenere algorithm.

    Args:
        key: Text string.
        rev: Boolean - reverse shifts direction for decoding.

    Returns:
        cycle() iterator - shifts defined by key.

    """
    key_ = []
    for char in key:
        char_num = ord(char)
        if char_num in range(*lat_range_1[:2]):
            char_num -= lat_range_1[0] - 1
        elif char_num in range(*lat_range_2[:2]):
            char_num -= lat_range_2[0] - 1
        elif char_num in range(*cyr_range_1[:2]):
            char_num -= cyr_range_1[0] - 1
        elif char_num in range(*cyr_range_2[:2]):
            char_num -= cyr_range_2[0] - 1
        else:
            char_num = 0

        if char_num:
            key_.append(char_num)

    if rev:
        key_ = map(lambda x: x * -1, key_)

    return cycle(key_)


def vigenere_transform(text, key):
    """Simple method of encrypting alphabetic text by using a series of
    interwoven Caesar ciphers, based on the letters of a keyword

    Args:
        text: Text string for conversion.
        key: cycle() iterator from vigenere_make_key() function.

    Returns:
        Text string - converted text.

    """
    new_text = ''
    for char in text:
        char_num = ord(char)
        start, len_ = 0, 1
        if char_num in range(*lat_range_1[:2]):
            start, len_ = lat_range_1[0], lat_range_1[2]
        elif char_num in range(*lat_range_2[:2]):
            start, len_ = lat_range_2[0], lat_range_2[2]
        elif char_num in range(*cyr_range_1[:2]):
            start, len_ = cyr_range_1[0], cyr_range_1[2]
        elif char_num in range(*cyr_range_2[:2]):
            start, len_ = cyr_range_2[0], cyr_range_2[2]

        if start:
            new_text += chr(start + (char_num - start + next(key)) % len_)
        else:
            new_text += char

    return new_text


def vigenere_encode(text, key):
    """Convert text by Vigenere algorithm with forward direction key

    Args:
        text: Text string for conversion.
        key: Text string defines key.

    Returns:
        Text string - converted text.

    """
    key = vigenere_make_key(key, rev=False)
    return vigenere_transform(text, key)


def vigenere_decode(text, key):
    """Convert text by Vigenere algorithm with backward direction key

    Args:
        text: Text string for conversion.
        key: Text string defines key.

    Returns:
        Text string - converted text.

    """
    key = vigenere_make_key(key, rev=True)
    return vigenere_transform(text, key)


def a1z26_encode(text):
    """Simple alphabetic text encoding by replacing
    each char with char number"""
    text = '-'.join(map(str, map(ord, text)))
    return text


def a1z26_decode(text):
    """Simple alphabetic text decoding by replacing
    each char number in source text by char itself"""
    text = ''.join(map(chr, map(int, text.split('-'))))
    return text


def main():
    """minimal funcs testing"""
    assert rot13('Some text here') == 'Fbzr grkg urer'
    assert rot13('Some text here', 0) == 'Some text here'
    assert rot13(rot13('Some text here', 5), -5) == 'Some text here'
    assert rot13('Некий текст тут') == 'Ътчхц ятчюя яая'
    assert rot13('Некий текст тут', 0) == 'Некий текст тут'
    assert rot13(rot13('Некий текст тут', 5), -5) == 'Некий текст тут'

    assert vigenere_encode('Some text here', 'key') == 'Dtlp ydiy gpwd'
    encoded = vigenere_encode('Some text here', 'key')
    assert vigenere_decode(encoded, 'key') == 'Some text here'
    assert vigenere_encode('Некий текст тут', 'ключ') == 'Шсйаф юдвью слэ'
    encoded = vigenere_encode('Некий текст тут', 'ключ')
    assert vigenere_decode(encoded, 'ключ') == 'Некий текст тут'


if __name__ == '__main__':
    main()
