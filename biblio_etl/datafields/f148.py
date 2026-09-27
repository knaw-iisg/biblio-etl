"""MARC datafield 148 (chronological term, main entry) -> ``iisgv:period``."""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import as_array
from ..prefixes import IISGV, PERIOD
from .common import link_authority_entity


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    link_authority_entity(
        g, item, subfields,
        predicate=IISGV.period, ns=PERIOD, cls=IISGV.Period,
    )
