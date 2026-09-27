"""MARC datafield 110 (corporate name, main entry / author organization)
-> ``sdo:creator``."""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import as_array
from ..prefixes import ORGANIZATION, SDO
from .common import link_authority_entity


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    link_authority_entity(
        g, item, subfields,
        predicate=SDO.creator, ns=ORGANIZATION, cls=SDO.Organization,
        name_predicate=SDO.name,
    )
