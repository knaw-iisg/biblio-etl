"""MARC datafield 035 ($a system control number) -> ``owl:sameAs`` a WorldCat
OCLC number, when the subfield holds an ``(OCoLC)...`` reference."""

from __future__ import annotations

from rdflib import OWL, Graph, URIRef

from ..context import as_array, get_code, get_text, mint_id
from ..prefixes import OCLC

_OCLC_PREFIX = "(OCoLC)"


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        if get_code(sub) != "a":
            continue
        text = get_text(sub)
        if not text or not text.startswith(_OCLC_PREFIX):
            continue
        oclc_id = text[len(_OCLC_PREFIX):]
        if not oclc_id:
            continue
        g.add((item, OWL.sameAs, OCLC[mint_id(oclc_id)]))
