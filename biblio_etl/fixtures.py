"""Loading ``static/biblio/sourceData/*.json`` fixtures.

One of the 20 fixtures shipped in the original zip
(``collections1135739.json``) is missing its enclosing ``{ }`` braces (and
carries two extra debug keys, ``$recordId``/``$environment``, not present in
the others) -- a pre-existing data issue in the source archive, not
introduced by this port. Rather than silently "fixing" the copied fixture
file, this loader tolerates that shape defensively.
"""

from __future__ import annotations

import json
from pathlib import Path


def load_fixture(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Missing only the opening brace (the file already ends with `}`).
        return json.loads("{" + text)
