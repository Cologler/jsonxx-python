# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import re
from json import JSONDecoder, JSONDecodeError

def _parse_regex(s: str, end: int, strict=True, *, memo: dict=None):
    """
    Scan the string s for a regex. End is the index of the
    character in s after the `/` that started the JSON string.

    Returns a tuple of the regex and the index of the character in s
    after the end quote.
    """
    s_len = len(s)
    begin = end - 1
    index = end

    if memo is None:
        memo = {}

    # read pattern
    try:
        while index < s_len:
            if s[index] == '\\': # enscape
                index += 1
            if s[index] == '/': # end
                break
            index += 1
    except IndexError:
        raise JSONDecodeError("Unterminated regex starting at", s, begin) from None
    pattern = s[end:index]
    index += 1

    # read flags
    flags = 0
    while index < s_len:
        char = s[index]
        if char == 'i':
            flags |= re.I
        elif char == 'm':
            flags |= re.M
        elif char == 'x':
            flags |= re.X
        elif char == 's':
            flags |= re.S
        else:
            break
        index += 1

    key = (re.Pattern, pattern, flags)
    try:
        regex = memo[key]
    except KeyError:
        try:
            regex = re.compile(pattern, flags)
        except re.error:
            regex = None
        memo[key] = regex

    if regex is None:
        raise JSONDecodeError("Invalid regex pattern starting at", s, begin)

    return (regex, index)

class RegexPlugin:
    def make_scanner(self, context: JSONDecoder):
        strict = context.strict
        memo = context.memo

        def match(s, idx, nextchar):
            return nextchar == '/'

        def parse(m, s, idx, scan_once):
            return _parse_regex(s, idx + 1, strict, memo=memo)

        return match, parse

