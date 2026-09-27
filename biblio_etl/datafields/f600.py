"""MARC datafield 600 (subject added entry - personal name) -> ``sdo:about``
a Person."""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import as_array
from ..prefixes import PERSON, SDO
from .common import link_authority_entity


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    link_authority_entity(
        g, item, subfields,
        predicate=SDO.about, ns=PERSON, cls=SDO.Person,
        name_predicate=SDO.name,
    )
