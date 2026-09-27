"""MARC datafield 611 (subject added entry - meeting name) -> ``sdo:about``
an Event, typed and named from either an ``(NL-AMISG)`` authority id or an
``(OCoLC)fst...`` reference on subfield ``$0``."""

from __future__ import annotations

from rdflib import RDF, Graph, Literal, URIRef

from ..context import as_array, get_code, get_text, replace_first, mint_id, nl_amisg_id
from ..prefixes import EVENT, SDO

_OCOLC_FST_PREFIX = "(OCoLC)fst"


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    for sub in subfields:
        if get_code(sub) != "0":
            continue
        text = get_text(sub)
        if not text:
            continue

        event_id = nl_amisg_id(text)
        if event_id is None and text.startswith(_OCOLC_FST_PREFIX):
            event_id = text[len(_OCOLC_FST_PREFIX):]
        if not event_id:
            continue

        event = EVENT[mint_id(event_id)]
        g.add((item, SDO.about, event))
        g.add((event, RDF.type, SDO.Event))
        for s2 in subfields:
            if get_code(s2) != "a":
                continue
            label = get_text(s2)
            if label:
                g.add((event, SDO.name, Literal(replace_first(label, ".") or label)))
