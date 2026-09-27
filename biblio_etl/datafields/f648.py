"""MARC datafield 648 (subject added entry - chronological term) ->
``iisgv:period``, with begin/end years parsed from a range like
``"1914-1918."``."""

from __future__ import annotations

from rdflib import RDF, RDFS, Graph, Literal, URIRef

from ..context import as_array, get_code, get_text, mint_id, nl_amisg_id
from ..prefixes import IISGV, PERIOD


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    for sub in subfields:
        text = get_text(sub)
        period_id = nl_amisg_id(text)
        if period_id is None:
            continue
        period = PERIOD[mint_id(period_id)]
        g.add((item, IISGV.period, period))

        for s2 in subfields:
            if get_code(s2) != "a":
                continue
            label = get_text(s2)
            if not label:
                continue
            g.add((period, RDF.type, IISGV.Period))
            g.add((period, RDFS.label, Literal(label)))
            date_parts = label.split("-")
            if len(date_parts) >= 2 and date_parts[0] and date_parts[1]:
                g.add((period, IISGV.begin, Literal(date_parts[0])))
                g.add((period, IISGV.end, Literal(date_parts[1])))
