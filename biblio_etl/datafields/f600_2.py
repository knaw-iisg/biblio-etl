"""MARC datafield 600, second pass: ``sdo:about`` (untyped person reference,
scanning every subfield rather than just code ``0``) plus
``sdo:alternateName`` from code ``a``."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef

from ..context import as_array, get_code, get_text, mint_id, nl_amisg_id
from ..prefixes import PERSON, SDO


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        text = get_text(sub)
        if not text:
            continue
        person_id = nl_amisg_id(text)
        if person_id is not None:
            g.add((item, SDO.about, PERSON[mint_id(person_id)]))
        if get_code(sub) == "a":
            g.add((item, SDO.alternateName, Literal(text)))
