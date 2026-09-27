"""MARC datafield 651 (subject added entry - geographic name) ->
``sdo:about`` a place reference."""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import as_array, get_text, mint_id, nl_amisg_id
from ..prefixes import PLACE, SDO


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        place_id = nl_amisg_id(get_text(sub))
        if place_id is not None:
            g.add((item, SDO.about, PLACE[mint_id(place_id)]))
