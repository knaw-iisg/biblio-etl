"""MARC datafield 651, second pass -- both handlers are registered for
``@tag == '651'`` and this one is identical to ``f651.py``, so it just
reuses that implementation."""

from __future__ import annotations

from . import f651

process = f651.process
