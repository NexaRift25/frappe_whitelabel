"""Compatibility import for leftover `whitelabel` references.

Some benches, installed-app rows, or scripts still `import whitelabel`.
This app's package name is `frappe_whitelabel`.
"""

from __future__ import annotations

import sys
from importlib import import_module

_app = import_module("frappe_whitelabel")
sys.modules[__name__] = _app
