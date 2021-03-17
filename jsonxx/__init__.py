# -*- coding: utf-8 -*-
#
# Copyright (c) 2021~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import json as std_json
from json import JSONDecodeError
import functools

from .decoder import JSONxxDecoder

load = functools.partial(std_json.load, cls=JSONxxDecoder)
loads = functools.partial(std_json.loads, cls=JSONxxDecoder)

__all__ = (
    'JSONxxDecoder', 'JSONDecodeError',
    'load', 'loads',
)
