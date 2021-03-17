# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import re
from json import JSONDecoder

class StringPlugin:
    def make_scanner(self, context: JSONDecoder):
        parse_string = context.parse_string
        strict = context.strict

        def match(s, idx, nextchar):
            return nextchar == '"'

        def parse(m, s, idx, scan_once):
            return parse_string(s, idx + 1, strict)

        return match, parse


class ObjectPlugin:
    def make_scanner(self, context: JSONDecoder):
        parse_object = context.parse_object
        strict = context.strict
        object_hook = context.object_hook
        object_pairs_hook = context.object_pairs_hook
        memo = context.memo

        def match(s, idx, nextchar):
            return nextchar == '{'

        def parse(m, s, idx, scan_once):
            return parse_object((s, idx + 1), strict,
                scan_once, object_hook, object_pairs_hook, memo)

        return match, parse


class ArrayPlugin:
    def make_scanner(self, context: JSONDecoder):
        parse_array = context.parse_array

        def match(s, idx, nextchar):
            return nextchar == '['

        def parse(m, s, idx, scan_once):
            return parse_array((s, idx + 1), scan_once)

        return match, parse


class NullPlugin:
    def make_scanner(self, context: JSONDecoder):

        def match(s, idx, nextchar):
            return nextchar == 'n' and s[idx:idx + 4] == 'null'

        def parse(m, s, idx, scan_once):
            return None, idx + 4

        return match, parse


class TruePlugin:
    def make_scanner(self, context: JSONDecoder):

        def match(s, idx, nextchar):
            return nextchar == 't' and s[idx:idx + 4] == 'true'

        def parse(m, s, idx, scan_once):
            return True, idx + 4

        return match, parse


class FalsePlugin:
    def make_scanner(self, context: JSONDecoder):

        def match(s, idx, nextchar):
            return nextchar == 'f' and s[idx:idx + 5] == 'false'

        def parse(m, s, idx, scan_once):
            return False, idx + 5

        return match, parse


class NumberPlugin:
    # copy from cpython\Lib\json\scanner.py
    _NUMBER_RE = re.compile(
        r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
        (re.VERBOSE | re.MULTILINE | re.DOTALL))

    def make_scanner(self, context: JSONDecoder):
        match_number = self._NUMBER_RE.match
        parse_float = context.parse_float
        parse_int = context.parse_int

        def match(s, idx, nextchar):
            return match_number(s, idx)

        def parse(m, s, idx, scan_once):
            integer, frac, exp = m.groups()
            if frac or exp:
                res = parse_float(integer + (frac or '') + (exp or ''))
            else:
                res = parse_int(integer)
            return res, m.end()

        return match, parse


SPEC_PLUGINS = (
    StringPlugin(),
    ObjectPlugin(),
    ArrayPlugin(),
    NullPlugin(),
    TruePlugin(),
    FalsePlugin(),
    NumberPlugin(),
)


class NaNPlugin:
    def make_scanner(self, context: JSONDecoder):
        parse_constant = context.parse_constant

        def match(s, idx, nextchar):
            return nextchar == 'N' and s[idx:idx + 3] == 'NaN'

        def parse(m, s, idx, scan_once):
            return parse_constant('NaN'), idx + 3

        return match, parse


class InfinityPlugin:
    def make_scanner(self, context: JSONDecoder):
        parse_constant = context.parse_constant

        def match(s, idx, nextchar):
            return nextchar == 'I' and s[idx:idx + 8] == 'Infinity'

        def parse(m, s, idx, scan_once):
            return parse_constant('Infinity'), idx + 8

        return match, parse


class NegInfinityPlugin:
    def make_scanner(self, context: JSONDecoder):
        parse_constant = context.parse_constant

        def match(s, idx, nextchar):
            return nextchar == '-' and s[idx:idx + 9] == '-Infinity'

        def parse(m, s, idx, scan_once):
            return parse_constant('-Infinity'), idx + 9

        return match, parse


STANDARD_PLUGINS = SPEC_PLUGINS + (
    NaNPlugin(),
    InfinityPlugin(),
    NegInfinityPlugin(),
)
