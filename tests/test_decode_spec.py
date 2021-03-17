# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from jsonxx import loads

def test_null():
    assert loads('null') == None

def test_false():
    assert loads('false') == False

def test_true():
    assert loads('true') == True

def test_int():
    assert loads('123') == 123

def test_str():
    assert loads('"123"') == "123"

def test_array():
    assert loads('["123", 123, false]') == ["123", 123, False]

def test_object():
    assert loads('{"123": 123}') == {"123": 123}
