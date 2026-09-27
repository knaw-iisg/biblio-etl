"""MARC datafield 610 (subject added entry - corporate name) -> ``sdo:about``
an Organization."""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import as_array
from ..prefixes import ORGANIZATION, SDO
from .common import link_authority_entity


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    link_authority_entity(
        g, item, subfields,
        predicate=SDO.about, ns=ORGANIZATION, cls=SDO.Organization,
        name_predicate=SDO.name,
    )
