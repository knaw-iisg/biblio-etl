"""MARC datafield 830 (series added entry - uniform title) ->
``iisgv:seriesTitle`` / ``iisgv:seriesVolume``."""

from __future__ import annotations

from rdflib import Graph, Literal, URIRef

from ..context import as_array, get_code, get_text, mint_id, nl_amisg_id
from ..prefixes import IISGV, TITLE


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        code = get_code(sub)
        text = get_text(sub)
        if not text:
            continue
        if code == "0":
            title_id = nl_amisg_id(text)
            if title_id is not None:
                g.add((item, IISGV.seriesTitle, TITLE[mint_id(title_id)]))
        elif code == "v":
            g.add((item, IISGV.seriesVolume, Literal(text)))
