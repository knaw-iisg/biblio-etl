"""MARC datafield 151 (geographic name, main entry) -> ``sdo:about`` a Place."""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import as_array
from ..prefixes import PLACE, SDO
from .common import link_authority_entity


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    link_authority_entity(
        g, item, subfields,
        predicate=SDO.about, ns=PLACE, cls=SDO.Place,
        name_predicate=SDO.name,
    )
