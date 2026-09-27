"""MARC datafield 150 (topical term, main entry) -> ``iisgv:topic``."""

from __future__ import annotations

from rdflib import RDFS, Graph, URIRef

from ..context import as_array
from ..prefixes import IISGV, TOPIC
from .common import link_authority_entity


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    link_authority_entity(
        g, item, subfields,
        predicate=IISGV.topic, ns=TOPIC, cls=IISGV.Topic,
        name_predicate=RDFS.label,
    )
