# jsonxx

An extendable JSON parser for Python.

## Usage

Just like the `json` module in python:

``` py
from jsonxx import loads

loads(...)
```

or extend with regex:

``` py
from jsonxx import loads
from jsonxx.plugins import RegexPlugin

obj = loads('/^axX$/i', plugins=(RegexPlugin(), ) + STANDARD_PLUGINS)
assert isinstance(obj, re.Pattern)
```
