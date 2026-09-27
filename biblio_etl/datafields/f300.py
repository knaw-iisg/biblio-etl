"""MARC datafield 300 (physical description) -> ``iisgv:physicalDescription``
/ ``numberOfPages`` / ``size``."""

from __future__ import annotations

import re

from rdflib import XSD, Graph, Literal, URIRef

from ..context import as_array, get_code, get_text, try_literal
from ..prefixes import IISGV

_PAGE_COUNT_RE = re.compile(r"^.*(\b\d+\b) [pP]\.")


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        code = get_code(sub)
        text = get_text(sub)
        if not text:
            continue
        if code == "a":
            g.add((item, IISGV.physicalDescription, Literal(text)))
            match = _PAGE_COUNT_RE.match(text)
            page_count = match.group(1) if match else text
            literal = try_literal(page_count, [XSD.integer, XSD.string])
            if literal is not None:
                g.add((item, IISGV.numberOfPages, literal))
        elif code == "g":
            g.add((item, IISGV.size, Literal(text)))
