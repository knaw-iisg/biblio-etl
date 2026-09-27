"""MARC datafield 500 ($a general note) -> language-tagged ``sdo:description``."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef

from ..context import as_array, get_code, get_text
from ..prefixes import SDO


def process(item: URIRef, datafield: dict, g: Graph, lang: str | None = None) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        if get_code(sub) != "a":
            continue
        text = get_text(sub)
        if text:
            g.add((item, SDO.description, Literal(text, lang=lang) if lang else Literal(text)))
