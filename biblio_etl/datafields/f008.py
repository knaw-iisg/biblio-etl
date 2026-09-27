"""MARC controlfield 008 -> ``sdo:inLanguage``, resolved once per record."""

from rdflib import Graph, URIRef

from .. import language


def process(item: URIRef, text_008: str, g: Graph) -> str | None:
    if not text_008:
        return None
    return language.process(item, text_008, g)
