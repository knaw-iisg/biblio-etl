"""MARC datafield 044 ($a country) -> ``iisgv:country``."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef

from ..context import as_array, get_code, get_text
from ..prefixes import IISGV


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        if get_code(sub) != "a":
            continue
        text = get_text(sub)
        if text:
            g.add((item, IISGV.country, Literal(text)))
