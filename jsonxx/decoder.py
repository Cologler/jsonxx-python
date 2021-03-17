# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import json
import re

from .plugins.standard import STANDARD_PLUGINS

def _make_scanner(context):
    plugin_scanners = [plugin.make_scanner(context) for plugin in context.plugins]
    memo = context.memo

    def _scan_once(string, idx):
        try:
            nextchar = string[idx]
        except IndexError:
            raise StopIteration(idx) from None

        for match, parse in plugin_scanners:
            state = match(string, idx, nextchar)
            if state:
                return parse(state, string, idx, _scan_once)

        raise StopIteration(idx)

    def scan_once(string, idx):
        try:
            return _scan_once(string, idx)
        finally:
            memo.clear()

    return scan_once

class JSONxxDecoder(json.JSONDecoder):
    '''
    a json+ decoder, which support regex
    '''
    def __init__(self, *args, plugins=STANDARD_PLUGINS, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugins = plugins
        self.scan_once = _make_scanner(self)
