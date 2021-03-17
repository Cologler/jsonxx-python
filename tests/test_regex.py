# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import re

from jsonxx import JSONDecodeError, loads
from jsonxx.plugins import *

from pytest import raises

BASE_FLAGS = re.compile('').flags
PLUGINS = [
    RegexPlugin(),
    *STANDARD_PLUGINS
]

def test_basic():
    # basic
    obj = loads('/^axX$/i', plugins=PLUGINS)
    assert isinstance(obj, re.Pattern)
    assert obj.pattern == '^axX$'
    assert obj.flags == BASE_FLAGS | re.I

    # more flags: https://docs.mongodb.com/manual/reference/operator/query/regex/
    obj = loads('/^axX$/imxs', plugins=PLUGINS)
    assert isinstance(obj, re.Pattern)
    assert obj.pattern == '^axX$'
    assert obj.flags == BASE_FLAGS | re.I | re.M | re.X | re.S

    # embedded object:
    obj = loads('{ "r": /^axX$/i, "i": 15 }', plugins=PLUGINS)
    assert obj['i'] == 15
    exp = obj['r']
    assert isinstance(exp, re.Pattern)
    assert exp.pattern == '^axX$'
    assert exp.flags == BASE_FLAGS | re.I

def test_bad_flags():
    with raises(JSONDecodeError) as ctx:
        loads('/^axX$/g', plugins=PLUGINS)
    assert str(ctx.value) == 'Invalid regex flag at: line 1 column 8 (char 7)'
    with raises(JSONDecodeError) as ctx:
        loads('/^axX$/ig', plugins=PLUGINS)
    assert str(ctx.value) == 'Invalid regex flag at: line 1 column 9 (char 8)'

def test_doc_example():
    obj = loads('/^axX$/i', plugins=(RegexPlugin(), ) + STANDARD_PLUGINS)
    assert isinstance(obj, re.Pattern)
