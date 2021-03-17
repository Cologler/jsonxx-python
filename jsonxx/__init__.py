# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import json as _std_json
import functools

from .decoder import JSONxxDecoder

load = functools.partial(_std_json.load, cls=JSONxxDecoder)
loads = functools.partial(_std_json.loads, cls=JSONxxDecoder)

__all__ = (
    'JSONxxDecoder'
)
