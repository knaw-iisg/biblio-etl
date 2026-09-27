"""MARC datafield 155 (genre/form term, main entry) -> ``iisgv:form``."""

from __future__ import annotations

from rdflib import Graph, URIRef

from ..context import as_array
from ..prefixes import FORM, IISGV
from .common import link_authority_entity


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    subfields = as_array(datafield.get("marc:subfield"))
    link_authority_entity(
        g, item, subfields,
        predicate=IISGV.form, ns=FORM, cls=IISGV.Form,
    )
