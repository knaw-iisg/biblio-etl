"""MARC datafield 902 ($a handle id) -> ``iisgv:nativeViewer``, as an
``xsd:anyURI``-typed string literal."""

from __future__ import annotations

from rdflib import XSD, Graph, Literal, URIRef

from ..context import as_array, get_code, get_text
from ..prefixes import HANDLE, IISGV

_PREFIXES = ("10622\\", "10622/")


def process(item: URIRef, datafield: dict, g: Graph) -> None:
    for sub in as_array(datafield.get("marc:subfield")):
        if get_code(sub) != "a":
            continue
        text = get_text(sub)
        if not text:
            continue
        for prefix in _PREFIXES:
            if text.startswith(prefix):
                handle_id = text[len(prefix):]
                if handle_id:
                    url = f"{HANDLE}{handle_id}"
                    g.add((item, IISGV.nativeViewer, Literal(url, datatype=XSD.anyURI)))
                break
