"""MARC datafield 130 (uniform title, main entry) -> ``iisgv:title``."""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import as_array
from ..prefixes import IISGV, SDO, TITLE
from .common import link_authority_entity


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    link_authority_entity(
        g, item, subfields,
        predicate=IISGV.title, ns=TITLE, cls=SDO.CreativeWorkSeries,
    )
