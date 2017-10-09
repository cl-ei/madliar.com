"""
Provides some encoding or decoding tools.

"""


def encode_ascii(s):
    """
    Converts any character into a ASCII sequence.

    For example:
    >>> print encode_ascii("abcdef")
    \0x61\0x62\0x63\0x64\0x65\0x66

    """
    return "".join(["\\0x%0x" % ord(c) for c in s])
