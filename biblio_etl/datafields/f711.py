"""MARC datafield 711 (added entry - meeting name), linked with the
``relator:cre`` predicate."""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import as_array
from ..prefixes import EVENT, RELATOR, SDO
from .common import link_authority_entity


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    link_authority_entity(
        g, item, subfields,
        predicate=RELATOR.cre, ns=EVENT, cls=SDO.Event,
        name_predicate=SDO.name,
    )
