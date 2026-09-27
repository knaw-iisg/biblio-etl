"""MARC datafield 100 (personal name, main entry / author) -> ``sdo:creator``,
with name, relator role and dates on the linked Person."""

from __future__ import annotations

import re

from rdflib import RDF, Graph, Literal, URIRef

from ..context import as_array, get_code, get_text, replace_first, mint_id, nl_amisg_id
from ..prefixes import IISGV, PERSON, SDO
from ..relators import RELATOR_NULLS, RELATOR_TABLE

_RELATOR_CLEAN_RE = re.compile(r"[^a-zA-Z']")


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    for sub in subfields:
        if get_code(sub) != "0":
            continue
        person_id = nl_amisg_id(get_text(sub))
        if person_id is None:
            continue
        person = PERSON[mint_id(person_id)]
        g.add((item, SDO.creator, person))
        g.add((person, RDF.type, SDO.Person))
        _apply_name_relator_date(g, item, person, subfields)


def _apply_name_relator_date(g: Graph, item: URIRef, person: URIRef, subfields: list[dict]) -> None:
    for sub in subfields:
        code = get_code(sub)
        text = get_text(sub)
        if not text:
            continue
        if code == "a":
            name = replace_first(text, ".")
            if name:
                g.add((person, SDO.name, Literal(name)))
        elif code == "e":
            cleaned = _RELATOR_CLEAN_RE.sub("", text)
            if cleaned and cleaned not in RELATOR_NULLS:
                predicate = RELATOR_TABLE.get(cleaned)
                if predicate is not None:
                    g.add((item, predicate, person))
        elif code == "d":
            g.add((person, IISGV.date, Literal(text)))
