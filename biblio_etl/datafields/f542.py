"""MARC datafield 542 $m -> ``iisgv:accessLevel``.

In standard MARC, 542 $m is "publication status"; IISG uses it locally for
how large the public may view the item's scans, e.g. ``pictoright`` (at
most 450 px) or ``restricted`` (at most 1500 px). IISG's image server
enforces the same levels. The values become IRIs under
``https://iisg.amsterdam/vocab/accessLevel/``, the same ones iisg-iiif
writes on the scans themselves, so the two can be queried together.
"""

from __future__ import annotations

import re

from rdflib import Graph, URIRef

from ..context import as_array, get_code, get_text
from ..prefixes import ACCESS_LEVEL, IISGV

_NON_SLUG = re.compile(r"[^a-z0-9]+")


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        if get_code(sub) != "m":
            continue
        level = _NON_SLUG.sub("-", (get_text(sub) or "").strip().lower()).strip("-")
        if level:
            g.add((item, IISGV.accessLevel, ACCESS_LEVEL[level]))
